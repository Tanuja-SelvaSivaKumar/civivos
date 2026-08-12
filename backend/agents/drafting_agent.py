from backend.drafting_models import (
    DraftRequest,
    DraftResponse,
    FirstAppealDraftRequest,
    FirstAppealDraftResponse,
)


class DraftingAgent:

    # ==================================================
    # NORMAL APPLICATION DRAFT
    # ==================================================

    def generate(
        self,
        request: DraftRequest
    ) -> DraftResponse:

        title = (
            f"{request.legal_route} Application"
        )

        body = f"""
To,
The Public Information Officer,
{request.department}

Subject:
Request under {request.legal_route}

Respected Sir/Madam,

I, {request.citizen_name}, respectfully submit this request.

Complaint:

{request.complaint}

Kindly provide the requested information/action
as per the applicable law.

Thank you.

Sincerely,

{request.citizen_name}
"""

        return DraftResponse(
            title=title,
            body=body.strip()
        )

    # ==================================================
    # FIRST APPEAL DRAFT
    # ==================================================

    def generate_first_appeal(
        self,
        request: FirstAppealDraftRequest
    ) -> FirstAppealDraftResponse:

        title = (
            f"First Appeal - {request.legal_route}"
        )

        body = f"""
To,
The Appellate Authority,
{request.department}

Subject:
First Appeal regarding pending response/application

Respected Sir/Madam,

I, {request.citizen_name}, respectfully submit
this first appeal regarding the following case.

Original Case ID:
{request.original_case_id}

Original Legal Route:
{request.legal_route}

Original Complaint:

{request.complaint}

The matter remains unresolved within the applicable
response period. I therefore request the competent
authority to review the matter and take appropriate
action.

Kindly consider this first appeal and provide the
appropriate response/action.

Thank you.

Sincerely,

{request.citizen_name}
"""

        return FirstAppealDraftResponse(
            title=title,
            body=body.strip(),
            original_case_id=request.original_case_id
        )