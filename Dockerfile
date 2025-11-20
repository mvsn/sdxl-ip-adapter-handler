# Use RunPod's official CUDA base image
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download models during build (optional but recommended for faster cold starts)
# Uncomment these lines to pre-download models:
# RUN python -c "from diffusers import StableDiffusionXLPipeline, AutoencoderKL; \
#     AutoencoderKL.from_pretrained('madebyollin/sdxl-vae-fp16-fix'); \
#     StableDiffusionXLPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-1.0', variant='fp16')"

# Copy handler code
COPY handler.py .

# Set the handler
CMD ["python", "-u", "handler.py"]
