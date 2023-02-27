import os
import json
import datetime as dt
import operator
from typing import List
from collections import Counter

from athena import utils, secrets
from athena.athena import athenaBaseClass

EXTENSION_VERSION = "prod/0.7.0"
DELIM = "/"


def map_attributes(source_class: athenaBaseClass, destination_class: athenaBaseClass):
    destination_class.__dict__.update(source_class.__dict__)
    return destination_class


######################
# athena_workflow_01 #
######################


def table_setup(class_obj) -> None:
    bucket_name = secrets.bucket_name
    test_set = secrets.test_set
    data_source = f"{bucket_name}/{test_set}"
    ts = "".join([c for c in str(dt.datetime.today()) if c in "1234567890 "]).replace(" ", "_")
    table_name = f"dev_test_table_{ts}"
    msg = utils.get_sample_msg()
    schema = " string,\n".join(list(msg)) + " string"

    class_obj.compose_new_table_query(table_name, schema, data_source)
    class_obj.save_query_to_ddl()


def put_check_get(class_obj_recursive_check, class_obj_put_method) -> dict:
    """
    the sequence is fairly generic after the unique query has been input, this
        method will create a robust method of getting results from a set of inputs

    input: class object put method
    output: results reponse json object
    """
    class_obj_put_method()
    return class_obj_recursive_check()


def extract_values_from_row(row) -> List[str]:
    data = []
    for ele in row:
        try:
            tmp = list(ele.values())[0]
        except IndexError:
            tmp = ""
        data.append(tmp)
    return data


def extract_values_from_result_set(rows) -> List[str]:
    data = []
    for row in rows:
        data.append(extract_values_from_row(row.get("Data")))
    return data


##########################
# get_events_workflow_01 #
##########################


def filter_events(event_list, filter_by, event_key, op_funk=operator.eq):
    tmp = list(
        filter(
            lambda x: op_funk(x.get(event_key), filter_by),
            event_list,
        ),
    )
    return tmp


def create_set_id(blob):
    return DELIM.join(blob.split(DELIM)[:-1])


def create_metadata_dict(res):
    keys = list(res)
    blob_metadata = {i: j for i, j in zip(keys, [len(res.get(key)) for key in keys])}
    print(len(blob_metadata))
    print(sum(blob_metadata.values()))
    return blob_metadata


def create_set_dict(obj_list):
    data = {}
    set_ids = {create_set_id(i) for i in obj_list}
    for blob in obj_list:
        for set_id in set_ids:
            if set_id in blob:
                if set_id in data:
                    data[set_id].append(blob)
                else:
                    data[set_id] = [blob]
    return data


def get_event_file_list(res):
    prod_set = [i for i in list(res) if EXTENSION_VERSION in i]
    return [item for sublist in [res[i] for i in prod_set] for item in sublist]


def get_json_data(file_name):
    with open(file_name, "r") as file:
        data = json.loads(file.read())
    return data


def generate_payload(data):
    return {
        "events": data,
        "count": len(data),
        "timestamp": str(dt.datetime.now()),
        "schema": dict(Counter([item for sublist in [list(i) for i in data] for item in sublist])),
    }


def write_json(payload):
    file_name = f'{EXTENSION_VERSION.replace("/","-").replace(".","")}_payload.json'
    with open(file_name, "w", encoding="utf8") as json_file:
        json.dump(payload, json_file, ensure_ascii=False)
    return file_name


def cleanup_local_files(file_names):
    for file_name in file_names:
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)
