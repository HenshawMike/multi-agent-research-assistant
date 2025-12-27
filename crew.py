import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
from crewai import Agent, Task, Crew, Process # pyright: ignore[reportMissingImports]
from crewai_tools import SerperDevTool, PDFSearchTool # pyright: ignore[reportMissingImports]
from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]
from models import ResearchReport

load_dotenv()

llm= ChatGoogleGenerativeAI(
    model="google/gemma-3n-e4b-it:free",
    apiKey= os.getenv("OPENROUTER_API_KEY"),
    baseUrl= "https://openrouter.ai/api/v1/chat/completions"
)

search_tool= SerperDevTool() 

def create_crew(topic: str, pdf_paths: list[str] | None = None):
    pdf_tool= PDFSearchTool()
    if pdf_paths:
        for path in pdf_paths:
            pdf_tool.add(path)
    researcher = Agent(
        role="Document Researcher",
        goal="Find relevant web sources and extract insights from provided PDFs."
        backstory="Expert at finding high-quality sources and deeply analyzing documents."
        tools=[search_tool, pdf_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    




