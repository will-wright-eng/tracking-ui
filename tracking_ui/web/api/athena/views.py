import json
import logging
import datetime

from fastapi import Request, APIRouter

from .sample_data import sample_json

router = APIRouter()
logger = logging.getLogger("fastapi")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


@router.get("/sample-json")
def athena_results(request: Request):
    return sample_json
