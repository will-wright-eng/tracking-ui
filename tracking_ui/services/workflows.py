import os
import datetime as dt
import operator
from pprint import pprint

import athena
import pandas as pd
from athena import utils
from athena.athena import athenaAssetTable
from media_mgmt_cli import mmgmt_aws

from .workflow_utils import (
    write_json,
    table_setup,
    filter_events,
    get_json_data,
    put_check_get,
    create_set_dict,
    generate_payload,
    cleanup_local_files,
    get_event_file_list,
    extract_values_from_result_set,
)

EXTENSION_VERSION = "prod/0.7.0"
DELIM = "/"


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


def get_events_workflow_01():
    aws = mmgmt_aws.AwsStorageMgmt(project_name="tracking-ui-athena-dev")
    obj_list = aws.get_bucket_object_keys()
    res = create_set_dict(obj_list)

    prod_file_set = get_event_file_list(res)

    for file in prod_file_set:
        aws.download_file(file)

    file_names = [i.split(DELIM)[-1] for i in prod_file_set]

    data = []
    for file_name in file_names:
        data.append(get_json_data(file_name))

    event_key = "tab_title"
    filter_by = None
    filtered_data = filter_events(data, filter_by, event_key, op_funk=operator.ne)

    payload = generate_payload(filtered_data)
    write_json(payload)

    cleanup_local_files(file_names)
    pprint(set(os.listdir(".")))
