#!/usr/bin/env python3
"""
Create Japanese Culture Video NOW - No waiting
Uses traditional images, placeholder or silent audio
"""

import subprocess
import os
from pathlib import Path

def create_video():
    """Create video immediately"""
    
    print("\n🎬 Creating Traditional Japanese Culture Video NOW\n")
    
    # Paths
    images_dir = "pinterest_downloads/japanese_traditional/traditional_japanese_culture_cherry_blossom_temple_tea_ceremony"
    output_file = "professional_videos/japanese_culture_traditional.mp4"
    
    # Check for any existing voice file to use as placeholder
    voice_options = [
        "narrations/japanese_traditional_voice.wav",
        "narrations/japanese_culture_voice.wav",
        "narrations/test_with_your_voice.wav"
    ]
    
    voice_file = None
    for v in voice_options:
        if Path(v).exists():
            voice_file = v
            print(f"✅ Using existing voice: {v}")
            break
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))[:12]
    
    if len(image_files) == 0:
        print("❌ No images found")
        return
    
    print(f"✅ Found {len(image_files)} traditional images")
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    if voice_file:
        # Get audio duration
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', voice_file],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        clip_duration = duration / len(image_files)
        
        print(f"📊 Duration: {duration:.1f}s ({clip_duration:.1f}s per image)")
        
        # Create input file list for ffmpeg
        with open('image_list_trad.txt', 'w') as f:
            for img in image_files:
                f.write(f"file '{img.absolute()}'\n")
                f.write(f"duration {clip_duration}\n")
            f.write(f"file '{image_files[-1].absolute()}'\n")
        
        # Create video with voice
        print("\n🎥 Creating video with images + voice...")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'image_list_trad.txt',
            '-i', voice_file,
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-r', '30',
            output_file
        ]
    else:
        # Create silent video (25 seconds)
        duration = 25.0
        clip_duration = duration / len(image_files)
        
        print(f"📊 Creating 25s silent video")
        
        # Create input file list
        with open('image_list_trad.txt', 'w') as f:
            for img in image_files:
                f.write(f"file '{img.absolute()}'\n")
                f.write(f"duration {clip_duration}\n")
            f.write(f"file '{image_files[-1].absolute()}'\n")
        
        # Create silent video
        print("\n🎥 Creating silent video...")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'image_list_trad.txt',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            '-t', str(duration),
            output_file
        ]
    
    subprocess.run(cmd, check=True)
    
    # Clean up
    if Path('image_list_trad.txt').exists():
        os.remove('image_list_trad.txt')
    
    print(f"\n✅ VIDEO CREATED!")
    print(f"📁 {output_file}")
    print("\n📝 Traditional Japanese Culture Images:")
    print("   ✅ Cherry blossoms")
    print("   ✅ Temples")
    print("   ✅ Tea ceremony")
    print("   ✅ Traditional architecture")
    print("\n🎙️  Add your cloned voice later when ready!")
    
    # Open the video
    subprocess.run(['open', output_file])
    
    return output_file

if __name__ == "__main__":
    create_video()
