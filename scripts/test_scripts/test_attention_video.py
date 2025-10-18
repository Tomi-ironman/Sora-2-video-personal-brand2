#!/usr/bin/env python3
"""
Test script for generating attention-grabbing videos with fantasy cutaways.
Creates a short-form video optimized for maximum scroll-stopping impact.
"""

from veo3_generator import Veo3VideoGenerator
from fantasy_cutaways import FantasyCutawayGenerator, create_attention_timeline, ATTENTION_PRESETS
from pathlib import Path

def main():
    generator = Veo3VideoGenerator()
    cutaway_gen = FantasyCutawayGenerator()
    
    # Short, punchy concept for attention-grabbing content
    main_concept = """
    Audio storytelling creates instant emotional connections that bypass logic and go straight to the heart.
    """
    
    # Shorter, more impactful dialogue for short-form content
    dialogue = """
    Here's the secret about audio stories - they don't just tell you something, they make you FEEL it. 
    When you combine the right narrative with immersive sound design, you create an emotional experience 
    that connects with people on a deeper level than any other medium. That's the power of creative audio.
    """
    
    print("🎬 Generating attention-grabbing video with fantasy cutaways...")
    print("📸 Using multi-reference identity lock")
    print("🎨 Creating surreal, colorful B-roll sequences")
    print("⚡ Optimized for short-form, scroll-stopping content")
    print(f"📝 Concept: {main_concept[:80]}...")
    print(f"🗣️ Dialogue: {dialogue[:80]}...")
    
    # Step 1: Generate main talking video with identity lock
    print("\n🎯 Step 1: Generating main video with your exact appearance...")
    main_video_path = generator.generate_image_to_video(
        main_concept=main_concept,
        dialogue_text=dialogue,
        aspect_ratio="9:16"
    )
    
    if not main_video_path:
        print("❌ Failed to generate main video")
        return
    
    print(f"✅ Main video generated: {Path(main_video_path).name}")
    
    # Step 2: Generate fantasy cutaways
    print("\n🎨 Step 2: Generating fantasy cutaway sequences...")
    
    # Use "neon_magic" preset for maximum visual impact
    cutaway_presets = ATTENTION_PRESETS["neon_magic"]  # ["neon_lantern_alley", "sound_wave_ocean"]
    
    cutaway_paths = []
    for preset in cutaway_presets:
        print(f"🌟 Generating {preset}...")
        cutaway_path = cutaway_gen.generate_cutaway(preset, duration=1.5)
        if cutaway_path:
            cutaway_paths.append(cutaway_path)
            print(f"✅ Generated: {Path(cutaway_path).name}")
    
    if not cutaway_paths:
        print("⚠️  No cutaways generated, using main video only")
        return main_video_path
    
    # Step 3: Assemble attention-grabbing timeline
    print("\n⚡ Step 3: Assembling attention-grabbing timeline...")
    print("📱 Pattern: You(2.5s) → Fantasy(1.2s) → You(2.5s) → Fantasy(1.2s) → You(final)")
    
    output_dir = Path.home() / "Desktop" / "AI-video-Generation"
    output_path = output_dir / f"attention_grabbing_{Path(main_video_path).stem}.mp4"
    
    final_video = create_attention_timeline(
        main_video_path=str(main_video_path),
        cutaway_paths=cutaway_paths,
        output_path=str(output_path)
    )
    
    print(f"\n🎉 ATTENTION-GRABBING VIDEO COMPLETE!")
    print(f"📁 Location: {Path(final_video).name}")
    print(f"🎯 Features:")
    print(f"   ✅ Your exact face (multi-reference locked)")
    print(f"   ✅ Fantasy cutaways for visual impact")
    print(f"   ✅ Short-form optimized pacing")
    print(f"   ✅ 9:16 mobile format")
    print(f"   ✅ Scroll-stopping visual hooks")

if __name__ == "__main__":
    main()
