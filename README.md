# RunPod SDXL + IP-Adapter Handler

This handler provides Stable Diffusion XL image generation with IP-Adapter support for character consistency across storyboard panels.

## Features

- **SDXL Base 1.0**: High-quality image generation
- **IP-Adapter Plus Face**: Maintains facial features and character appearance across panels
- **Optimized VAE**: Uses madebyollin's fp16 VAE fix for better quality
- **Character Consistency**: Reference image support with configurable strength

## Deployment to RunPod

### Option 1: Docker Container (Recommended)

1. **Build and push Docker image:**
   ```bash
   cd runpod-handler
   docker build -t your-dockerhub-username/sdxl-ip-adapter:latest .
   docker push your-dockerhub-username/sdxl-ip-adapter:latest
   ```

2. **Create RunPod Serverless Endpoint:**
   - Go to https://www.runpod.io/console/serverless
   - Click "New Endpoint"
   - Select your Docker image: `your-dockerhub-username/sdxl-ip-adapter:latest`
   - Configure GPU: RTX 4090 or A40 (24GB VRAM recommended)
   - Set timeout: 60 seconds
   - Set max workers: 3-5 (adjust based on traffic)
   - Click "Deploy"

3. **Copy Endpoint ID:**
   - After deployment, copy the endpoint ID (e.g., `5t10c0lkjq0x6c`)
   - Update your `RUNPOD_ENDPOINT_ID` environment variable in Replit

### Option 2: GitHub Deployment

1. **Push to GitHub:**
   ```bash
   cd runpod-handler
   git init
   git add .
   git commit -m "SDXL IP-Adapter handler"
   git remote add origin https://github.com/yourusername/sdxl-handler.git
   git push -u origin main
   ```

2. **Deploy from GitHub:**
   - In RunPod console, select "Deploy from GitHub"
   - Enter repository URL
   - RunPod will build and deploy automatically

## API Usage

### Input Parameters

```json
{
  "prompt": "A professional 30s woman checking her phone while standing near a modern apartment building entrance...",
  "reference_image": "base64_encoded_image_string",
  "ip_adapter_scale": 0.75,
  "negative_prompt": "ugly, distorted, bad anatomy...",
  "num_inference_steps": 30,
  "guidance_scale": 7.5,
  "width": 1024,
  "height": 1365,
  "seed": 42
}
```

### Parameters Explained

- `prompt` (required): Text description of the image to generate
- `reference_image` (optional): Base64-encoded character reference image
- `ip_adapter_scale` (default: 0.75): How strongly to maintain character consistency (0.0-1.0)
  - 0.5-0.6: Loose consistency, more variation
  - 0.7-0.8: Strong consistency (recommended)
  - 0.9-1.0: Very strict consistency
- `negative_prompt` (optional): What to avoid in the image
- `num_inference_steps` (default: 30): Quality vs speed (20-50)
- `guidance_scale` (default: 7.5): How closely to follow prompt (5-15)
- `width` (default: 1024): Image width in pixels
- `height` (default: 1365): Image height in pixels (4:3 = 1024x1365)
- `seed` (optional): Random seed for reproducibility

### Response Format

```json
{
  "image": "base64_encoded_output_image"
}
```

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test handler
python test_handler.py
```

## Performance

- **Cold Start**: ~30-60 seconds (first request loads models)
- **Warm Generation**: ~3-8 seconds per image
- **With IP-Adapter**: +1-2 seconds vs standard SDXL
- **VRAM Usage**: ~18GB for SDXL + IP-Adapter

## Cost Comparison

- **RunPod RTX 4090**: ~$0.002-0.005 per image (3-8 seconds @ ~$0.00069/sec)
- **DALL-E 3**: $0.040 per image
- **Savings**: 88-92% cost reduction

## Troubleshooting

### Handler returns no output

Check logs for:
- Model loading errors
- CUDA out of memory (use smaller dimensions or RTX A6000)
- Invalid base64 reference image

### Images don't match reference character

Try adjusting `ip_adapter_scale`:
- Too low (< 0.5): Character features not preserved
- Too high (> 0.9): Image may look artificial

### Slow generation

- Reduce `num_inference_steps` to 20-25
- Use smaller dimensions (896x1152)
- Increase max workers for better parallelization

## Model Credits

- **SDXL**: Stability AI
- **IP-Adapter**: Tencent AI Lab
- **VAE Fix**: madebyollin
