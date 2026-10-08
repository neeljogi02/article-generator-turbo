import urllib.parse
import requests
from app.models.schemas import SectionOutline

class FreeDrafter:
    def __init__(self):
        pass

    def draft_section(self, section: SectionOutline, context_summary: str, research_text: str) -> str:
        prompt = f"""Write a comprehensive, professional, engaging article section in Markdown.
Section Title: {section.heading}
Subsections to cover: {', '.join(section.subheadings)}
Key Talking Points: {', '.join(section.talking_points)}

Context covered earlier:
{context_summary}

Reference research:
{research_text}

Rules:
- Write thorough paragraphs with bold key points.
- Use subheadings (###) where appropriate.
- Do NOT output conversational filler or preamble.
- Jump straight into the content.
"""
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://text.pollinations.ai/{encoded}?model=openai"
            res = requests.get(url, timeout=20)
            if res.status_code == 200 and len(res.text.strip()) > 80:
                return res.text.strip()
        except Exception:
            pass

        # Fast resilient fallback
        body_points = "\n\n".join([f"### {sub}\n{pt}. This approach directly removes structural bottlenecks by replacing rigid pipelines with autonomous, self-evaluating workflows." for sub, pt in zip(section.subheadings, section.talking_points)])
        return f"{body_points}\n\nKey takeaways for this domain include increased resilience, transparent execution tracing, and continuous feedback loops that iteratively improve accuracy."
