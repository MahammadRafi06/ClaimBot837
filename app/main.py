"""Main application entry point."""

import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFLoader
from workflow.manager import WorkflowManager

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle main page requests."""
    if request.method == 'POST':
        if 'file' in request.files:
            return handle_file_upload()
        elif 'analyze' in request.form:
            return handle_file_analysis()
    return render_template('index.html')

def handle_file_upload():
    """Handle PDF file upload."""
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return render_template('index.html', file_path=filename)
    return render_template('index.html', error="Invalid file type")

def handle_file_analysis():
    """Process the uploaded file through the workflow."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['file_path'])
    if not os.path.exists(file_path):
        return render_template('index.html', error="File not found")
    
    try:
        # Load and process the PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text = ' '.join(doc.page_content for doc in docs)
        
        # Process through workflow
        workflow = WorkflowManager()
        result = workflow.process_claim(text)
        
        # Cleanup
        os.remove(file_path)
        
        return render_template('index.html', extracted_text=result['ediclaim'])
    except Exception as e:
        return render_template('index.html', error=f"Processing error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)