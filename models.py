from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]
from typing import List

class ResearchFinding(BaseModel):
    title: str = Field(..., description="Title of the research finding")
    summary: str = Field(..., description="Key summary points from search")
    sources: List[str] = Field(..., description="List of sources URls like em citation and shit")

class ResearchReport(BaseModel):
    topic: str = Field(..., description="Topic of research report ")
    introduction: str
    key_findings: List[ResearchFinding]
    conclusion: str
    recommendations: str = Field(default="", description="Recommendations for future research")