from dotenv import load_dotenv
load_dotenv()  # Must execute before importing elements dependent on environment variables

import streamlit as st
import os
from core_engine import TenderEngine
from doc_generator import generate_checklist_docx

# Application Config
st.set_page_config(page_title="GovTender Intelligence Center", layout="wide")
st.title("Government Tender Simplifier & Multi-Criterion Checker")

# Engine State Initialization
if "engine" not in st.session_state:
    st.session_state.engine = TenderEngine()
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# Sidebar Control: Structured Identity Inputs for Evaluation
st.sidebar.header("Vendor Identity Profiles")
vendor_name = st.sidebar.text_input("Entity Name", placeholder="e.g., Tech Corp")
vendor_turnover = st.sidebar.number_input("Verified Annual Turnover (INR in Lakhs)", min_value=0.0, format="%.2f")
msme_status = st.sidebar.selectbox("MSME Registration Status", ["Select", "Micro Enterprise", "Small Enterprise", "Medium Enterprise", "Not Registered"])
iso_status = st.sidebar.selectbox("ISO 9001 Certification Status", ["Select", "Certified", "Not Certified"])

# Main Application File Ingestion
uploaded_file = st.file_uploader("Upload Live Tender Document (PDF Format Only)", type=["pdf"])

if uploaded_file:
    # Buffer writing to dynamic workspace directory
    os.makedirs("data", exist_ok=True)
    temp_path = os.path.join("data", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Lazy indexing execution block
    if st.session_state.vector_store is None:
        with st.spinner("Extracting strings and updating FAISS index weights locally..."):
            raw_text = st.session_state.engine.extract_text_from_pdf(temp_path)
            st.session_state.vector_store = st.session_state.engine.create_vector_store(raw_text)
            st.success("Indexing sequence complete.")

    # Execution Tabs mapping precisely to mandatory problem statement clauses
    tab1, tab2, tab3 = st.tabs(["Tender Simplification", "Automated Eligibility Engine", "Operational Checklist Export"])
    
    with tab1:
        st.subheader("Plain-Language Summary Compilation")
        if st.button("Synthesize Executive Breakdown"):
            summary_prompt = (
                "Transform the source documentation precisely into exactly five core sections without introducing outside data: "
                "1. Scope of Work, 2. Financial Requirements (EMD, Tender Fee, Performance Security), "
                "3. Core Eligibility Benchmarks, 4. Critical Milestones/Timelines, 5. Absolute Disqualification Clauses."
            )
            with st.spinner("Processing local FAISS chunks via Llama-3..."):
                summary_output = st.session_state.engine.query_tender(
                    st.session_state.vector_store, summary_prompt, "Generate explicit summary."
                )
                st.markdown(summary_output)

    with tab2:
        st.subheader("Automated Multi-Criterion Compliance Matcher")
        if st.button("Evaluate Compliance Matrix"):
            if vendor_name == "" or msme_status == "Select" or iso_status == "Select":
                st.error("Identity inputs inside the sidebar workspace are incomplete.")
            else:
                profile_context = (
                    f"Vendor Identity Matrix:\n- Entity Name: {vendor_name}\n"
                    f"- Turnover Profile: {vendor_turnover} Lakhs\n"
                    f"- MSME Class: {msme_status}\n- ISO 9001 Status: {iso_status}"
                )
                compliance_prompt = (
                    "Cross-reference the submitted Vendor Identity Matrix against the rules extracted from the documentation. "
                    "Provide an itemized comparison table indicating a clear 'PASS', 'FAIL', or 'POTENTIAL MSME EXEMPTION' for "
                    "turnover thresholds, registration bounds, and credential verification. Cite sections or text context rules directly."
                )
                with st.spinner("Evaluating compliance structures..."):
                    evaluation_output = st.session_state.engine.query_tender(
                        st.session_state.vector_store, compliance_prompt, profile_context
                    )
                    st.markdown(evaluation_output)

    with tab3:
        st.subheader("Bid Document Compilation Matrix")
        if st.button("Build Procurement Roadmap"):
            checklist_prompt = (
                "Locate and compile all compliance documents required for submission, fee timelines, "
                "technical bid envelope prerequisites, financial bid rules, and specific annexures mentioned "
                "in the source document. Format clean headers with descriptive items."
            )
            with st.spinner("Isolating procedural components..."):
                checklist_output = st.session_state.engine.query_tender(
                    st.session_state.vector_store, checklist_prompt, "Extract checklist fields."
                )
                st.text_area("Live Matrix View", checklist_output, height=250)
                
                # Document build action
                docx_buffer = generate_checklist_docx(uploaded_file.name, checklist_output)
                st.download_button(
                    label="Download Compiled Checklist (.docx)",
                    data=docx_buffer,
                    file_name=f"Roadmap_{uploaded_file.name.replace('.pdf', '')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )