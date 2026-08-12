from datetime import datetime

from backend.models.case_state import CaseState
from backend.models.watcher_result import WatcherResult
from backend.policy.response_policy import ResponsePolicy


class WatcherAgent:

    def __init__(
        self,
        policy: ResponsePolicy | None = None
    ):

        self.policy = (
            policy
            if policy is not None
            else ResponsePolicy()
        )

    # ==========================================
    # CHECK CASE
    # ==========================================

    def check_case(self, case):

        now = datetime.now()

        # --------------------------------------
        # Ask the policy what should happen
        # --------------------------------------

        decision = self.policy.evaluate(
            case,
            now
        )

        # --------------------------------------
        # Case is not currently watchable
        # --------------------------------------

        if decision == "IGNORED":

            return WatcherResult(

                case_id=case.case_id,

                action_taken=False,

                action="IGNORED",

                reason=(
                    "Case is not currently waiting "
                    "for a government response."
                )
            )

        # --------------------------------------
        # No usable deadline
        # --------------------------------------

        if decision == "NONE":

            return WatcherResult(

                case_id=case.case_id,

                action_taken=False,

                action="NONE",

                reason="No deadline available."
            )

        # --------------------------------------
        # Deadline reached
        # --------------------------------------

        if decision == "FIRST_APPEAL_REQUIRED":

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

        # --------------------------------------
        # Still waiting
        # --------------------------------------

        return WatcherResult(

            case_id=case.case_id,

            action_taken=False,

            action="WAITING",

            reason="Deadline not reached."
        )