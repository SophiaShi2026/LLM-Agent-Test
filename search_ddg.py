###Searches DuckDuckGo and returns web pages matching the query.
### `search_duckduckgo(query: str, max_results: int = 10, safesearch: str = 'moderate', timelimit: str = 'm') → List[Dict[str, Optional[str]]]`
# **Parameters**:
# - `query` (str): Search query string
# - `max_results` (int): Maximum number of results to return (default: 10)
# - `safesearch` (str): Safety filter level - 'Off', 'Moderate', 'Strict' (default: 'moderate')
# - `timelimit` (str): Time filter - 'd' (day), 'w' (week), 'm' (month), 'y' (year) (default: 'm')

# **Returns**: List of dictionaries with keys:
# - `title`: Page title
# - `url`: Page URL
# - `description`: Page snippet/description

# **Raises**:
# - `RuntimeError`: If `ddgs` library is not installed
# - `TypeError`: If `query` is not a string """
###############################################################################
import os   
from typing import List, Dict, Optional

try:
    from ddgs import DDGS
except Exception:  # keep import error visible at runtime if ddgs is missing
    DDGS = None  # type: ignore


def search_duckduckgo(query: str, max_results: int = 10, safesearch: str = 'moderate', timelimit: str = 'm') -> List[Dict[str, Optional[str]]]:
    """Search using DuckDuckGo and return webpages.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.
        safesearch: safesearch setting passed to ddgs (e.g. 'Off', 'Moderate', 'Strict').

    Returns:
        A list of dict items with keys: 'title', 'url', 'description'.

    Raises:
        RuntimeError: If the `ddgs` library is not installed.
        TypeError: If `query` is not a string.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")

    if DDGS is None:
        raise RuntimeError("ddgs library is not available. Install with 'pip install ddgs'")

    results: List[Dict[str, Optional[str]]] = []

    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, safesearch=safesearch, timelimit=timelimit):
                url = item.get('link') or item.get('url') or item.get('href')
                results.append({
                    'title': item.get('title'),
                    'url': url,
                    'description': item.get('body') or item.get('desc') or None,
                })
                if len(results) >= max_results:
                    break 
    except Exception as e:
        print(f"Error during DuckDuckGo search: {e}")
    return results

#example usage
#output = search_duckduckgo('openAI', max_results=5)
#print(output)


