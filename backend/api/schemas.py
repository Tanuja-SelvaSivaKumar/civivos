from pydantic import BaseModel
from typing import List



class CaseCreateRequest(BaseModel):

    citizen_name: str

    complaint: str



class AlternativeRoute(BaseModel):

    route: str

    status: str

    reason: str



class ReasoningResponse(BaseModel):

    selected_route: str

    reasoning: str

    evidence: List[str]

    rejected_routes: List[str]

    legal_reference: str

    confidence: str



class DraftResponseSchema(BaseModel):

    title: str

    body: str



class CaseResponse(BaseModel):

    case_id: str

    citizen_name: str

    complaint: str

    department: str

    legal_route: str

    state: str



class CaseCreateResponse(BaseModel):

    case: CaseResponse

    reasoning: ReasoningResponse

    draft: DraftResponseSchema