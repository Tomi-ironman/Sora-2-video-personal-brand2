#!/usr/bin/env python3
"""
Zenyai Podcast Creator Commercial - "The File Wave"
Authentic podcast scenario: Recording interrupted by file organization chaos
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Authentic podcast scenario with dramatic file wave metaphor
    prompt = """
Create a dramatic 8-second commercial in 9:16 vertical format showing an authentic podcast recording scenario that transforms into a visual metaphor of being overwhelmed by audio files. The video should immediately identify the target audience (podcasters) then show the exact moment file organization chaos strikes.

VISUAL STYLE: Starts realistic and authentic (real podcast setup), then becomes cinematic and dramatic for the file wave sequence. POV/selfie camera angle for authenticity. High contrast between calm recording and chaotic file wave.

TARGET AUDIENCE IDENTIFICATION: Opens with clear podcast recording setup so viewers immediately know "this is for podcasters"

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): AUTHENTIC PODCAST RECORDING - Immediate target identification:
- POV shot of podcaster looking directly at camera in authentic recording setup
- Real podcast environment: professional microphone, headphones, recording interface visible
- Warm, inviting podcast studio lighting with acoustic panels in background
- Podcaster speaking naturally to camera: "Hey everyone, welcome back to the show..."
- Authentic, conversational tone that every podcaster will recognize
- Clean, organized workspace showing a professional podcaster at work

Beat 2 (2-4s): THE TRIGGER MOMENT - The relatable interruption:
- Phone notification sound (text message ping)
- Podcaster's expression changes from confident to slightly concerned
- Podcaster checks phone while still wearing headphones
- Authentic reaction: "Oh, hold on everyone - my team just sent me some files I need to organize"
- Slight worry creeping into their voice
- Still in authentic podcast recording position, maintaining the POV angle

Beat 3 (4-6s): THE FILE WAVE - Dramatic visual metaphor:
- Sudden dramatic shift as a massive wave of audio files crashes into the podcast setup
- Files have realistic names: "Episode_47_RAW.wav", "Guest_Interview_FINAL_v3.mp4", "Show_Notes_Draft.docx", "Sponsor_Read_Take_5.wav"
- Podcaster gets swept away by the digital tsunami of files
- Dramatic lighting shift from warm studio to chaotic storm-like atmosphere
- Files swirling and overwhelming the previously organized podcast space
- Podcaster's expression of shock and being overwhelmed

Beat 4 (6-8s): THE WARNING & SOLUTION - Clean resolution:
- Cut to calm, organized podcast setup with professional lighting
- Calm, authoritative narrator voice over the clean scene
- Text overlay appears: "Don't let this happen to you."
- Clean, perfectly organized podcast environment with Zenyai interface visible on screen
- Final message: "Organize your audio with Zenyai. AI-native Asset Management."
- Zenyai logo appears with website: "Zenyai.io"

TECHNICAL DETAILS: 720x1280 vertical format. POV camera angle for authenticity in first half, then cinematic camera work for dramatic file wave. Realistic podcast studio environment with professional equipment. High-quality file rendering for the wave sequence. Audio should include authentic podcast recording ambiance, then dramatic wave sounds, then calm resolution.

EMOTIONAL JOURNEY: Confident professionalism → Mild concern → Overwhelming chaos → Calm resolution and empowerment. Every podcaster should think "That could be me" in the first 4 seconds.

AUTHENTICITY FACTORS: Real podcast equipment, authentic podcaster language, relatable scenario of team sending files, realistic file naming conventions that podcasters will recognize.

CALL TO ACTION: "Don't let this happen to you. Organize your audio with Zenyai."
"""

    print("🌊 Generating Podcast Creator Commercial - 'The File Wave'...")
    print("🎯 Target: Podcasters in authentic recording environment")
    print("🎬 Style: POV podcast recording → dramatic file wave → clean resolution")
    print("⚡ Core Concept: Team sends files → chaos ensues → Zenyai prevents this")
    print("💡 Hook: Immediate podcaster identification + relatable scenario")
    print("📊 Based on: Research showing file organization as #1 podcast pain point")
    print("🔥 Strategy: Authentic setup + dramatic metaphor + direct warning")
    
    # Generate the commercial
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Authentic 'File Wave' Commercial created!")
        print("🔥 Authentic Features:")
        print("   ✅ POV podcast recording setup - immediate target identification")
        print("   ✅ Relatable scenario: 'team just sent me files to organize'")
        print("   ✅ Authentic podcast environment with real equipment")
        print("   ✅ Dramatic file wave metaphor grounded in reality")
        print("   ✅ Realistic file names podcasters will recognize")
        print("   ✅ Emotional journey: Confidence → Concern → Chaos → Resolution")
        print("   ✅ Direct warning: 'Don't let this happen to you'")
        print("   ✅ Clear solution: 'Organize your audio with Zenyai'")
        print("   ✅ 8s, 9:16 format optimized for social media")
        print("")
        print("🎯 This concept perfectly combines:")
        print("   • Immediate target audience identification")
        print("   • Relatable, authentic scenario")
        print("   • Dramatic visual metaphor")
        print("   • Clear problem → solution messaging")
        print("")
        print("💡 Every podcaster will think: 'That could be me!'")
    else:
        print("❌ Failed to generate File Wave Commercial")

if __name__ == "__main__":
    main()
