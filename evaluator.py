### Evaluates the quality and accuracy of a RAG-generated response.
### `evaluate_response(query: str, answer: str, sources: list, model: str = "deepseek-chat") → Dict[str, Any]`

# **Parameters**:
# - `query` (str): Original user query
# - `answer` (str): Generated answer text
# - `sources` (list): List of source dictionaries used in answer generation
# - `model` (str): DeepSeek model for evaluation (default: "deepseek-chat")

# **Returns**: Dictionary with keys:
# - `accuracy_score` (0-10): Factual correctness and source support
# - `relevance_score` (0-10): How well answer addresses the query
# - `search_quality` (0-10): Quality and completeness of search results
# - `citation_quality` (0-10): Quality and appropriateness of source citations
# - `overall_score` (0-10): Average of all three scores
# - `feedback` (str): Explanation of scores
# - `strengths` (str): What the response does well
# - `weaknesses` (str): Areas for improvement
# ############################################################################

import os
import json
from typing import Dict, Any

from openai import OpenAI


def evaluate_response(query: str, answer: str, sources: list, model: str = "deepseek-chat") -> Dict[str, Any]:
    """
    Evaluate the quality and accuracy of response using an LLM.
    
    Args:
        query: Original user query
        answer: Generated answer from RAG agent
        sources: List of source dicts with 'title', 'url', 'description'
        model: OpenAI model to use for evaluation
    
    Returns:
        Dict with keys: 'accuracy_score' (0-10), 'relevance_score' (0-10), search_quality' (0-10),
        'citation_quality' (0-10), 'feedback', 'overall_score' (0-10)
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key or OpenAI is None:
        return _fallback_evaluation(query, answer, sources)

    client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1")   
    
    # Build source context for the evaluator
    sources_text = "\n".join([
        f"- {s.get('title', 'N/A')}: {s.get('url', 'N/A')}\n  {s.get('description', '')}"
        for s in sources
    ])
    
    eval_prompt = f"""You are an expert evaluator assessing agent's responses to query based on sources materials used.

User Query: {query}

Generated Answer:
{answer}

Source Material Used:
{sources_text}

Evaluate the response on these criteria:
1. **Accuracy (0-10)**: How factually correct and supported by sources is the answer?
2. **Relevance (0-10)**: How much and directly does the answer address the user's query?
3. **Search quality (0-10)**: Does the search results complete and reflect up-to-date and authoritative information to the query?
4. **Citation Quality (0-10)**: Are sources properly cited and used appropriately?


Respond in JSON format only with this exact structure (no markdown, no code blocks):
{{
  "accuracy_score": <int 0-10>,
  "relevance_score": <int 0-10>,
  "search_quality": <int 0-10>,
  "citation_quality": <int 0-10>,
  "feedback": "<brief explanation of scores>",
  "strengths": "<what the response does well>",
  "opportunity": "<what could be improved>"
}}"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": eval_prompt}],
            max_tokens=512,
            temperature=1,
        )
        eval_text = resp.choices[0].message.content.strip()
        
        # Parse JSON response
        eval_dict = json.loads(eval_text)
        
        # Calculate overall score as average
        overall = (eval_dict.get("accuracy_score", 5)*0.3+ 
                   eval_dict.get("relevance_score", 5)*0.3+
                   eval_dict.get("search_quality", 5)*0.3+ 
                   eval_dict.get("citation_quality", 5)*0.1) 
        eval_dict["overall_score"] = round(overall, 1)
        
        return eval_dict
    
    except (json.JSONDecodeError, KeyError, Exception) as e:
        # Fallback if parsing fails
        return {
            "accuracy_score": 5,
            "relevance_score": 5,
            "citation_quality": 5,
            "search_quality": 5,
            "overall_score": 5.0,
            "feedback": f"Evaluation failed: {str(e)}. Using neutral scores.",
            "strengths": "Evaluation system error, unable to evaluate.",
            "opportunity": "Evaluation system error, unable to evaluate."
        }


def _fallback_evaluation(query: str, answer: str, sources: list) -> Dict[str, Any]:
    """Heuristic-based evaluation when no LLM is available."""
    # Simple heuristic checks
    answer_len = len(answer.split())
    has_citations = "[" in answer and "]" in answer
    has_sources = len(sources) > 0
    
    accuracy = 6 if has_sources else 4
    relevance = 7 if answer_len > 20 else 5
    citation = 8 if has_citations else 4
    
    return {
        "accuracy_score": accuracy,
        "relevance_score": relevance,
        "citation_quality": citation,
        "overall_score": round((accuracy + relevance + citation) / 3, 1),
        "feedback": "Heuristic evaluation (no LLM available). Actual quality may vary.",
        "strengths": "Response generated successfully" if answer_len > 10 else "Short response",
        "opportunity": "Use OpenAI API key for evaluation" if not os.environ.get("DEEPSEEK_API_KEY") else "None detected"
    }