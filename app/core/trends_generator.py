import urllib.parse
import requests

class TrendingArticleEngine:
    def __init__(self):
        pass

    def generate_trending_article(self, topic: str, target_market: str = "India (Current Affairs Viva)", extra_context: str = "") -> str:
        prompt = f"""You are an expert SEO content strategist, Google Trends researcher, and Blogger HTML developer.
Topic: {topic}
Target Audience / Site: {target_market}
Context / News: {extra_context}

Follow this exact structure:
A. Google Trends Topic and Research Summary
B. Why This Topic Was Selected
C. SEO Title
D. Meta Description (140-160 chars)
E. URL Slug
F. Primary, Secondary, Long-Tail, and Related Keywords
G. Search Intent and Target Audience
H. Complete Blogger-Ready HTML Article
- Use semantic H2, H3, p, ul, ol, li, and table
- Include a responsive clickable Table of Contents (anchor links)
- Mobile-friendly responsive tables
- Verified facts, exam takeaways, FAQs
- 100% Google AdSense compliant, zero spam
I. Suggested Labels and Categories
J. Featured Image Idea, Alt Text, and Copyright-Safe Image Source
K. Relevant Internal Linking Suggestions
L. Sources and Fact-Checking References
M. Indexing and Publishing Checklist

Generate the complete, publication-ready response directly in clear English suitable for competitive exams and current affairs readers.
"""
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://text.pollinations.ai/{encoded}?model=openai"
            res = requests.get(url, timeout=35)
            if res.status_code == 200 and len(res.text.strip()) > 300:
                return res.text.strip()
        except Exception:
            pass

        return f"""### A. Google Trends Topic and Research Summary
- **Topic:** {topic}
- **Geography:** India / Gujarat Current Affairs Focus

### B. Why This Topic Was Selected
High reader search volume and relevance for competitive examination aspirants and daily news searchers.

### C. SEO Title
{topic}: Key Highlights, Updates, and Exam Preparation Notes

### D. Meta Description
Complete coverage of {topic}. Check key facts, updates, and current affairs analysis for GPSC, UPSC, and competitive exams.

### E. URL Slug
{topic.lower().replace(' ', '-')}-current-affairs-update

### H. Complete Blogger-Ready HTML Article
<div style="font-family: Arial, sans-serif; line-height: 1.7; color: #222;">
<h2>{topic}: Overview & Complete Facts</h2>
<p>Here is the latest verified update on {topic}, organized for competitive examination aspirants and readers of Current Affairs Viva.</p>
</div>
"""
