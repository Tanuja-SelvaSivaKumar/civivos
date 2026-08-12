from datetime import datetime, timedelta

from backend.actions.action_engine import ActionEngine
from backend.database.local_store import LocalStore
from backend.memory.memory_engine import MemoryEngine
from backend.models.case import Case
from backend.models.case_state import CaseState
from backend.workflow.workflow import WorkflowEngine


def create_case(
    case_id: str,
    state: CaseState
):

    now = datetime.now()

    return Case(
        case_id=case_id,
        citizen_name="Action Test Citizen",
        complaint="Ration card pending",
        department="Food Department",
        legal_route="DARPG CPGRAMS",
        state=state,
        created_at=now,
        last_updated=now,
        deadline=now + timedelta(days=30)
    )


def create_action_engine(tmp_path):

    storage = LocalStore(
        tmp_path / "actions_test.db"
    )

    memory = MemoryEngine(
        storage
    )

    workflow = WorkflowEngine()

    actions = ActionEngine(
        workflow,
        memory
    )

    return memory, workflow, actions


# ==================================================
# REMINDER
# ==================================================

def test_send_reminder(tmp_path):

    memory, workflow, actions = (
        create_action_engine(tmp_path)
    )

    case = create_case(
        "ACTION-001",
        CaseState.WAITING_RESPONSE
    )

    memory.add_case(
        case
    )

    case = actions.send_reminder(
        case
    )

    assert (
        case.state
        == CaseState.REMINDER_SENT
    )

    stored_case = memory.get_case(
        case.case_id
    )

    assert stored_case is not None

    assert (
        stored_case.state
        == CaseState.REMINDER_SENT
    )

    timeline = memory.get_timeline(
        case.case_id
    )

    assert len(timeline) == 1

    assert (
        timeline[0].event
        == "Reminder Sent"
    )


# ==================================================
# ESCALATION
# ==================================================

def test_escalate_case(tmp_path):

    memory, workflow, actions = (
        create_action_engine(tmp_path)
    )

    case = create_case(
        "ACTION-002",
        CaseState.REMINDER_SENT
    )

    memory.add_case(
        case
    )

    case = actions.escalate(
        case
    )

    assert (
        case.state
        == CaseState.ESCALATED
    )

    stored_case = memory.get_case(
        case.case_id
    )

    assert stored_case is not None

    assert (
        stored_case.state
        == CaseState.ESCALATED
    )

    timeline = memory.get_timeline(
        case.case_id
    )

    assert len(timeline) == 1

    assert (
        timeline[0].event
        == "Case Escalated"
    )


# ==================================================
# FIRST APPEAL
# ==================================================

def test_require_first_appeal(tmp_path):

    memory, workflow, actions = (
        create_action_engine(tmp_path)
    )

    case = create_case(
        "ACTION-003",
        CaseState.ESCALATED
    )

    memory.add_case(
        case
    )

    case = actions.require_first_appeal(
        case
    )

    assert (
        case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )

    stored_case = memory.get_case(
        case.case_id
    )

    assert stored_case is not None

    assert (
        stored_case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )

    timeline = memory.get_timeline(
        case.case_id
    )

    assert len(timeline) == 1

    assert (
        timeline[0].event
        == "First Appeal Required"
    )


# ==================================================
# FULL ACTION CHAIN
# ==================================================

def test_full_action_chain(tmp_path):

    memory, workflow, actions = (
        create_action_engine(tmp_path)
    )

    case = create_case(
        "ACTION-004",
        CaseState.WAITING_RESPONSE
    )

    memory.add_case(
        case
    )

    # WAITING_RESPONSE
    #        ↓
    # REMINDER_SENT

    case = actions.send_reminder(
        case
    )

    assert (
        case.state
        == CaseState.REMINDER_SENT
    )

    # REMINDER_SENT
    #       ↓
    # ESCALATED

    case = actions.escalate(
        case
    )

    assert (
        case.state
        == CaseState.ESCALATED
    )

    # ESCALATED
    #       ↓
    # FIRST_APPEAL_REQUIRED

    case = actions.require_first_appeal(
        case
    )

    assert (
        case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )

    # -----------------------------------
    # Verify persisted timeline
    # -----------------------------------

    timeline = memory.get_timeline(
        case.case_id
    )

    assert len(timeline) == 3

    assert (
        timeline[0].event
        == "Reminder Sent"
    )

    assert (
        timeline[1].event
        == "Case Escalated"
    )

    assert (
        timeline[2].event
        == "First Appeal Required"
    )