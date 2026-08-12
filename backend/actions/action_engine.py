from uuid import uuid4

from backend.actions.escalation_action import EscalationAction
from backend.actions.reminder_action import ReminderAction
from backend.appeal_models import FirstAppeal
from backend.drafting_models import FirstAppealDraftRequest
from backend.models.case import Case
from backend.models.case_state import CaseState


class ActionEngine:

    def __init__(
        self,
        workflow,
        memory,
        drafter
    ):

        self.workflow = workflow
        self.memory = memory
        self.drafter = drafter

        self.reminder_action = ReminderAction()

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
        case: Case,
        record_event: bool = True
    ) -> Case:

        # -----------------------------------
        # Transition
        # -----------------------------------

        if case.state == CaseState.ESCALATED:

            case = self.workflow.require_first_appeal(
                case
            )

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
        # Persist case state
        # -----------------------------------

        self.memory.update_case(
            case
        )

        # -----------------------------------
        # Generate first-appeal draft
        # -----------------------------------

        request = FirstAppealDraftRequest(
            citizen_name=case.citizen_name,
            complaint=case.complaint,
            department=case.department,
            legal_route=case.legal_route,
            original_case_id=case.case_id
        )

        draft = (
            self.drafter.generate_first_appeal(
                request
            )
        )

        # -----------------------------------
        # Persist first appeal
        # -----------------------------------

        existing_appeal = (
            self.memory.get_first_appeal(
                case.case_id
            )
        )

        if existing_appeal is None:

            appeal = FirstAppeal(
                appeal_id=str(uuid4()),
                case_id=case.case_id,
                citizen_name=case.citizen_name,
                department=case.department,
                legal_route=case.legal_route,
                title=draft.title,
                body=draft.body,
                created_at=case.last_updated
            )

            self.memory.add_first_appeal(
                appeal
            )

        # -----------------------------------
        # Timeline
        # -----------------------------------

        if record_event:

            self.memory.add_event(
                case.case_id,
                "First Appeal Required",
                (
                    "CivivOS determined that a first appeal "
                    "is required and generated a first-appeal draft."
                )
            )

        return case