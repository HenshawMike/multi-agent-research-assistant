# Multi-Agent Research Assistant 🚀

A production-ready agentic AI app that researches any topic using web search + uploaded PDFs, with real-time streaming and structured JSON output.

**Live Demo**: [streamlit.app link here]

## Features
- Multi-agent collaboration (Researcher → Analyzer → Writer)
- Web search + PDF RAG analysis
- File upload for custom documents
- Real-time token streaming
- Structured Pydantic/JSON output
- Clean architecture & MLOps-ready

## Architecture Diagram
```mermaid
graph TD
    A[User Input + PDFs] --> B(Streamlit UI)
    B --> C[CrewAI Crew]
    C --> D[Researcher Agent<br/>Serper + PDFSearchTool]
    C --> E[Analyzer Agent<br/>PDF RAG]
    C --> F[Writer Agent<br/>Pydantic Output]
    F --> G[Streaming + JSON Report]