#!/usr/bin/env python3
"""
Add ONE WORD AT A TIME captions - NO background, transparent, simple
"""

import subprocess
from pathlib import Path

def create_word_by_word_srt():
    """Create SRT with one word at a time from script"""
    
    # Read the actual script
    script_file = "scripts/japanese_culture_traditional.txt"
    with open(script_file, 'r') as f:
        script_text = f.read()
    
    # Remove empty lines and combine into one text
    script_text = ' '.join(line.strip() for line in script_text.split('\n') if line.strip())
    
    # Split into individual words
    words = script_text.split()
    
    print(f"📝 Script has {len(words)} words")
    
    # Get video duration
    input_video = "professional_videos/japanese_culture_zoom.mp4"
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
         '-of', 'default=noprint_wrappers=1:nokey=1', input_video],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    
    # Calculate time per word
    time_per_word = duration / len(words)
    
    print(f"⏱️  Video duration: {duration:.1f}s")
    print(f"⏱️  Time per word: {time_per_word:.2f}s")
    
    # Create SRT file with one word at a time
    srt_file = "word_by_word.srt"
    with open(srt_file, 'w', encoding='utf-8') as f:
        for i, word in enumerate(words, 1):
            start_time = (i - 1) * time_per_word
            end_time = i * time_per_word
            
            # Format as SRT timestamp
            start_h = int(start_time // 3600)
            start_m = int((start_time % 3600) // 60)
            start_s = int(start_time % 60)
            start_ms = int((start_time % 1) * 1000)
            
            end_h = int(end_time // 3600)
            end_m = int((end_time % 3600) // 60)
            end_s = int(end_time % 60)
            end_ms = int((end_time % 1) * 1000)
            
            f.write(f"{i}\n")
            f.write(f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> ")
            f.write(f"{end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}\n")
            f.write(f"{word}\n")
            f.write("\n")
    
    return srt_file

def add_captions():
    """Add clean word-by-word captions"""
    
    print("\n📝 Adding ONE WORD AT A TIME Captions\n")
    
    input_video = "professional_videos/japanese_culture_zoom.mp4"
    output_video = "professional_videos/japanese_culture_FINAL.mp4"
    
    # Create SRT file
    print("📄 Creating word-by-word subtitle file...")
    srt_file = create_word_by_word_srt()
    
    print("\n🎬 Rendering video with clean captions...")
    
    # Simple caption style: White text, black outline, NO BACKGROUND, centered
    subtitle_style = (
        "force_style='"
        "FontName=Arial Bold,"
        "FontSize=28,"
        "PrimaryColour=&H00FFFFFF,"  # White
        "OutlineColour=&H00000000,"  # Black outline
        "BorderStyle=1,"  # Outline only (NO BOX)
        "Outline=3,"  # Thick outline
        "Shadow=0,"  # No shadow
        "Alignment=2,"  # Bottom center
        "MarginV=100"  # 100px from bottom
        "'"
    )
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', f"subtitles={srt_file}:{subtitle_style}",
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-preset', 'medium',
        '-crf', '23',
        output_video
    ]
    
    subprocess.run(cmd, check=True)
    
    # Clean up
    Path(srt_file).unlink()
    
    print(f"\n✅ FINAL VIDEO WITH WORD-BY-WORD CAPTIONS!")
    print(f"📁 {output_video}")
    print(f"\n✨ Features:")
    print(f"   📝 ONE WORD at a time")
    print(f"   🚫 NO background (transparent)")
    print(f"   📖 From actual script")
    print(f"   🔥 HYPER-FAST hook")
    print(f"   🎥 Cinematic zoom effects")
    print(f"\n🎉 CLEAN & SIMPLE!")
    
    # Open the final video
    subprocess.run(['open', output_video])
    
    return output_video

if __name__ == "__main__":
    add_captions()
