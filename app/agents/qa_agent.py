"""Quality Assurance agent for reviewing EDI claims."""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..components.llms import llm_openai
from ..components.classes import comment_approve

class QAAgent(BaseAgent):
    """Agent responsible for reviewing and validating EDI claims."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.llm = llm_openai.with_structured_output(comment_approve)
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Review EDI claim for accuracy and compliance.
        
        Args:
            state: Current state containing claim and context
            
        Returns:
            Updated state with review results
        """
        prompt = f"""Review this EDI claim as an expert medical coder:

        Medical Chart: {state["medicalreport"]}
        Patient Info: {state["patient"]}
        Insurance Info: {state["insurance_company"]}
        EDI Claim: {state["ediclaim"]}
        Coder Comments: {state["coder_comments"]}

        Verify accuracy and compliance. Respond with specific issues if any exist.
        """
        
        review = self.llm.invoke(prompt)
        
        return {
            "reviewer_comments": review['review_comments'],
            "approved": review["approval"]
        } 