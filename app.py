import os
import streamlit as st  # pyright: ignore[reportMissingImports] 
from crew import create_crew
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 

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
    crew= create_crew(topic, pdf_paths  if uploaded_files else None)

    with st.spinner("Agents Starting Research..."):
        result_stream= crew.kickoff(inputs={"topic": topic})
        placeholder= st.empty()
        full_response=""

        for chunk in result_stream:
            if hasattr(chunk, "content"):
                token= chunk.content
            elif isinstance(chunk, (list, tuple)) and len(chunk)>0:
                token= chunk[0]
            else:
                token= str(chunk)
            full_response+= token
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

        if hasattr(crew.kickoff_result, "pydantic"):
            st.success("Research Report Generated Successfully!")
            st.json(crew.kickoff_result.pydantic.model_dump())

        st.download_button("Download Raw Report",full_response, file_name="research_report.md")
        if hasattr(crew.kickoff_result, "pydantic"):
            st.download_button(
                "Download JSON Report",
                crew.kickoff_result.pydantic.model_dump_json(indent=2),
                file_name="report.json"
            )
    for path in pdf_paths:
        os.remove(path)