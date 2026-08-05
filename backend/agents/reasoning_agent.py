from knowledge.context import KnowledgeContext

from agents.models import ReasoningResult
from agents.prompt_builder import build_reasoning_prompt


class ReasoningAgent:

    def reason(self, context: KnowledgeContext) -> ReasoningResult:

        prompt = build_reasoning_prompt(context)

        print("\n========== PROMPT ==========\n")
        print(prompt)

        # Temporary mock response
        return ReasoningResult(
            selected_route="RTI",

            reasoning=(
                "The complaint requests the status of a government application. "
                "The RTI Act is specifically designed for obtaining information "
                "from public authorities."
            ),

            evidence=[
                "Citizen requests application status",
                "Department identified successfully",
                "Information is held by a public authority"
            ],

            rejected_routes=[
                "CPGRAMS"
            ],

            legal_reference="RTI Act, 2005 - Section 6",

            confidence="High"
        )