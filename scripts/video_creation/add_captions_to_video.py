#!/usr/bin/env python3
"""
Add Beautiful Captions to Japanese Culture Video
"""

import subprocess
from pathlib import Path

def add_captions():
    """Add animated captions to the video"""
    
    print("\n📝 Adding Beautiful Captions\n")
    
    input_video = "professional_videos/japanese_culture_zoom.mp4"
    output_video = "professional_videos/japanese_culture_FINAL.mp4"
    
    # Get video duration
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
         '-of', 'default=noprint_wrappers=1:nokey=1', input_video],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    
    # Script with timing
    captions = [
        {"text": "One thing AI can't take away from us", "start": 0.0, "duration": 2.5},
        {"text": "is Japanese culture.", "start": 2.5, "duration": 2.0},
        {"text": "Cherry blossoms bloom", "start": 4.5, "duration": 1.8},
        {"text": "for just two weeks.", "start": 6.3, "duration": 1.7},
        {"text": "A reminder that beauty is fleeting.", "start": 8.0, "duration": 2.5},
        {"text": "Tea ceremony.", "start": 10.5, "duration": 1.0},
        {"text": "Four hundred years of mindfulness.", "start": 11.5, "duration": 2.0},
        {"text": "Wabi-sabi.", "start": 13.5, "duration": 1.0},
        {"text": "Finding perfection in imperfection.", "start": 14.5, "duration": 2.5},
        {"text": "This is culture.", "start": 17.0, "duration": 1.5},
        {"text": "Timeless. Human. Irreplaceable.", "start": 18.5, "duration": 3.0},
    ]
    
    print(f"📊 Video duration: {duration:.1f}s")
    print(f"📝 Adding {len(captions)} caption segments")
    
    # Create drawtext filter with all captions
    filters = []
    for i, cap in enumerate(captions):
        end_time = cap['start'] + cap['duration']
        
        # Modern caption style: Bold white text with black outline, centered, animated
        # Fade in (0.3s) and fade out (0.3s)
        fade_in = cap['start'] + 0.3
        fade_out = end_time - 0.3
        
        text_filter = (
            f"drawtext="
            f"text='{cap['text']}'"
            f":fontfile=/System/Library/Fonts/Helvetica.ttc"
            f":fontsize=70"
            f":fontcolor=white"
            f":borderw=4"
            f":bordercolor=black"
            f":x=(w-text_w)/2"
            f":y=h*0.75"  # 75% down the screen
            f":enable='between(t,{cap['start']},{end_time})'"
            f":alpha='if(lt(t,{fade_in}),(t-{cap['start']})/0.3,if(gt(t,{fade_out}),({end_time}-t)/0.3,1))'"
        )
        filters.append(text_filter)
    
    # Combine all filters
    vf_filter = ','.join(filters)
    
    # Apply captions to video
    print("\n🎬 Rendering video with captions...")
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', vf_filter,
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-preset', 'medium',
        '-crf', '23',
        output_video
    ]
    
    subprocess.run(cmd, check=True)
    
    print(f"\n✅ FINAL VIDEO WITH CAPTIONS READY!")
    print(f"📁 {output_video}")
    print(f"\n✨ Features:")
    print(f"   🔥 HYPER-FAST hook (0-3s)")
    print(f"   🎥 Cinematic zoom effects")
    print(f"   📝 Beautiful animated captions")
    print(f"   🎙️  Your cloned voice")
    print(f"   🎨 Drawn Japanese art style")
    
    # Open the final video
    subprocess.run(['open', output_video])
    
    return output_video

if __name__ == "__main__":
    add_captions()
