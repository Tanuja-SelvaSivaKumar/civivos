from backend.knowledge.knowledge_loader import KnowledgeLoader
from backend.agents.reasoning_agent import ReasoningAgent


loader = KnowledgeLoader()
agent = ReasoningAgent()

context = loader.build_context(
    "My ration card application has been pending for four months."
)

result = agent.reason(context)

print("\n========== RESULT ==========\n")
print(result)