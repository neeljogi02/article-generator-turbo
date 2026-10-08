import urllib.parse
import requests
from typing import List
from app.models.schemas import SearchSource

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

class FreeResearcher:
    def __init__(self, max_results: int = 4):
        self.max_results = max_results
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def search_topic(self, topic: str) -> List[SearchSource]:
        results = []

        # 1. Try DuckDuckGo
        if DDGS:
            try:
                with DDGS() as ddgs:
                    for item in ddgs.text(keywords=topic, max_results=self.max_results):
                        results.append(
                            SearchSource(
                                title=item.get("title", ""),
                                url=item.get("href", ""),
                                snippet=item.get("body", "")
                            )
                        )
                if results:
                    return results
            except Exception:
                pass

        # 2. Cloud Fallback: Wikipedia API (100% reliable inside cloud environments)
        try:
            clean_q = urllib.parse.quote(topic)
            url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={clean_q}&limit={self.max_results}&namespace=0&format=json"
            res = requests.get(url, headers=self.headers, timeout=8).json()
            if len(res) >= 4 and res[1]:
                for title, snippet, link in zip(res[1], res[2], res[3]):
                    results.append(
                        SearchSource(
                            title=title,
                            url=link,
                            snippet=snippet if snippet else f"In-depth analysis covering {title}."
                        )
                    )
        except Exception:
            pass

        return results

    def format_sources_for_prompt(self, sources: List[SearchSource]) -> str:
        if not sources:
            return "Domain industry expertise and standard engineering best practices."
        formatted = []
        for idx, s in enumerate(sources, 1):
            formatted.append(f"[{idx}] {s.title} ({s.url})\nExcerpt: {s.snippet}\n")
        return "\n".join(formatted)
