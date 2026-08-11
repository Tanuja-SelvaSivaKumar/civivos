from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from backend.app import app
from backend.core.container import case_controller
from backend.models.case_state import CaseState


client = TestClient(app)


# ==================================================
# TEST CASE CREATOR
# ==================================================

def create_test_case():

    response = client.post(
        "/api/cases",
        json={
            "citizen_name": "Tanuj",
            "complaint": (
                "My ration card has been pending for 3 months"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "case" in data
    assert "reasoning" in data
    assert "draft" in data

    case = data["case"]

    assert case["case_id"] is not None

    assert case["citizen_name"] == "Tanuj"

    assert case["complaint"] == (
        "My ration card has been pending for 3 months"
    )

    # -----------------------------------
    # Initial API lifecycle state
    # -----------------------------------
    #
    # CREATED
    #     ↓
    # ANALYZING
    #     ↓
    # DRAFT_READY
    #     ↓
    # WAITING_APPROVAL
    #
    # create_case() currently ends here.

    assert case["state"] == "WAITING_APPROVAL"

    return case["case_id"]


# ==================================================
# CREATE CASE
# ==================================================

def test_create_case():

    create_test_case()


# ==================================================
# GET CASE
# ==================================================

def test_get_case():

    case_id = create_test_case()

    response = client.get(
        f"/api/cases/{case_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == case_id
    assert data["citizen_name"] == "Tanuj"


# ==================================================
# GET CASE TIMELINE
# ==================================================

def test_get_case_timeline():

    case_id = create_test_case()

    response = client.get(
        f"/api/cases/{case_id}/timeline"
    )

    assert response.status_code == 200

    timeline = response.json()

    assert isinstance(timeline, list)

    assert len(timeline) > 0


# ==================================================
# NONEXISTENT CASE
# ==================================================

def test_get_nonexistent_case():

    response = client.get(
        "/api/cases/nonexistent-case-id"
    )

    assert response.status_code == 404


# ==================================================
# APPROVE CASE
# ==================================================

def test_approve_case():

    case_id = create_test_case()

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == case_id

    assert data["state"] == "CITIZEN_APPROVED"


# ==================================================
# FILE CASE
# ==================================================

def test_file_case():

    case_id = create_test_case()

    # -----------------------------------
    # Approve first
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    # -----------------------------------
    # File case
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == case_id

    assert data["state"] == "FILED"


# ==================================================
# WAIT FOR RESPONSE
# ==================================================

def test_wait_for_response():

    case_id = create_test_case()

    # -----------------------------------
    # Approve
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    # -----------------------------------
    # File
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 200

    # -----------------------------------
    # Start waiting
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/wait"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["case_id"] == case_id

    assert data["state"] == "WAITING_RESPONSE"


# ==================================================
# INVALID APPROVAL FLOW
# ==================================================

def test_approve_case_after_filing_is_invalid():

    case_id = create_test_case()

    # -----------------------------------
    # Approve
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    # -----------------------------------
    # File
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 200

    # -----------------------------------
    # Trying to approve again must fail
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 400


# ==================================================
# FILE BEFORE APPROVAL
# ==================================================

def test_file_case_before_approval():

    case_id = create_test_case()

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 400


# ==================================================
# WAIT BEFORE FILING
# ==================================================

def test_wait_before_filing():

    case_id = create_test_case()

    response = client.post(
        f"/api/cases/{case_id}/wait"
    )

    assert response.status_code == 400


# ==================================================
# RUN WATCHER
# ==================================================

def test_watcher_endpoint():

    response = client.post(
        "/api/watcher/run"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ==================================================
# FULL API LIFECYCLE
# ==================================================

def test_full_api_case_lifecycle():

    # -----------------------------------
    # CREATE CASE
    # -----------------------------------

    response = client.post(
        "/api/cases",
        json={
            "citizen_name": "Tanuj",
            "complaint": (
                "My ration card has been pending for 3 months"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    case_id = data["case"]["case_id"]

    assert data["case"]["state"] == "WAITING_APPROVAL"

    # -----------------------------------
    # CITIZEN APPROVES
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    case = response.json()

    assert case["case_id"] == case_id
    assert case["state"] == "CITIZEN_APPROVED"

    # -----------------------------------
    # FILE CASE
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 200

    case = response.json()

    assert case["case_id"] == case_id
    assert case["state"] == "FILED"

    # -----------------------------------
    # WAIT FOR RESPONSE
    # -----------------------------------

    response = client.post(
        f"/api/cases/{case_id}/wait"
    )

    assert response.status_code == 200

    case = response.json()

    assert case["case_id"] == case_id
    assert case["state"] == "WAITING_RESPONSE"

    # -----------------------------------
    # GET STORED CASE
    # -----------------------------------
    #
    # We access the existing in-memory store
    # ONLY so the test can simulate time passing.
    #
    # We are NOT adding a production endpoint
    # for changing deadlines.

    stored_case = (
        case_controller
        .orchestrator
        .memory
        .get_case(case_id)
    )

    assert stored_case is not None

    assert (
        stored_case.state
        == CaseState.WAITING_RESPONSE
    )

    # -----------------------------------
    # SIMULATE DEADLINE PASSING
    # -----------------------------------

    stored_case.deadline = (
        datetime.now() - timedelta(days=1)
    )

    case_controller.orchestrator.memory.update_case(
        stored_case
    )

    # -----------------------------------
    # RUN WATCHER THROUGH API
    # -----------------------------------

    response = client.post(
        "/api/watcher/run"
    )

    assert response.status_code == 200

    results = response.json()

    assert isinstance(results, list)

    assert len(results) > 0

    # -----------------------------------
    # FIND OUR CASE
    # -----------------------------------

    watcher_result = next(
        result
        for result in results
        if result["case_id"] == case_id
    )

    # -----------------------------------
    # VERIFY WATCHER ACTION
    # -----------------------------------

    assert watcher_result["action_taken"] is True

    assert (
        watcher_result["action"]
        == "FIRST_APPEAL_REQUIRED"
    )

    assert (
        watcher_result["reason"]
        == "Response deadline crossed."
    )

    # -----------------------------------
    # GET FINAL CASE THROUGH API
    # -----------------------------------

    response = client.get(
        f"/api/cases/{case_id}"
    )

    assert response.status_code == 200

    final_case = response.json()

    assert final_case["case_id"] == case_id

    # -----------------------------------
    # FINAL LIFECYCLE STATE
    # -----------------------------------

    assert (
        final_case["state"]
        == "FIRST_APPEAL_REQUIRED"
    )