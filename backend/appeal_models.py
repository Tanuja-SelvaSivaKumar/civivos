from datetime import datetime

from pydantic import BaseModel


class FirstAppeal(BaseModel):

    appeal_id: str

    case_id: str

    citizen_name: str

    department: str

    legal_route: str

    title: str

    body: str

    created_at: datetime