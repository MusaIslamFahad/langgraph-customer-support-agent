"""
Customer Support Agent — Main Entry Point
Run this file to test the agent with sample queries.
"""

from agents.support_agent import run_customer_support

sample_queries = [
    "My internet connection keeps dropping every few minutes!",   # escalate (negative)
    "I need help setting up two-factor authentication.",          # technical
    "Where can I find my invoice for last month?",               # billing
    "What are your business hours?",                             # general
]

def main():
    for query in sample_queries:
        print(f"{'─' * 60}")
        print(f"Query     : {query}")
        result = run_customer_support(query)
        print(f"Category  : {result['category']}")
        print(f"Sentiment : {result['sentiment']}")
        print(f"Response  : {result['response']}")
        print()

if __name__ == "__main__":
    main()
