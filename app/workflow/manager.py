"""Workflow manager for orchestrating the claims processing pipeline."""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from ..agents.coder_agent import CoderAgent
from ..agents.qa_agent import QAAgent
from ..agents.extractor_agent import ExtractorAgent
from ..components.classes import patientgraph

class WorkflowManager:
    """Manages the workflow of the claims processing system."""
    
    def __init__(self):
        self.extractor = ExtractorAgent("Extractor")
        self.coder = CoderAgent("Coder")
        self.qa = QAAgent("QA")
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the workflow graph.
        
        Returns:
            Compiled StateGraph
        """
        builder = StateGraph(patientgraph)
        
        # Add nodes
        builder.add_node("extract", self.extractor.process)
        builder.add_node("code", self.coder.process)
        builder.add_node("review", self.qa.process)
        
        # Define edges
        builder.add_edge("extract", "code")
        builder.add_edge("code", "review")
        
        # Add conditional routing
        builder.add_conditional_edges(
            "review",
            self._route_review,
            [END, "code"]
        )
        
        return builder.compile()
    
    def _route_review(self, state: Dict[str, Any]) -> str:
        """Route based on QA review results."""
        if state["approved"] == "yes":
            return END
        return "code"
    
    def process_claim(self, medical_record: str) -> Dict[str, Any]:
        """Process a medical record through the workflow.
        
        Args:
            medical_record: The medical record text
            
        Returns:
            Final state with processed claim
        """
        initial_state = {
            "messages": [],
            "medicalreport": medical_record,
            "max_coders": 1
        }
        
        return self.graph.invoke(initial_state) 