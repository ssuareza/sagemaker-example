FROM python:3.10-slim

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

# Copy model files
COPY src ./src
COPY output ./output

RUN echo pwd

# Define environment variables
ENV PYTHONUNBUFFERED=TRUE

# Set up command
CMD ["python", "/app/src/inference.py"]
