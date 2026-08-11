from backend.knowledge.context import KnowledgeContext


def build_reasoning_prompt(context: KnowledgeContext) -> str:

    prompt = f"""
You are an expert Indian civic legal advisor.

Citizen Complaint:
{context.complaint}

Citizen Issue:
{context.issue.issue_type}

Relevant Department:
{context.department.name}

Authority:
{context.department.authority}

Available Legal Routes:

"""

    for rule in context.legal_rules:

        prompt += f"""
----------------------------------

Route:
{rule.law}

Description:
{rule.description}

Applicable Conditions:
"""

        for condition in rule.conditions:
            prompt += f"- {condition}\n"

        if rule.not_for:

            prompt += "\nDo NOT use when:\n"

            for item in rule.not_for:
                prompt += f"- {item}\n"

        prompt += f"""

Legal Section:
{rule.section if rule.section else "N/A"}

"""


    prompt += """

Your task:

1. Decide the BEST legal route.

2. Explain WHY.

3. Explain why every other route was rejected.

4. Cite the applicable law.

Return ONLY JSON.

Example:

{
    "selected_route": "RTI",

    "reasoning": "...",

    "evidence": [
        "Citizen requests application status",
        "Information is held by a public authority"
    ],

    "rejected_routes": [
        "CPGRAMS"
    ],

    "legal_reference":
        "RTI Act, 2005 - Section 6",

    "confidence":
        "High"
}

"""

    return prompt