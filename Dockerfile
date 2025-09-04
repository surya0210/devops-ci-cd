# Use slim Python base
FROM python:3.10.12-slim

# No .pyc files, unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working dir
WORKDIR /app

# Copy deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy whole project (app/ package + app.py)
COPY . .

# Expose port
EXPOSE 5001

# Flask environment
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Run with Flask CLI
CMD ["flask", "run"]
