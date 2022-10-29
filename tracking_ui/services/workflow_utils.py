import datetime as dt
from typing import List

from athena import utils, secrets
from athena.athena import athenaBaseClass, athenaAssetTable


def map_attributes(source_class: athenaBaseClass, destination_class: athenaBaseClass):
    destination_class.__dict__.update(source_class.__dict__)
    return destination_class


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
