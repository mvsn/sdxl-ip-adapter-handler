# Pre-Deployment Checklist

Before deploying, make sure you have:

## ✅ Prerequisites

- [ ] GitHub account
- [ ] RunPod account (https://www.runpod.io/)
- [ ] RunPod billing set up (add payment method)
- [ ] Git installed on your computer
- [ ] RUNPOD_API_KEY saved (from RunPod Settings → API Keys)

## ✅ Files Ready

All these files should be in your downloaded folder:

- [ ] handler.py
- [ ] requirements.txt
- [ ] Dockerfile
- [ ] README.md
- [ ] GITHUB_DEPLOY.md
- [ ] DEPLOY.md
- [ ] START_HERE.txt
- [ ] CHECKLIST.md (this file)
- [ ] .gitignore

## ✅ Deployment Steps

Follow these in order:

### 1. Create GitHub Repo
- [ ] Go to https://github.com/new
- [ ] Name: `sdxl-ip-adapter-handler`
- [ ] Visibility: Public
- [ ] Don't check "Add README"

### 2. Push to GitHub
```bash
cd /path/to/downloaded/runpod-handler
git init
git add .
git commit -m "Initial commit: SDXL IP-Adapter handler"
git remote add origin https://github.com/YOUR_USERNAME/sdxl-ip-adapter-handler.git
git push -u origin main
```

- [ ] Pushed successfully to GitHub
- [ ] Verify files appear on GitHub website

### 3. Deploy on RunPod
- [ ] Go to https://www.runpod.io/console/serverless
- [ ] Click "New Endpoint"
- [ ] Select "Build from GitHub" or enter repo URL
- [ ] Repository: `https://github.com/YOUR_USERNAME/sdxl-ip-adapter-handler`
- [ ] Branch: `main`
- [ ] GPU: RTX 4090 selected
- [ ] Max Workers: 3-5
- [ ] Timeout: 60 seconds
- [ ] Flashboot: Enabled
- [ ] Click "Deploy"

### 4. Wait for Build
- [ ] Build started (check build logs)
- [ ] Build completed (5-10 minutes)
- [ ] Endpoint status: "Active"

### 5. Get Endpoint Info
- [ ] Copy Endpoint ID (e.g., `abc123def456`)
- [ ] Save it somewhere safe

### 6. Update Replit

In your Replit project:

- [ ] Open Tools → Secrets
- [ ] Update `RUNPOD_ENDPOINT_ID` with new endpoint ID
- [ ] Verify `RUNPOD_API_KEY` is set
- [ ] Save secrets

### 7. Enable Stable Diffusion

Edit `lib/character-reference.ts`:

```typescript
const SD_ENABLED_BRANDS = [
  'Airbnb',  // ← Uncomment this line
  'TestBrand',
  // ...
]
```

- [ ] Uncommented 'Airbnb' in SD_ENABLED_BRANDS array
- [ ] Saved file

### 8. Test the Integration

- [ ] Restart Replit app
- [ ] Navigate to `/cfa` page
- [ ] Fetch Airbnb feedback
- [ ] Open Mapwalah Settings
- [ ] Select "Artistic" visual style
- [ ] Generate storyboard
- [ ] Check console logs for "[STABLE-DIFFUSION]" messages
- [ ] Verify storyboard images show character consistency

## ✅ Success Indicators

You'll know it's working when:

- [ ] Logs show: `[STABLE-DIFFUSION] Has output: true`
- [ ] Logs show: `[STABLE-DIFFUSION] Output.image exists: true`
- [ ] Storyboard panels render successfully
- [ ] Character faces look consistent across panels
- [ ] No "Unexpected RunPod response" errors

## 🐛 Troubleshooting

### Build fails on RunPod
- Check build logs in RunPod console
- Verify all files committed to GitHub
- Ensure Dockerfile is in repo root

### Endpoint times out
- Check RunPod endpoint is "Active"
- Verify timeout is 60+ seconds
- Check RunPod has available workers

### No output from handler
- Check RunPod logs for errors
- Verify GPU has 24GB VRAM
- Try reducing image dimensions

### Character consistency issues
- Verify reference image was created
- Check `ip_adapter_scale` is 0.7-0.8
- Ensure reference image is clear headshot

## 📊 Monitor Usage

After deployment:

- [ ] Check RunPod dashboard for usage
- [ ] Monitor cost per request (~$0.002-0.006)
- [ ] Compare to DALL-E 3 ($0.040)
- [ ] Verify 88-92% cost savings

## 🎯 Next Steps

Once everything works:

- [ ] Enable more brands in whitelist
- [ ] Fine-tune `ip_adapter_scale` per brand
- [ ] Adjust max workers based on traffic
- [ ] Monitor RunPod spend vs DALL-E

---

**Need Help?**
- RunPod Docs: https://docs.runpod.io/
- RunPod Discord: https://discord.gg/runpod
- Check GITHUB_DEPLOY.md for detailed instructions
