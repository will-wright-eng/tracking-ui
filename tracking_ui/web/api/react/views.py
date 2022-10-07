# import datetime
# import json
# import logging
# import os
# from pathlib import Path

from fastapi import APIRouter

# from fastapi import APIRouter, Form, Request, status
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates

# from tracking_ui.services.athena.athena import athenaMgmt

# BASE_PATH = Path(__file__).resolve().parents[3]
# TEMPLATE_PATH = os.path.join(BASE_PATH, "templates")
# templates = Jinja2Templates(directory=TEMPLATE_PATH)

router = APIRouter()
# logger = logging.getLogger("fastapi")


# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, z):
#         if isinstance(z, datetime.datetime):
#             return str(z)
#         else:
#             return super().default(z)


# data = {"query_id": "39d23ec9-82b8-41cc-a2a4-2f711d87439b"}
# athena = athenaMgmt()

todos = [
    {
        "id": "1",
        "item": "Read a book.",
    },
    {
        "id": "2",
        "item": "Cycle around town.",
    },
]

# @router.get("/athena-results")
# def athena_results(request: Request):
#     if data:
#         logger.info(json.dumps(data))
#         response = athena.check_status(data.get("query_id"))
#         return templates.TemplateResponse(
#             "display-athena-resp-json.html",
#             context={"request": request, "resp": response},
#         )
#     else:
#         return templates.TemplateResponse(
#             "go-get-data.html",
#             context={"request": request},
#         )


@router.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": todos}
