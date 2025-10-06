# Use a Python image that already has build tools
FROM python:3.11-slim

# Install system dependencies for dlib & face_recognition
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to cache layers
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port (Render will map it automatically)
EXPOSE 3001

# Start the Flask app
CMD ["python", "app.py"]
