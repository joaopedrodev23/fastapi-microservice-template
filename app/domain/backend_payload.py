from pydantic import BaseModel, Field


class BackendPayload(BaseModel):
    """
    Placeholder schema for the outbound backend payload.
    Replace these fields with the real backend contract fields.
    """

    example_field_1: str = Field(..., description="Replace with real field")
    example_field_2: str = Field(..., description="Replace with real field")
