"""
Local test script for the RunPod handler
"""
import base64
from handler import generate_image

def test_without_reference():
    """Test standard SDXL generation without IP-Adapter"""
    print("\n=== Test 1: Standard SDXL (no reference) ===")
    
    input_data = {
        "prompt": "A professional 30-year-old woman in business casual attire, standing near a modern apartment building, holding a smartphone, warm afternoon lighting, photorealistic style",
        "num_inference_steps": 25,
        "guidance_scale": 7.5,
        "width": 1024,
        "height": 1365,
    }
    
    result = generate_image(input_data)
    
    if "image" in result:
        # Save output
        with open("test_output_standard.png", "wb") as f:
            f.write(base64.b64decode(result["image"]))
        print("✓ Standard generation successful! Saved to test_output_standard.png")
    else:
        print(f"✗ Error: {result}")

def test_with_reference():
    """Test IP-Adapter generation with character reference"""
    print("\n=== Test 2: IP-Adapter (with reference) ===")
    
    # Load a test reference image
    try:
        with open("test_reference.jpg", "rb") as f:
            reference_base64 = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        print("✗ test_reference.jpg not found - skipping reference test")
        print("  Create a test_reference.jpg file with a character portrait to test IP-Adapter")
        return
    
    input_data = {
        "prompt": "A professional 30-year-old woman in business casual attire, standing near a modern apartment building, holding a smartphone, warm afternoon lighting, photorealistic style",
        "reference_image": reference_base64,
        "ip_adapter_scale": 0.75,
        "num_inference_steps": 25,
        "guidance_scale": 7.5,
        "width": 1024,
        "height": 1365,
    }
    
    result = generate_image(input_data)
    
    if "image" in result:
        # Save output
        with open("test_output_with_reference.png", "wb") as f:
            f.write(base64.b64decode(result["image"]))
        print("✓ IP-Adapter generation successful! Saved to test_output_with_reference.png")
    else:
        print(f"✗ Error: {result}")

if __name__ == "__main__":
    print("RunPod Handler Test Suite")
    print("=" * 50)
    
    # Run tests
    test_without_reference()
    test_with_reference()
    
    print("\n" + "=" * 50)
    print("Tests complete!")
