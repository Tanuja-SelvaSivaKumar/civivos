from datetime import datetime

from backend.models.case import Case
from backend.models.case_state import CaseState
from backend.workflow.workflow import WorkflowEngine


def create_test_case():
    return Case(
        case_id="123",
        citizen_name="Tanuj",
        complaint="Ration card pending",
        department="Food Department",
        legal_route="CPGRAMS",
        state=CaseState.CREATED,
        created_at=datetime.now(),
        last_updated=datetime.now(),
    )


def test_complete_case_workflow():
    workflow = WorkflowEngine()
    case = create_test_case()

    # -----------------------------------
    # Initial
    # -----------------------------------

    assert case.state == CaseState.CREATED

    # -----------------------------------
    # Analyze
    # -----------------------------------

    workflow.analyze_case(case)

    assert case.state == CaseState.ANALYZING

    # -----------------------------------
    # Generate Draft
    # -----------------------------------

    workflow.draft_case(case)

    assert case.state == CaseState.DRAFT_READY

    # -----------------------------------
    # Wait For Citizen Approval
    # -----------------------------------

    workflow.wait_for_approval(case)

    assert case.state == CaseState.WAITING_APPROVAL

    # -----------------------------------
    # Citizen Approves
    # -----------------------------------

    workflow.approve_case(case)

    assert case.state == CaseState.CITIZEN_APPROVED

    # -----------------------------------
    # File Case
    # -----------------------------------

    workflow.file_case(case)

    assert case.state == CaseState.FILED

    # -----------------------------------
    # Wait For Government Response
    # -----------------------------------

    workflow.wait_for_response(case)

    assert case.state == CaseState.WAITING_RESPONSE

    # -----------------------------------
    # First Appeal
    # -----------------------------------

    workflow.first_appeal(case)

    assert case.state == CaseState.FIRST_APPEAL_REQUIRED

    # -----------------------------------
    # Second Appeal
    # -----------------------------------

    workflow.second_appeal(case)

    assert case.state == CaseState.ESCALATED

    # -----------------------------------
    # Close Case
    # -----------------------------------

    workflow.close_case(case)

    assert case.state == CaseState.CLOSED


def test_invalid_analysis_transition():
    workflow = WorkflowEngine()
    case = create_test_case()

    workflow.analyze_case(case)

    try:
        workflow.analyze_case(case)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_invalid_approval_transition():
    workflow = WorkflowEngine()
    case = create_test_case()

    try:
        workflow.approve_case(case)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_invalid_file_transition():
    workflow = WorkflowEngine()
    case = create_test_case()

    try:
        workflow.file_case(case)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_close_case():
    workflow = WorkflowEngine()
    case = create_test_case()

    workflow.close_case(case)

    assert case.state == CaseState.CLOSED