#!/usr/bin/env python3
"""
Text-to-video approach for apartment scene with your character description
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    generator = Sora2DirectAPI()
    
    # Text-to-video prompt describing your character and scene
    apartment_prompt = """
    A professional young Black man with short well-groomed hair and a confident smile speaking in a modern apartment. 
    He has warm brown eyes, defined cheekbones, and is wearing a casual button-down shirt. 
    
    Setting: Contemporary apartment with warm ambient lighting, modern furniture, and city lights visible through windows.
    
    The man speaks directly to the camera with natural gestures and engaging eye contact, saying:
    "Welcome to my creative space. This is where audio stories come to life and connect with people on a deeper level."
    
    Professional presentation style with natural lip synchronization and confident demeanor.
    Vertical 9:16 format optimized for mobile viewing.
    """
    
    print("🎬 Creating apartment video with text-to-video approach...")
    print("📱 Format: 9:16 vertical")
    print("🎯 Describing your character in the prompt")
    print("🏠 Modern apartment setting")
    
    # Generate text-to-video
    result = generator.generate_video(
        prompt=apartment_prompt,
        seconds=8,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Apartment video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        print("✅ Professional character description")
        print("✅ Modern apartment setting")
        print("✅ 9:16 vertical format")
        print("✅ Direct audience engagement")
    else:
        print("❌ Failed to generate video")

if __name__ == "__main__":
    main()
