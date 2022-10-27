import json
from pathlib import Path


def upload_to_storage(file_name: str, storage_prefix: str = "input") -> None:
    from media_mgmt_cli.aws import AwsStorageMgmt

    s3_mgmt = AwsStorageMgmt(project_name="tracking-ui-athena-dev")
    s3_mgmt.upload_file(file_name, additional_prefix=storage_prefix)


def get_sample_msg() -> dict:
    p = Path(".") / "athena" / "tracking_extension_2022-10-04T06:39:13.406Z.json"
    with open(str(p), "r") as file:
        msg = json.loads(file.read())
    return msg


def check_not_none(*args):
    if all([*args]):
        pass
    else:
        for arg in list(args):
            arg_name = f"{arg=}".partition("=")[0]
            print(f"{arg_name} = {arg}")
        raise ValueError("*args not valid")


def validate_args(func):
    def wrapper(*args, **kwargs):
        if all([*args]):
            return func(*args, **kwargs)
        else:
            for arg in list(args):
                arg_name = f"{arg=}".partition("=")[0]
                print(f"{arg_name} = {arg}")
            raise ValueError("*args not valid")

    return wrapper
