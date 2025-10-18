#!/usr/bin/env python3
"""
Create Japanese Culture Video with HYPER-FAST HOOK
- First 3 seconds: 10 clips at 0.3s each (HOOK)
- Remaining 22 seconds: storytelling pace
"""

import subprocess
import os
from pathlib import Path

def create_video():
    """Create video with fast hook + storytelling"""
    
    print("\n🎬 Creating Japanese Culture Video with HYPER-FAST HOOK\n")
    
    # Paths
    voice_file = "narrations/japanese_culture_voice.wav"
    images_dir = "pinterest_downloads/japanese_art/japanese_art_illustration_drawing_traditional_aesthetic_anime_style"
    output_file = "professional_videos/japanese_culture_hook.mp4"
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))
    
    if len(image_files) < 20:
        print(f"⚠️  Only {len(image_files)} images, need at least 20")
    
    print(f"✅ Found {len(image_files)} artistic/drawn images")
    
    # Video structure
    # Hook: 0-3s = 10 clips at 0.3s each
    # Story: 3-25s = 22s / 10 clips = 2.2s each
    
    hook_clips = 10
    story_clips = 10
    hook_duration = 0.3  # 300ms per clip
    story_duration = 2.2  # 2.2s per clip
    
    total_clips = hook_clips + story_clips
    
    if len(image_files) < total_clips:
        print(f"⚠️  Using {len(image_files)} images (need {total_clips})")
        total_clips = len(image_files)
        story_clips = total_clips - hook_clips
    
    print(f"\n📊 Video Structure:")
    print(f"   🔥 HOOK (0-3s): {hook_clips} clips @ {hook_duration}s each = HYPER FAST")
    print(f"   📖 STORY (3-25s): {story_clips} clips @ {story_duration}s each")
    print(f"   ⏱️  Total: {3 + (story_clips * story_duration):.1f}s")
    
    # Create input file list for ffmpeg
    with open('image_list_hook.txt', 'w') as f:
        # HOOK: First 10 images at 0.3s each
        for i in range(hook_clips):
            img = image_files[i]
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {hook_duration}\n")
        
        # STORY: Next images at 2.2s each
        for i in range(hook_clips, hook_clips + story_clips):
            if i >= len(image_files):
                break
            img = image_files[i]
            f.write(f"file '{img.absolute()}'\n")
            f.write(f"duration {story_duration}\n")
        
        # Add last image again (ffmpeg quirk)
        f.write(f"file '{image_files[min(hook_clips + story_clips - 1, len(image_files) - 1)].absolute()}'\n")
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    # Create video with ffmpeg
    print("\n🎥 Creating video with HYPER-FAST HOOK...")
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'image_list_hook.txt',
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
    os.remove('image_list_hook.txt')
    
    print(f"\n✅ VIDEO CREATED WITH HYPER-FAST HOOK!")
    print(f"📁 {output_file}")
    print(f"\n🔥 HOOK: First 3 seconds = LIGHTNING FAST (0.3s per clip)")
    print(f"📖 STORY: Next 22 seconds = Beautiful storytelling")
    print(f"🎨 STYLE: Drawn/artistic Japanese images (NOT photos)")
    
    # Open the video
    subprocess.run(['open', output_file])
    
    return output_file

if __name__ == "__main__":
    create_video()
