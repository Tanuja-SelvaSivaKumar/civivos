from backend.memory.memory_store import MemoryStore


memory = MemoryStore()

memory.create_case("CASE001")

memory.add_event(
    "CASE001",
    "Case Created"
)

memory.add_event(
    "CASE001",
    "Reasoning Completed"
)

memory.add_event(
    "CASE001",
    "Draft Generated"
)

history = memory.get_history("CASE001")

print()

print("========== TIMELINE ==========")

for event in history.events:

    print(event.timestamp)

    print(event.event)

    print()