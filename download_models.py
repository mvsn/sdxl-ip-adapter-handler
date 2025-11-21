#!/usr/bin/env python3
"""
Pre-download all models during Docker build to avoid runtime disk space issues.
This script downloads SDXL, VAE, CLIP Vision, and IP-Adapter models to cache.
"""

import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from transformers import CLIPVisionModelWithProjection
from huggingface_hub import hf_hub_download
import os

print("=" * 80)
print("Starting model download (this will take 10-15 minutes)...")
print("=" * 80)

# Set cache directory
cache_dir = os.environ.get('HF_HOME', '/root/.cache/huggingface')
print(f"Cache directory: {cache_dir}")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 1. Download VAE (smaller, ~335MB)
print("\n[1/4] Downloading SDXL VAE...")
vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix",
    torch_dtype=torch.float16,
    cache_dir=cache_dir
)
print("✓ VAE downloaded")

# 2. Download SDXL base model (~6.9GB)
print("\n[2/4] Downloading SDXL base model (this is large, ~6.9GB)...")
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
    cache_dir=cache_dir
)
print("✓ SDXL base model downloaded")

# 3. Download CLIP Vision encoder (~3.94GB - the one causing disk space issues)
print("\n[3/4] Downloading CLIP Vision encoder (large, ~3.94GB)...")
clip_model = CLIPVisionModelWithProjection.from_pretrained(
    "laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
    torch_dtype=torch.float16,
    cache_dir=cache_dir
)
print("✓ CLIP Vision encoder downloaded")

# 4. Download IP-Adapter weights (~680MB)
print("\n[4/4] Downloading IP-Adapter weights...")
ip_adapter_path = hf_hub_download(
    repo_id="h94/IP-Adapter",
    filename="sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors",
    cache_dir=cache_dir
)
print(f"✓ IP-Adapter weights downloaded to: {ip_adapter_path}")

print("\n" + "=" * 80)
print("All models downloaded successfully!")
print("Total downloaded: ~11.8GB")
print("=" * 80)
