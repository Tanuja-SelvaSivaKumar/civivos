from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from backend.models.case_state import CaseState


class Case(BaseModel):
    case_id: str

    citizen_name: str

    complaint: str

    department: str

    legal_route: str

    state: CaseState = CaseState.CREATED

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    last_updated: datetime = Field(
        default_factory=datetime.now
    )

    deadline: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=30)
    )