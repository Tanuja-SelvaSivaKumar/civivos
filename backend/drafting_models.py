from pydantic import BaseModel


class DraftRequest(BaseModel):
    citizen_name: str
    complaint: str
    department: str
    legal_route: str


class DraftResponse(BaseModel):
    title: str
    body: str


class FirstAppealDraftRequest(BaseModel):
    citizen_name: str
    complaint: str
    department: str
    legal_route: str
    original_case_id: str


class FirstAppealDraftResponse(BaseModel):
    title: str
    body: str
    original_case_id: str