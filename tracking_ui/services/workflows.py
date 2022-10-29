import datetime as dt

import athena
import pandas as pd
from athena import utils
from athena.athena import athenaAssetTable

from .workflow_utils import table_setup, put_check_get, extract_values_from_result_set


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
