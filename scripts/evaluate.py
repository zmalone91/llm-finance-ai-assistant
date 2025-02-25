#!/usr/bin/env python3
"""Script to evaluate both forecasting and LLM models."""

import argparse
from src.models.evaluate_models import evaluate_models

def main(args):
    evaluate_models()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate ML models.")
    args = parser.parse_args()
    main(args)
