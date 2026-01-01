import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
from crewai import LLM, Agent, Task, Crew, Process # pyright: ignore[reportMissingImports]
from crewai_tools import SerperDevTool, PDFSearchTool # pyright: ignore[reportMissingImports]
from langchain_openai import ChatOpenAI # pyright: ignore[reportMissingImports]
from models import ResearchReport



load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")


llm= LLM(
    model="openrouter/meta-llama/llama-3.1-405b-instruct:free",
    api_key= api_key,
    base_url= "https://openrouter.ai/api/v1",
    temperature=0.7,
)

search_tool= SerperDevTool() 

def create_crew(topic: str, pdf_paths: list[str] | None = None):
    pdf_tool= PDFSearchTool()
    if pdf_paths:
        for path in pdf_paths:
            pdf_tool.add(path)
    researcher = Agent(
        role="Document Researcher",
        goal="Find relevant web sources and extract insights from provided PDFs.",
        backstory="Expert at finding high-quality sources and deeply analyzing documents.",
        tools=[search_tool, pdf_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        )
    analyzer= Agent(
        role="Research Analyst",
        goal="Synthesize information from web and PDFs into key findings.",
        backstory="PhD-level analyst skilled in distilling complex information.",
        tools=[pdf_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    writer= Agent(
        role="Structured Report Writer",
        goal="Transform findings into a well-structured research report.",
        backstory="Experienced technical writer with a knack for clarity and precision.",
        tools=[pdf_tool],
        llm=llm,
        verbose=True,       
        allow_delegation=False,
    )

    task1= Task(
        description=f"""Search  the web for recent sources on "{topic}" and , if PDFs are provided, 
        extract relevant sections. Prioritize arXiv/academic papers. Output top 5-8 sources with brief relevance.""", 
        expected_output="List of sources  with  titles, URLs/files, and relevance notes.",
        agent= researcher,
    )
    task2= Task(
        description=f"""Deeply analyze the sources and PDFs for key insights on "{topic}". 
        Focus on methods, results, implications.""",
        expected_output="Detailed bullet-point insights with citations.",
        agent=analyzer,
    )
    task3= Task(
        description=f"""Compile a structured research report on "{topic}" following the exact JSON schema.
        Include introduction, key findings (with sources), conclusion, and recommendations.""",
        expected_output="Valid JSON matching ResearchReport schema.",
        agent=writer,
        output_pydantic=ResearchReport,
    )
    return Crew(
        agents=[researcher, analyzer, writer],
        tasks=[task1, task2, task3],
        verbose=1,
        process=Process.sequential
    )

