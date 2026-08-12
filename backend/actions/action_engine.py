from backend.actions.escalation_action import EscalationAction
from backend.actions.reminder_action import ReminderAction
from backend.models.case import Case


class ActionEngine:

    def __init__(
        self,
        workflow,
        memory
    ):

        self.workflow = workflow

        self.memory = memory

        self.reminder_action = (
            ReminderAction()
        )

        self.escalation_action = (
            EscalationAction()
        )

    # ==================================================
    # SEND REMINDER
    # ==================================================

    def send_reminder(
        self,
        case: Case
    ) -> Case:

        return self.reminder_action.execute(
            case,
            self.workflow,
            self.memory
        )

    # ==================================================
    # ESCALATE CASE
    # ==================================================

    def escalate(
        self,
        case: Case
    ) -> Case:

        return self.escalation_action.execute(
            case,
            self.workflow,
            self.memory
        )

    # ==================================================
    # REQUIRE FIRST APPEAL
    # ==================================================

    def require_first_appeal(
        self,
        case: Case
    ) -> Case:

        case = self.workflow.require_first_appeal(
            case
        )

        self.memory.update_case(
            case
        )

        self.memory.add_event(
            case.case_id,
            "First Appeal Required",
            (
                "CivivOS determined that a first appeal "
                "is required."
            )
        )

        return case