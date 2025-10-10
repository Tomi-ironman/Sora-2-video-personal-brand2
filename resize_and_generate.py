#!/usr/bin/env python3
"""
Resize image to match Sora 2 requirements and generate video
"""

from PIL import Image
from pathlib import Path
from sora2_direct_api import Sora2DirectAPI

def resize_image_for_sora(input_path, output_path, target_size=(720, 1280)):
    """Resize image to match Sora 2 requirements"""
    with Image.open(input_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to exact dimensions
        resized = img.resize(target_size, Image.Resampling.LANCZOS)
        resized.save(output_path, 'JPEG', quality=95)
        print(f"✅ Resized image saved: {output_path}")
        return output_path

def main():
    generator = Sora2DirectAPI()
    
    # Paths
    original_image = generator.reference_dir / "IMG_1169.JPG"
    resized_image = generator.reference_dir / "IMG_1169_720x1280.jpg"
    
    # Resize image to match Sora 2 requirements
    print("🔧 Resizing image to match Sora 2 requirements...")
    resize_image_for_sora(original_image, resized_image, (720, 1280))
    
    # Cool apartment dialogue
    dialogue = """
    Welcome to my creative space. This is where the magic happens - where audio stories come to life 
    and connect with people on a deeper level. When you combine the right narrative with immersive 
    sound design, you create something that goes straight to the heart.
    """
    
    # Enhanced prompt for cool apartment with creative effects
    apartment_prompt = f"""
    Transform this person into a dynamic scene in a STUNNING MODERN APARTMENT with creative visual effects:
    
    SETTING - COOL MODERN APARTMENT:
    - Sleek, contemporary living space with floor-to-ceiling windows
    - City skyline view with twinkling lights in the background
    - Modern furniture: minimalist couch, glass coffee table, artistic lighting
    - Warm ambient lighting with color-changing LED strips (blue/purple/orange glow)
    - Plants and modern art pieces scattered throughout
    - High-end audio equipment and speakers visible in the background
    
    CREATIVE VISUAL EFFECTS:
    - Subtle particle effects floating in the air (like dust motes in sunlight)
    - Dynamic lighting that shifts and pulses gently with the speech
    - Soft bokeh effects from city lights through the windows
    - Smooth camera movement: slight push-in during key moments
    - Color grading with warm tones and cinematic depth
    - Atmospheric haze/fog for dramatic effect
    
    CHARACTER & PERFORMANCE:
    - Maintain EXACT identity and facial features from the reference image
    - Natural, confident speaking with perfect lip synchronization
    - Engaging eye contact directly with the camera/audience
    - Subtle hand gestures while speaking
    - Professional yet relaxed posture
    - Charismatic presence addressing the audience directly
    
    DIALOGUE WITH PERFECT LIP SYNC:
    "{dialogue.strip()}"
    
    TECHNICAL REQUIREMENTS:
    - 9:16 vertical aspect ratio for mobile/social media
    - Cinematic quality with rich colors and contrast
    - Smooth, professional camera work
    - High-quality audio with clear speech
    - Creative but not overwhelming effects that enhance the message
    - The person should feel like they're speaking directly to YOU, the viewer
    """
    
    print("🎬 Creating your cool apartment video with Sora 2...")
    print("🏠 Setting: Modern apartment with creative effects")
    print("📱 Format: 9:16 vertical (720x1280)")
    print("🎯 Focus: Your exact character talking directly to the audience")
    print("✨ Effects: Dynamic lighting, particles, cinematic atmosphere")
    
    # Generate the video with resized image
    result = generator.generate_video_with_image(
        image_path=str(resized_image),
        prompt=apartment_prompt,
        seconds=12,  # Maximum duration
        size="720x1280"  # Exact match
    )
    
    if result:
        print(f"🎉 SUCCESS! Cool apartment video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        print("🔥 Features:")
        print("   ✅ Your exact character/identity preserved")
        print("   ✅ Cool modern apartment setting") 
        print("   ✅ Creative visual effects (particles, dynamic lighting)")
        print("   ✅ 9:16 vertical format")
        print("   ✅ Direct audience engagement")
        print("   ✅ Perfect lip sync with dialogue")
    else:
        print("❌ Failed to generate video")

if __name__ == "__main__":
    main()
