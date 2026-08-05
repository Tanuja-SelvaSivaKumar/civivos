from pydantic import BaseModel


# ==========================
# Reasoning Agent Result
# ==========================

class ReasoningResult(BaseModel):

    selected_route: str

    reasoning: str

    evidence: list[str]

    rejected_routes: list[str]

    legal_reference: str

    confidence: str


# ==========================
# Drafting Agent Result
# ==========================

class DraftingResult(BaseModel):

    title: str

    subject: str

    body: str

    legal_reference: str