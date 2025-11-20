import runpod
import torch
import base64
from io import BytesIO
from PIL import Image
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from ip_adapter import IPAdapterPlusXL

# Global variables to cache models
pipe = None
ip_adapter = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_models():
    """Load SDXL and IP-Adapter models (called once on cold start)"""
    global pipe, ip_adapter
    
    print("[HANDLER] Loading SDXL base model...")
    
    # Load VAE for better quality
    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=torch.float16
    )
    
    # Load SDXL base model
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        vae=vae,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    pipe.to(device)
    
    print("[HANDLER] Loading IP-Adapter Plus Face...")
    
    # Load IP-Adapter for facial consistency
    ip_adapter = IPAdapterPlusXL(
        pipe,
        image_encoder_path="laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
        ip_ckpt="h94/IP-Adapter/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors",
        device=device,
        num_tokens=16,
    )
    
    print("[HANDLER] Models loaded successfully!")

def base64_to_pil(base64_str):
    """Convert base64 string to PIL Image"""
    if base64_str.startswith('data:'):
        base64_str = base64_str.split(',')[1]
    
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    return image.convert('RGB')

def pil_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def generate_image(input_data):
    """Generate image with IP-Adapter for character consistency"""
    global pipe, ip_adapter
    
    # Load models on first request
    if pipe is None or ip_adapter is None:
        load_models()
    
    # Extract parameters
    prompt = input_data.get('prompt', '')
    negative_prompt = input_data.get('negative_prompt', 
        'deformed, distorted, disfigured, bad anatomy, bad proportions, '
        'extra limbs, cloned face, malformed limbs, missing arms, missing legs, '
        'extra arms, extra legs, fused fingers, too many fingers, long neck, '
        'ugly, duplicate, morbid, mutilated, poorly drawn hands, poorly drawn face, '
        'mutation, blurry, bad quality, worst quality, low quality'
    )
    
    reference_image_base64 = input_data.get('reference_image')
    ip_adapter_scale = float(input_data.get('ip_adapter_scale', 0.75))
    num_inference_steps = int(input_data.get('num_inference_steps', 30))
    guidance_scale = float(input_data.get('guidance_scale', 7.5))
    width = int(input_data.get('width', 1024))
    height = int(input_data.get('height', 1365))  # 4:3 aspect ratio
    seed = input_data.get('seed', None)
    
    print(f"[HANDLER] Generating image with IP-Adapter scale: {ip_adapter_scale}")
    
    # Set random seed if provided
    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(int(seed))
    
    # Generate with or without IP-Adapter
    if reference_image_base64:
        # Convert reference image from base64
        reference_image = base64_to_pil(reference_image_base64)
        print("[HANDLER] Using IP-Adapter with reference image")
        
        # Generate with IP-Adapter for character consistency
        output_image = ip_adapter.generate(
            pil_image=reference_image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            scale=ip_adapter_scale,
            num_samples=1,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            height=height,
            width=width,
            generator=generator,
        )[0]
    else:
        # Generate without IP-Adapter (standard SDXL)
        print("[HANDLER] Generating without IP-Adapter")
        output_image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            height=height,
            width=width,
            generator=generator,
        ).images[0]
    
    # Convert to base64
    output_base64 = pil_to_base64(output_image)
    
    print("[HANDLER] Image generated successfully")
    
    return {
        "image": output_base64
    }

def handler(event):
    """RunPod handler function"""
    try:
        input_data = event.get('input', {})
        output = generate_image(input_data)
        return output
    except Exception as e:
        print(f"[HANDLER] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
