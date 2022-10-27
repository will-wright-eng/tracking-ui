import os
import time

import boto3

from .config import ConfigHandler  # # replace with sys-config
from .utils import check_not_none, upload_to_storage, validate_args


class athenaBaseClass:
    def __init__(self, project_name):
        self.client = boto3.client(service_name="athena", region_name="us-west-1")
        self.cache = {"execution_id": []}
        self.config = ConfigHandler(project_name=project_name)
        if self.config.check_config_exists():
            self.configs = self.config.get_configs()
            self.bucket = self.configs.get("aws_bucket", None)
            self.output_results = os.path.join(
                "s3://",
                self.bucket,
                self.configs.get("object_prefix", None),
                "output/",
            )
            self.input_queries = os.path.join(
                self.configs.get("object_prefix", None),
                "input",
            )
            self.object_prefix = self.configs.get("object_prefix", None)
            self.database_name = self.configs.get("athena_db", None)
        else:
            print("config file does not exist, run `smgmt` to configure project")

    def check_status(self, execution_id: str = None):
        """return: query_status"""
        return self.client.get_query_execution(
            QueryExecutionId=execution_id if execution_id else self.cache.get("execution_id")[-1],
        )

    def has_query_succeeded(self, execution_id: str = None):
        """return: query_status"""
        state = "RUNNING"
        max_execution = 5
        while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
            print(f"num tries remaining = {max_execution}")
            max_execution -= 1
            response = self.check_status()
            if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
            ):
                state = response["QueryExecution"]["Status"]["State"]
                if state == "SUCCEEDED":
                    print(f"state == {state}")
                    return True
                else:
                    print(f"state == {state}")
            time.sleep(30)
        return False

    def has_query_succeeded_recursive(self) -> dict:
        if self.has_query_succeeded():
            return self.get_results()
        else:
            return self.has_query_succeeded_recursive()

    def set_database_name(self, database_name):
        if self.database_name:
            print(f"replacing {self.database_name} with {database_name}")
            self.database_name = database_name
        else:
            print(f"database name set to: {database_name}")
            self.database_name = database_name

    def set_table_name(self, table_name):
        self.table_ddl = f"{table_name}.ddl"
        self.table_name = table_name

    def set_catalog(self, catalog_name):
        self.catalog_name = catalog_name

    def get_catalogs(self):
        resp = self.client.list_data_catalogs()
        first_catalog = resp.get("DataCatalogsSummary")[0].get("CatalogName")
        return first_catalog, resp

    def get_databases(self):
        return self.client.list_databases(
            CatalogName=self.catalog_name,
        )

    def get_tables(self):
        resp = self.client.list_table_metadata(
            CatalogName=self.catalog_name,
            DatabaseName=self.database_name,
        )
        first_table = resp.get("TableMetadataList")[0].get("Name")
        return first_table, resp


class athenaAssetDb(athenaBaseClass):
    def __init__(self, project_name: str = "tracking-ui-athena-dev"):
        super().__init__(project_name)

    def create_database(self):
        """return: execution_id"""
        check_not_none(self.database_name)
        response = self.client.start_query_execution(
            QueryString=f"create database {self.database_name}",
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        self.cache.get("execution_id").append(response["QueryExecutionId"])
        return response


class athenaAssetTable(athenaBaseClass):
    def __init__(self, project_name: str = "tracking-ui-athena-dev"):
        super().__init__(project_name)

    def put_query_table_from_ddl(self):
        """return: execution_id"""
        with open(self.table_ddl) as ddl:
            response = self.client.start_query_execution(
                QueryExecutionContext={"Database": self.database_name},
                QueryString=ddl.read(),
                ResultConfiguration={"OutputLocation": self.output_results},
            )
        self.cache.get("execution_id").append(response["QueryExecutionId"])
        return response

    def put_query_row_num_count(self):
        """return: execution_id"""
        check_not_none(self.database_name, self.table_name)
        query = f"SELECT COUNT(*) from {self.database_name}.{self.table_name}"
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        self.cache.get("execution_id").append(response["QueryExecutionId"])
        return response

    def put_query_table_sample(self):
        """return: execution_id"""
        query = f"SELECT * from {self.database_name}.{self.table_name} limit 100"
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        self.cache.get("execution_id").append(response["QueryExecutionId"])
        return response

    def put_query_select_all(self):
        """return: execution_id"""
        query = f"SELECT * from {self.database_name}.{self.table_name}"
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        self.cache.get("execution_id").append(response["QueryExecutionId"])
        return response

    def get_results(self, execution_id: str = None):
        """return: list of row dictionaries"""
        response = self.client.get_query_results(
            QueryExecutionId=execution_id if execution_id else self.cache.get("execution_id")[-1],
        )
        self.query_results = response["ResultSet"]["Rows"]
        return response

    def save_query_to_ddl(self):
        with open(self.table_ddl, "w") as file:
            file.write(self.query)

    def upload_ddl(self):
        upload_to_storage(self.table_ddl)

    @validate_args
    def compose_new_table_query(
        self,
        table_name: str,
        schema: str,
        data_source: str,
    ) -> str:
        self.set_table_name(table_name)
        self.query = f"""
        create external table {self.table_name} (
        {schema}
        )
        ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
        WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
        location '{data_source}';
        """
        self.save_query_to_ddl()
        print(self.query)
