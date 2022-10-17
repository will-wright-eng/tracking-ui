import json
import time
import pathlib
import configparser

import boto3

from .utils import upload_to_storage


class athenaMgmt:
    def __init__(self):
        self.client = boto3.client(service_name="athena", region_name="us-west-1")

        self.config = ConfigHandler(project_name)
        if self.config.check_config_exists():
            self.configs = self.config.get_configs()
            self.bucket = self.configs.get("aws_bucket", None)
            self.output_results = os.path.join(
                self.configs.get("object_prefix", None),
                "output",
            )
            self.input_queries = os.path.join(
                self.configs.get("object_prefix", None),
                "input",
            )
            self.object_prefix = self.configs.get("object_prefix", None)
            self.database_name = self.configs.get("athena_db", None)
        else:
            echo("config file does not exist, run `smgmt` to configure project")

    def set_table_name(self, table_name):
        self.table_ddl = f"{table_name}.ddl"
        self.table_name = table_name

    def has_query_succeeded(self, execution_id):
        """return: query_status"""
        state = "RUNNING"
        max_execution = 5
        while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
            max_execution -= 1
            response = self.client.get_query_execution(QueryExecutionId=execution_id)
            if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
            ):
                state = response["QueryExecution"]["Status"]["State"]
                if state == "SUCCEEDED":
                    return True
            time.sleep(30)
        return False

    def check_status(self, execution_id):
        """return: query_status"""
        response = self.client.get_query_execution(QueryExecutionId=execution_id)
        return response

    def create_database(self):
        """return: execution_id"""
        response = self.client.start_query_execution(
            QueryString=f"create database {self.database_name}",
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        return response["QueryExecutionId"]

    def create_table(self):
        """return: execution_id"""
        with open(self.table_ddl) as ddl:
            response = self.client.start_query_execution(
                QueryString=ddl.read(),
                ResultConfiguration={"OutputLocation": self.output_results},
            )
            return response["QueryExecutionId"]

    def get_num_rows(self):
        """return: execution_id"""
        query = f"SELECT COUNT(*) from {self.database_name}.{self.table_name}"
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.output_results},
        )
        return response["QueryExecutionId"]

    def get_query_results(self, execution_id):
        """return: list of row dictionaries"""
        response = self.client.get_query_results(
            QueryExecutionId=execution_id,
        )
        results = response["ResultSet"]["Rows"]
        return results

    def build_create_table_query(
        self,
        table_name: str,
        schema: str,
        s3_path: str,
    ) -> str:
        self.query = f"""
        create external table {table_name} (
        {schema}
        )
        ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
        WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
        location '{s3_path}';
        """

    def save_ddl_local(self):
        with open(self.table_ddl, "w") as file:
            file.write(self.query)

    def upload_ddl(self):
        upload_to_storage(self.table_ddl)
