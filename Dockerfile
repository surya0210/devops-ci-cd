# Use Python 3.10.12 slim image as base
FROM python:3.10.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and templates
COPY app.py .
COPY templates/ templates/

# Expose the port the app runs on
EXPOSE 5001

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python3", "app.py"]
