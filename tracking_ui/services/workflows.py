import datetime as dt
from typing import List

import athena
import pandas as pd
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


def athena_workflow_01():
    """
    athena workflow 01: workflow to process test set of json msgs

    1. create class instance
    2. declair catalog and database
    3. compose table and save ddl
    4. put check get
            - create table view in athena database
            - query view and retrieve data
    5. convert results into dataframe
            - TODO: pagentate results
    6. save csv and upload to s3
    """
    PROJECT_NAME = athena.PROJECT_NAME
    DATABASE_NAME = athena.DATABASE_NAME
    CATALOG_NAME = athena.CATALOG_NAME

    table = athenaAssetTable(project_name=PROJECT_NAME)
    table.set_catalog(CATALOG_NAME)
    table.set_database_name(DATABASE_NAME)

    table_setup(table)

    resp = put_check_get(table.has_query_succeeded_recursive, table.put_query_table_from_ddl)
    resp = put_check_get(table.has_query_succeeded_recursive, table.put_query_select_all)

    rows = resp.get("ResultSet").get("Rows")
    data = extract_values_from_result_set(rows)

    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df["processed_timestamp"] = str(dt.datetime.now())
    filename = f"{table.table_name}.csv"
    df.to_csv(filename, index=False)
    utils.upload_to_storage(filename, storage_prefix="output/csv")
