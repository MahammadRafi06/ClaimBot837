from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

db = SQLDatabase.from_uri("mysql+pymysql://root:Tasneem1996@localhost:3306/medical")
toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(model="gpt-4o"))
tools = toolkit.get_tools()
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")


from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o",temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


import operator
from typing import List, Annotated
from typing_extensions import TypedDict

class patientgraph(TypedDict):
    patient: str # Research topic
    messages: Annotated[list, operator.add] # Send() API key
    medicalreport: str # Content for the final report
    ediclaim: str # Final report


from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader
def assistant(state: patientgraph):
    loader = PyPDFLoader("./EmilyDavis.pdf",)
    docs = loader.load()
    text = ''
    for doc in docs:
        text = text + doc.page_content 
    content="""You are an SQL expert trying to find patient and his/her insurance details from a sql database based on pateint details found in a given text {text}. 
                                The output json should have should have two main keys i.e. patient and insurer. Dates are in US format.
                                Your output should be list of dictionaries keys as column names and values as column values. Nothing else should be returned. Do not add any code blocks. """

    human_msg = content.format(text = text)
    return {"messages": [llm_with_tools.invoke([human_msg] + state["messages"])], "medicalreport": text}



def claim_generation(state: patientgraph):
    chart = state['medicalreport']
    content = """You are an expert in medical coding and EDI (Electronic Data Interchange) standards. 
                 Your task is to generate a compliant X12 837 Professional EDI claim file based on the provided details. Please strictly adhere to EDI formatting rules and include the necessary 
                 segments (e.g., ISA, GS, ST, BHT, NM1, HL, CLM, SV1, DTP, etc.) as per the ANSI X12 standard.

                ### Instructions:
                1. Use correct segment identifiers and maintain the hierarchical structure of the EDI document.
                2. Populate the EDI fields with the provided information.
                3. Ensure placeholders for any mandatory segments where data is missing.
                4. Return the output as raw EDI text without explanations or extra formatting.
                ### Output Format:
                Start your output with ISA and include all required segments in the EDI format. Do not explain the output; simply provide the formatted EDI claim text.
                """
    hum_msg = HumanMessage(content=content)
    return {"ediclaim":[llm_with_tools.invoke([hum_msg] + [SystemMessage(content=state["messages"][-1].content)] + [SystemMessage(content=chart)])] }


def route_graph(state: patientgraph):
   if "tool_calls" in state['messages'][-1].additional_kwargs:
    return "tools"
   else:
     return "claim_generation"
   

from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display

# class patientgraph(MessagesState):
#       patient: patient
# Graph
builder = StateGraph(patientgraph)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("claim_generation", claim_generation)


# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
# builder.add_edge("assistant","claim_generation")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant1 is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant1 is a not a tool call -> tools_condition routes to END
    route_graph, ["tools","claim_generation" ]
)

builder.add_edge("tools", "assistant")
builder.add_edge("claim_generation", END)
react_graph = builder.compile()


from langchain_core.tracers.context import tracing_v2_enabled
import os
import json

with tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT")):
    messages = [HumanMessage(content="Start process")]
    messages = react_graph.invoke({"messages": messages, "medicalreport":''})


for m in messages['ediclaim']:
    m.pretty_print()