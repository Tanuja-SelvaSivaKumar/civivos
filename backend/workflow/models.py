from datetime import datetime, timedelta

from pydantic import BaseModel

from workflow.states import CaseState


class Case(BaseModel):

    case_id: str

    citizen_name: str

    complaint: str

    department: str

    legal_route: str

    state: CaseState = CaseState.NEW

    created_at: datetime = datetime.now()

    last_updated: datetime = datetime.now()

    deadline: datetime = datetime.now() + timedelta(days=30)