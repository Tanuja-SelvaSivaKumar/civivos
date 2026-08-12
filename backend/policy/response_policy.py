from datetime import datetime

from backend.models.case import Case
from backend.models.case_state import CaseState


class ResponsePolicy:

    # ==================================================
    # EVALUATE CASE
    # ==================================================

    def evaluate(
        self,
        case: Case,
        now: datetime | None = None
    ) -> str:

        if now is None:
            now = datetime.now()

        # -----------------------------------
        # Only waiting cases are evaluated
        # -----------------------------------

        if case.state != CaseState.WAITING_RESPONSE:
            return "IGNORED"

        # -----------------------------------
        # No deadline
        # -----------------------------------

        if case.deadline is None:
            return "NONE"

        # -----------------------------------
        # Deadline reached
        # -----------------------------------

        if now >= case.deadline:
            return "FIRST_APPEAL_REQUIRED"

        # -----------------------------------
        # Still waiting
        # -----------------------------------

        return "WAITING"