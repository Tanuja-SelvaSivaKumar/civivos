from datetime import datetime, timedelta

from backend.actions.action_engine import ActionEngine
from backend.database.local_store import LocalStore
from backend.memory.memory_engine import MemoryEngine
from backend.models.case import Case
from backend.models.case_state import CaseState
from backend.workflow.workflow import WorkflowEngine
from backend.agents.drafting_agent import DraftingAgent


def create_engine(tmp_path):

    storage = LocalStore(
        tmp_path / "first_appeal_test.db"
    )

    memory = MemoryEngine(
        storage
    )

    workflow = WorkflowEngine()

    drafter = DraftingAgent()

    actions = ActionEngine(
        workflow,
        memory,
        drafter
    )

    return memory, workflow, actions


def create_case():

    now = datetime.now()

    return Case(
        case_id="APPEAL-001",
        citizen_name="Tanuj",
        complaint="My ration card has been pending for 3 months.",
        department="Food and Civil Supplies Department",
        legal_route="DARPG CPGRAMS",
        state=CaseState.ESCALATED,
        created_at=now,
        last_updated=now,
        deadline=now + timedelta(days=30)
    )


def test_first_appeal_draft_is_generated_and_persisted(
    tmp_path
):

    memory, workflow, actions = (
        create_engine(tmp_path)
    )

    case = create_case()

    memory.add_case(
        case
    )

    actions.require_first_appeal(
        case
    )

    assert (
        case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )

    appeal = memory.get_first_appeal(
        case.case_id
    )

    assert appeal is not None

    assert (
        appeal.case_id
        == case.case_id
    )

    assert (
        appeal.citizen_name
        == "Tanuj"
    )

    assert (
        appeal.legal_route
        == "DARPG CPGRAMS"
    )

    assert (
        appeal.title
        == "First Appeal - DARPG CPGRAMS"
    )

    assert "Original Case ID:" in appeal.body

    assert case.case_id in appeal.body


def test_first_appeal_survives_storage_reload(
    tmp_path
):

    db_path = (
        tmp_path
        / "first_appeal_reload.db"
    )

    first_storage = LocalStore(
        db_path
    )

    first_memory = MemoryEngine(
        first_storage
    )

    workflow = WorkflowEngine()

    drafter = DraftingAgent()

    actions = ActionEngine(
        workflow,
        first_memory,
        drafter
    )

    case = create_case()

    first_memory.add_case(
        case
    )

    actions.require_first_appeal(
        case
    )

    second_storage = LocalStore(
        db_path
    )

    second_memory = MemoryEngine(
        second_storage
    )

    restored_appeal = (
        second_memory.get_first_appeal(
            case.case_id
        )
    )

    assert restored_appeal is not None

    assert (
        restored_appeal.case_id
        == case.case_id
    )

    assert (
        restored_appeal.title
        == "First Appeal - DARPG CPGRAMS"
    )