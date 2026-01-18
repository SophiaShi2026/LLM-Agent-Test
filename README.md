# RAG (Retrieval-Augmented Generation) CLI - Usage Guide

A Python-based command-line tool that searches the web using DuckDuckGo, retrieves relevant information, and uses the DeepSeek API to generate accurate, source-cited answers,and  evaluates response quality.

## Features

- **Web Search**: Uses DuckDuckGo to find relevant sources, limit time frame to 1 month to get more recent content.
- **Answer Generation**: Uses DeepSeek API to synthesize answers from search results.
- **Source Citation**: Automatically cites sources in generated answers.
- **Response Evaluation**: LLM-based evaluation of answer quality (accuracy, relevance, search and citation quality).
- **Fallback Support**: Works gracefully without API keys using heuristic evaluation.

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup

1. **Clone/download the project** to your local machine

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with your API key:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

## Project Structure

```
├── cli.py                 # Command-line interface entry point
├── rag_agent.py           # Core RAG logic (search + answer generation)
├── evaluator.py           # Response quality evaluation
├── search_ddg.py          # DuckDuckGo search wrapper
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this file)
└── README.txt             # This file
```



## Usage

### Example: Query with Evaluation

```powershell
python cli.py "What is machine learning?"
```

**Output**:
```
=== Generated Answer ===

Machine learning is a field of artificial intelligence where computers learn autonomously from data to identify patterns and make decisions, without being explicitly programmed for each specific task [1][2][5].

Sources used: [1], [2], [5]

=== Sources ===

[1] Machine learning - Wikipedia - https://en.wikipedia.org/wiki/Machine_learning
[2] What Is Machine Learning? | Definition, Tools, & Applications ... - https://www.britannica.com/technology/What-Is-Machine-Learning
[3] What is machine learning? - IBM - https://www.ibm.com/think/topics/machine-learning?category=663b58b76ad9dab9159c9887
[4] What is Machine Learning? How It Works & Use Cases in 2026 - https://graffersid.com/what-is-machine-learning/
[5] Machine Learning Tutorial - GeeksforGeeks - https://www.geeksforgeeks.org/machine-learning/machine-learning/

=== Evaluating Response ===

Accuracy Score:      9/10
Relevance Score:     10/10
Search Quality:     9/10
Citation Quality:    7/10
Overall Score:       9.1/10

Feedback: The answer is highly accurate and directly relevant, sourced from authoritative materials. The search results are excellent, but the citation could be more precise regarding the specific information drawn from each source.
Strengths: The response provides a concise, correct, and clear definition that directly answers the query. It correctly identifies the core concepts of learning from data, pattern recognition, and autonomous decision-making without explicit programming, which are well-supported by the provided sources.
Opportunity: The citation [5] is used, but the GeeksforGeeks source is not explicitly quoted in the generated text, making its specific contribution unclear. The response could be slightly expanded to mention its basis in statistical algorithms or its role as a subfield of AI for a more comprehensive answer, with clearer attribution of ideas to specific sources.

