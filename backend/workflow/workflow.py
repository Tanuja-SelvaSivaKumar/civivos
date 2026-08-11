from datetime import datetime

from backend.models.case import Case
from backend.models.case_state import CaseState


class WorkflowEngine:

    # -----------------------------------
    # Analyze Case
    # -----------------------------------

    def analyze_case(self, case: Case):

        if case.state != CaseState.CREATED:
            raise ValueError(
                "Case must be in CREATED state before analysis."
            )

        case.state = CaseState.ANALYZING
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Generate Draft
    # -----------------------------------

    def draft_case(self, case: Case):

        if case.state != CaseState.ANALYZING:
            raise ValueError(
                "Case must be analyzing before draft generation."
            )

        case.state = CaseState.DRAFT_READY
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Legacy Compatibility
    # -----------------------------------

    def complete_analysis(self, case: Case):

        return self.draft_case(case)

    # -----------------------------------
    # Wait For Citizen Approval
    # -----------------------------------

    def wait_for_approval(self, case: Case):

        if case.state != CaseState.DRAFT_READY:
            raise ValueError(
                "Draft must be ready before waiting for approval."
            )

        case.state = CaseState.WAITING_APPROVAL
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Approve Draft
    # -----------------------------------

    def approve_case(self, case: Case):

        if case.state != CaseState.WAITING_APPROVAL:
            raise ValueError(
                "Case must be waiting for approval."
            )

        case.state = CaseState.CITIZEN_APPROVED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # File Case
    # -----------------------------------

    def file_case(self, case: Case):

        if case.state != CaseState.CITIZEN_APPROVED:
            raise ValueError(
                "Case must be approved before filing."
            )

        case.state = CaseState.FILED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Wait For Government Response
    # -----------------------------------

    def wait_for_response(self, case: Case):

        if case.state != CaseState.FILED:
            raise ValueError(
                "Case must be filed before waiting for a response."
            )

        case.state = CaseState.WAITING_RESPONSE
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Send Reminder
    # -----------------------------------

    def send_reminder(self, case: Case):

        if case.state != CaseState.WAITING_RESPONSE:
            raise ValueError(
                "Reminder can only be sent while waiting for a response."
            )

        case.state = CaseState.REMINDER_SENT
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Escalate Case
    # -----------------------------------

    def escalate_case(self, case: Case):

        if case.state not in (
            CaseState.WAITING_RESPONSE,
            CaseState.REMINDER_SENT
        ):
            raise ValueError(
                "Case must be awaiting a response before escalation."
            )

        case.state = CaseState.ESCALATED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # First Appeal
    # -----------------------------------

    def require_first_appeal(self, case: Case):

        if case.state != CaseState.ESCALATED:
            raise ValueError(
                "First appeal requires an escalated case."
            )

        case.state = CaseState.FIRST_APPEAL_REQUIRED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Legacy Compatibility
    # -----------------------------------

    def first_appeal(self, case: Case):

        if case.state not in (
            CaseState.WAITING_RESPONSE,
            CaseState.REMINDER_SENT,
            CaseState.ESCALATED
        ):
            raise ValueError(
                "First appeal requires a pending or escalated case."
            )

        case.state = CaseState.FIRST_APPEAL_REQUIRED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Second Appeal
    # -----------------------------------

    def second_appeal(self, case: Case):

        if case.state != CaseState.FIRST_APPEAL_REQUIRED:
            raise ValueError(
                "Second appeal requires the first appeal stage."
            )

        # CaseState currently has no SECOND_APPEAL_REQUIRED state.
        # Keep the case escalated until a dedicated second-appeal
        # state is added to CaseState.

        case.state = CaseState.ESCALATED
        case.last_updated = datetime.now()

        return case

    # -----------------------------------
    # Close Case
    # -----------------------------------

    def close_case(self, case: Case):

        if case.state == CaseState.CLOSED:
            raise ValueError(
                "Case is already closed."
            )

        case.state = CaseState.CLOSED
        case.last_updated = datetime.now()

        return case