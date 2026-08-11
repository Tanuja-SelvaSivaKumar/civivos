from backend.engine.orchestrator import Orchestrator


class CaseController:

    def __init__(self):
        self.orchestrator = Orchestrator()

    # -----------------------------------
    # Create Case
    # -----------------------------------

    def create_case(
        self,
        citizen_name: str,
        complaint: str
    ):

        case, reasoning, draft = (
            self.orchestrator.create_case(
                citizen_name,
                complaint
            )
        )

        return {
            "case": case,
            "reasoning": reasoning,
            "draft": draft
        }

    # -----------------------------------
    # Get Case
    # -----------------------------------

    def get_case(
        self,
        case_id: str
    ):

        return self.orchestrator.memory.get_case(
            case_id
        )

    # -----------------------------------
    # Get Timeline
    # -----------------------------------

    def get_timeline(
        self,
        case_id: str
    ):

        return self.orchestrator.memory.get_timeline(
            case_id
        )

    # -----------------------------------
    # Approve Case
    # -----------------------------------

    def approve_case(
        self,
        case_id: str
    ):

        case = self.orchestrator.memory.get_case(
            case_id
        )

        if case is None:
            return None

        case = self.orchestrator.workflow.approve_case(
            case
        )

        self.orchestrator.memory.update_case(
            case
        )

        self.orchestrator.memory.add_event(
            case_id,
            "Citizen Approved Draft",
            "Citizen reviewed and approved the generated draft."
        )

        return case

    # -----------------------------------
    # File Case
    # -----------------------------------

    def file_case(
        self,
        case_id: str
    ):

        case = self.orchestrator.memory.get_case(
            case_id
        )

        if case is None:
            return None

        case = self.orchestrator.workflow.file_case(
            case
        )

        self.orchestrator.memory.update_case(
            case
        )

        self.orchestrator.memory.add_event(
            case_id,
            "Case Filed",
            "Application was filed with the appropriate authority."
        )

        return case

    # -----------------------------------
    # Start Waiting For Response
    # -----------------------------------

    def wait_for_response(
        self,
        case_id: str
    ):

        case = self.orchestrator.memory.get_case(
            case_id
        )

        if case is None:
            return None

        case = self.orchestrator.workflow.wait_for_response(
            case
        )

        self.orchestrator.memory.update_case(
            case
        )

        self.orchestrator.memory.add_event(
            case_id,
            "Waiting For Government Response",
            "Civivos is waiting for the government department to respond."
        )

        return case

    # -----------------------------------
    # Run Watcher
    # -----------------------------------

    def run_watcher(self):

        return self.orchestrator.run_daily_watcher()