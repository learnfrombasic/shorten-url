# Use a lightweight base image and specify a fixed version for reproducibility
FROM python:3.10-slim-bullseye AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip in the same layer to avoid extra intermediate image size
RUN pip install --no-cache-dir --upgrade pip

# Stage 2: Build Dependencies
FROM base AS build

# Install gcc and other essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies for the application
COPY requirements.txt /app/requirements.txt
RUN pip install "fastapi[standard]" && \
    pip install --no-cache-dir -r /app/requirements.txt

# Stage 3: Runtime Environment
FROM python:3.10-slim-bullseye AS runtime

WORKDIR /app

# Install runtime dependencies (including curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the build stage
COPY --from=build /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=build /usr/local/bin /usr/local/bin

# Copy application source code
COPY app /app/app

EXPOSE 1802
