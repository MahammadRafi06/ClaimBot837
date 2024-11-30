# AI Agents for Medical Coding
This project leverages LangGraph, LangChain tools, and advanced LLMs (e.g., GPT-4) to automate the generation of Electronic Data Interchange (EDI) claims from medical records. It integrates a MySQL database to manage patient and insurance data while using LangGraph to design a dynamic, agent-based workflow for medical coding, claim generation, and quality assurance.

## Key Features

1. LangGraph-Powered Workflow
   * Utilizes a graph-based workflow to process medical records, generate EDI claims, and perform iterative quality assurance.
   *  Modular and scalable design with well-defined tasks such as:
         - Coder creation
         - Claim generation
         - Quality review and feedback
2. Database Integration
   * MySQL database for storing and querying patient and insurance information.
   * Tools to automate schema exploration, structured queries, and data extraction.
3. Natural Language Processing
   * Employs OpenAI's GPT-4 for text comprehension, structured output generation, and decision-making.
   * Extracts critical information from medical PDFs and maps it to database entities.
4. EDI Claim Automation
   * Generates ANSI X12 837 Professional EDI claims that comply with industry standards.
   * Iteratively improves claims by incorporating feedback to ensure compliance and accuracy.

## Workflow Overview
1. Input Data
   * PDF Medical Charts: Extracts patient and insurance details from files like John_Doe.pdf.
   * MySQL Database: Retrieves stored data related to patients and their insurance providers.
2. Processing Steps
   * Coder Creation: Dynamically generates medical coder personas using GPT-4.
   * Data Extraction: Extracts structured data from medical charts and database records.
3. EDI Claim Generation: Produces fully compliant X12 837 EDI claim files.
4. Quality Assurance: Reviews claims, provides actionable feedback, and flags necessary corrections.
5. Iterative Updates: Refines claims based on feedback until final approval.

## Output 
Compliant EDI Claims: A validated X12 837 Professional EDI file, starting with the ISA segment, ready for submission.


## Project Structure

├── app/
│   ├── components/            # Core functional components
│   │   ├── classes/           # Pydantic models and typed dictionaries
│   │   ├── llms/              # LLM configurations and interactions
│   │   ├── nodes/             # LangGraph nodes for workflow tasks
│   │   ├── prompts/           # Custom GPT prompts
│   │   ├── sql/               # SQL utilities and database tools
│   ├── data/
│   │   ├── pdf_charts/        # Sample PDF charts for testing
│   ├── Dockerfile             # Docker configuration for app container
│   ├── main.py                # Entry point for running the workflow
│   ├── requirements.txt       # Python dependencies
│
├── db/                        
│   ├── init.sql               # MySQL initialization script
│
├── docker-compose.yaml        # Multi-container configuration for app and database
├── LICENSE                    # Project license
├── README.md                  # Project documentation

# Setup and Usage
Prerequisites
   Python 3.9+ (Ensure you have the required version installed)
   MySQL (Database for patient and insurance data)
   Docker (Optional but recommended for environment setup)
