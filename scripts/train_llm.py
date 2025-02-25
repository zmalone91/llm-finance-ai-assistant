#!/usr/bin/env python3
"""Script to fine-tune or prompt-tune an LLM for financial Q&A."""

import argparse
from src.models.llm.train_llm import train_financial_llm

def main(args):
    train_financial_llm()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune a financial LLM model.")
    # parser.add_argument("--model_name", type=str, default="gpt2", help="Base model name")
    args = parser.parse_args()
    main(args)
