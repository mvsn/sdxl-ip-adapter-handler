# GitHub Deployment (No Docker Required!)

This method deploys directly from GitHub without needing Docker on your computer.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `sdxl-ip-adapter-handler`)
3. Make it **Public** or **Private** (your choice)
4. Don't initialize with README (we have files already)

## Step 2: Push Files to GitHub

### From Replit Shell:

```bash
cd runpod-handler

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "SDXL IP-Adapter handler for RunPod"

# Connect to your GitHub repo (replace with your username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/sdxl-ip-adapter-handler.git

# Push to GitHub
git push -u origin main
```

**Note:** You'll need to authenticate with GitHub. Use a Personal Access Token if prompted.

## Step 3: Deploy from GitHub on RunPod

1. Go to https://www.runpod.io/console/serverless

2. Click **"New Endpoint"**

3. Under **"Select a Template"**, choose **"Build from GitHub"** or **"Custom"**

4. Enter your repository details:
   - Repository URL: `https://github.com/YOUR_USERNAME/sdxl-ip-adapter-handler`
   - Branch: `main`
   - Dockerfile path: `Dockerfile` (it's in the root of the handler folder)

5. Configure GPU:
   - Select **RTX 4090** (recommended)
   - Or **RTX A6000** if you need more VRAM

6. Endpoint Settings:
   - Max Workers: 3-5
   - Timeout: 60 seconds
   - Idle Timeout: 5 seconds
   - Enable Flashboot: Yes

7. Click **"Deploy"**

## Step 4: Wait for Build

- First deployment takes 5-10 minutes (building Docker image)
- RunPod will show build logs
- Wait until status shows "Active"

## Step 5: Copy Endpoint ID

Once deployed:
1. Click on your endpoint
2. Copy the **Endpoint ID** (looks like: `abc123def456`)
3. Save this - you'll need it for Replit

## Step 6: Update Replit

In your Replit project:
1. Go to **Tools → Secrets**
2. Update `RUNPOD_ENDPOINT_ID` with your new endpoint ID
3. Keep `RUNPOD_API_KEY` unchanged

## Step 7: Re-enable Stable Diffusion

In Replit, edit `lib/character-reference.ts`:

```typescript
const SD_ENABLED_BRANDS = [
  'Airbnb',        // ✅ Re-enable
  'TestBrand',
  'DemoCompany',
  // Add more brands here
]
```

## Step 8: Test!

1. Restart your Replit app
2. Go to `/cfa`
3. Analyze Airbnb feedback
4. Select **"Artistic"** style
5. Generate storyboard
6. Check for character consistency across panels!

## Troubleshooting

### GitHub Push Failed
- Make sure you have a GitHub Personal Access Token
- Generate one at: https://github.com/settings/tokens
- Use it as your password when pushing

### RunPod Build Failed
- Check build logs in RunPod console
- Verify Dockerfile is present
- Ensure requirements.txt has all dependencies

### Endpoint Shows Error
- Check endpoint logs in RunPod console
- Verify GPU has enough VRAM (24GB recommended)
- Try reducing image size in handler.py

## Cost

First deployment is free to build. Usage costs:
- RTX 4090: ~$0.00069/second
- Typical image: 3-8 seconds = $0.002-0.006
- 88-92% cheaper than DALL-E 3!

## Next Steps

Once working:
1. Monitor usage in RunPod dashboard
2. Adjust workers based on traffic
3. Enable more brands in whitelist
4. Fine-tune IP-Adapter scale per brand
