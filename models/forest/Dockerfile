# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files and to buffer output
ENV PATH="/app:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and model artifact
COPY src ./src
COPY output/model.pkl ./output/model.pkl
COPY serve .

# Make the serve script executable
RUN chmod +x serve

# Expose port 8080
EXPOSE 8080

# Set the CMD
CMD ["serve"]
