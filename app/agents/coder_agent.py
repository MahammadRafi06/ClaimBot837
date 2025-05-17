"""Medical coding agent responsible for EDI claim generation."""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..components.llms import llm_openai
from ..components.classes import ClaimOutput

class CoderAgent(BaseAgent):
    """Agent responsible for generating EDI claims from medical records."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.llm = llm_openai.with_structured_output(ClaimOutput)
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate EDI claim from medical record.
        
        Args:
            state: Current state containing medical record and other context
            
        Returns:
            Updated state with generated EDI claim
        """
        chart = state['medicalreport']
        reviewer_comments = state.get("reviewer_comments", "Comments are not available yet")
        
        prompt = f"""You are an expert in medical coding and EDI standards.
        Generate a compliant X12 837 Professional EDI claim based on:
        
        Medical Record: {chart}
        Previous Review Comments: {reviewer_comments}
        
        Ensure strict adherence to EDI formatting and include all required segments.
        """
        
        output = self.llm.invoke(prompt)
        
        return {
            "ediclaim": output["ediclaim"],
            "coder_comments": output["coder_comments"]
        } 