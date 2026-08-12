from datetime import datetime, timedelta

from backend.models.case import Case
from backend.models.case_state import CaseState
from backend.policy.response_policy import ResponsePolicy


def make_case(
    state: CaseState,
    deadline: datetime
):

    now = datetime.now()

    return Case(
        case_id="POLICY-001",
        citizen_name="Policy Test Citizen",
        complaint="Policy test complaint",
        department="Test Department",
        legal_route="TEST",
        state=state,
        created_at=now,
        last_updated=now,
        deadline=deadline
    )


# ==================================================
# BEFORE DEADLINE
# ==================================================

def test_policy_returns_waiting_before_deadline():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_RESPONSE,
        now + timedelta(days=1)
    )

    policy = ResponsePolicy()

    result = policy.evaluate(
        case,
        now
    )

    assert result == "WAITING"


# ==================================================
# AFTER DEADLINE
# ==================================================

def test_policy_returns_first_appeal_after_deadline():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_RESPONSE,
        now - timedelta(days=1)
    )

    policy = ResponsePolicy()

    result = policy.evaluate(
        case,
        now
    )

    assert result == "FIRST_APPEAL_REQUIRED"


# ==================================================
# WRONG STATE
# ==================================================

def test_policy_ignores_non_waiting_case():

    now = datetime.now()

    case = make_case(
        CaseState.WAITING_APPROVAL,
        now - timedelta(days=1)
    )

    policy = ResponsePolicy()

    result = policy.evaluate(
        case,
        now
    )

    assert result == "IGNORED"