#!/usr/bin/env python3
"""
Create German Culture Video with GIFs
"""

from create_pinterest_culture_video import create_culture_video_from_gifs

# German culture script
GERMAN_SCRIPT = """
German culture is rich with tradition and artistry.
From the Alpine dances to the haunting sounds of the accordion.
Traditional instruments like the zither and alphorn echo through the mountains.
Folk dances celebrate community and heritage.
Lederhosen and dirndls tell stories of generations past.
This is culture that endures through time.
"""

result = create_culture_video_from_gifs(
    gif_dir="/Users/tomi/Desktop/pinterest_gifs/german_culture",
    audio_path="narrations/tomi_zenyai_test.wav",
    script_text=GERMAN_SCRIPT.strip(),
    output_path="professional_videos/german_culture_gifs.mp4"
)

if result:
    print("✅ German culture GIF video created!")
else:
    print("❌ Failed")
