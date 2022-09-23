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

- python class attributes
```py
self.client = boto3.client("athena")
self.database_name = "athena_tutorial"
self.results_output_location = "s3://wwtestbucket/athena_test/queries/"
self.table_ddl = "funding_data.ddl"
self.table_name = "funding_data"
```
