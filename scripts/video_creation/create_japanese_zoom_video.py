#!/usr/bin/env python3
"""
Create Japanese Culture Video with HYPER-FAST HOOK + ZOOM EFFECT
- First 3 seconds: 10 clips at 0.3s each (HOOK - no zoom)
- Remaining 22 seconds: storytelling with ZOOM IN effect
"""

import subprocess
import os
from pathlib import Path

def create_video():
    """Create video with fast hook + zooming storytelling"""
    
    print("\n🎬 Creating Japanese Culture Video with HOOK + ZOOM\n")
    
    # Paths
    voice_file = "narrations/japanese_culture_voice.wav"
    images_dir = "pinterest_downloads/japanese_art/japanese_art_illustration_drawing_traditional_aesthetic_anime_style"
    output_file = "professional_videos/japanese_culture_zoom.mp4"
    temp_dir = Path("temp_clips")
    temp_dir.mkdir(exist_ok=True)
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))
    
    print(f"✅ Found {len(image_files)} artistic/drawn images")
    
    # Video structure
    hook_clips = 10
    story_clips = 10
    hook_duration = 0.3  # 300ms per clip
    story_duration = 2.2  # 2.2s per clip
    
    total_clips = hook_clips + story_clips
    
    if len(image_files) < total_clips:
        story_clips = len(image_files) - hook_clips
        total_clips = len(image_files)
    
    print(f"\n📊 Video Structure:")
    print(f"   🔥 HOOK (0-3s): {hook_clips} clips @ {hook_duration}s = HYPER FAST")
    print(f"   🎥 STORY (3-25s): {story_clips} clips @ {story_duration}s with ZOOM IN")
    
    # Step 1: Create HOOK clips (no zoom)
    print("\n🔥 Creating HOOK clips (fast, no zoom)...")
    hook_list = []
    for i in range(hook_clips):
        img = image_files[i]
        output_clip = temp_dir / f"hook_{i:03d}.mp4"
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(img),
            '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:v', 'libx264',
            '-t', str(hook_duration),
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            str(output_clip)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        hook_list.append(output_clip)
    
    # Step 2: Create STORY clips (with zoom in)
    print("\n🎥 Creating STORY clips (with cinematic zoom in)...")
    story_list = []
    for i in range(story_clips):
        img_idx = hook_clips + i
        if img_idx >= len(image_files):
            break
        img = image_files[img_idx]
        output_clip = temp_dir / f"story_{i:03d}.mp4"
        
        # Zoom from 1.0x to 1.15x over duration (15% zoom in)
        zoom_filter = f'zoompan=z=\'min(zoom+0.0005,1.15)\':d={int(story_duration * 30)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920'
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(img),
            '-vf', f'scale=1200:2150:force_original_aspect_ratio=increase,{zoom_filter}',
            '-c:v', 'libx264',
            '-t', str(story_duration),
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            str(output_clip)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        story_list.append(output_clip)
    
    # Step 3: Concatenate all clips
    print("\n🔗 Combining clips...")
    concat_file = 'concat_list.txt'
    with open(concat_file, 'w') as f:
        for clip in hook_list + story_list:
            f.write(f"file '{clip.absolute()}'\n")
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    # Concatenate video
    temp_video = "temp_video_no_audio.mp4"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        temp_video
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    
    # Add audio
    print("\n🎙️  Adding audio...")
    cmd = [
        'ffmpeg', '-y',
        '-i', temp_video,
        '-i', voice_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_file
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    
    # Clean up
    print("\n🧹 Cleaning up...")
    os.remove(concat_file)
    os.remove(temp_video)
    for clip in hook_list + story_list:
        clip.unlink()
    temp_dir.rmdir()
    
    print(f"\n✅ VIDEO CREATED WITH ZOOM EFFECT!")
    print(f"📁 {output_file}")
    print(f"\n🔥 HOOK: First 3s = LIGHTNING FAST (no zoom)")
    print(f"🎥 STORY: Next 22s = Cinematic ZOOM IN effect")
    print(f"🎨 STYLE: Drawn/artistic Japanese images")
    
    # Open the video
    subprocess.run(['open', output_file])
    
    return output_file

if __name__ == "__main__":
    create_video()
