# Fixed RunPod Deployment Guide

## What Was Fixed

The original deployment failed because the IP-Adapter library installation from git was failing during Docker build, causing all workers to crash before the handler could start.

### Key Changes:

1. **Dockerfile improvements**:
   - Install system dependencies (git) explicitly
   - Install base Python packages first
   - Clone and install IP-Adapter manually instead of using git+ pip syntax
   - Add verification step to ensure IP-Adapter imports correctly
   - Add enhanced logging to catch startup errors

2. **Requirements.txt cleanup**:
   - Removed problematic `ip-adapter @ git+...` line
   - Added missing dependencies (opencv-python, insightface)
   - IP-Adapter is now installed via Dockerfile git clone

3. **Handler logging**:
   - Added startup logging to see Python version, PyTorch version, CUDA status
   - Added error handling with traceback for debugging

---

## Deployment Steps

### 1. Commit and Push Changes to GitHub

```bash
cd runpod-handler
git add .
git commit -m "Fix IP-Adapter installation in Dockerfile"
git push origin main
```

### 2. Deploy to RunPod

1. Go to https://runpod.io/console/serverless
2. Find your endpoint: **sdxl-ip-adapter-handler** (ID: `6xuoh8w8w4fu0u`)
3. Click **"Edit"** or create a new endpoint
4. Configuration:
   - **Template Type**: GitHub Repository
   - **Repository**: `your-username/sdxl-ip-adapter-handler`
   - **Branch**: `main`
   - **Build Context**: `.` (root directory)
   - **Dockerfile Path**: `Dockerfile`
   - **Container Disk**: 10 GB minimum
   - **GPU**: RTX A5000 or better (16GB+ VRAM recommended)

5. Click **"Deploy"**

### 3. Wait for Build

- Build time: 10-15 minutes (downloads ~8GB of models)
- Watch the **Builds** tab for progress
- Look for: "Dockerfile build complete - all dependencies installed"

### 4. Verify Workers are Healthy

1. Go to **Workers** tab
2. Wait for workers to show **"Healthy"** status (green checkmark)
3. Check worker logs for startup messages:
   ```
   [STARTUP] Handler script starting...
   [STARTUP] Python version: 3.10.x
   [STARTUP] PyTorch version: 2.1.0
   [STARTUP] CUDA available: True
   [STARTUP] Using device: cuda
   [STARTUP] Starting RunPod serverless handler...
   ```

### 5. Test with Your App

1. In Mapwalah, go to CFA page
2. Settings: **Visual Style: Artistic**
3. Generate storyboard
4. Check logs for successful image generation (not IN_QUEUE timeout)

---

## Troubleshooting

### If Build Fails:

1. **Check Builds tab** for error messages
2. **Common issues**:
   - Out of memory: Increase container disk to 15-20GB
   - GitHub connection failed: Check repository is public
   - Timeout: RunPod may be experiencing high load, retry

### If Workers Stay Unhealthy:

1. **Click on unhealthy worker** to view logs
2. **Look for Python errors** during startup
3. **Check for**:
   - `ImportError: cannot import name 'IPAdapterPlusXL'` - IP-Adapter installation failed
   - `CUDA out of memory` - Need larger GPU
   - `ModuleNotFoundError` - Missing dependency

### If Jobs Stay IN_QUEUE:

- This means no healthy workers are available
- Go back to Workers tab and fix the health issue first
- Jobs will process automatically once a worker becomes healthy

---

## Testing Locally (Optional)

You can test the Docker build locally before deploying:

```bash
# Build the image
docker build -t sdxl-ip-adapter-test .

# Run the test script
docker run --rm sdxl-ip-adapter-test python test-handler.py

# If test passes, you're ready to deploy!
```

---

## Expected Performance

Once healthy:
- **Cold start**: 30-60 seconds (first request loads models)
- **Warm requests**: 8-12 seconds per image
- **Cost**: ~$0.002-0.005 per image (88-92% cheaper than DALL-E 3)
- **Character consistency**: ✓ IP-Adapter maintains facial features across panels

---

## Next Steps After Deployment

1. ✅ Verify workers are healthy
2. ✅ Test with Airbnb storyboard (Artistic style)
3. ✅ Compare quality vs DALL-E 3
4. ✅ Monitor costs and performance
5. 📊 Add more brands to SD_ENABLED_BRANDS whitelist if satisfied

Good luck! 🚀
