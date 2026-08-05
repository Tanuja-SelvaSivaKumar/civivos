from pydantic import BaseModel
from typing import List


class ComplaintRequest(BaseModel):
    name: str
    complaint: str


class AlternativeRoute(BaseModel):
    route: str
    status: str
    reason: str


class ReasoningResult(BaseModel):
    issue_type: str
    department: str
    recommended_route: str
    reason: str
    alternatives: List[AlternativeRoute]
    required_documents: List[str]