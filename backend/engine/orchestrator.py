from uuid import uuid4
from datetime import datetime, timedelta

from drafting_models import DraftRequest

from knowledge.knowledge_loader import KnowledgeLoader

from agents.reasoning_agent import ReasoningAgent
from agents.drafting_agent import DraftingAgent
from agents.watcher_agent import WatcherAgent

from workflow.workflow import WorkflowEngine
from workflow.states import CaseState
from workflow.models import Case

from memory.memory_engine import MemoryEngine


class Orchestrator:

    def __init__(self):

        self.loader = KnowledgeLoader()

        self.reasoner = ReasoningAgent()

        self.drafter = DraftingAgent()

        self.watcher = WatcherAgent()

        self.workflow = WorkflowEngine()

        self.memory = MemoryEngine()

    def create_case(self, citizen_name: str, complaint: str):

        # ----------------------------
        # Load Knowledge
        # ----------------------------

        context = self.loader.build_context(complaint)

        if context is None:
            raise ValueError("Unable to identify the citizen issue.")

        # ----------------------------
        # AI Reasoning
        # ----------------------------

        reasoning = self.reasoner.reason(context)

        # ----------------------------
        # Draft Document
        # ----------------------------

        request = DraftRequest(
            citizen_name=citizen_name,
            complaint=complaint,
            department=context.department.name,
            legal_route=reasoning.selected_route
        )

        draft = self.drafter.generate(request)

        # ----------------------------
        # Create Case
        # ----------------------------

        case = Case(
    case_id=str(uuid4()),
    citizen_name=citizen_name,
    complaint=complaint,
    department=context.department.name,
    legal_route=reasoning.selected_route,
    state=CaseState.NEW,
    created_at=datetime.now(),
    last_updated=datetime.now()
)
        # ----------------------------
        # Workflow
        # ----------------------------

        case = self.workflow.analyze_case(case)
        case = self.workflow.draft_case(case)
        case = self.workflow.wait_for_approval(case)

        # Demo: auto approve for now
        case = self.workflow.approve_case(case)

        # ----------------------------
        # Memory
        # ----------------------------

        self.memory.add_case(case)

        self.memory.add_event(
            case.case_id,
            "Case Created"
        )

        self.memory.add_event(
            case.case_id,
            "Reasoning Completed"
        )

        self.memory.add_event(
            case.case_id,
            "Draft Generated"
        )

        self.memory.add_event(
            case.case_id,
            "Citizen Approved Draft"
        )

        self.memory.add_event(
            case.case_id,
            "RTI Filed"
        )

        return case, reasoning, draft

    def run_daily_watcher(self):

        results = []

        for case in self.memory.get_all_cases():

            result = self.watcher.check_case(case)

            if result.action_taken:

                self.memory.add_event(
                    case.case_id,
                    result.action
                )

            results.append(result)

        return results