FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 3001
# CMD ["python", "app.py"]
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --timeout 600 app:app"]


