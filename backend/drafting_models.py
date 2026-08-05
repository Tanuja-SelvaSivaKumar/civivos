from pydantic import BaseModel


class DraftRequest(BaseModel):
    citizen_name: str
    complaint: str
    department: str
    legal_route: str


class DraftResponse(BaseModel):
    title: str
    body: str