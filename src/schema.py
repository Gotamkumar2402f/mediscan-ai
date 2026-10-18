"""Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    source: str
    score: float = 0.0
    snippet: str = ""

class ClinicalAnswer(BaseModel):
    condition: Optional[str] = None
    summary: str = ""
    symptoms: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)
    treatment_overview: List[str] = Field(default_factory=list)
    when_to_see_doctor: str = ""
    follow_up_questions: List[str] = Field(default_factory=list)
    emergency: bool = False
    citations: List[Citation] = Field(default_factory=list)
    disclaimer: str = ""