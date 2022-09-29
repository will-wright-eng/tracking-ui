import time
import pathlib
import configparser

import boto3

# def get_default_region() -> str:
#     config_file_path = pathlib.Path.home() / ".aws" / "config"
#     if os.path.isfile(config_file_path):
#         config = configparser.ConfigParser()
#         config.read(config_file_path)
#         return config["default"]["region"]
#     else:
#         region = "us-west-1"
#         return region


class athenaMgmt:
    def __init__(self):
        # self.client = boto3.client(service_name="athena", region_name=get_default_region())
        self.client = boto3.client(service_name="athena", region_name="us-west-1")
        self.database_name = "athena_tutorial"
        self.results_output_location = "s3://wwtestbucket/athena_test/queries/"
        self.table_ddl = "funding_data.ddl"
        self.table_name = "funding_data"

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
            ResultConfiguration={"OutputLocation": self.results_output_location},
        )
        return response["QueryExecutionId"]

    def create_table(self):
        """return: execution_id"""
        with open(self.table_ddl) as ddl:
            response = self.client.start_query_execution(
                QueryString=ddl.read(),
                ResultConfiguration={"OutputLocation": self.results_output_location},
            )
            return response["QueryExecutionId"]

    def get_num_rows(self):
        """return: execution_id"""
        query = f"SELECT COUNT(*) from {self.database_name}.{self.table_name}"
        response = self.client.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.results_output_location},
        )
        return response["QueryExecutionId"]

    def get_query_results(self, execution_id):
        """return: list of row dictionaries"""
        response = self.client.get_query_results(
            QueryExecutionId=execution_id,
        )
        results = response["ResultSet"]["Rows"]
        return results
