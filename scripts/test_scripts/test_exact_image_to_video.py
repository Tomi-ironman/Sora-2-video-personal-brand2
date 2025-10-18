#!/usr/bin/env python3
"""
Generate a video by animating a SPECIFIC reference image exactly as-is,
preserving the background and composition. No B-roll, no environment rebuild.
"""
from pathlib import Path
from veo3_generator import Veo3VideoGenerator

def main():
    gen = Veo3VideoGenerator()

    # Choose the exact image to animate (must be in ./Reference Character/)
    image_name = "IMG_1169.JPG"  # change if you want to try a different one

    dialogue = (
        "You know, there's something magical about storytelling through audio. "
        "When you combine the right narrative with immersive sound design, you create "
        "an experience people feel instantly."
    )

    print("🎬 Generating exact image-to-video (no changes to the image, just mouth/eyes/head)...")
    out = gen.generate_talk_from_specific_image(image_name=image_name, dialogue_text=dialogue, aspect_ratio="9:16")
    if out:
        p = Path(out)
        print(f"✅ Done: {p.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Failed to generate exact image-to-video.")

if __name__ == "__main__":
    main()
