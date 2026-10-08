import json
import re
import urllib.parse
import requests
from typing import List
from app.models.schemas import ArticlePlan, SectionOutline, SearchSource

class FreeOutliner:
    def __init__(self, provider: str = "pollinations"):
        self.provider = provider

    def generate_plan(self, topic: str, audience: str, sources: List[SearchSource], research_text: str) -> ArticlePlan:
        prompt = f"""You are an elite SEO strategist.
Topic: {topic}
Audience: {audience}
Research Context:
{research_text}

Output ONLY valid JSON without markdown fences using this exact structure:
{{
  "seo_title": "Catchy SEO Title Here",
  "meta_description": "Meta description under 160 characters",
  "primary_keywords": ["keyword 1", "keyword 2"],
  "secondary_keywords": ["keyword 3", "keyword 4"],
  "sections": [
    {{
      "heading": "H2 Heading",
      "subheadings": ["H3 Subheading 1", "H3 Subheading 2"],
      "talking_points": ["Key point 1", "Key point 2"],
      "image_prompt": "A realistic photo prompt describing this section"
    }}
  ]
}}
Provide exactly 4 high-value sections. Output ONLY the JSON string.
"""
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}?json=true&model=openai"

        try:
            res = requests.get(url, timeout=45)
            res.raise_for_status()
            raw_text = res.text.strip()
            clean_json = re.sub(r"^```json\s*|\s*```$", "", raw_text).strip()
            data = json.loads(clean_json)
        except Exception:
            # Resilient fallback structure if public server is busy
            data = {
                "seo_title": f"The Ultimate Guide to {topic}",
                "meta_description": f"Explore everything you need to know about {topic}, practical breakdowns, and expert insights.",
                "primary_keywords": [topic, f"{topic} guide"],
                "secondary_keywords": ["best practices", "future trends"],
                "sections": [
                    {
                        "heading": f"Understanding {topic}: Fundamentals & Context",
                        "subheadings": ["Core Concepts", "Why It Matters Now"],
                        "talking_points": ["Historical shift", "Immediate operational benefits"],
                        "image_prompt": f"Modern conceptual digital visualization of {topic}"
                    },
                    {
                        "heading": "Key Architecture & Operational Mechanics",
                        "subheadings": ["Core Components", "Workflow Integration"],
                        "talking_points": ["Step-by-step pipeline", "Overcoming structural bottlenecks"],
                        "image_prompt": "Futuristic workflow node diagram glowing on a dark screen"
                    },
                    {
                        "heading": "Real-World Applications and Case Studies",
                        "subheadings": ["Industry Adoption", "Measurable Outcomes"],
                        "talking_points": ["Efficiency gains", "Common failure modes to avoid"],
                        "image_prompt": "Engineers collaborating over a modern dashboard in a bright studio"
                    },
                    {
                        "heading": "Strategic Roadmap and Future Outlook",
                        "subheadings": ["Upcoming Shifts", "Actionable Next Steps"],
                        "talking_points": ["Long-term ROI", "Implementation checklist"],
                        "image_prompt": "Clean minimalist roadmap graphic with ascending progress markers"
                    }
                ]
            }

        parsed_sections = [
            SectionOutline(
                heading=s.get("heading", "Key Concept"),
                subheadings=s.get("subheadings", []),
                talking_points=s.get("talking_points", []),
                image_prompt=s.get("image_prompt", "Illustration of technology")
            )
            for s in data.get("sections", [])
        ]

        return ArticlePlan(
            topic=topic,
            target_audience=audience,
            seo_title=data.get("seo_title", f"Guide to {topic}"),
            meta_description=data.get("meta_description", ""),
            primary_keywords=data.get("primary_keywords", []),
            secondary_keywords=data.get("secondary_keywords", []),
            sections=parsed_sections,
            sources=sources
        )
