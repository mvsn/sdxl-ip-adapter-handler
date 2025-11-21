# Use RunPod's official CUDA base image
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install all dependencies from requirements.txt (matches successful build)
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler code
COPY handler.py .

# Set the handler
CMD ["python", "-u", "handler.py"]
