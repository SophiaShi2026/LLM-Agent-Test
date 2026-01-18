###Performs Retrieval-Augmented Generation on the query.
### `rag_answer(query: str, max_results: int = 10, model: str = "deepseek-chat") → Dict[str, Any]`
#**Parameters**:
#- `query` (str): Your question or search query
#- `max_results` (int): Number of search results to retrieve (default: 10)
#- `model` (str): model name (default: "deepseek-chat")

# **Returns**: Dictionary with keys:
# - `query`: The original query
# - `answer`: Generated answer with citations
# - `sources`: List of source dictionaries used
##############################################################################

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any
from search_ddg import search_duckduckgo

# Load environment variables from .env file
load_dotenv()

def rag_answer(query: str, max_results: int = 10, model: str = "deepseek-chat") -> Dict[str, Any]:
    """Perform a simple Retrieval-Augmented Generation using DuckDuckGo search results.

    If `DEEPSEEK_API_KEY` is set and `openai` is installed, the function will call DeepSeek's
     API to generate an answer using the retrieved documents. Otherwise
    it returns an aggregated fallback result built from titles and descriptions.

    Returns a dict with keys: `query`, `answer`, `sources`.
    """
    results = search_duckduckgo(query, max_results=max_results)

    # Build a compact context from retrieved results
    docs: List[str] = []
    for i, r in enumerate(results, start=1):
        title = r.get("title") or "(no title)"
        url = r.get("url") or "(no url)"
        desc = r.get("description") or ""
        docs.append(f"[{i}] {title}\n{url}\n{desc}")

    context = "\n\n".join(docs)

    # If DeepSeek API key is available and openai is installed, use it to generate an answer
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if api_key and OpenAI is not None:
        # Configure openai client to use DeepSeek API
        client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1")
        
        system = (
            "You are a helpful assistant. Answer the user's question using only the content in provided"
            " webpages from search results. Cite sources by their number in square brackets, e.g. [1]."
        )
        user_prompt = (
            f"Question: {query}\n\nSearch results:\n{context}\n\n"
            "Answer concisely and list which sources you used at the end."
        )

        # print("user_prompt:", user_prompt)

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
                max_tokens=512,
                temperature=1,
                timeout=60
            )
            answer = resp.choices[0].message.content.strip()
            #print("DeepSeek API response:", answer)
            return {"query": query, "answer": answer, "sources": results}
        except Exception as e:
            fallback_answer = f"DeepSeek API error: {str(e)}\n\nFallback search results:\n{context}"
            return {"query": query, "answer": fallback_answer, "sources": results}

    # Fallback: return aggregated snippets when no DeepSeek API key available
    fallback_answer = (
        "No DEEPSEEK_API_KEY set or `openai` package not found. Returning aggregated search snippets:\n\n"
        + context
    )
    return {"query": query, "answer": fallback_answer, "sources": results}


if __name__ == "__main__":
    # simple ad-hoc test when run directly
    q = "How to use openAI library in Python?"
    out = rag_answer(q, max_results=3)
    print("--- Answer ---")
    print(out["answer"])
    print("--- Sources ---")
    for s in out["sources"]:
        print(s.get("title"), "-", s.get("url"))