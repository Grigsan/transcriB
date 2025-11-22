# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install ffmpeg (required by whisper)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the port
EXPOSE 5003

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5003", "app:app"]
