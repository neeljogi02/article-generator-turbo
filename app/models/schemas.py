from typing import List, Optional
from pydantic import BaseModel, Field

class SearchSource(BaseModel):
    title: str
    url: str
    snippet: str

class SectionOutline(BaseModel):
    heading: str = Field(description="H2 heading text")
    subheadings: List[str] = Field(default_factory=list, description="List of H3 subsections")
    talking_points: List[str] = Field(description="Key facts/arguments to cover")
    image_prompt: str = Field(description="Visual search prompt for an illustration or photo")

class ArticlePlan(BaseModel):
    topic: str
    target_audience: str
    seo_title: str
    meta_description: str
    primary_keywords: List[str]
    secondary_keywords: List[str]
    sections: List[SectionOutline]
    sources: List[SearchSource] = Field(default_factory=list)