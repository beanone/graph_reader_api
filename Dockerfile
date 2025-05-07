FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools to secure versions
RUN pip install --no-cache-dir -U pip setuptools>=70.0.0

# Copy project files
COPY pyproject.toml ./
COPY src /app
COPY requirements.txt ./

# Install dependencies and the package
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "graph_reader_api.app:application", "--host", "0.0.0.0", "--port", "8000"]
