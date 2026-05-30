import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

class TenderEngine:
    def __init__(self):
        # Local execution on CPU; automatically downloads (~90MB) on first run
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Free cloud compute tier via Groq
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=1500
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts text layer sequentially from a local PDF file."""
        reader = PdfReader(pdf_path)
        raw_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"
        return raw_text

    def create_vector_store(self, raw_text: str):
        """Splits raw text into overlapping tokens and commits to FAISS index."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(raw_text)
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        return vector_store

    def query_tender(self, vector_store, system_prompt: str, user_query: str) -> str:
        """Executes context-bounded retrieval and structures output via Llama-3."""
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "User Request: {input}\n\nRetrieved Source Context Documents:\n{context}")
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = rag_chain.invoke({"input": user_query})
        return response["answer"]