from typing import List

from pydantic import BaseModel

from knowledge.models import (
    IssueProfile,
    Department,
    LegalRule,
)


class KnowledgeContext(BaseModel):

    issue: IssueProfile

    department: Department

    legal_rules: List[LegalRule]