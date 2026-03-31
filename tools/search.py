from langchain_core.tools import tool
from config import config
import logging

logger = logging.getLogger(__name__)

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information on any topic.
    Use this when the user asks about recent events, news, current prices,
    live data, or anything that requires up-to-date information.
    Input should be a clear search query string.
    """
    # Try Tavily first (better quality)
    if config.tavily_api_key:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=config.tavily_api_key)
            results = client.search(
                query=query,
                max_results=config.max_search_results,
                search_depth="basic"
            )
            if results.get("results"):
                formatted = []
                for r in results["results"][:config.max_search_results]:
                    formatted.append(
                        f"Title: {r.get('title', 'No title')}\n"
                        f"URL: {r.get('url', '')}\n"
                        f"Summary: {r.get('content', '')[:400]}"
                    )
                return "\n\n---\n\n".join(formatted)
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}, falling back to DuckDuckGo")

    # Fallback to DuckDuckGo
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=config.max_search_results))
        if results:
            formatted = []
            for r in results:
                formatted.append(
                    f"Title: {r.get('title', '')}\n"
                    f"URL: {r.get('href', '')}\n"
                    f"Summary: {r.get('body', '')[:400]}"
                )
            return "\n\n---\n\n".join(formatted)
        return "No search results found."
    except Exception as e:
        logger.error(f"DuckDuckGo search also failed: {e}")
        return f"Search failed: {str(e)}"
