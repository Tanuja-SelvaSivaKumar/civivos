import json

from backend.knowledge.context import KnowledgeContext
from backend.agents.models import ReasoningResult
from backend.agents.prompt_builder import build_reasoning_prompt
from backend.llm.factor import get_provider


class ReasoningAgent:

    def __init__(self):

        self.llm = get_provider()


    def reason(self, context: KnowledgeContext) -> ReasoningResult:

        prompt = build_reasoning_prompt(context)

        print("\n========== PROMPT ==========\n")
        print(prompt)


        response = self.llm.generate(prompt)


        print("\n========== LLM RESPONSE ==========\n")
        print(response)


        data = json.loads(response)


        return ReasoningResult(**data)