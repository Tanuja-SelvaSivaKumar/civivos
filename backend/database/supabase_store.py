from backend.database.storage import StorageBackend
from backend.models.case import Case
from backend.models.event import CaseEvent


class SupabaseStore(StorageBackend):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "SupabaseStore is reserved for the production "
            "Supabase integration milestone."
        )

    def add_case(self, case: Case) -> None:
        raise NotImplementedError

    def update_case(self, case: Case) -> None:
        raise NotImplementedError

    def get_case(self, case_id: str) -> Case | None:
        raise NotImplementedError

    def get_all_cases(self) -> list[Case]:
        raise NotImplementedError

    def add_event(
        self,
        case_id: str,
        event: CaseEvent
    ) -> None:
        raise NotImplementedError

    def get_timeline(
        self,
        case_id: str
    ) -> list[CaseEvent]:
        raise NotImplementedError