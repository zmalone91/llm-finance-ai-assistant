# Dockerfile for the Financial Assistant AI Project
# Example base image (Python 3.9 slim)
FROM python:3.9-slim

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml ./
COPY setup.py ./
# If you have a requirements.txt, copy it here
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
# Install in editable mode
COPY src/ ./src/
RUN pip install .

# Copy the rest of the project files
COPY . .

CMD ["bash"]
