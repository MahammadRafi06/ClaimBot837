
import os
import json
import pathlib

from components.nodes import create_coders, assistant, extract_pp, claim_generation, route_graph, qa, route_review
from components.sql import tools


from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


app = Flask(__name__)

UPLOAD_FOLDER = './data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_file(file_path):
            from components.classes import Coders, patient, insurance_company, patientgraph, Perspectives, pull_pi, ClaimOutput,comment_approve
            from langgraph.graph import START, StateGraph, END
            from langgraph.prebuilt import tools_condition
            from langchain_core.messages import HumanMessage, SystemMessage
            from langgraph.prebuilt import ToolNode
            from langchain_core.tracers.context import tracing_v2_enabled
            builder = StateGraph(patientgraph)

            # Define nodes: these do the work
            builder.add_node("assistant", assistant)
            builder.add_node("tools", ToolNode(tools))
            builder.add_node("claim_generation", claim_generation)
            builder.add_node("extract_pp",extract_pp)
            builder.add_node("create_coders", create_coders)
            builder.add_node("qa", qa)


            # Define edges: these determine how the control flow moves
            builder.add_edge(START, "create_coders")
            builder.add_edge("create_coders", "assistant")
            # builder.add_edge("assistant","claim_generation")
            builder.add_conditional_edges(
                "assistant",
                # If the latest message (result) from assistant1 is a tool call -> tools_condition routes to tools
                # If the latest message (result) from assistant1 is a not a tool call -> tools_condition routes to END
                route_graph, ["tools","extract_pp" ]
            )

            builder.add_edge("tools", "assistant")
            builder.add_edge("extract_pp", "claim_generation")

            builder.add_edge("claim_generation", "qa")
            builder.add_conditional_edges(
                "qa",
                # If the latest message (result) from assistant1 is a tool call -> tools_condition routes to tools
                # If the latest message (result) from assistant1 is a not a tool call -> tools_condition routes to END
                route_review, [END,"claim_generation" ]
            )
            react_graph = builder.compile()
            with tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT")):
                messages = [HumanMessage(content="Start process")]
                messages = react_graph.invoke({"messages": messages, "medicalreport":'', "max_coders":3})
            pt = f"{pathlib.Path(__file__).parent}/data"
            os.remove(f"{pt}/{os.listdir(pt)[0]}")
            return messages['ediclaim']
 
            #return "Hello, Mahammad"

@app.route('/', methods=['GET', 'POST'])
def index():
    saved_file_path = None
    if request.method == 'POST':
        if 'file' in request.files:  # Handle file upload
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(saved_file_path)
                return render_template('index.html', extracted_text="File saved!", file_path=filename)
        elif 'analyze' in request.form:  # Handle Analyze button
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['file_path'])
            if os.path.exists(file_path):
                analysis_result = analyze_file(file_path)
                return render_template('index.html', extracted_text=analysis_result)
            else:
                return render_template('index.html', error="File not found for analysis.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






















