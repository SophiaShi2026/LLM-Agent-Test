import os
import sys
import argparse
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')

from rag_agent import rag_answer
from evaluator import evaluate_response


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="RAG CLI: search DuckDuckGo and generate an answer")
    p.add_argument('query', nargs='*', help='Query string (if omitted, will prompt)')
    p.add_argument('-n', '--max-results', type=int, default=5, help='Maximum number of search results')
    p.add_argument('--model', default='deepseek-chat', help='DeepSeek model to use (default: deepseek-chat)')
    p.add_argument('--deepseek-key', default=None, help='Temporarily set DEEPSEEK_API_KEY for this run')
    p.add_argument('--evaluate', default = True, help='Run LLM-based evaluation of response quality')
    p.add_argument('--eval-model', default='deepseek-chat', help='DeepSeek model for evaluation')
    return p


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.deepseek_key:
        os.environ['DEEPSEEK_API_KEY'] = args.deepseek_key

    if args.query:
        query = ' '.join(args.query)
    else:
        query = input('Enter your query: ')



    out = rag_answer(query, max_results=args.max_results, model=args.model)

    print('\n=== Generated Answer ===\n')
    print(out['answer'])
    print('\n=== Sources ===\n')
    for i, s in enumerate(out['sources'], start=1):
        print(f"[{i}]", s.get('title'), '-', s.get('url'))

        
    if args.evaluate:
        print('\n=== Evaluating Response ===\n')
        eval_result = evaluate_response(
            query, 
            out['answer'], 
            out['sources'],
            model=args.eval_model
        )
        
        print(f"Accuracy Score:      {eval_result['accuracy_score']}/10")
        print(f"Relevance Score:     {eval_result['relevance_score']}/10")
        print(f"Search Quality:     {eval_result['search_quality']}/10")
        print(f"Citation Quality:    {eval_result['citation_quality']}/10")
        print(f"Overall Score:       {eval_result['overall_score']}/10")
        print(f"\nFeedback: {eval_result['feedback']}")
        print(f"Strengths: {eval_result['strengths']}")
        print(f"Opportunity: {eval_result['opportunity']}")


if __name__ == '__main__':
    main()