# State-of-the-art Sentinel-X Container
# Base image with Python 3.11 and GIS dependencies
FROM python:3.11-slim

# Install system-level GIS and CV dependencies
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    libfiona-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Set environment variables for GIS
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the API port
EXPOSE 8000

# Command to run the Sentinel-X AI Engine
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
