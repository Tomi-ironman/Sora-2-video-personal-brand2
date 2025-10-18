#!/usr/bin/env python3
"""
Test Sora 2 image-to-video with your reference image
Simple talking avatar generation
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    generator = Sora2DirectAPI()
    
    # Use your best reference image
    image_name = "IMG_1169.JPG"  # Your primary reference image
    
    # Simple dialogue for testing
    dialogue = "You know, there's something magical about storytelling through audio. When you combine the right narrative with immersive sound design, you create an experience people feel instantly."
    
    print("🎬 Testing Sora 2 image-to-video...")
    print(f"📸 Using image: {image_name}")
    print(f"🗣️ Dialogue: {dialogue[:50]}...")
    print("⚡ Simple approach: just animate the image with lip sync")
    
    # Generate the talking avatar video
    result = generator.generate_talking_avatar_from_image(
        image_name=image_name,
        dialogue=dialogue,
        seconds=8
    )
    
    if result:
        print(f"✅ Success! Video saved: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Failed to generate video")

if __name__ == "__main__":
    main()
