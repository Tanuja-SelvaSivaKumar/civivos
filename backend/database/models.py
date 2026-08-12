from datetime import datetime

from pydantic import BaseModel


class CaseRecord(BaseModel):
    case_id: str
    citizen_name: str
    complaint: str
    department: str
    legal_route: str
    state: str
    created_at: datetime
    last_updated: datetime
    deadline: datetime


class EventRecord(BaseModel):
    event_id: str
    case_id: str
    timestamp: datetime
    event: str
    description: str | None = None