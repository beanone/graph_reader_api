FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install build dependencies and clean up in the same layer
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Upgrade pip and setuptools to secure versions
RUN pip install --no-cache-dir -U pip setuptools>=70.0.0

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src /app

# Set Python path
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run the application
CMD ["uvicorn", "graph_reader_api.app:application", "--host", "0.0.0.0", "--port", "8000"]
