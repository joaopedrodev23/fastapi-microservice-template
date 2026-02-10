import logging
from typing import Any, Dict

import httpx

from app.core.config import Settings

logger = logging.getLogger(__name__)


class OutboundError(RuntimeError):
    """Controlled error for outbound REST failures."""


def _build_url(settings: Settings) -> str:
    base = settings.backend.base_url.rstrip("/")
    path = settings.backend.endpoint_path.lstrip("/")
    if path:
        return f"{base}/{path}"
    return base


async def send_to_backend(payload: Dict[str, Any], settings: Settings) -> None:
    if settings.backend.mock_enabled:
        logger.info("Mock outbound REST called")
        return

    url = _build_url(settings)
    logger.info("Calling backend", extra={"backend_url": url})

    try:
        async with httpx.AsyncClient(timeout=settings.backend.timeout_seconds) as client:
            response = await client.post(url, json=payload, headers=settings.backend.headers)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.exception("Backend returned non-success status: %s", exc.response.status_code)
        raise OutboundError("Falha ao encaminhar para o backend.") from exc
    except httpx.RequestError as exc:
        logger.exception("Backend request failed")
        raise OutboundError("Falha ao encaminhar para o backend.") from exc
