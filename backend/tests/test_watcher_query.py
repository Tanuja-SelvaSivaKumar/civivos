from datetime import datetime, timedelta

from backend.database.local_store import LocalStore
from backend.memory.memory_engine import MemoryEngine
from backend.models.case import Case
from backend.models.case_state import CaseState


def make_case(
    case_id: str,
    state: CaseState
):

    now = datetime.now()

    return Case(
        case_id=case_id,
        citizen_name="Watcher Test",
        complaint="Watcher filtering test",
        department="Test Department",
        legal_route="TEST",
        state=state,
        created_at=now,
        last_updated=now,
        deadline=now + timedelta(days=30)
    )


def test_get_waiting_response_cases_returns_only_waiting_cases(
    tmp_path
):

    db_path = tmp_path / "watcher_filter_test.db"

    storage = LocalStore(
        db_path
    )

    memory = MemoryEngine(
        storage
    )

    waiting_case = make_case(
        "WAITING-001",
        CaseState.WAITING_RESPONSE
    )

    approval_case = make_case(
        "APPROVAL-001",
        CaseState.WAITING_APPROVAL
    )

    filed_case = make_case(
        "FILED-001",
        CaseState.FILED
    )

    memory.add_case(
        waiting_case
    )

    memory.add_case(
        approval_case
    )

    memory.add_case(
        filed_case
    )

    cases = memory.get_waiting_response_cases()

    case_ids = {
        case.case_id
        for case in cases
    }

    assert case_ids == {
        "WAITING-001"
    }