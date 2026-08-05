from typing import List
from pydantic import BaseModel


class IssueProfile(BaseModel):
    issue_type: str
    department_id: str


class Department(BaseModel):
    name: str
    authority: str


class LegalRule(BaseModel):
    description: str
    conditions: List[str]
    not_for: List[str] = []
    law: str
    section: str | None = None