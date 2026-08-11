import json
from pathlib import Path

from backend.knowledge.context import KnowledgeContext
from backend.knowledge.models import (
    IssueProfile,
    Department,
    LegalRule,
)


class KnowledgeLoader:

    def __init__(self):

        base_path = Path(__file__).parent

        with open(base_path / "issue_mapping.json", "r", encoding="utf-8") as f:
            self.issue_mapping = json.load(f)

        with open(base_path / "departments.json", "r", encoding="utf-8") as f:
            self.departments = json.load(f)

        with open(base_path / "legal_rules.json", "r", encoding="utf-8") as f:
            self.legal_rules = json.load(f)

    def identify_issue(self, complaint: str) -> IssueProfile | None:

        complaint = complaint.lower()

        for keyword, issue in self.issue_mapping.items():

            if keyword.lower() in complaint:
                return IssueProfile(**issue)

        return None

    def get_department(self, department_id: str) -> Department | None:

        department = self.departments.get(department_id)

        if department:
            return Department(**department)

        return None

    def get_rule(self, rule_name: str) -> LegalRule | None:

        rule = self.legal_rules.get(rule_name)

        if rule:
            return LegalRule(**rule)

        return None

    def build_context(self, complaint: str) -> KnowledgeContext | None:

        issue = self.identify_issue(complaint)

        if issue is None:
            return None

        department = self.get_department(issue.department_id)

        if department is None:
            return None

        legal_rules = []

        for rule in self.legal_rules.values():
            legal_rules.append(LegalRule(**rule))

        return KnowledgeContext(
    complaint=complaint,
    issue=issue,
    department=department,
    legal_rules=legal_rules,
)