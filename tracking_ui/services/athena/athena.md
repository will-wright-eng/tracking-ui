## athena

- [tutorial](https://www.learnaws.org/2022/01/16/aws-athena-boto3-guide/)

- command line

```sh
touch funding_data.ddl
aws s3 mb s3://wwtestbucket
aws s3 cp funding_data.ddl s3://wwtestbucket/athena_test/queries/funding_data.ddl
aws s3 cp athena_data.csv s3://wwtestbucket/input/
```

- `funding_data.ddl`

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS
athena_tutorial.funding_data (
  Permalink string,
  Company string,
  NumEmps string,
  Category string,
  City string,
  State string,
  FundedDate string,
  RaisedAmt string,
  RaisedCurrency string,
  Round string
) ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '\"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://wwtestbucket/input/';
```

- python class attributes/properties

```py
self.client = boto3.client("athena")
self.database_name = "athena_tutorial"
self.results_output_location = "s3://wwtestbucket/athena_test/queries/"
self.table_ddl = "funding_data.ddl"
self.table_name = "funding_data"
```

## 2022-10-16

- ideally I can pull a sample json to determine the schema... for now this needs to be done manually
*my failed attempt:*

```py
import os
from media_mgmt_cli.aws import AwsStorageMgmt

s3_mgmt = AwsStorageMgmt(project_name='tracking-ui')
file_list = s3_mgmt.get_files(location='s3')
tmp = [file for file in file_list if test_set and 'json' in file][0]
json_obj = tmp.split('/')[-1]
sample_json = os.path.join(test_set,  json_obj)
# 'dev/api-gateway/ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c/tracking_extension_2022-09-18T08:24:31.599Z.json'
s3_mgmt.download_file(sample_json)
```
