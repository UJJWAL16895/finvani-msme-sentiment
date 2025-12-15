FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if any (usually gcc/python3-dev might be needed for some packages, but start slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
# Copy and install Python dependencies
COPY requirements.txt .

# CRITICAL STEP: 
# 1. Remove 'torch' from requirements.txt inside the container so pip doesn't try to overwrite our CPU version with the huge GPU version.
RUN sed -i '/torch/d' requirements.txt

# 2. Install CPU-only torch explicitly (~150MB vs 2GB+)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 3. Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
