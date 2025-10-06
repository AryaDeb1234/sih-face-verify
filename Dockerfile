# Use a base image with prebuilt dlib + face_recognition to save memory
FROM cmusatyalab/face_recognition:latest

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt .

# Install Python dependencies (excluding face_recognition since it's already installed)
RUN pip install --no-cache-dir \
    --upgrade pip && \
    pip install --no-cache-dir \
    -r requirements.txt \
    --no-deps  # skip reinstalling face_recognition

# Copy the rest of your application
COPY . .

# Expose port (Render will map it automatically)
EXPOSE 3001

# Start the Flask app
CMD ["python", "app.py"]
