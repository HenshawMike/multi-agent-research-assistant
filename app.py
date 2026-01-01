import os
import json 
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
    
    
    crew = create_crew(topic, pdf_paths if uploaded_files else None)

    
    with st.spinner("Agents are researching..."):
        status_container = st.status("Initializing crew...")



        def callback(task_output):
            status_container.update(
                label=f"Task: {task_output.description[:100]}...",
                state="running",
                expanded=True
            )
            status_container.markdown(f"**Raw output so far:**\n{task_output.raw}")
        
        for task in crew.tasks:
            task.callback= callback
        
        # Stream the results
        try:
            result = crew.kickoff(inputs={"topic": topic})
            if isinstance(result, str):
                try:
                    # Try to parse as JSON first
                    json.loads(result)
                    final_report = result
                except json.JSONDecodeError:
                    # If not valid JSON, wrap in a JSON object
                    final_report = json.dumps({"content": result})
                token_usage = None
            else:
                try:
                    # Handle the raw result
                    if hasattr(result, 'raw'):
                        if isinstance(result.raw, str):
                            try:
                                json.loads(result.raw)  # Validate JSON
                                final_report = result.raw
                            except json.JSONDecodeError:
                                final_report = json.dumps({"content": result.raw})
                        else:
                            final_report = json.dumps(result.raw)
                    else:
                        final_report = json.dumps({"content": str(result)})
                except Exception as e:
                    st.error(f"Error processing report: {str(e)}")
                    final_report = json.dumps({"error": f"Error processing report: {str(e)}"})
                
                # Safely extract token usage if available
                token_usage = None
                if hasattr(result, "token_usage") and result.token_usage is not None:
                    token_usage = {
                        "prompt_tokens": getattr(result.token_usage, "prompt_tokens", 0),
                        "completion_tokens": getattr(result.token_usage, "completion_tokens", 0),
                        "total_tokens": getattr(result.token_usage, "total_tokens", 0)
                    }

            status_container.update(label="Research Complete!", state="complete", expanded=False)
            st.markdown(final_report)  

            json_data = {
                "topic": topic,
                "report": final_report,
                "token_usage": token_usage
            }

            st.download_button(
                label="Download Research Report (JSON)",
                data=json.dumps(json_data, indent=2, ensure_ascii=False),
                mime="application/json"
            )  
            # Process the streaming response
            #for chunk in result:
             #   if hasattr(chunk, "content"):
              #      token = str(chunk.content)
               # elif isinstance(chunk, (list, tuple)) and len(chunk) > 0:
                #    token = str(chunk[0])
                #else:
                 #   token = str(chunk)
                
                #full_response += token
                #placeholder.markdown(full_response + "▌")
            
            
           # placeholder.markdown(full_response)
          #  st.success("✅ Research Complete!")
            
            # Add download button
           # st.download_button(
            #    label="📥 Download Research Report",
             #   data=full_response,
              ## mime="text/markdown"
            #)
            
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