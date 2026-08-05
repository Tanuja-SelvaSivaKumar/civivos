from datetime import datetime

from pydantic import BaseModel


class MemoryEvent(BaseModel):

    timestamp: datetime

    event: str