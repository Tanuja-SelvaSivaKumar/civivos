from datetime import datetime, timedelta

from backend.engine.orchestrator import Orchestrator
from backend.models.case_state import CaseState


# ==================================================
# CREATE CASE
# ==================================================

def test_create_case():

    orch = Orchestrator()

    case, reasoning, draft = orch.create_case(
        "Rahul Sharma",
        "My ration card application has been pending for three months.",
    )

    # -----------------------------------
    # Case
    # -----------------------------------

    assert case is not None

    assert case.citizen_name == "Rahul Sharma"

    assert (
        case.complaint
        == "My ration card application has been pending for three months."
    )

    # -----------------------------------
    # Reasoning
    # -----------------------------------

    assert reasoning is not None

    # -----------------------------------
    # Draft
    # -----------------------------------

    assert draft is not None

    assert draft.title is not None

    # -----------------------------------
    # Workflow
    #
    # create_case() completes:
    #
    # CREATED
    #     ↓
    # ANALYZING
    #     ↓
    # DRAFT_READY
    #     ↓
    # WAITING_APPROVAL
    #
    # -----------------------------------

    assert case.state == CaseState.WAITING_APPROVAL


# ==================================================
# CASE TIMELINE
# ==================================================

def test_case_timeline_exists():

    orch = Orchestrator()

    case, reasoning, draft = orch.create_case(
        "Rahul Sharma",
        "My ration card application has been pending for three months.",
    )

    timeline = orch.memory.get_timeline(
        case.case_id
    )

    assert timeline is not None

    assert len(timeline) > 0


# ==================================================
# DAILY WATCHER
# ==================================================

def test_daily_watcher():

    orch = Orchestrator()

    case, reasoning, draft = orch.create_case(
        "Rahul Sharma",
        "My ration card application has been pending for three months.",
    )

    # -----------------------------------
    # Case is still waiting for citizen
    # approval, so it is NOT watchable.
    # -----------------------------------

    assert case.state == CaseState.WAITING_APPROVAL

    # -----------------------------------
    # Save the case ID so we can verify
    # that THIS case is not returned by
    # the watcher.
    # -----------------------------------

    case_id = case.case_id

    # -----------------------------------
    # Run watcher.
    #
    # The persistent database may contain
    # other WAITING_RESPONSE cases.
    # -----------------------------------

    results = orch.run_daily_watcher()

    assert results is not None

    # -----------------------------------
    # Our WAITING_APPROVAL case must not
    # appear in watcher results.
    # -----------------------------------

    watched_case_ids = {
        result.case_id
        for result in results
    }

    assert case_id not in watched_case_ids


# ==================================================
# WATCHER → FIRST APPEAL
# ==================================================

def test_watcher_moves_expired_case_to_first_appeal():

    orch = Orchestrator()

    # -----------------------------------
    # Create Case
    #
    # create_case() ends at:
    #
    # WAITING_APPROVAL
    # -----------------------------------

    case, reasoning, draft = orch.create_case(
        "Tanuja",
        "My ration card application has been pending for three months.",
    )

    assert case.state == CaseState.WAITING_APPROVAL

    # -----------------------------------
    # Citizen approves draft
    #
    # WAITING_APPROVAL
    #        ↓
    # CITIZEN_APPROVED
    # -----------------------------------

    case = orch.workflow.approve_case(
        case
    )

    assert case.state == CaseState.CITIZEN_APPROVED

    # -----------------------------------
    # File Case
    #
    # CITIZEN_APPROVED
    #        ↓
    # FILED
    # -----------------------------------

    case = orch.workflow.file_case(
        case
    )

    assert case.state == CaseState.FILED

    # -----------------------------------
    # Start Waiting For Response
    #
    # FILED
    #        ↓
    # WAITING_RESPONSE
    # -----------------------------------

    case = orch.workflow.wait_for_response(
        case
    )

    assert case.state == CaseState.WAITING_RESPONSE

    # -----------------------------------
    # Simulate deadline passing
    # -----------------------------------

    case.deadline = (
        datetime.now()
        - timedelta(days=1)
    )

    # -----------------------------------
    # Save updated case
    # -----------------------------------

    orch.memory.update_case(
        case
    )

    # -----------------------------------
    # Run Watcher
    # -----------------------------------

    results = orch.run_daily_watcher()

    assert results is not None

    assert len(results) > 0

    # -----------------------------------
    # Find our case's result
    # -----------------------------------

    result = next(
        result
        for result in results
        if result.case_id == case.case_id
    )

    # -----------------------------------
    # Verify watcher action
    # -----------------------------------

    assert result.action_taken is True

    assert (
        result.action
        == "FIRST_APPEAL_REQUIRED"
    )

    assert (
        result.reason
        == "Response deadline crossed."
    )

    # -----------------------------------
    # Verify final case state
    # -----------------------------------

    updated_case = orch.memory.get_case(
        case.case_id
    )

    assert updated_case is not None

    assert (
        updated_case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )

    # -----------------------------------
    # Verify timeline contains the
    # watcher action exactly once.
    # -----------------------------------

    timeline = orch.memory.get_timeline(
        case.case_id
    )

    appeal_events = [
        event
        for event in timeline
        if event.event
        == "FIRST_APPEAL_REQUIRED"
    ]

    assert len(appeal_events) == 1