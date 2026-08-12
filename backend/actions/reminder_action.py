from backend.models.case import Case


class ReminderAction:

    def execute(
        self,
        case: Case,
        workflow,
        memory
    ) -> Case:

        # -----------------------------------
        # WAITING_RESPONSE
        #        ↓
        # REMINDER_SENT
        # -----------------------------------

        case = workflow.send_reminder(
            case
        )

        memory.update_case(
            case
        )

        memory.add_event(
            case.case_id,
            "Reminder Sent",
            (
                "CivivOS sent a reminder while "
                "waiting for a government response."
            )
        )

        return case