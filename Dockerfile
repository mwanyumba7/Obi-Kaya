# Use the official lightweight Python image.
# You can change the version (e.g., 3.10-slim, 3.12-slim) based on your needs.
FROM python:3.11-slim

# Force Python to not buffer standard output and standard error.
# This ensures log messages are immediately sent to Cloud Logging.
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
# --no-cache-dir keeps the image size small by not caching the downloaded packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code
COPY . .

# Run the web service on container startup.
# We use Gunicorn to manage Uvicorn workers, bound to the dynamic $PORT injected by Cloud Run.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app
