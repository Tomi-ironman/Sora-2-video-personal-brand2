#!/usr/bin/env python3
"""
Zenyai Podcast Creator Commercial - "File Avalanche"
Dramatic visual metaphor: Podcaster buried under avalanche of audio files
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Dramatic visual metaphor commercial - File Avalanche
    prompt = """
Create a dramatic 8-second commercial in 9:16 vertical format using the visual metaphor of a podcaster being buried under an avalanche of audio files, then rescued by AI organization. Cinematic style with high contrast between chaos and salvation.

VISUAL STYLE: Cinematic with dramatic lighting. Dark chaotic beginning transitioning to bright organized ending. Surreal but relatable visual metaphor showing file organization chaos as an avalanche of files.

CORE METAPHOR: File organization problems = Buried under avalanche of files, Zenyai solution = AI rescue and perfect organization

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): THE AVALANCHE - Epic establishing shot:
- Wide cinematic shot of a podcaster standing on a mountain of audio files
- Thousands of files begin sliding down like an avalanche: "Episode_12_FINAL_v3.mp4", "guest_audio_broken.wav", "show_notes_draft_v7.docx"
- Dramatic mountain landscape with ominous storm clouds
- Files have realistic 3D appearance, tumbling and sliding
- Podcaster looking panicked as files cascade toward them
- Dark, desaturated color palette with dramatic shadows

Beat 2 (2-4s): BURIED IN CHAOS - Overwhelming situation:
- Close-up of podcaster's face showing panic and frustration
- Files completely covering the podcaster like snow in an avalanche
- Platform logos (Spotify, YouTube, Apple Podcasts) mixed in with the file avalanche
- More files continuing to fall from above
- Dramatic sound design: rumbling, crashing, overwhelming chaos
- Podcaster's muffled voice: "Help... too many files... can't find anything..."

Beat 3 (4-6s): THE AI RESCUE - Zenyai intervention:
- Sudden beam of bright, warm light cuts through the darkness
- Zenyai logo appears in the sky like a beacon, glowing with AI energy
- Calm, powerful AI voice speaks: "Zenyai - AI-native Audio Asset Management"
- The chaotic files begin organizing themselves, floating up and arranging in perfect order
- Files transform from scattered mess into organized, geometric patterns
- Light becomes brighter, chaos subsides
- Podcaster emerges from the files, looking amazed

Beat 4 (6-8s): PERFECT ORGANIZATION - New reality:
- Podcaster now standing confidently on perfectly organized platforms made of files
- Serene mountain landscape with clean, organized file structures as architectural elements
- Files are labeled clearly and arranged in beautiful, logical patterns
- Peaceful, confident atmosphere with warm, golden lighting
- Podcaster stands with arms crossed, smiling confidently
- Text overlay in elegant, modern font: "Rise above the chaos. Start creating."
- Final logo: "Zenyai.io"

TECHNICAL DETAILS: 720x1280 vertical format. Cinematic camera movements with dramatic angles. Realistic file physics and avalanche effects. Epic orchestral undertones building to triumphant resolution. High-quality VFX for file organization transformation. Color grading from dark/desaturated to bright/warm.

EMOTIONAL JOURNEY: Panic and overwhelm → Buried helplessness → Hope appears → Empowerment and confidence. The visual metaphor should be immediately understood by anyone who's ever felt buried under digital file chaos.

CALL TO ACTION: "Rise above the chaos. Start creating. Zenyai.io"
"""

    print("🏔️ Generating Podcast Creator Commercial - 'File Avalanche'...")
    print("🎯 Target: Podcast creators overwhelmed by file organization")
    print("🎬 Style: Cinematic visual metaphor - buried under avalanche of files")
    print("⚡ Core Metaphor: File chaos = Avalanche burial, Zenyai = AI rescue")
    print("💡 Solution: Zenyai organizing files into perfect mountain platforms")
    print("📊 Based on: Research showing file organization as #1 podcast pain point")
    print("🔥 Strategy: Memorable 'buried in files' metaphor people will remember")
    
    # Generate the commercial
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Dramatic 'File Avalanche' Commercial created!")
        print("🔥 Cinematic Features:")
        print("   ✅ Epic visual metaphor: Podcaster buried under file avalanche")
        print("   ✅ Movie-quality production with dramatic mountain setting")
        print("   ✅ Research-based pain points transformed into visual drama")
        print("   ✅ Memorable imagery: 'buried in files' concept")
        print("   ✅ Emotional journey: Panic → Helplessness → Hope → Empowerment")
        print("   ✅ Zenyai as heroic AI rescue organizing chaos")
        print("   ✅ Striking contrast: Dark avalanche → Bright organization")
        print("   ✅ Strong CTA: 'Rise above the chaos. Start creating.'")
        print("   ✅ 8s, 9:16 format optimized for social media")
        print("")
        print("🎯 This 'avalanche' metaphor is visually striking and safe!")
        print("💡 Future strategy: Research + Visual metaphors = Maximum impact!")
    else:
        print("❌ Failed to generate File Avalanche Commercial")

if __name__ == "__main__":
    main()
