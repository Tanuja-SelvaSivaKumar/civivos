from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class CaseEvent(BaseModel):
    """
    Represents a single event in the lifecycle
    of a Civivos case.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = Field(
        default_factory=datetime.now
    )

    event: str

    description: str | None = None