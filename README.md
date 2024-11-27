# Ai Agents for Medical Coding
This project leverages **LangGraph**, **LangChain tools**, and **LLMs (like GPT-4)** to build a structured workflow for automating the generation of Electronic Data Interchange (EDI) claims from medical records. It integrates a MySQL database to manage patient and insurance data and uses LangGraph to design a dynamic agent-based flow for medical coding and claim generation.

---

## Key Features

### **LangGraph-Powered Workflow**
- A **graph-based workflow** to process medical records, generate claims, and handle quality assurance.
- Modular design with defined tasks like coder creation, claim generation, and iterative feedback.

### **Database Integration**
- MySQL database for storing patient and insurance details.
- Automated tools to query and extract structured data from the database.

### **Natural Language Processing**
- Uses OpenAI's GPT-4 models with LangChain tools for text processing and structured output generation.
- Extracts medical record data from PDFs and maps it to database entities.

### **EDI Claim Automation**
- Generates ANSI X12 837 Professional EDI claim files compliant with industry standards.
- Provides iterative feedback to ensure high-quality, accurate claims.

---

## Workflow Overview

### **Input Data**
1. Medical records in PDF format (e.g., `John_Doe.pdf`).
2. Patient and insurance details from the MySQL database.

### **Processing Steps**
1. **Coder Creation**:
   - Dynamically creates medical coder personas using LLMs.
2. **Data Extraction**:
   - Extracts structured patient and insurance details using LangChain tools.
3. **EDI Claim Generation**:
   - Produces fully compliant X12 837 claims based on input data.
4. **Quality Assurance**:
   - Reviews claims for accuracy, providing actionable feedback if revisions are needed.
5. **Iterative Updates**:
   - Adjusts and refines claims based on QA results until approval.

### **Output**
- A validated X12 837 Professional EDI claim file, starting with the `ISA` segment.

---

