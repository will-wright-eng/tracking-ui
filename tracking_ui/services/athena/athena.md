# athena implementation notes

- [tutorial](https://www.learnaws.org/2022/01/16/aws-athena-boto3-guide/)

- command line

```sh
touch funding_data.ddl
aws s3 mb s3://<test bucket>
aws s3 cp funding_data.ddl s3://<test bucket>/athena_test/queries/funding_data.ddl
aws s3 cp athena_data.csv s3://<test bucket>/input/
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
LOCATION 's3://<test bucket>/input/';
```

- python class attributes/properties

```py
self.client = boto3.client("athena")
self.database_name = "athena_tutorial"
self.results_output_location = "s3://<test bucket>/athena_test/queries/"
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

## 2022-10-28

### sample json

- aggregate multiple events into serialized payload that fits react example app

```python
%reset -f

import os
import json
from collections import Counter
import datetime as dt

def get_events():
    files = os.listdir('.')
    flist = [i for i in files if 'event_' in i]
    data = []
    for file in flist:
        with open(file, 'r') as f:
            data.append(json.loads(f.read()))
    return data

def generate_payload(data):
    payload = {}
    payload.update({
        'events': data,
        'count': len(data),
        'timestamp': str(dt.datetime.now()),
        'schema': dict(Counter([item for sublist in [list(i) for i in data] for item in sublist]))
    })
    return payload

def write_json(payload):
    filename = 'sample_payload.json'
    with open(filename, 'w') as file:
        file.write(json.dumps(payload))

data = get_events()
payload = generate_payload(data)
write_json(payload)
```

> client blocked access when using Brave, works on Chrome

### old endpoints

```python
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from tracking_ui.services.athena.athena import athenaMgmt

BASE_PATH = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = os.path.join(BASE_PATH, "templates")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

data = {"query_id": "39d23ec9-82b8-41cc-a2a4-2f711d87439b"}
athena = athenaMgmt()

@router.get("/athena-results")
def athena_results(request: Request):
    if data:
        logger.info(json.dumps(data))
        response = athena.check_status(data.get("query_id"))
        return templates.TemplateResponse(
            "display-athena-resp-json.html",
            context={"request": request, "resp": response},
        )
    else:
        return templates.TemplateResponse(
            "go-get-data.html",
            context={"request": request},
        )


@router.post("/athena-results")
def athena_results(request: Request):
    redirect_url = request.url_for("athena_test")
    logger.info(redirect_url)
    return RedirectResponse(
        redirect_url,
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/athena-test")
def athena_test(request: Request):
    return templates.TemplateResponse(
        "form-athena.html",
        context={"request": request},
    )


@router.post("/athena-test")
def athena_test(request: Request):
    query_id = athena.get_num_rows()
    # data['query_id'] = query_id <-- see above
    redirect_url = request.url_for("athena_results")
    logger.info(redirect_url)
    return RedirectResponse(
        redirect_url,
        status_code=status.HTTP_302_FOUND,
    )
```
