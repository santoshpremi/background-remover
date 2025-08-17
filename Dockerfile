# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.9

# Use a smaller base image
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed for PyTorch
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Create the 'appuser' user
RUN useradd -m -s /bin/bash appuser

# Install Python dependencies in a separate stage for better caching
FROM base as dependencies

# Copy only requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies globally (not --user)
RUN pip install --no-cache-dir -r requirements.txt

# Final stage - copy only necessary files
FROM base as final

# Copy Python packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Switch to the non-privileged 'appuser'.
USER appuser

# Copy only the necessary source code (exclude unnecessary files)
COPY --chown=appuser:appuser engine.py main.py model.py utils.py ./
COPY --chown=appuser:appuser static/ ./static/
COPY --chown=appuser:appuser u2netp.pth ./

# Expose the port that the application listens on.
EXPOSE 8000

# Set default port for Render
ENV PORT=8000

# Run the application. Use a single worker to avoid duplicating model RAM.
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV UVICORN_WORKERS=1

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${UVICORN_WORKERS}




