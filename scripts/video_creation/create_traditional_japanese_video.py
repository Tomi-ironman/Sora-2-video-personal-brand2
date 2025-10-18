#!/usr/bin/env python3
"""
Create Traditional Japanese Culture Video
Research-based, authentic, beautiful
"""

import subprocess
import os
from pathlib import Path
import time

def create_video():
    """Create video using ffmpeg"""
    
    print("\n🎬 Creating Traditional Japanese Culture Video\n")
    
    # Paths
    voice_file = "narrations/japanese_traditional_voice.wav"
    images_dir = "pinterest_downloads/japanese_traditional/traditional_japanese_culture_cherry_blossom_temple_tea_ceremony"
    output_file = "professional_videos/japanese_culture_traditional.mp4"
    
    # Wait for voice
    print("⏳ Waiting for voice generation...")
    max_wait = 300  # 5 minutes
    waited = 0
    while not Path(voice_file).exists() and waited < max_wait:
        time.sleep(5)
        waited += 5
        if waited % 30 == 0:
            print(f"   Still waiting... ({waited}s)")
    
    if not Path(voice_file).exists():
        print("❌ Voice file not ready yet")
        return
    
    print("✅ Voice ready!")
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))[:12]
    
    if len(image_files) == 0:
        print("❌ No images found")
        return
    
    print(f"✅ Found {len(image_files)} traditional images")
    
    # Get audio duration
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
         '-of', 'default=noprint_wrappers=1:nokey=1', voice_file],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    clip_duration = duration / len(image_files)
    
    print(f"📊 Total duration: {duration:.1f}s")
    print(f"📊 Each image: {clip_duration:.1f}s")
    
    # Create input file list for ffmpeg
    with open('image_list_traditional.txt', 'w') as f:
        for img in image_files:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {clip_duration}\n")
        # Add last image again (ffmpeg quirk)
        f.write(f"file '{image_files[-1].absolute()}'\n")
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    # Create video with ffmpeg
    print("\n🎥 Creating video with traditional Japanese imagery...")
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'image_list_traditional.txt',
        '-i', voice_file,
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        '-r', '30',
        output_file
    ]
    
    subprocess.run(cmd, check=True)
    
    # Clean up
    os.remove('image_list_traditional.txt')
    
    print(f"\n✅ Traditional Japanese Culture Video Created!")
    print(f"📁 {output_file}")
    print("\n📝 SCRIPT (Research-Based):")
    print("   - AI can't take away Japanese culture")
    print("   - Cherry blossoms: 2-week bloom symbolizes fleeting beauty")
    print("   - Tea ceremony: 400+ years of mindfulness tradition")
    print("   - Wabi-sabi: Japanese aesthetic philosophy")
    print("   - Calligraphy: Discipline meets art")
    print("   - Timeless, human, irreplaceable")
    
    # Open the video
    subprocess.run(['open', output_file])
    
    return output_file

if __name__ == "__main__":
    create_video()
