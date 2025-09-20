# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Git LFS
RUN apt-get update && apt-get install -y git-lfs && git-lfs install

# Copy app files
COPY app.py model1.h5 ./
COPY templates/ ./templates/
COPY dataset/sample/ ./dataset/sample/

# Expose ports
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]