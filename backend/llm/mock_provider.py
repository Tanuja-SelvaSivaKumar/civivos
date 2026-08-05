import json

from llm.base import BaseLLMProvider


class MockProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:

        response = {

            "selected_route": "RTI",

            "reasoning":
                "The citizen is requesting the status of a government application.",

            "evidence": [
                "Application status requested",
                "Government department identified"
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