import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.inbound import build_response, router
from app.core.config import get_settings
from app.core.logging import set_event_id, setup_logging

settings = get_settings()
setup_logging(settings.logging.level)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.service.name)
app.include_router(router)


def _extract_event_id(body: Dict[str, Any]) -> str:
    header = body.get("header") or {}
    event_id = header.get("eventId")
    if event_id is None:
        return "-"
    return str(event_id)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    event_id = "-"
    try:
        body = await request.json()
        if isinstance(body, dict):
            event_id = _extract_event_id(body)
    except Exception:
        pass

    set_event_id(event_id)
    logger.warning("Validation error: %s", exc)

    return JSONResponse(
        status_code=400,
        content=build_response(
            "ERROR",
            "Requisicao invalida. Verifique o payload DME.",
            event_id,
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    event_id = "-"
    try:
        body = await request.json()
        if isinstance(body, dict):
            event_id = _extract_event_id(body)
    except Exception:
        pass

    set_event_id(event_id)
    logger.exception("Unhandled error")

    return JSONResponse(
        status_code=500,
        content=build_response("ERROR", "Erro interno inesperado.", event_id),
    )
