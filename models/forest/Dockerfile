# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \ 
  tini \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model code
COPY src ./src

ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["python", "-m", "src.inference"]
CMD ["python", "/app/src/inference.py", "--model=/app/data/model.pkl"]
# CMD ["python, "src.inference"]
