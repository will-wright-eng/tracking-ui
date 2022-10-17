from pathlib import Path


def upload_to_storage(file_name):
    from media_mgmt_cli.aws import AwsStorageMgmt

    s3_mgmt = AwsStorageMgmt(project_name="tracking-ui")
    s3_mgmt.upload_file(file_name, additional_prefix="input")


def get_sample_msg():
    # p = Path('.') / 'athena' / 'tracking_extension_2022-10-04T06:39:13.406Z.json'
    with open(str(p), "r") as file:
        msg = json.loads(file.read())
    return msg
