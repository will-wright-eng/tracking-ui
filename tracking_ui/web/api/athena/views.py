import json
import logging
import datetime

from fastapi import Request, APIRouter

from .sample_data import sample_json, prod070_payload

router = APIRouter()
logger = logging.getLogger("fastapi")


@router.get("/sample-json")
def athena_results(request: Request):
    return sample_json


@router.get("/prod-payload")
def prod_payload(request: Request):
    return prod070_payload
