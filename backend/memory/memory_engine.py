from datetime import datetime

from memory.event import MemoryEvent


class MemoryEngine:

    def __init__(self):

        self.timeline = {}

        self.cases = {}

    def add_case(self, case):

        self.cases[case.case_id] = case

        self.timeline[case.case_id] = []

    def get_case(self, case_id):

        return self.cases.get(case_id)

    def get_all_cases(self):

        return list(self.cases.values())

    def add_event(self, case_id, event):

        if case_id not in self.timeline:
            self.timeline[case_id] = []

        self.timeline[case_id].append(
            MemoryEvent(
                timestamp=datetime.now(),
                event=event
            )
        )

    def get_timeline(self, case_id):

        return self.timeline.get(case_id, [])