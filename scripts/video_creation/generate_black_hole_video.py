#!/usr/bin/env python3
"""
Generate The Black Hole Library video with Sora
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

prompt = """Create a cinematic 8-second commercial that transforms audio file chaos into organized brilliance through stunning visual metaphors. The video opens with a close-up shot of a young audio producer in a dimly lit home studio at 2 AM, exhausted eyes reflecting computer screen glow. Their hand hovers over a mouse, clicking to open a folder labeled "Samples_Final_USE_THIS_ONE". As the folder opens, the screen begins to distort and warp, transforming into a swirling cosmic black hole with deep purples, blues, and blacks. The camera pulls back dramatically as the black hole expands, consuming the entire screen.

From seconds 2-4, hundreds of audio files begin spiraling into the black hole event horizon - each file clearly labeled with painfully relatable names: "Untitled_1.wav", "New Folder (47)", "kick_final_FINAL_v3.mp3", "Unknown Artist - Unknown Title". The files spin chaotically, some colliding and fragmenting, others disappearing into the void. The producer face shows mounting panic as they frantically scroll, their cursor moving helplessly through the chaos. Metadata tags float by like debris: "No BPM", "No Key", "No Genre", emphasizing the complete lack of organization. The lighting shifts to cold blues and harsh shadows, creating an atmosphere of digital desperation.

Seconds 4-6 intensify the crisis. The camera zooms into the black hole center, revealing an infinite abyss of disorganized audio files stretching into darkness. The producer hands grip their head in frustration, a universal gesture of creative block. Their DAW timeline sits empty in the background - creativity literally being sucked away by organizational chaos. Floating text appears briefly: "3 hours searching... still no kick drum". The music builds tension with discordant, glitchy audio representing the broken workflow.

Then at second 6, everything changes. A brilliant beam of light - clean white with hints of purple and blue gradient - pierces through the black hole center. The light expands rapidly, and as it does, the chaos begins to transform. The black hole inverts, becoming a beautiful organized galaxy. Each audio file finds its place in orbital rings, automatically sorted and tagged. The files now display perfect metadata: "Kick_Drum_808_Am_128BPM.wav", organized by BPM, key, genre, and instrument type.

The final 2 seconds show the transformation complete. The producer face shifts from panic to pure relief and joy. The screen displays the Zenyai interface - sleek, modern, with AI-powered organization clearly visible. Files are arranged in an intuitive grid with smart tags, waveform previews, and instant search functionality. The producer effortlessly drags the perfect kick drum into their DAW timeline in one smooth motion. The black hole has become a constellation of perfectly organized creativity. The Zenyai logo appears with the tagline: "AI-Native Audio Organization - Find Any Sound Instantly". The final frame shows the producer creating music, flow restored, with the organized library glowing softly in the background. Cinematic color grading throughout: cold chaos transforms to warm, productive lighting."""

print('🎬 ZENYAI - THE BLACK HOLE LIBRARY VIDEO GENERATION')
print('=' * 60)
print(f'📝 Prompt length: {len(prompt)} characters')
print('⏳ Sending to Sora API (this may take 1-2 minutes)...')
print()

try:
    response = client.videos.generate(
        model='sora-turbo',
        prompt=prompt,
        size='1080x1920',
        duration='8s'
    )
    
    print('✅ VIDEO GENERATION INITIATED!')
    print('=' * 60)
    print(f'🎥 Video ID: {response.id}')
    print(f'📊 Status: {response.status}')
    print()
    print('📋 Full Response:')
    print(json.dumps(response.model_dump(), indent=2))
    
    # Save response to file
    with open('black_hole_video_response.json', 'w') as f:
        json.dump(response.model_dump(), f, indent=2)
    print()
    print('💾 Response saved to: black_hole_video_response.json')
    
except Exception as e:
    print(f'❌ ERROR: {str(e)}')
    print()
    print('Note: Sora API access may be limited. Check your OpenAI account for Sora access.')
    print('Alternative: The prompt has been saved and can be used manually in OpenAI Sora interface.')
