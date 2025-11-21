# Use RunPod's official CUDA base image
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set HuggingFace cache directory to persist models in the image
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_DATASETS_CACHE=/app/models

# Copy model download script
COPY download_models.py .

# Pre-download all models during build (prevents runtime disk space errors)
# This adds ~11.8GB to the image but ensures workers never run out of space
RUN python download_models.py

# Copy handler code
COPY handler.py .

# Set the handler
CMD ["python", "-u", "handler.py"]
