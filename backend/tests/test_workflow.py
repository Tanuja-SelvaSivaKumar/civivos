from workflow.models import Case
from workflow.workflow import WorkflowEngine


workflow = WorkflowEngine()

case = Case(
    case_id="CASE001",
    citizen_name="Rahul Sharma",
    complaint="My ration card application has been pending for three months.",
    department="Food and Civil Supplies Department",
    legal_route="RTI"
)

print("\n========== INITIAL ==========")
print(case.state)

workflow.analyze_case(case)

print("\n========== ANALYZED ==========")
print(case.state)

workflow.draft_case(case)

print("\n========== DRAFTED ==========")
print(case.state)

workflow.wait_for_approval(case)

print("\n========== WAITING ==========")
print(case.state)

workflow.approve_case(case)

print("\n========== FILED ==========")
print(case.state)

workflow.wait_for_response(case)

print("\n========== WAITING RESPONSE ==========")
print(case.state)

workflow.first_appeal(case)

print("\n========== FIRST APPEAL ==========")
print(case.state)

workflow.second_appeal(case)

print("\n========== SECOND APPEAL ==========")
print(case.state)

workflow.close_case(case)

print("\n========== CLOSED ==========")
print(case.state)