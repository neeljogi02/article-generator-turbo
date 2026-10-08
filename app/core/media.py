import urllib.parse

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

class FreeMediaFetcher:
    def __init__(self):
        pass

    def get_image_url(self, prompt: str) -> str:
        """Fetches a free stock photo URL via DuckDuckGo Images, or generates a Pollinations AI image URL."""
        if DDGS:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.images(keywords=prompt, max_results=1))
                    if results and "image" in results[0]:
                        return results[0]["image"]
            except Exception:
                pass

        encoded_prompt = urllib.parse.quote(prompt)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
