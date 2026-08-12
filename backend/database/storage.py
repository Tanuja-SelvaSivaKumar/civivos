from abc import ABC, abstractmethod

from backend.models.case import Case
from backend.models.event import CaseEvent


class StorageBackend(ABC):

    @abstractmethod
    def add_case(
        self,
        case: Case
    ) -> None:
        pass

    @abstractmethod
    def update_case(
        self,
        case: Case
    ) -> None:
        pass

    @abstractmethod
    def get_case(
        self,
        case_id: str
    ) -> Case | None:
        pass

    @abstractmethod
    def get_all_cases(
        self
    ) -> list[Case]:
        pass

    @abstractmethod
    def get_waiting_response_cases(
        self
    ) -> list[Case]:
        pass

    @abstractmethod
    def add_event(
        self,
        case_id: str,
        event: CaseEvent
    ) -> None:
        pass

    @abstractmethod
    def get_timeline(
        self,
        case_id: str
    ) -> list[CaseEvent]:
        pass

    @abstractmethod
    def add_first_appeal(
        self,
        appeal
    ) -> None:
        pass

    @abstractmethod
    def get_first_appeal(
        self,
        case_id: str
    ):
        pass