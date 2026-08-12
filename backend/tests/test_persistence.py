from datetime import datetime, timedelta

from backend.database.local_store import LocalStore
from backend.memory.memory_engine import MemoryEngine
from backend.models.case import Case
from backend.models.case_state import CaseState


def make_case():

    now = datetime.now()

    return Case(
        case_id="PERSISTENCE-001",
        citizen_name="Persistence Test",
        complaint="Test complaint",
        department="Test Department",
        legal_route="TEST",
        state=CaseState.DRAFT_READY,
        created_at=now,
        last_updated=now,
        deadline=now + timedelta(days=30)
    )


def test_case_persists_across_memory_engine_instances(tmp_path):

    db_path = tmp_path / "civivos_test.db"

    first_store = LocalStore(
        db_path
    )

    first_memory = MemoryEngine(
        first_store
    )

    case = make_case()

    first_memory.add_case(
        case
    )

    first_memory.add_event(
        case.case_id,
        "Case Created",
        "Persistence test event."
    )

    second_store = LocalStore(
        db_path
    )

    second_memory = MemoryEngine(
        second_store
    )

    restored_case = second_memory.get_case(
        case.case_id
    )

    assert restored_case is not None

    assert (
        restored_case.case_id
        == case.case_id
    )

    assert (
        restored_case.citizen_name
        == case.citizen_name
    )

    assert (
        restored_case.state
        == CaseState.DRAFT_READY
    )

    timeline = second_memory.get_timeline(
        case.case_id
    )

    assert len(timeline) == 1

    assert (
        timeline[0].event
        == "Case Created"
    )