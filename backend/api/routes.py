from fastapi import APIRouter

from api.schemas import ComplaintRequest
from agents.reasoning_agent import ReasoningAgent

router = APIRouter()

reasoning_agent = ReasoningAgent()


@router.post("/complaints")
def create_complaint(request: ComplaintRequest):

    reasoning = reasoning_agent.analyze(request.complaint)

    return {
        "message": "Complaint analyzed successfully.",
        "reasoning": reasoning.model_dump()
    }