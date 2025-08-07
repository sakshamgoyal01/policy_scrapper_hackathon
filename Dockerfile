# Use slim base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies (you likely only need these if you're using PyMuPDF)
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install only what's needed
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port (informational; Render still uses $PORT)
EXPOSE 8000
ENV PORT=8000
# Start app using dynamic port from Render
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
