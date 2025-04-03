# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model files
COPY models/ ./models/

# Copy the source code
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8001

# Expose the port the app runs on
EXPOSE 8001

# Command to run the API
CMD ["python", "src/run_api.py"] 