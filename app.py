import streamlit as st  # pyright: ignore[reportMissingImports] 
from crew import create_crew
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
import os

load_dotenv()

st.set_page_config(page_title="Multi-Agent AI Researcher", layout="wide")
st.title("🔍 Multi-Agent Research Assistant")
st.markdown("Enter a topic, optionally upload PDFs, and watch agents collaborate in real-time")

with st.sidebar:
    st.header("PDF upload(optional fr)")
    uploaded_files = st.file_uploader(
        "Upload research papers (PDFs)", 
        type="pdf", accept_multiple_files=True
        )
topic= st.text_input("Research Topic", placeholder="e.g., Advances in Agentic AI 2026")

if st.button("Start Research") and topic:
    os.makedirs("uploads", exist_ok=True)
    pdf_paths= []
    for uploaded_file in uploaded_files or []:
        path= f"uploads/{uploaded_file.name}"
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            pdf_paths.append(path)
            st.sidebar.success(f"Uploaded: {uploaded_file.name}")