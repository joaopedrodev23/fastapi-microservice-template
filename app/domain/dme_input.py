from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field


class DMEHeader(BaseModel):
    eventId: UUID = Field(..., description="Unique event identifier")
    source: str = Field(..., min_length=1, description="Event source")
    timestamp: datetime = Field(..., description="ISO-8601 timestamp")


class DMEPayload(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict, description="Service-specific data")


class DMEInput(BaseModel):
    header: DMEHeader
    payload: DMEPayload
