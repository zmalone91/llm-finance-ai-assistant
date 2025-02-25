#!/usr/bin/env python3
"""Script to run inference:
- Forecast next month's expenses
- Ask financial questions to the LLM"""

import argparse
from src.inference import run_inference

def main(args):
    # Example usage
    run_inference(question="What is my average monthly expense?")
    run_inference(stock_symbol="AAPL")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference using the Financial Assistant.")
    args = parser.parse_args()
    main(args)
