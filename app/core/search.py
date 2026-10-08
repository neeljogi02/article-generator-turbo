from duckduckgo_search import DDGS
from app.models.schemas import SearchSource
from typing import List

class FreeResearcher:
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.ddgs = DDGS()

    def search_topic(self, topic: str) -> List[SearchSource]:
        """Runs a live web search on DuckDuckGo and returns structured sources."""
        results = []
        try:
            # Query DuckDuckGo text search
            raw_results = self.ddgs.text(keywords=topic, max_results=self.max_results)
            for item in raw_results:
                results.append(
                    SearchSource(
                        title=item.get("title", ""),
                        url=item.get("href", ""),
                        snippet=item.get("body", "")
                    )
                )
        except Exception as e:
            print(f"[Warning] Web search failed: {e}. Falling back to zero-shot context.")
        return results

    def format_sources_for_prompt(self, sources: List[SearchSource]) -> str:
        """Formats search findings into compact markdown context for the LLM."""
        if not sources:
            return "No live external search results available."
        
        formatted = []
        for idx, s in enumerate(sources, 1):
            formatted.append(f"[{idx}] {s.title}\nURL: {s.url}\nExcerpt: {s.snippet}\n")
        return "\n".join(formatted)