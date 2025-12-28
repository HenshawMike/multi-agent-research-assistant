import os
import streamlit as st
from crew import create_crew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="Multi-Agent AI Researcher", layout="wide")
st.title("🔍 Multi-Agent Research Assistant")
st.markdown("Enter a topic, optionally upload PDFs, and watch agents collaborate in real-time")

# Sidebar for PDF uploads
with st.sidebar:
    st.header("PDF Upload (Optional)")
    uploaded_files = st.file_uploader(
        "Upload research papers (PDFs)", 
        type="pdf", 
        accept_multiple_files=True
    )

# Main input
topic = st.text_input("Research Topic", placeholder="e.g., Advances in Agentic AI 2026")

if st.button("Start Research") and topic:
    # Handle file uploads
    os.makedirs("uploads", exist_ok=True)
    pdf_paths = []
    
    for uploaded_file in uploaded_files or []:
        path = f"uploads/{uploaded_file.name}"
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            pdf_paths.append(path)
            st.sidebar.success(f"Uploaded: {uploaded_file.name}")
    
    # Initialize crew
    crew = create_crew(topic, pdf_paths if uploaded_files else None)

    # Start the research process
    with st.spinner("Agents are researching..."):
        # Initialize the display
        placeholder = st.empty()
        full_response = ""
        
        # Stream the results
        try:
            result_stream = crew.kickoff(inputs={"topic": topic})
            
            # Process the streaming response
            for chunk in result_stream:
                if hasattr(chunk, "content"):
                    token = str(chunk.content)
                elif isinstance(chunk, (list, tuple)) and len(chunk) > 0:
                    token = str(chunk[0])
                else:
                    token = str(chunk)
                
                full_response += token
                placeholder.markdown(full_response + "▌")
            
            # Final display
            placeholder.markdown(full_response)
            st.success("✅ Research Complete!")
            
            # Add download button
            st.download_button(
                label="📥 Download Research Report",
                data=full_response,
                file_name="research_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up uploaded files
            for path in pdf_paths:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception as e:
                    st.error(f"Error cleaning up file {path}: {str(e)}")