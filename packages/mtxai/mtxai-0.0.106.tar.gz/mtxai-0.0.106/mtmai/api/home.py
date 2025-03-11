import structlog
from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_oauth2_redirect_html

# from mtmlib.decorators.mtform.mtform import MtForm
from opentelemetry import trace

from mtmai.core.config import settings

# from mtmai.models.models import Message

# from mtmai.types.types import Theme
# from mtmai.utils import generate_test_email, send_email

tracer = trace.get_tracer_provider().get_tracer(__name__)
LOG = structlog.get_logger()


# mimetypes.add_type("application/javascript", ".js")
# mimetypes.add_type("text/css", ".css")


router = APIRouter()


@router.get("/health", include_in_schema=False)
async def health_check():
    with tracer.start_as_current_span("health-span"):
        LOG.info("get /health")
        current_span = trace.get_current_span()
        current_span.add_event("This is a span event")
        LOG.warning("This is a log message")
        return {"health": True}


@router.get("/swagger-ui-oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=router.app().openapi_url,
        title=router.app().title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


@router.get("/info", include_in_schema=False)
async def app_info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


# @router.post(
#     "/test-email/",
#     dependencies=[Depends(get_current_active_superuser)],
#     status_code=201,
#     include_in_schema=False,
# )
# class TestUrlReq(BaseModel):
#     url: str


# class TypesResponse(BaseModel):
#     """
#     如果使用openapi 生成前端代码，缺少了某些类型，请在这里补充
#     """

#     thread_form: ThreadForm | None = None
#     uiState: ChatBotUiStateResponse | None = None
#     thread_ui_state: ThreadUIState | None = None
#     chat_profile: ChatProfile | None = None
#     list_view_props: ListViewProps | None = None
#     # mt_form: MtForm | None = None
#     open_canvas_state: OpenCanvasState | None = None


# @router.get("/types", include_in_schema=True, response_model=TypesResponse)
# async def types():
#     """
#     无实际功能，仅用于openapi生成前端代码
#     """
#     return TypesResponse()
