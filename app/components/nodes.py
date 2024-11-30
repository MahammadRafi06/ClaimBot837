from components.prompts import coder_instructions,content_assistant, content_clm, qa_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from components.classes import Coders, patient, insurance_company, patientgraph, Perspectives, pull_pi, ClaimOutput,comment_approve
from langgraph.graph import START, StateGraph, END
from components.llms import llm_openai
from components.sql import tools
import os
import pathlib

import random
from langchain_community.document_loaders import PyPDFLoader



llm_with_tools = llm_openai.bind_tools(tools, parallel_tool_calls=False)
structured_llm = llm_openai.with_structured_output(Perspectives)
llm_pull_pi = llm_openai.with_structured_output(pull_pi)
ClaimOutput_llm = llm_openai.with_structured_output(ClaimOutput)
llm_review = llm_openai.with_structured_output(comment_approve)


def create_coders(state:patientgraph):
    max_coders = state['max_coders']
    system_message = coder_instructions.format(max_coders=max_coders)

    # Generate question 
    coders = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Generate the set of coders.")])
    
    # Write the list of analysis to state
    return {"coders": coders.coders}


def assistant(state: patientgraph):
    pt = f"{pathlib.Path(__file__).parent.parent}/data"
    loader = PyPDFLoader(f"{pt}/{os.listdir(pt)[0]}")
    docs = loader.load()
    text = ''
    for doc in docs:
        text = text + doc.page_content 
    content_assistant="""You are an SQL expert trying to find patient and his/her insurance details from a sql database based on pateint details found in a given text {text}. 
                                The output should be a json and it should have two main keys i.e. patient and insurance company. Dates are in US format.
                                Your output should be list of dictionaries keys as column names and values as column values. Nothing else should be returned. Do not add any code blocks. """

    human_msg = content_assistant.format(text = text)
    return {"messages": [llm_with_tools.invoke([human_msg] + state["messages"])], "medicalreport": text}


def extract_pp(state: patientgraph):
    output = llm_pull_pi.invoke(state["messages"][-1].content)
    return {
            "patient": output["patient"], "insurance_company": output["insurance_company"] }


def claim_generation(state: patientgraph):
    chart = state['medicalreport']
    content_clm = """You are an expert in medical coding and EDI (Electronic Data Interchange) standards.
                Your task is to generate a fully compliant X12 837 Professional EDI claim file based on the provided details. 
                Strictly adhere to EDI formatting rules and include all necessary segments (e.g., ISA, GS, ST, BHT, NM1, HL, CLM, SV1, DTP, etc.) 
                as mandated by the ANSI X12 standard.

                Key Instructions:
                Review Comments: Carefully incorporate or address the review comments, if any, provided in {comments}.
                Segment Hierarchy: Use the correct segment identifiers and maintain the hierarchical structure required for an 837 Professional EDI claim.
                Data Handling: Populate the EDI fields with the provided information, leaving placeholders (e.g., ~) for any mandatory segments where data is not available.
                Validation: Ensure the generated EDI file is ready for submission, compliant with validation requirements, and includes all required data elements.
                Output: Provide the result as raw EDI text, beginning with the ISA segment and including all required segments. Avoid explanations, comments, or any extra formatting.
                Review and Feedback:
                You are expected to incorporate expert review comments where applicable and make necessary corrections for compliance.
                Example Workflow:
                Include all control segments (ISA, GS, etc.).
                Ensure accurate provider (NM1) and patient (HL) data segments.
                Correctly format claim details (CLM, SV1) and date (DTP) segments.
                Validate the hierarchical structure of the document.
                Output Format:
                Your output must start with ISA and include all required segments in the EDI format. Do not provide explanations, extra formatting, or comments in the output.
                """
    content = content_clm.format(comments= state.get("reviewer_comments", "Comments are not available yet"))
    #content = content.format(comments= state["reviewer_comments"])
    hum_msg = HumanMessage(content=content)
    output = ClaimOutput_llm.invoke([hum_msg] + [SystemMessage(content=state["messages"][-1].content)] + [SystemMessage(content=chart)])
    return {"ediclaim":output["ediclaim"],"coder_comments":output["coder_comments"]  }




def qa(state:patientgraph):
    qa_prompt = """You are an expert in medical coding with extensive experience in the field. You are tasked with reviewing the work of your subordinate, who has compiled an EDI claim based on the details of a medical chart. 
                    Your objective is to ensure the EDI claim aligns perfectly with the information in the medical chart.
                    Instructions:

                    The medical chart, which serves as the source of truth, is provided here: {chart}.
                    The patient is: {patient}.
                    The insurance_company is: {insurance_company}.
                    The subordinate's EDI claim is provided here: {ediclaim}.
                    The subordinate's comments are provided here: {coder_comments}.
                    Your task:

                    If the EDI claim is accurate and matches all details from the medical chart, respond with "Approved: Yes".
                    If there are discrepancies or errors, respond with specific comments identifying what needs to be corrected in the coded claim so the subordinate can revise and resend the EDI claim.
                    Please follow the instructions carefully. Your feedback should be concise and actionable."""
    qa_prompt = qa_prompt.format(chart=state["medicalreport"], patient=state["patient"],insurance_company=state["insurance_company"],ediclaim=state["ediclaim"],coder_comments=state["coder_comments"] )

    review = llm_review.invoke(qa_prompt)
    it = random.randint(1, 2)
    return {"reviewer_comments":review['review_comments'],"approved": review["approval"], "iteration": it}



def route_review(state: patientgraph):
   if state["approved"] == "yes" or state["iteration"]==1:
    return END
   else:
     return "claim_generation"
   
def route_graph(state: patientgraph):
   if "tool_calls" in state['messages'][-1].additional_kwargs:
    return "tools"
   else:
     return "extract_pp"
   
