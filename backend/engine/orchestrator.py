from datetime import datetime
from uuid import uuid4

from backend.drafting_models import DraftRequest

from backend.actions.action_engine import ActionEngine

from backend.agents.drafting_agent import DraftingAgent
from backend.agents.reasoning_agent import ReasoningAgent
from backend.agents.watcher_agent import WatcherAgent

from backend.knowledge.knowledge_loader import KnowledgeLoader

from backend.memory.memory_engine import MemoryEngine

from backend.models.case import Case
from backend.models.case_state import CaseState

from backend.workflow.workflow import WorkflowEngine


class Orchestrator:

    def __init__(self):

        self.loader = KnowledgeLoader()

        self.reasoner = ReasoningAgent()

        self.drafter = DraftingAgent()

        self.workflow = WorkflowEngine()

        self.memory = MemoryEngine()

        # -----------------------------------
        # Action Engine
        # -----------------------------------

        self.actions = ActionEngine(
            self.workflow,
            self.memory,
            self.drafter
        )

        # -----------------------------------
        # Watcher
        # -----------------------------------

        self.watcher = WatcherAgent(
            action_engine=self.actions
        )

    # ==================================================
    # CREATE CASE
    # ==================================================

    def create_case(
        self,
        citizen_name: str,
        complaint: str
    ):

        # -----------------------------------
        # Load Knowledge
        # -----------------------------------

        context = self.loader.build_context(
            complaint
        )

        if context is None:

            raise ValueError(
                "Unable to identify the citizen issue."
            )

        # -----------------------------------
        # Create Initial Case
        # -----------------------------------

        now = datetime.now()

        case = Case(
            case_id=str(uuid4()),
            citizen_name=citizen_name,
            complaint=complaint,
            department=context.department.name,
            legal_route="PENDING",
            state=CaseState.CREATED,
            created_at=now,
            last_updated=now
        )

        # -----------------------------------
        # Store Initial Case
        # -----------------------------------

        self.memory.add_case(
            case
        )

        self.memory.add_event(
            case.case_id,
            "Case Created",
            "Citizen complaint received by CivivOS."
        )

        # -----------------------------------
        # Start Analysis
        # -----------------------------------

        case = self.workflow.analyze_case(
            case
        )

        self.memory.update_case(
            case
        )

        self.memory.add_event(
            case.case_id,
            "AI Analysis Started",
            "CivivOS AI started analyzing the complaint."
        )

        # -----------------------------------
        # AI Reasoning
        # -----------------------------------

        reasoning = self.reasoner.reason(
            context
        )

        # -----------------------------------
        # Store Legal Route
        # -----------------------------------

        case.legal_route = (
            reasoning.selected_route
        )

        self.memory.update_case(
            case
        )

        # -----------------------------------
        # Generate Draft
        # -----------------------------------

        request = DraftRequest(
            citizen_name=citizen_name,
            complaint=complaint,
            department=context.department.name,
            legal_route=reasoning.selected_route
        )

        draft = self.drafter.generate(
            request
        )

        # -----------------------------------
        # Complete Analysis
        #
        # ANALYZING → DRAFT_READY
        # -----------------------------------

        case = self.workflow.complete_analysis(
            case
        )

        self.memory.update_case(
            case
        )

        self.memory.add_event(
            case.case_id,
            "AI Analysis Completed",
            "AI reasoning completed and the legal route was selected."
        )

        # -----------------------------------
        # Draft Generated
        # -----------------------------------

        self.memory.add_event(
            case.case_id,
            "Draft Generated",
            "CivivOS generated the application draft."
        )

        # -----------------------------------
        # Citizen Approval Stage
        #
        # DRAFT_READY → WAITING_APPROVAL
        # -----------------------------------

        case = self.workflow.wait_for_approval(
            case
        )

        self.memory.update_case(
            case
        )

        self.memory.add_event(
            case.case_id,
            "Waiting For Citizen Approval",
            (
                "CivivOS is waiting for the citizen "
                "to review and approve the draft."
            )
        )

        return case, reasoning, draft

    # ==================================================
    # DAILY WATCHER
    # ==================================================

    def run_daily_watcher(self):

        results = []

        # -----------------------------------
        # Query only active response cases
        # -----------------------------------

        cases = (
            self.memory
            .get_waiting_response_cases()
        )

        for case in cases:

            result = self.watcher.check_case(
                case
            )

            # -----------------------------------
            # Persist watcher-driven changes
            # -----------------------------------

            if result.action_taken:

                self.memory.update_case(
                    case
                )

                self.memory.add_event(
                    case.case_id,
                    result.action,
                    result.reason
                )

            results.append(
                result
            )

        return results