from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from backend.app import app
from backend.core.container import case_controller


client = TestClient(app)


def create_waiting_case():

    response = client.post(
        "/api/cases",
        json={
            "citizen_name": "API Appeal Test",
            "complaint": (
                "My ration card application has "
                "been pending for three months."
            ),
        },
    )

    assert response.status_code == 200

    case_id = response.json()[
        "case"
    ]["case_id"]

    response = client.post(
        f"/api/cases/{case_id}/approve"
    )

    assert response.status_code == 200

    response = client.post(
        f"/api/cases/{case_id}/file"
    )

    assert response.status_code == 200

    response = client.post(
        f"/api/cases/{case_id}/wait"
    )

    assert response.status_code == 200

    return case_id


def test_first_appeal_api_returns_generated_appeal():

    case_id = create_waiting_case()

    stored_case = (
        case_controller
        .orchestrator
        .memory
        .get_case(case_id)
    )

    assert stored_case is not None

    stored_case.deadline = (
        datetime.now()
        - timedelta(days=1)
    )

    case_controller.orchestrator.memory.update_case(
        stored_case
    )

    response = client.post(
        "/api/watcher/run"
    )

    assert response.status_code == 200

    watcher_results = response.json()

    watcher_result = next(
        result
        for result in watcher_results
        if result["case_id"] == case_id
    )

    assert (
        watcher_result["action"]
        == "FIRST_APPEAL_REQUIRED"
    )

    response = client.get(
        f"/api/cases/{case_id}/first-appeal"
    )

    assert response.status_code == 200

    appeal = response.json()

    assert appeal["case_id"] == case_id

    assert (
        appeal["citizen_name"]
        == "API Appeal Test"
    )

    assert (
        appeal["title"]
        == "First Appeal - DARPG CPGRAMS"
    )

    assert "Original Case ID:" in appeal["body"]

    assert case_id in appeal["body"]


def test_first_appeal_api_returns_404_when_missing():

    case_id = create_waiting_case()

    response = client.get(
        f"/api/cases/{case_id}/first-appeal"
    )

    assert response.status_code == 404


def test_first_appeal_api_returns_404_for_unknown_case():

    response = client.get(
        "/api/cases/nonexistent-case-id/first-appeal"
    )

    assert response.status_code == 404