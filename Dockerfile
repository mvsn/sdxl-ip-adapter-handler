# Use RunPod's official CUDA base image
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (without IP-Adapter)
COPY requirements.txt .

# Install base dependencies first (excluding IP-Adapter)
RUN pip install --no-cache-dir runpod torch==2.1.0 torchvision==0.16.0 \
    diffusers==0.25.0 transformers==4.36.0 accelerate==0.25.0 \
    safetensors==0.4.1 pillow==10.1.0

# Install IP-Adapter dependencies
RUN echo "Installing IP-Adapter dependencies..." && \
    pip install --no-cache-dir opencv-python insightface

# Clone IP-Adapter to use as local module (more reliable than pip install)
RUN echo "Cloning IP-Adapter repository..." && \
    git clone https://github.com/tencent-ailab/IP-Adapter.git /app/IP-Adapter && \
    echo "IP-Adapter cloned successfully"

# Add IP-Adapter to Python path so it can be imported
ENV PYTHONPATH="/app/IP-Adapter:${PYTHONPATH}"

# Verify IP-Adapter can be imported
RUN echo "Testing IP-Adapter import..." && \
    python -c "import sys; print('Python path:', sys.path)" && \
    python -c "from ip_adapter import IPAdapterPlusXL; print('✓ IP-Adapter imported successfully!')"

# Copy handler code
COPY handler.py .

# Add startup logging
RUN echo "Dockerfile build complete - all dependencies installed"

# Set the handler
CMD ["python", "-u", "handler.py"]
