from datetime import datetime

from backend.memory.timeline import (
    TimelineEvent,
    CaseHistory
)


class MemoryStore:

    def __init__(self):

        self.store = {}


    def create_case(self, case_id: str):

        self.store[case_id] = CaseHistory()


    def add_event(
        self,
        case_id: str,
        event: str
    ):

        if case_id not in self.store:
            self.create_case(case_id)


        self.store[case_id].events.append(

            TimelineEvent(
                timestamp=datetime.now(),
                event=event
            )

        )


    def get_history(
        self,
        case_id: str
    ):

        return self.store.get(case_id)