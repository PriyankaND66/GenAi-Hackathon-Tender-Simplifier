# 🏛️ PS-L8: Government Tender Intelligence & Eligibility Engine

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/RAG-LangChain-green.svg)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama--3-black.svg)](https://groq.com/)

> A GenAI-powered architecture engineered to rapidly decode complex government e-tender documents (CPPP & State e-Procurement), extract core criteria, and execute automated eligibility matching for MSMEs.

---

## ⚙️ Architecture & Tech Stack

*   **Frontend Interface:** Streamlit
*   **RAG Pipeline:** LangChain
*   **Vector Store:** FAISS (CPU-Optimized)
*   **Embedding Model:** HuggingFace (`all-MiniLM-L6-v2`)
*   **Inference Engine:** Groq API (`llama-3.3-70b-versatile`)
*   **Document Parsing:** PyPDF2, python-docx

---

## 🚀 Deployment Protocol

### 1. Clone Repository
```bash
git clone [https://github.com/PriyankaND66/GenAi-Hackathon-Tender-Simplifier.git](https://github.com/PriyankaND66/GenAi-Hackathon-Tender-Simplifier.git)
cd GenAi-Hackathon-Tender-Simplifier
```

### 2. Initialize Environment (Windows)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and inject your Groq API key:
```text
GROQ_API_KEY="your_groq_api_key_here"
```

---

## 💻 Execution & Operations

Launch the primary interface:
```powershell
streamlit run app.py
```

### Operational Workflow

1.  **Ingestion:** Download a PDF tender document from the CPPP or Karnataka e-Procurement portal and upload it via the application interface.
2.  **Identity Matrix Definition:** Input the vendor's financial turnover, MSME status, and ISO certifications into the sidebar control panel.
3.  **Evaluate:**
    *   Navigate to the **Plain-Language Summary** tab to generate a 5-section executive breakdown.
    *   Navigate to the **Automated Eligibility Engine** to run a hard pass/fail check against the tender's criteria.
    *   Navigate to the **Operational Checklist** tab to generate and download a `.docx` bid preparation roadmap.