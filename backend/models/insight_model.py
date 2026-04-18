from pydantic import BaseModel, Field
from typing import Literal, Optional

class Insight(BaseModel):
    title: str = Field(..., max_length=100)
    text: str = Field(..., max_length=300)
    category: Literal["finance", "clients", "marketing", "retention", "operations"]
    priority: Literal["low", "medium", "high"]

class InsightResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[Insight]

class InsightRequest(BaseModel):
    focus: Optional[str] = Field(None, max_length=500)
    observations: Optional[str] = Field(None, max_length=1000)
