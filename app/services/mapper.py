from typing import Any, Dict

from app.domain.backend_payload import BackendPayload


class MappingError(ValueError):
    """Controlled error for mapping issues (missing fields, invalid formats)."""


def map_dme_to_backend(data: Dict[str, Any]) -> BackendPayload:
    """
    Explicit mapping from DME payload.data to BackendPayload.

    IMPORTANT: Replace the required_fields and mapping below with real fields
    from your service's DME contract.
    """

    required_fields = ["example_field_1", "example_field_2"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise MappingError(f"Campos obrigatorios ausentes no payload.data: {', '.join(missing)}")

    return BackendPayload(
        example_field_1=str(data["example_field_1"]),
        example_field_2=str(data["example_field_2"]),
    )
