from agents.drafting_agent import DraftingAgent
from drafting_models import DraftRequest


agent = DraftingAgent()

request = DraftRequest(
    citizen_name="Rahul Sharma",
    complaint="My ration card application has been pending for three months.",
    department="Food and Civil Supplies Department",
    legal_route="RTI"
)

response = agent.generate(request)

print("\n========== TITLE ==========\n")
print(response.title)

print("\n========== BODY ==========\n")
print(response.body)