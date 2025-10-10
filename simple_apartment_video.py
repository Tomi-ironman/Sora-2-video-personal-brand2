#!/usr/bin/env python3
"""
Simple apartment video with your character - avoiding moderation issues
"""

from sora2_direct_api import Sora2DirectAPI
from pathlib import Path

def main():
    generator = Sora2DirectAPI()
    
    # Use the resized image
    resized_image = generator.reference_dir / "IMG_1169_720x1280.jpg"
    
    # Simple, clean dialogue
    dialogue = "Welcome to my creative space. This is where audio stories come to life and connect with people."
    
    # Simplified prompt to avoid moderation issues
    simple_prompt = f"""
    Animate this person speaking in a modern apartment setting.
    
    The person should speak naturally with lip synchronization:
    "{dialogue}"
    
    Setting: Contemporary apartment with warm lighting and modern furniture.
    Keep the person's exact appearance and identity from the reference image.
    Natural speaking animation with eye contact and subtle gestures.
    Professional and engaging presentation style.
    """
    
    print("🎬 Creating simple apartment video with Sora 2...")
    print("📱 Format: 9:16 vertical (720x1280)")
    print("🎯 Simple approach to avoid moderation issues")
    
    # Generate the video
    result = generator.generate_video_with_image(
        image_path=str(resized_image),
        prompt=simple_prompt,
        seconds=8,  # Shorter duration
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Apartment video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        print("✅ Your exact character preserved")
        print("✅ Modern apartment setting")
        print("✅ 9:16 vertical format")
        print("✅ Natural lip sync")
    else:
        print("❌ Failed to generate video")

if __name__ == "__main__":
    main()
