import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.logging import set_event_id
from app.domain.dme_input import DMEInput
from app.integrations.outbound_rest import OutboundError, send_to_backend
from app.services.mapper import MappingError, map_dme_to_backend

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter()


class StandardResponse(BaseModel):
    status: str
    message: str
    eventId: str


def build_response(status_value: str, message: str, event_id: str) -> dict:
    return {
        "status": status_value,
        "message": message,
        "eventId": event_id,
    }


@router.post(f"/{settings.service.name}", response_model=StandardResponse, status_code=200)
async def receive_dme(dme: DMEInput):
    event_id = str(dme.header.eventId)
    set_event_id(event_id)

    logger.info("Received DME")

    try:
        backend_payload = map_dme_to_backend(dme.payload.data)
    except MappingError as exc:
        logger.warning("Mapping error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=build_response("ERROR", str(exc), event_id),
        )

    try:
        await send_to_backend(backend_payload.dict(), settings)
    except OutboundError as exc:
        logger.warning("Outbound error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=build_response("ERROR", str(exc), event_id),
        )

    return build_response("SUCCESS", "Operacao realizada com sucesso.", event_id)
