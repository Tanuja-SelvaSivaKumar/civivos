import json

from backend.llm.base import BaseLLMProvider


class MockProvider(BaseLLMProvider):

   def generate(self, prompt: str) -> str:

    prompt_lower = prompt.lower()


    if "delay" in prompt_lower or "pending" in prompt_lower:

        response = {
            "selected_route": "DARPG CPGRAMS",
            "reasoning": 
            "The citizen is reporting delay in government service delivery.",
            "evidence": [
                "Service delay reported",
                "Government department involved"
            ],
            "rejected_routes": [
                "RTI Act, 2005"
            ],
            "legal_reference": 
            "DARPG CPGRAMS Guidelines",
            "confidence": "High"
        }


    else:

        response = {
            "selected_route": "RTI",
            "reasoning":
            "The citizen is requesting information from a public authority.",
            "evidence": [
                "Information requested",
                "Public authority involved"
            ],
            "rejected_routes": [
                "CPGRAMS"
            ],
            "legal_reference":
            "RTI Act, 2005 - Section 6",
            "confidence":
            "High"
        }


    return json.dumps(response)