#!/usr/bin/env python3
"""
Create German Culture Video
"""

from create_cinematic_image_video import create_cinematic_video_from_images

# German culture script
GERMAN_SCRIPT = """
German culture is rich with tradition and artistry.
From the Alpine dances to the haunting sounds of the accordion.
Traditional instruments like the zither and alphorn echo through the mountains.
Folk dances celebrate community and heritage.
Lederhosen and dirndls tell stories of generations past.
This is culture that endures through time.
"""

result = create_cinematic_video_from_images(
    image_dir="/Users/tomi/Desktop/pinterest_images/german_culture_traditional_art_illustration",
    audio_path="narrations/tomi_zenyai_test.wav",
    script_text=GERMAN_SCRIPT.strip(),
    output_path="professional_videos/german_culture_video.mp4",
    seconds_per_image=3.0
)

if result:
    print("✅ German culture video created!")
else:
    print("❌ Failed")
