from fastapi.routing import APIRouter

from tracking_ui.web.api import react, athena, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router, prefix="/health")
api_router.include_router(athena.router, prefix="/athena")
api_router.include_router(react.router, prefix="/react")
