from setuptools import setup, find_packages

setup(
    name="finance_ai_assistant",
    version="0.1.0",
    description="A Financial Assistant Project with LLM and Forecasting",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.2.0",
        "scikit-learn>=1.0.0"
        # Add more core dependencies or just rely on pyproject.toml
    ],
)
