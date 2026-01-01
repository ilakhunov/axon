from typing import List, Dict
from duckduckgo_search import DDGS
from axon.retry import retry

@retry(max_attempts=3, backoff=2.0)
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return results.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted string with search results including titles, URLs, and snippets
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"No results found for query: '{query}'"
        
        # Format results
        formatted = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            url = result.get('href', 'No URL')
            body = result.get('body', 'No description')
            formatted += f"{i}. **{title}**\n   URL: {url}\n   {body}\n\n"
        
        return formatted.strip()
    
    except Exception as e:
        return f"Error performing web search: {str(e)}"
