from datetime import datetime, timedelta

from engine.orchestrator import Orchestrator


orch = Orchestrator()

case, reasoning, draft = orch.create_case(
    "Rahul Sharma",
    "My ration card application has been pending for three months."
)

print("\n========== CASE ==========\n")

print(case)

print("\n========== REASONING ==========\n")

print(reasoning)

print("\n========== DRAFT ==========\n")

print(draft.title)

print("\n========== EVENTS ==========\n")

for event in orch.memory.get_timeline(case.case_id):

    print(event.timestamp)

    print(event.event)

    print()

# ----------------------------------------
# Simulate deadline passing
# ----------------------------------------

case.deadline = datetime.now() - timedelta(days=1)

print("\n========== WATCHER ==========\n")

results = orch.run_daily_watcher()

for result in results:

    print(result)

print("\n========== UPDATED TIMELINE ==========\n")

for event in orch.memory.get_timeline(case.case_id):

    print(event.timestamp)

    print(event.event)

    print()