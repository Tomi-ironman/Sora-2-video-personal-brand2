#!/usr/bin/env python3
"""
Create Japanese Culture Video - SIMPLE VERSION
Uses ffmpeg directly for speed
"""

import subprocess
import os
from pathlib import Path

def create_video():
    """Create video using ffmpeg"""
    
    print("\n🎬 Creating Japanese Culture Video (Simple Method)\n")
    
    # Paths
    voice_file = "narrations/japanese_culture_voice.wav"
    images_dir = "pinterest_downloads/japanese_culture/futuristic_japanese_cyberpunk_samurai_neon"
    output_file = "professional_videos/japanese_culture.mp4"
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))[:12]
    
    if len(image_files) == 0:
        print("❌ No images found")
        return
    
    print(f"✅ Found {len(image_files)} images")
    print(f"✅ Voice: {voice_file}")
    
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
    with open('image_list.txt', 'w') as f:
        for img in image_files:
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {clip_duration}\n")
        # Add last image again (ffmpeg quirk)
        f.write(f"file '{image_files[-1].absolute()}'\n")
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    # Create video with ffmpeg
    print("\n🎥 Creating video...")
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'image_list.txt',
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
    os.remove('image_list.txt')
    
    print(f"\n✅ Video created: {output_file}")
    
    # Open the video
    subprocess.run(['open', output_file])
    
    return output_file

if __name__ == "__main__":
    create_video()
