from drafting_models import DraftRequest, DraftResponse


class DraftingAgent:

    def generate(self, request: DraftRequest) -> DraftResponse:

        title = f"{request.legal_route} Application"

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

Kindly provide the requested information/action as per the applicable law.

Thank you.

Sincerely,

{request.citizen_name}
"""

        return DraftResponse(
            title=title,
            body=body.strip()
        )