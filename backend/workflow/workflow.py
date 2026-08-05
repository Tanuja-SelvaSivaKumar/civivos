from workflow.models import Case
from workflow.states import CaseState


class WorkflowEngine:

    def analyze_case(self, case: Case):

        case.state = CaseState.ANALYZED

        return case

    def draft_case(self, case: Case):

        case.state = CaseState.DRAFTED

        return case

    def wait_for_approval(self, case: Case):

        case.state = CaseState.WAITING_FOR_APPROVAL

        return case

    def approve_case(self, case: Case):

        case.state = CaseState.FILED

        return case

    def wait_for_response(self, case: Case):

        case.state = CaseState.WAITING_FOR_RESPONSE

        return case

    def first_appeal(self, case: Case):

        case.state = CaseState.FIRST_APPEAL

        return case

    def second_appeal(self, case: Case):

        case.state = CaseState.SECOND_APPEAL

        return case

    def close_case(self, case: Case):

        case.state = CaseState.CLOSED

        return case