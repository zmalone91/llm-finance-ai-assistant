# Design Decisions

1. **Airflow vs. Prefect**: TBD for scheduling. Starting with a simpler approach.
2. **LLM Choice**: Use a pretrained Hugging Face model (GPT-2 or GPT-Neo).
3. **Model Registry**: Considering MLflow for experiment tracking.
4. **Deployment**: Docker + docker-compose for local dev. Potentially K8s for production.
