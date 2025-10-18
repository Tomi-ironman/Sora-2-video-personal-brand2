#!/usr/bin/env python3
"""Generate 15-second version of The Endless Search video"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
base_url = 'https://api.openai.com/v1/videos'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

prompt = """Create a powerful 15-second commercial showing the emotional pain of audio professionals desperately searching for files in surreal, eye-catching locations. The video opens with a close-up of a young audio producer hunched over a laptop in an airplane seat at 35,000 feet. The cabin is dimly lit with overhead lights. Their face shows deep exhaustion and mounting frustration as they frantically click through endless folders: "Untitled_1.wav", "New Folder (47)", "kick_final_FINAL_v3.mp3", "Unknown Artist". Their eyes are bloodshot, dark circles visible. Other passengers sleep peacefully around them, highlighting their isolation and stress.

At seconds 3-5, the scene transitions with a dramatic visual effect - the producer is now searching in a different surreal location: inside a moving car at night, laptop balanced precariously, city lights blurring past the windows. They are still clicking desperately through the same chaotic folders. Their frustration intensifies - they rub their temples, grip their hair. The folder names keep repeating, creating a nightmarish loop: "New Folder (48)", "New Folder (49)", "samples_final_USE_THIS". The searching never ends. Coffee cups multiply around them. The emotional toll is visible.

At seconds 6-8, another surreal transition - the producer is now on a train, laptop open on the fold-down table, scenery rushing past the window. They are STILL searching through the same endless folders. Their face shows they are breaking down emotionally. Tears well up in their eyes. Their hands shake as they scroll. The folder chaos continues relentlessly. Time stamps on files show this has been going on for hours. The emotional pain is visceral and relatable. They look defeated.

At seconds 9-10, the scene shifts dramatically. The producer is back in their home studio, but something is different. A brilliant beam of light - clean white with purple and blue gradient (Zenyai brand colors) - illuminates their workspace. The chaos on screen begins to dissolve. The Zenyai interface appears, replacing the folder nightmare. The producer face transforms from despair to shock to hope. They sit up straighter.

At seconds 11-12, the transformation completes. The Zenyai interface displays perfectly organized audio files in an intuitive grid with smart AI tags, waveform previews, BPM, key, and genre automatically labeled. The producer searches for "kick drum 128 BPM" and finds it INSTANTLY - no folders, no scrolling, no chaos. Their face shows pure relief and joy. The exhaustion melts away. They smile genuinely for the first time in the video.

At seconds 13-14, the producer effortlessly drags the perfect file into their DAW timeline. Music starts playing. They lean back in their chair, finally relaxed. The creative flow has been restored. Bold text appears with time to read: "Stop Searching. Start Creating." followed by "Zenyai - AI Audio Organization".

The final second shows the Zenyai logo glowing softly as the producer creates music with confidence and joy. The lighting has completely shifted from cold stressed blues to warm productive golden tones. The emotional journey from desperation to relief is complete, powerful, and has time to breathe. Cinematic color grading throughout emphasizes the emotional transformation from chaos to clarity."""

print('🎬 REGENERATING: The Endless Search (15 SECONDS - Complete Story)')
print('=' * 70)
print(f'📝 Prompt: {len(prompt)} characters')
print('⏳ Sending to Sora 2 API...')
print()

data = {
    'model': 'sora-2',
    'prompt': prompt,
    'seconds': '12',
    'size': '720x1280'
}

response = requests.post(base_url, headers=headers, json=data)

if response.status_code == 200:
    job_data = response.json()
    print(f'✅ Video job created!')
    print(f'🎥 Video ID: {job_data.get("id")}')
    print(f'📊 Status: {job_data.get("status")}')
    print(f'⏳ Duration: 15 seconds (no more cut-offs!)')
    print(f'⏰ Estimated time: 2-4 minutes')
    
    with open('video_15sec_id.txt', 'w') as f:
        f.write(job_data.get('id'))
    
    print(f'\n💾 Video ID saved to: video_15sec_id.txt')
else:
    print(f'❌ Error: {response.status_code}')
    print(response.text)
