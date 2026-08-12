from datetime import datetime, timedelta

from backend.agents.watcher_agent import WatcherAgent
from backend.models.case import Case
from backend.models.case_state import CaseState
from backend.policy.response_policy import ResponsePolicy


def make_case(
    state: CaseState,
    deadline: datetime
):

    now = datetime.now()

    return Case(
        case_id="WATCHER-POLICY-001",
        citizen_name="Watcher Policy Test",
        complaint="Ration card pending",
        department="Food Department",
        legal_route="DARPG CPGRAMS",
        state=state,
        created_at=now,
        last_updated=now,
        deadline=deadline
    )


def test_watcher_uses_policy_before_deadline():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_RESPONSE,
        now + timedelta(days=1)
    )

    watcher = WatcherAgent(
        ResponsePolicy()
    )

    result = watcher.check_case(
        case
    )

    assert result.action_taken is False
    assert result.action == "WAITING"
    assert result.reason == "Deadline not reached."

    assert case.state == CaseState.WAITING_RESPONSE


def test_watcher_uses_policy_after_deadline():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_RESPONSE,
        now - timedelta(days=1)
    )

    watcher = WatcherAgent(
        ResponsePolicy()
    )

    result = watcher.check_case(
        case
    )

    assert result.action_taken is True

    assert (
        result.action
        == "FIRST_APPEAL_REQUIRED"
    )

    assert (
        result.reason
        == "Response deadline crossed."
    )

    assert (
        case.state
        == CaseState.FIRST_APPEAL_REQUIRED
    )


def test_watcher_ignores_non_waiting_case():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_APPROVAL,
        now - timedelta(days=1)
    )

    watcher = WatcherAgent(
        ResponsePolicy()
    )

    result = watcher.check_case(
        case
    )

    assert result.action_taken is False
    assert result.action == "IGNORED"

    assert (
        case.state
        == CaseState.WAITING_APPROVAL
    )