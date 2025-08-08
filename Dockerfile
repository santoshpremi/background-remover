# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.9

FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create the 'appuser' user with a home directory.
RUN useradd -ms /bin/bash appuser

# Download dependencies as a separate step to leverage caching.
# Use a cache mount to speed up subsequent builds.
# Bind mount the requirements.txt to avoid copying it into this layer.


RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt


# Switch to the non-privileged 'appuser'.
USER appuser

# Copy the source code into the container.
COPY . .

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




