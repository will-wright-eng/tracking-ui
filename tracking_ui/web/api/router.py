from fastapi.routing import APIRouter

from tracking_ui.web.api import monitoring, ui

api_router = APIRouter()
api_router.include_router(monitoring.router, prefix="/health")
api_router.include_router(ui.router, prefix="/ui")
