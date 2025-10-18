#!/usr/bin/env python3
"""
Create Japanese Culture Video with Voice, Pinterest Images, and Captions
"""

import os
import subprocess
from pathlib import Path
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
import random

def create_japanese_culture_video():
    """Create the complete Japanese culture video"""
    
    print("\n🎬 Creating Japanese Culture Video\n")
    
    # Paths
    voice_file = "narrations/japanese_culture_voice.wav"
    images_dir = "pinterest_downloads/japanese_culture/futuristic_japanese_cyberpunk_samurai_neon"
    output_file = "professional_videos/japanese_culture_complete.mp4"
    
    # Wait for voice to be generated
    print("⏳ Waiting for voice generation...")
    import time
    max_wait = 300  # 5 minutes
    waited = 0
    while not Path(voice_file).exists() and waited < max_wait:
        time.sleep(5)
        waited += 5
        if waited % 30 == 0:
            print(f"   Still waiting... ({waited}s)")
    
    if not Path(voice_file).exists():
        print("❌ Voice file not ready yet")
        return None
    
    print("✅ Voice ready!")
    
    # Load voice to get duration
    voice_clip = AudioFileClip(voice_file)
    total_duration = voice_clip.duration
    print(f"📊 Voice duration: {total_duration:.1f}s")
    
    # Get all images
    image_files = list(Path(images_dir).glob("*.jpg")) + list(Path(images_dir).glob("*.png"))
    if len(image_files) == 0:
        print("❌ No images found")
        return None
    
    # Shuffle for variety
    random.shuffle(image_files)
    print(f"🖼️  Found {len(image_files)} images")
    
    # Calculate clips
    num_clips = min(len(image_files), 12)  # Use up to 12 images
    clip_duration = total_duration / num_clips
    
    print(f"📹 Creating {num_clips} clips ({clip_duration:.1f}s each)")
    
    # Create video clips from images
    video_clips = []
    for i, img_path in enumerate(image_files[:num_clips]):
        print(f"   Processing image {i+1}/{num_clips}...")
        
        # Load image
        img_clip = ImageClip(str(img_path))
        
        # Resize to 9:16 (1080x1920)
        img_clip = img_clip.resize(height=1920, method='bilinear')
        
        # Center crop to 1080 width
        if img_clip.w > 1080:
            x_center = img_clip.w / 2
            img_clip = img_clip.crop(
                x_center=x_center,
                width=1080,
                height=1920
            )
        
        # Set duration
        img_clip = img_clip.set_duration(clip_duration)
        
        # Add fade in/out
        img_clip = fadein(img_clip, 0.5)
        img_clip = fadeout(img_clip, 0.5)
        
        # Add subtle zoom effect
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            zoom = 1 + (t / clip_duration) * 0.1  # 10% zoom over duration
            return frame
        
        video_clips.append(img_clip)
    
    # Concatenate all clips
    print("🎬 Concatenating clips...")
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # Add voice
    print("🎙️  Adding voice...")
    final_video = final_video.set_audio(voice_clip)
    
    # Create output directory
    Path("professional_videos").mkdir(exist_ok=True)
    
    # Export
    print("💾 Exporting video...")
    final_video.write_videofile(
        output_file,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        preset='medium',
        threads=4
    )
    
    print(f"\n✅ Video created: {output_file}")
    
    # Clean up
    voice_clip.close()
    final_video.close()
    
    return output_file

def add_captions(video_file):
    """Add beautiful captions to the video"""
    
    print("\n📝 Adding captions...")
    
    script_lines = [
        "One thing they can't take away from us",
        "is our culture.",
        "",
        "Japanese culture.",
        "Where ancient honor meets tomorrow's dreams.",
        "",
        "The samurai's code.",
        "The tea ceremony's grace.",
        "The cherry blossoms that bloom",
        "for just one moment.",
        "",
        "But imagine this reimagined.",
        "Neon temples rising from digital gardens.",
        "Geishas dancing in holographic silk.",
        "Tradition breathing in a cyberpunk world.",
        "",
        "This is culture evolving.",
        "Past and future, hand in hand.",
        "",
        "The spirit of Japan,",
        "eternal and electric.",
        "",
        "One thing they can't take away from us",
        "is our culture."
    ]
    
    # Load video
    video = VideoFileClip(video_file)
    duration = video.duration
    
    # Calculate timing for each line
    time_per_line = duration / len([l for l in script_lines if l])  # Only count non-empty lines
    
    # Create caption clips
    caption_clips = []
    current_time = 0
    
    for line in script_lines:
        if not line:  # Skip empty lines but advance time
            current_time += time_per_line * 0.3
            continue
        
        # Create text clip
        txt_clip = TextClip(
            line,
            fontsize=70,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=3,
            method='caption',
            size=(900, None)
        )
        
        # Position and timing
        txt_clip = txt_clip.set_position(('center', 'center'))
        txt_clip = txt_clip.set_start(current_time)
        txt_clip = txt_clip.set_duration(time_per_line)
        
        # Add fade
        txt_clip = fadein(txt_clip, 0.3)
        txt_clip = fadeout(txt_clip, 0.3)
        
        caption_clips.append(txt_clip)
        current_time += time_per_line
    
    # Composite video with captions
    print("🎬 Compositing captions...")
    final = CompositeVideoClip([video] + caption_clips)
    
    # Output file
    output_file = video_file.replace('.mp4', '_WITH_CAPTIONS.mp4')
    
    # Export
    print("💾 Exporting final video...")
    final.write_videofile(
        output_file,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        preset='medium',
        threads=4
    )
    
    print(f"\n✅ Final video with captions: {output_file}")
    
    # Clean up
    video.close()
    final.close()
    
    return output_file

if __name__ == "__main__":
    # Create base video
    video_file = create_japanese_culture_video()
    
    if video_file:
        # Add captions
        final_file = add_captions(video_file)
        
        print(f"\n🎉 COMPLETE! Your Japanese culture video is ready!")
        print(f"📁 {final_file}")
        
        # Open the video
        subprocess.run(['open', final_file])
