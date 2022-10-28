import json
import logging
import datetime

from fastapi import Request, APIRouter

router = APIRouter()
logger = logging.getLogger("fastapi")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


sample_json = {
    "events": [
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "https://github.com/will-wright-eng/tracking-extension/pull/12/files",
            "tab_id": 1004773783,
            "tab_title": "navigation experiment by will-wright-eng \u00b7 Pull Request #12 \u00b7 will-wright-eng/tracking-extension",
            "tab_window_id": 1004773774,
            "created_timestamp": "2022-10-14T03:00:10.492Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "http://0.0.0.0:8000/api/docs#/",
            "tab_id": 1004773770,
            "tab_title": "tracking_ui - Swagger UI",
            "tab_window_id": 1004773769,
            "created_timestamp": "2022-10-14T03:00:02.749Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "https://testdriven.io/blog/fastapi-react/",
            "tab_id": 1004773756,
            "tab_title": "Developing a Single Page App with FastAPI and React | TestDriven.io",
            "tab_window_id": 1004773755,
            "created_timestamp": "2022-10-14T03:00:09.356Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "http://localhost:8888/lab/tree/tracking_ui/services/Untitled.ipynb",
            "tab_id": 1004773768,
            "tab_title": "JupyterLab",
            "tab_window_id": 1004773762,
            "created_timestamp": "2022-10-14T03:00:03.818Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onRemoved",
            "tab_id": 1004773771,
            "tab_window_id": 1004773769,
            "created_timestamp": "2022-10-14T03:00:15.437Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "https://duckduckgo.com/?q=chrome+event+click&atb=v344-4vb&ia=web",
            "tab_id": 1004773784,
            "tab_title": "chrome event click at DuckDuckGo",
            "tab_window_id": 1004773774,
            "created_timestamp": "2022-10-14T03:00:05.600Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onRemoved",
            "tab_id": 1004773770,
            "tab_window_id": 1004773769,
            "created_timestamp": "2022-10-14T03:00:14.489Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "https://github.com/testdrivenio/fastapi-react/tree/master/frontend",
            "tab_id": 1004773757,
            "tab_title": "fastapi-react/frontend at master \u00b7 testdrivenio/fastapi-react",
            "tab_window_id": 1004773755,
            "created_timestamp": "2022-10-14T03:00:11.331Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "http://localhost:8888/lab/tree/tracking_ui/services",
            "tab_id": 1004773768,
            "tab_title": "JupyterLab",
            "tab_window_id": 1004773762,
            "created_timestamp": "2022-10-14T03:00:09.999Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "http://0.0.0.0:8000/v1/athena/athena-results",
            "tab_id": 1004773771,
            "tab_title": "Sample Form",
            "tab_window_id": 1004773769,
            "created_timestamp": "2022-10-14T03:00:15.360Z",
        },
        {
            "info_os": "mac",
            "info_arch": "x86-64",
            "manifest_version": "0.6.0",
            "info_user_id": "ea8268ef8df977938db5097dfd18f7cc3d0dcf5c6c57c6cea37fa427050d08c",
            "tab_event": "chrome.tabs.onUpdated",
            "tab_url": "https://www.netlify.com/blog/2016/07/22/deploy-react-apps-in-less-than-30-seconds/",
            "tab_id": 1004773759,
            "tab_title": "How to deploy React Apps in less than 30 Seconds",
            "tab_window_id": 1004773758,
            "created_timestamp": "2022-10-14T03:00:07.770Z",
        },
    ],
    "count": 11,
    "timestamp": "2022-10-27 03:16:36.495249",
    "schema": {
        "info_os": 11,
        "info_arch": 11,
        "manifest_version": 11,
        "info_user_id": 11,
        "tab_event": 11,
        "tab_url": 9,
        "tab_id": 11,
        "tab_title": 9,
        "tab_window_id": 11,
        "created_timestamp": 11,
    },
}


@router.get("/sample-json")
def athena_results(request: Request):
    return sample_json
