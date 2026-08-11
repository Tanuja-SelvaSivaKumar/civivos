from fastapi import APIRouter, HTTPException

from backend.api.schemas import CaseCreateRequest
from backend.core.container import case_controller


router = APIRouter(
    tags=["Civivos"]
)


# ==================================================
# CREATE CASE
# ==================================================

@router.post("/cases")
def create_case(request: CaseCreateRequest):

    try:

        result = case_controller.create_case(
            citizen_name=request.citizen_name,
            complaint=request.complaint
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


# ==================================================
# GET CASE
# ==================================================

@router.get("/cases/{case_id}")
def get_case(case_id: str):

    case = case_controller.get_case(
        case_id
    )

    if case is None:

        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case


# ==================================================
# CASE TIMELINE
# ==================================================

@router.get("/cases/{case_id}/timeline")
def get_timeline(case_id: str):

    timeline = case_controller.get_timeline(
        case_id
    )

    return timeline


# ==================================================
# APPROVE CASE
# ==================================================

@router.post("/cases/{case_id}/approve")
def approve_case(case_id: str):

    try:

        case = case_controller.approve_case(
            case_id
        )

        if case is None:

            raise HTTPException(
                status_code=404,
                detail="Case not found"
            )

        return case

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


# ==================================================
# FILE CASE
# ==================================================

@router.post("/cases/{case_id}/file")
def file_case(case_id: str):

    try:

        case = case_controller.file_case(
            case_id
        )

        if case is None:

            raise HTTPException(
                status_code=404,
                detail="Case not found"
            )

        return case

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


# ==================================================
# WAIT FOR GOVERNMENT RESPONSE
# ==================================================

@router.post("/cases/{case_id}/wait")
def wait_for_response(case_id: str):

    try:

        case = case_controller.wait_for_response(
            case_id
        )

        if case is None:

            raise HTTPException(
                status_code=404,
                detail="Case not found"
            )

        return case

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


# ==================================================
# RUN WATCHER
# ==================================================

@router.post("/watcher/run")
def run_watcher():

    return case_controller.run_watcher()