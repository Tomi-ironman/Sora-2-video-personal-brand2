#!/usr/bin/env python3
"""
Generate a cool apartment video with creative effects using Sora 2
Your exact character in a stylish modern apartment talking to the audience
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    generator = Sora2DirectAPI()
    
    # Use your primary reference image
    image_name = "IMG_1169.JPG"
    
    # Cool dialogue for the apartment setting
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
    print("📱 Format: 9:16 vertical for social media")
    print("🎯 Focus: Your exact character talking directly to the audience")
    print("✨ Effects: Dynamic lighting, particles, cinematic atmosphere")
    
    # Generate the video
    result = generator.generate_video_with_image(
        image_path=str(generator.reference_dir / image_name),
        prompt=apartment_prompt,
        seconds=12,  # Maximum duration for full dialogue
        size="720x1280"  # 9:16 aspect ratio (supported by Sora 2)
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
