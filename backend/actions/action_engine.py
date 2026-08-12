from backend.actions.escalation_action import EscalationAction
from backend.actions.reminder_action import ReminderAction
from backend.models.case import Case
from backend.models.case_state import CaseState


class ActionEngine:

    def __init__(
        self,
        workflow,
        memory
    ):

        self.workflow = workflow
        self.memory = memory

        self.reminder_action = ReminderAction()
        self.escalation_action = EscalationAction()

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
        case: Case,
        record_event: bool = True
    ) -> Case:

        # -----------------------------------
        # Direct escalation path
        #
        # ESCALATED
        #     ↓
        # FIRST_APPEAL_REQUIRED
        # -----------------------------------

        if case.state == CaseState.ESCALATED:

            case = self.workflow.require_first_appeal(
                case
            )

        # -----------------------------------
        # Legacy / direct watcher path
        #
        # WAITING_RESPONSE
        # REMINDER_SENT
        # ESCALATED
        #     ↓
        # FIRST_APPEAL_REQUIRED
        # -----------------------------------

        elif case.state in (
            CaseState.WAITING_RESPONSE,
            CaseState.REMINDER_SENT
        ):

            case = self.workflow.first_appeal(
                case
            )

        else:

            raise ValueError(
                "First appeal cannot be required "
                f"from case state '{case.state}'."
            )

        # -----------------------------------
        # Persist state
        # -----------------------------------

        self.memory.update_case(
            case
        )

        # -----------------------------------
        # Timeline event
        # -----------------------------------

        if record_event:

            self.memory.add_event(
                case.case_id,
                "First Appeal Required",
                (
                    "CivivOS determined that a first appeal "
                    "is required."
                )
            )

        return case