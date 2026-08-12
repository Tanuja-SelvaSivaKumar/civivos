from backend.models.case import Case


class EscalationAction:

    def execute(
        self,
        case: Case,
        workflow,
        memory
    ) -> Case:

        # -----------------------------------
        # REMINDER_SENT / WAITING_RESPONSE
        #              ↓
        #          ESCALATED
        # -----------------------------------

        case = workflow.escalate_case(
            case
        )

        memory.update_case(
            case
        )

        memory.add_event(
            case.case_id,
            "Case Escalated",
            (
                "CivivOS escalated the case "
                "after the response remained pending."
            )
        )

        return case