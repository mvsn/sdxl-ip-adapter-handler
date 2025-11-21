import base64
from io import BytesIO

import runpod
import torch
from PIL import Image
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from runpod.serverless import start

# -------------------------
# Global config
# -------------------------

pipe = None

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

# One consistent storyboard style for all panels
GLOBAL_STYLE_PROMPT = (
    "clean flat illustrative storyboard, modern product design style, soft colors, "
    "subtle lighting, minimal background clutter, business environment, "
    "average, relatable people, natural body types, realistic proportions, "
    "subtle facial expressions, no speech bubbles, no on-image text, no UI screenshots"
)

# Strong but generic negative prompt to keep panels clean
GLOBAL_NEGATIVE_PROMPT = (
    "blurry, distorted, disfigured, extra limbs, extra fingers, missing limbs, "
    "text, caption, subtitles, watermark, logo, words, extreme closeup, fisheye, "
    "overly muscular, caricature, exaggerated expression, horror, gore, low quality"
)


# -------------------------
# Helpers
# -------------------------

def _load_models():
    """Lazy-load SDXL + VAE on first request."""
    global pipe
    if pipe is not None:
        return

    print("[HANDLER] Loading SDXL base + VAE...")
    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=dtype,
    )

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        vae=vae,
        torch_dtype=dtype,
        variant="fp16" if dtype == torch.float16 else None,
        use_safetensors=True,
    )

    pipe.to(device)

    # Use memory-friendly settings; xformers is not guaranteed in serverless
    if device == "cuda":
        pipe.enable_attention_slicing()
    else:
        pipe.enable_sequential_cpu_offload()

    print(f"[HANDLER] Models loaded on device: {device}")


def _pil_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _build_prompt(panel_prompt: str,
                  character_prompt: str | None,
                  style_prompt: str | None) -> str:
    """
    Build a consistent storyboard prompt:

    panel_prompt      – what happens in this panel
    character_prompt  – how recurring characters should look (optional)
    style_prompt      – override GLOBAL_STYLE_PROMPT if desired (optional)
    """
    style = style_prompt.strip() if style_prompt else GLOBAL_STYLE_PROMPT

    parts = [panel_prompt.strip()]
    if character_prompt:
        parts.append(character_prompt.strip())
    parts.append(style)

    # Filter out any empty fragments and join into one sentence.
    return ". ".join([p for p in parts if p])


# -------------------------
# Core generation
# -------------------------

def generate_storyboard_image(input_data: dict) -> dict:
    """Generate a single storyboard frame with SDXL."""
    _load_models()

    # Panel-level description (required)
    panel_prompt = (
        input_data.get("panel_prompt")
        or input_data.get("prompt")
        or ""
    ).strip()

    if not panel_prompt:
        raise ValueError("Missing 'panel_prompt' or 'prompt' in input.")

    # Optional knobs for consistency & style
    character_prompt = input_data.get("character_prompt")  # e.g. “Jamal, mid-30s…”
    style_prompt = input_data.get("style_prompt")          # override global style if needed

    negative_prompt = input_data.get("negative_prompt", GLOBAL_NEGATIVE_PROMPT)

    width = int(input_data.get("width", 1024))
    height = int(input_data.get("height", 768))  # 4:3 works nicely for panels

    num_inference_steps = int(input_data.get("num_inference_steps", 28))
    guidance_scale = float(input_data.get("guidance_scale", 6.5))

    seed = input_data.get("seed")
    generator = None
    if seed is not None:
        generator = torch.Generator(device=device).manual_seed(int(seed))

    full_prompt = _build_prompt(panel_prompt, character_prompt, style_prompt)

    print("[HANDLER] Generating storyboard frame")
    print(f"[HANDLER] Prompt: {full_prompt}")
    print(f"[HANDLER] Seed: {seed}")

    result = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )

    image = result.images[0]
    image_b64 = _pil_to_base64(image)

    print("[HANDLER] Frame generated successfully")

    return {
        "image": image_b64,
        "prompt_used": full_prompt,
        "seed": seed,
    }


# -------------------------
# RunPod handler
# -------------------------

def handler(event):
    """
    RunPod serverless handler.

    Expects event of the form:
    {
      "input": {
        "panel_prompt": "A CX lead presenting results to her team",
        "character_prompt": "Jamal, mid-30s, brown skin, short curly hair, "
                            "average build, casual shirt and jeans",
        "style_prompt": "...",         # optional
        "seed": 1234,                  # optional
        "width": 1024,                 # optional
        "height": 768,                 # optional
        "num_inference_steps": 28,     # optional
        "guidance_scale": 6.5          # optional
      }
    }
    """
    try:
        input_data = event.get("input", {}) or {}
        return generate_storyboard_image(input_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


# Start RunPod serverless
start({"handler": handler})

