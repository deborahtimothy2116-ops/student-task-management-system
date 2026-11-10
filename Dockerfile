# ==============================================================================
# Multi-Stage Production Dockerfile for EduTask
# Student Task Management System - Course 231CS523 Unit-V
# ==============================================================================

# Stage 1: Build & Dependencies
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime Environment
FROM python:3.11-slim AS runner

WORKDIR /app

# Create non-root user for security best practices
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code and static assets
COPY src/ /app/src/
COPY tests/ /app/tests/

# Set ownership to appuser
RUN chown -R appuser:appgroup /app /home/appuser

# Configure environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    PORT=8000

# Switch to non-privileged user
USER appuser

# Expose web service port
EXPOSE 8000

# Built-in Docker Health Check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Production server execution entrypoint
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
