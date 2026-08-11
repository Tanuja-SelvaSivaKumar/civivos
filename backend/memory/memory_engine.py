from backend.models.case import Case
from backend.models.event import CaseEvent


class MemoryEngine:

    def __init__(self):

        self.cases: dict[str, Case] = {}

        self.timeline: dict[str, list[CaseEvent]] = {}


    # -----------------------------------
    # Store Case
    # -----------------------------------

    def add_case(
        self,
        case: Case
    ):

        self.cases[case.case_id] = case

        self.timeline.setdefault(
            case.case_id,
            []
        )


    # -----------------------------------
    # Update Case
    # -----------------------------------

    def update_case(
        self,
        case: Case
    ):

        if case.case_id not in self.cases:

            raise ValueError(
                f"Case '{case.case_id}' does not exist."
            )

        self.cases[case.case_id] = case


    # -----------------------------------
    # Get Case
    # -----------------------------------

    def get_case(
        self,
        case_id: str
    ):

        return self.cases.get(
            case_id
        )


    # -----------------------------------
    # Get All Cases
    # -----------------------------------

    def get_all_cases(self):

        return list(
            self.cases.values()
        )


    # -----------------------------------
    # Add Timeline Event
    # -----------------------------------

    def add_event(
        self,
        case_id: str,
        event: str,
        description: str | None = None
    ):

        if case_id not in self.cases:

            raise ValueError(
                f"Cannot add event. "
                f"Case '{case_id}' does not exist."
            )


        timeline = self.timeline.setdefault(
            case_id,
            []
        )


        timeline.append(

            CaseEvent(

                event=event,

                description=description

            )

        )


    # -----------------------------------
    # Get Timeline
    # -----------------------------------

    def get_timeline(
        self,
        case_id: str
    ):

        return self.timeline.get(
            case_id,
            []
        )