import logging

from fastapi import Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .sample_data import prod070_payload

router = APIRouter()
logger = logging.getLogger("fastapi")


@router.get("/sample-json")
def athena_results(request: Request):
    return JSONResponse(content=jsonable_encoder(prod070_payload))


# note: this is is differnt approach that would achieve the same thing
# @app.get('/')
# def main():
#     json_str = json.dumps(d, indent=4, default=str)
#     return Response(content=json_str, media_type='application/json')
