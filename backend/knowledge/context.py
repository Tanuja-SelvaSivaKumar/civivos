from typing import List

from pydantic import BaseModel

from backend.knowledge.models import (
    IssueProfile,
    Department,
    LegalRule,
)


class KnowledgeContext(BaseModel):

    complaint: str

    issue: IssueProfile

    department: Department

    legal_rules: List[LegalRule]