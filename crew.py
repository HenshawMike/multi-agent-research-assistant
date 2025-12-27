import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports] 
from crewai import Agent, Task, Crew, Process # pyright: ignore[reportMissingImports]
from crewai_tools import SerperDevTool, PDFSearchTool # pyright: ignore[reportMissingImports]
from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]
from models import ResearchReport

load_dotenv()

llm= ChatGoogleGenerativeAI(
    model="google/gemma-3n-e4b-it:free"
    apiKey= os.getenv("OPENROUTER_API_KEY")
    baseUrl= "https://openrouter.ai/api/v1/chat/completions"

)



