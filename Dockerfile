# Multi-stage build for Python Flask application
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Add metadata
LABEL maintainer="NAB POC Team"
LABEL description="NAB Python Hello World Application for Harness CI/CD"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    APP_VERSION=${APP_VERSION:-1.0.0}

WORKDIR /app

# Create non-root user first
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1001 appuser

# Copy dependencies from builder to a location accessible by appuser
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app.py .
COPY requirements.txt .

# Change ownership of all files to appuser
RUN chown -R appuser:appuser /app /home/appuser/.local

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health').read()" || exit 1

# Start application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]
