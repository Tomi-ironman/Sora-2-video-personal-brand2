#!/usr/bin/env python3
"""
Zenyai Podcast Creator Commercial - "Drowning in Files"
Dramatic visual metaphor based on research: Podcaster literally drowning in audio files
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Dramatic visual metaphor commercial based on podcast creator research
    prompt = """
Create a dramatic 8-second commercial in 9:16 vertical format using the visual metaphor of a podcaster overwhelmed in a chaotic storm of floating audio files. Cinematic style with high contrast between chaos and salvation.

VISUAL STYLE: Cinematic with dramatic lighting. Dark chaotic beginning transitioning to bright organized ending. Surreal but relatable visual metaphor showing file organization chaos as being caught in a whirlwind of files.

CORE METAPHOR: File organization problems = Caught in storm of files, Zenyai solution = Calm and organization

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): THE CHAOS - Epic establishing shot:
- Wide cinematic shot of a podcaster standing in the center of a chaotic whirlwind of floating audio files
- Thousands of files swirling around them like a tornado: "Episode_12_FINAL_v3.mp4", "guest_audio_broken.wav", "show_notes_draft_v7.docx", "thumbnail_maybe.png"
- Dramatic storm clouds overhead with lightning
- Files have realistic 3D appearance, spinning and floating in the air
- Podcaster desperately reaching for files that keep flying away
- Dark, desaturated color palette with ominous lighting

Beat 2 (2-4s): THE STORM INTENSIFIES - Chaos building:
- Close-up of podcaster's face, looking overwhelmed and frustrated
- More audio files begin falling from the stormy sky like rain
- Platform logos (Spotify, YouTube, Apple Podcasts, Google Podcasts) swirling in the storm like a tornado
- Files multiplying exponentially - the whirlwind becomes completely chaotic
- Dramatic sound design: thunder, wind, overwhelming chaos
- Podcaster's desperate voice: "Help... too many files... can't organize..."

Beat 3 (4-6s): THE RESCUE - Zenyai intervention:
- Sudden beam of bright, warm light cuts through the storm clouds
- Zenyai logo appears in the sky like a beacon, glowing with AI energy
- Calm, powerful AI voice speaks: "Zenyai - AI-native Audio Asset Management"
- The chaotic files begin organizing themselves into perfect, geometric formations
- Files transform from scattered debris into organized, floating platforms
- Storm clouds start clearing, water becomes calmer
- Podcaster looks up with hope and amazement

Beat 4 (6-8s): THE SALVATION - New reality:
- Podcaster now standing confidently on solid ground made of perfectly organized, glowing audio files
- Serene, bright environment with clean, organized file structures visible as architectural elements
- Files are labeled clearly and arranged in beautiful, logical patterns
- Peaceful, confident atmosphere with warm, golden lighting
- Podcaster stands with arms crossed, smiling confidently
- Text overlay in elegant, modern font: "Stop drowning. Start creating."
- Final logo: "Zenyai.io"

TECHNICAL DETAILS: 720x1280 vertical format. Cinematic camera movements with dramatic angles. Realistic water physics and file rendering. Epic orchestral undertones building to triumphant resolution. High-quality VFX for file organization transformation. Color grading from dark/desaturated to bright/warm.

EMOTIONAL JOURNEY: Overwhelming desperation → Escalating panic → Hope appears → Relief and empowerment. The visual metaphor should be immediately understood by anyone who's ever felt overwhelmed by digital file chaos.

MEMORABLE FACTOR: This commercial should be the "drowning in files" commercial that people remember and reference. The visual metaphor is striking enough to be shared and talked about while directly addressing the real pain points from our research.

CALL TO ACTION: "Stop drowning. Start creating. Zenyai.io"
"""

    print("🌊 Generating Podcast Creator Commercial - 'Drowning in Files'...")
    print("🎯 Target: Podcast creators overwhelmed by file organization")
    print("🎬 Style: Cinematic visual metaphor - literal drowning in audio files")
    print("⚡ Core Metaphor: File chaos = Drowning in ocean of files")
    print("💡 Solution: Zenyai as rescue beacon organizing files into solid ground")
    print("📊 Based on: Research showing file organization as #1 podcast pain point")
    print("🔥 Strategy: Memorable visual metaphor people will remember and share")
    
    # Generate the commercial
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Dramatic 'Drowning in Files' Commercial created!")
        print("🔥 Cinematic Features:")
        print("   ✅ Epic visual metaphor: Podcaster drowning in ocean of files")
        print("   ✅ Movie-trailer quality production value")
        print("   ✅ Research-based pain points transformed into drama")
        print("   ✅ Memorable imagery people will remember and share")
        print("   ✅ Emotional journey: Desperation → Panic → Hope → Empowerment")
        print("   ✅ Zenyai as heroic rescue beacon organizing chaos")
        print("   ✅ Striking contrast: Dark storm → Bright salvation")
        print("   ✅ Strong CTA: 'Stop drowning. Start creating.'")
        print("   ✅ 8s, 9:16 format optimized for social media")
        print("")
        print("🎯 This visual metaphor strategy will be MUCH more memorable than")
        print("   generic 'person at computer' commercials!")
        print("")
        print("💡 FUTURE STRATEGY NOTED: Research pain points → Transform into")
        print("   dramatic visual metaphors for maximum impact and shareability!")
    else:
        print("❌ Failed to generate Drowning in Files Commercial")

if __name__ == "__main__":
    main()
