FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.py ./
COPY src ./src

# Install dependencies and the package
RUN pip install beanone_graph && \
    pip install -e .

# Set Python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "graph_reader_api.app:app", "--host", "0.0.0.0", "--port", "8000"]