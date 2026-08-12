import os

from backend.database.local_store import LocalStore
from backend.database.storage import StorageBackend
from backend.models.case import Case
from backend.models.event import CaseEvent


class MemoryEngine:

    def __init__(
        self,
        storage: StorageBackend | None = None
    ):

        if storage is not None:

            self.storage = storage

            return

        database_path = os.getenv(
            "CIVIVOS_DB_PATH",
            "data/civivos.db"
        )

        self.storage = LocalStore(
            database_path
        )

    # ==================================================
    # CASES
    # ==================================================

    def add_case(
        self,
        case: Case
    ):

        self.storage.add_case(
            case
        )

    def update_case(
        self,
        case: Case
    ):

        self.storage.update_case(
            case
        )

    def get_case(
        self,
        case_id: str
    ):

        return self.storage.get_case(
            case_id
        )

    def get_all_cases(self):

        return self.storage.get_all_cases()

    def get_waiting_response_cases(self):

        return self.storage.get_waiting_response_cases()

    # ==================================================
    # EVENTS
    # ==================================================

    def add_event(
        self,
        case_id: str,
        event: str,
        description: str | None = None
    ):

        if self.storage.get_case(case_id) is None:

            raise ValueError(
                f"Cannot add event. "
                f"Case '{case_id}' does not exist."
            )

        timeline_event = CaseEvent(
            event=event,
            description=description
        )

        self.storage.add_event(
            case_id,
            timeline_event
        )

    def get_timeline(
        self,
        case_id: str
    ):

        return self.storage.get_timeline(
            case_id
        )

    # ==================================================
    # FIRST APPEAL
    # ==================================================

    def add_first_appeal(
        self,
        appeal
    ):

        self.storage.add_first_appeal(
            appeal
        )

    def get_first_appeal(
        self,
        case_id: str
    ):

        return self.storage.get_first_appeal(
            case_id
        )