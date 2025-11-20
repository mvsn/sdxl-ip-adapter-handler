# Quick Deployment Guide

## Prerequisites
- Docker installed locally
- DockerHub account (or other container registry)
- RunPod account with billing set up

## Deployment Steps

### 1. Build and Push Docker Image

```bash
# Navigate to handler directory
cd runpod-handler

# Build the image
docker build -t YOUR_DOCKERHUB_USERNAME/sdxl-ip-adapter:latest .

# Push to DockerHub
docker push YOUR_DOCKERHUB_USERNAME/sdxl-ip-adapter:latest
```

Replace `YOUR_DOCKERHUB_USERNAME` with your actual DockerHub username.

### 2. Deploy to RunPod Serverless

1. Visit https://www.runpod.io/console/serverless
2. Click **"New Endpoint"**
3. **Container Configuration:**
   - Container Image: `YOUR_DOCKERHUB_USERNAME/sdxl-ip-adapter:latest`
   - Container Disk: 10 GB (for models)
   
4. **GPU Selection:**
   - Recommended: **RTX 4090** (~$0.00069/sec)
   - Alternative: **RTX A6000** (more VRAM if needed)
   
5. **Endpoint Settings:**
   - Max Workers: 3-5
   - Execution Timeout: 60 seconds
   - Idle Timeout: 5 seconds
   - Flashboot: Enabled (faster cold starts)
   
6. Click **"Deploy"**

### 3. Get Endpoint ID

After deployment completes:
1. Copy the **Endpoint ID** (e.g., `abc123def456`)
2. This is the alphanumeric code in the endpoint URL

### 4. Update Replit Environment

In your Replit project:
1. Open **Secrets** (Tools → Secrets)
2. Update or create:
   - Key: `RUNPOD_ENDPOINT_ID`
   - Value: `YOUR_NEW_ENDPOINT_ID`
3. Keep `RUNPOD_API_KEY` as-is

### 5. Enable Brands for Stable Diffusion

Edit `lib/character-reference.ts`:

```typescript
const SD_ENABLED_BRANDS = [
  'Airbnb',        // Re-enable Airbnb
  'TestBrand',
  'YourBrand',     // Add your brands here
  // ...
]
```

### 6. Test the Integration

1. Restart your Replit app
2. Go to `/cfa` page
3. Analyze Airbnb feedback
4. Select **"Artistic"** style in settings
5. Generate storyboard
6. Check logs for `[STABLE-DIFFUSION]` messages

## Expected Behavior

### Success Indicators:
- ✅ Logs show: `[STABLE-DIFFUSION] Has output: true`
- ✅ Logs show: `[STABLE-DIFFUSION] Output.image exists: true`
- ✅ Storyboard panels render with consistent character
- ✅ Cost per image: ~$0.002-0.005

### If Issues Occur:

**No output from RunPod:**
- Check Docker image built correctly
- Verify GPU has 24GB VRAM
- Check RunPod logs in console

**Out of memory:**
- Reduce image dimensions in handler
- Use RTX A6000 instead of 4090

**Slow cold starts (>60s):**
- Enable Flashboot in endpoint settings
- Pre-download models in Dockerfile (uncomment lines)

## Cost Optimization

### Current Setup:
- **DALL-E 3**: $0.040/image
- **Stable Diffusion + RunPod**: ~$0.002-0.005/image
- **Savings**: 88-92%

### RunPod Pricing:
- RTX 4090: $0.00069/sec
- Typical generation: 3-8 seconds
- Cost per image: $0.002-0.006

### Tips to Reduce Costs:
1. Lower `num_inference_steps` to 20-25
2. Use smaller dimensions (896x1152 instead of 1024x1365)
3. Enable aggressive idle timeout
4. Use Flashboot to reduce cold start waste

## Troubleshooting

### Handler logs show model loading errors
```bash
# Pre-download models in Dockerfile
# Uncomment lines 18-21 in Dockerfile
docker build -t YOUR_USERNAME/sdxl-ip-adapter:latest .
docker push YOUR_USERNAME/sdxl-ip-adapter:latest
```

### Character consistency not working
- Check `ip_adapter_scale` is 0.7-0.8
- Verify reference image is clear headshot
- Ensure reference image is RGB format

### Deployment fails
- Check Docker image exists on DockerHub
- Verify RunPod billing is active
- Try deploying from RunPod template first

## Next Steps

Once deployed successfully:
1. Monitor RunPod usage in console
2. Adjust max workers based on traffic
3. Enable more brands in whitelist
4. Fine-tune `ip_adapter_scale` per brand

## Support

- RunPod Docs: https://docs.runpod.io/
- RunPod Discord: https://discord.gg/runpod
- Handler Issues: Check logs in RunPod console
