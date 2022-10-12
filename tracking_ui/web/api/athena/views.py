import os
import json
import logging
import datetime
from pathlib import Path

from fastapi import Form, Request, APIRouter, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from tracking_ui.services.athena.athena import athenaMgmt

BASE_PATH = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = os.path.join(BASE_PATH, "templates")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

router = APIRouter()
logger = logging.getLogger("fastapi")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


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

    # if athena.has_query_succeeded(query_id):
    #     result = athena.get_query_results(execution_id=query_id)
    # else:
    #     result = 'status unknown'
    # return templates.TemplateResponse(
    #     "form.html",
    #     context={"request": request, "result": result},
    # )
