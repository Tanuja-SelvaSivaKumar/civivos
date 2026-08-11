from enum import Enum


class CaseState(str, Enum):
    """
    Represents the complete lifecycle of a CivivOS case.
    Every case moves through these states.
    """

    # Case received by CivivOS
    CREATED = "CREATED"

    # AI analyzing complaint
    ANALYZING = "ANALYZING"

    # AI completed reasoning and generated draft
    DRAFT_READY = "DRAFT_READY"

    # Waiting for citizen confirmation
    WAITING_APPROVAL = "WAITING_APPROVAL"

    # Citizen approved generated draft
    CITIZEN_APPROVED = "CITIZEN_APPROVED"

    # Application/grievance submitted
    FILED = "FILED"

    # Waiting for department response
    WAITING_RESPONSE = "WAITING_RESPONSE"

    # Reminder sent
    REMINDER_SENT = "REMINDER_SENT"

    # Escalated to higher authority
    ESCALATED = "ESCALATED"

    # First appeal required
    FIRST_APPEAL_REQUIRED = "FIRST_APPEAL_REQUIRED"

    # Completed
    CLOSED = "CLOSED"


    def label(self):
        """
        Human readable status names
        for citizen dashboard.
        """

        labels = {

            "CREATED":
                "Case Created",

            "ANALYZING":
                "AI Analysis In Progress",

            "DRAFT_READY":
                "Application Draft Ready",

            "WAITING_APPROVAL":
                "Waiting For Citizen Approval",

            "CITIZEN_APPROVED":
                "Draft Approved By Citizen",

            "FILED":
                "Application Filed",

            "WAITING_RESPONSE":
                "Waiting For Government Response",

            "REMINDER_SENT":
                "Reminder Sent",

            "ESCALATED":
                "Case Escalated",

            "FIRST_APPEAL_REQUIRED":
                "First Appeal Required",

            "CLOSED":
                "Case Closed"
        }

        return labels[self.value]