"""Data extraction agent for processing medical records."""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..components.llms import llm_openai
from ..components.classes import pull_pi
from ..components.sql import tools

class ExtractorAgent(BaseAgent):
    """Agent responsible for extracting patient and insurance information."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.llm = llm_openai.with_structured_output(pull_pi)
        self.llm_with_tools = llm_openai.bind_tools(tools)
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract patient and insurance information from medical records.
        
        Args:
            state: Current state containing medical record
            
        Returns:
            Updated state with extracted information
        """
        text = state["medicalreport"]
        
        # Query database for matching records
        db_query_prompt = f"""Find patient and insurance details from the database based on:
        {text}
        Return results as structured data with patient and insurance company information."""
        
        db_results = self.llm_with_tools.invoke(db_query_prompt)
        
        # Extract and structure the information
        extracted_info = self.llm.invoke(db_results.content)
        
        return {
            "patient": extracted_info["patient"],
            "insurance_company": extracted_info["insurance_company"]
        } 