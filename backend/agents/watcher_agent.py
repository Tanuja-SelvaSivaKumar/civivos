from datetime import datetime

from workflow.states import CaseState
from models.watcher_result import WatcherResult


class WatcherAgent:

    def check_case(self, case):

        today = datetime.now()

        if case.deadline is None:

            return WatcherResult(
                case_id=case.case_id,
                action_taken=False,
                action="None",
                reason="No deadline available."
            )

        if today >= case.deadline:

            case.state = CaseState.FIRST_APPEAL

            return WatcherResult(
                case_id=case.case_id,
                action_taken=True,
                action="First Appeal",
                reason="Statutory deadline crossed."
            )

        return WatcherResult(
            case_id=case.case_id,
            action_taken=False,
            action="Waiting",
            reason="Deadline not reached."
        )