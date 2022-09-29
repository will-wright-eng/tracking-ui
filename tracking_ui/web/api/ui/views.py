import os
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = os.path.join(BASE_PATH, "templates")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

router = APIRouter()


@router.get("/")
def read_root():
    return "hello world"


@router.get("/basepath")
def base_path():
    return BASE_PATH


@router.get("/square")
def square(num: int):
    result = num**2
    return {"squared number": result}


@router.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "form.html",
        context={"request": request, "result": result},
    )


@router.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = str(num)
    return templates.TemplateResponse(
        "form.html",
        context={"request": request, "result": result},
    )


@router.get("/athena-test")
def athena_test(request: Request):
    # result = "Type a number"
    # do struff to get athena data
    return templates.TemplateResponse(
        "form.html",
        context={"request": request, "result": result},
    )
