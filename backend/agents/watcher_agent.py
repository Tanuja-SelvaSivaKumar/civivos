from datetime import datetime

from backend.models.case_state import CaseState
from backend.models.watcher_result import WatcherResult


class WatcherAgent:

    # -----------------------------------
    # Check Case
    # -----------------------------------

    def check_case(self, case):

        now = datetime.now()

        # --------------------------------
        # Only monitor waiting cases
        # --------------------------------

        if case.state != CaseState.WAITING_RESPONSE:

            return WatcherResult(

                case_id=case.case_id,

                action_taken=False,

                action="IGNORED",

                reason=(
                    "Case is not currently waiting "
                    "for a government response."
                )
            )

        # --------------------------------
        # No deadline
        # --------------------------------

        if case.deadline is None:

            return WatcherResult(

                case_id=case.case_id,

                action_taken=False,

                action="NONE",

                reason="No deadline available."
            )

        # --------------------------------
        # Deadline crossed
        # --------------------------------

        if now >= case.deadline:

            case.state = (
                CaseState.FIRST_APPEAL_REQUIRED
            )

            case.last_updated = now

            return WatcherResult(

                case_id=case.case_id,

                action_taken=True,

                action="FIRST_APPEAL_REQUIRED",

                reason="Response deadline crossed."
            )

        # --------------------------------
        # Still waiting
        # --------------------------------

        return WatcherResult(

            case_id=case.case_id,

            action_taken=False,

            action="WAITING",

            reason="Deadline not reached."
        )