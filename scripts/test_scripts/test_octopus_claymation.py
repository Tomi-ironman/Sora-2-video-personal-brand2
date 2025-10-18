#!/usr/bin/env python3
"""
Zenyai Claymation Ad: Purple Octopus TAG Campaign
8s stop-motion style with handcrafted textures and witty tone
"""

from sora2_direct_api import Sora2DirectAPI


def main():
    gen = Sora2DirectAPI()

    prompt = """
Create an 8-second Claymation-style advertisement in 9:16 vertical format. Stop-motion aesthetic similar to Wallace and Gromit meets Fantastic Mr. Fox - rich textures where you can see fingerprints in the clay, slightly jerky motion like real stop-motion, handcrafted and imaginative feel.

VISUAL STYLE: Cinematic but playful lighting with glowing purples, pinks, and orange highlights. Witty, chaotic, and colorful tone. World feels handcrafted, imaginative, and surreal. Camera has slight handheld jitter mimicking real stop-motion camera work.

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): Camera pans across a miniature Claymation city made of colorful clay buildings - purple, teal, and orange skyscrapers that wobble slightly like Play-Doh. Vibrant and alive with tiny clay cars rolling slowly, clay people bustling around. A faint rumble shakes the scene. Camera zooms out revealing a giant purple octopus rising from behind buildings - made of shiny clay with exaggerated textures and glossy reflections.

Beat 2 (2-4s): The purple octopus extends tentacles across the city. Each tentacle slaps the ground rhythmically in sync with "TAG" being heard as a beat. As tentacles strike, big bold Claymation letters pop up - "TAG", "TAG", "TAG" - each accompanied by bright color flashes (neon pink, electric blue, vibrant yellow). Camera shakes slightly with each tentacle hit for comedic energy.

Beat 3 (4-6s): Octopus grows larger, towering over city, wrapping tentacles around clay skyscrapers that squish like jelly instead of breaking. Buildings deform humorously. Octopus freezes mid-motion, turns massive expressive clay eyes toward camera, grins mischievously. Mouth moves in exaggerated Claymation lip sync: "Why aren't you tagging your audio?"

Beat 4 (6-8s): Octopus points one tentacle at camera, then flicks to reveal glowing clay sign floating in sky reading "Use Zenyai - AI-native Audio Asset Management. Tag smarter. Sync faster. Collaborate in the cloud." Camera zooms out showing octopus proudly sitting atop squishy city skyline now glowing in Zenyai brand purple. Octopus waves cheerfully with one tentacle and says with confident, witty tone: "Link in bio!"

TECHNICAL: 720x1280 vertical. Warm golden sunset tones transitioning to electric purples and pinks. Brand colors purple (#7D3FEF) dominant with pink and teal accents. Comedic "TAG!" beats, playful whooshes, squishy clay sounds. Deep yet funny voiceover for octopus. Witty, confident, slightly absurd but smart and memorable tone.
"""

    print("🎬 Generating Claymation Octopus Zenyai Ad (8s, 9:16)...")
    print("🐙 Style: Stop-motion clay animation")
    print("🎨 Colors: Purple brand dominant with pink/teal accents")
    print("🎯 Message: 'Why aren't you tagging your audio?' + 'Link in bio'")
    
    out = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    if out:
        print(f"✅ Saved: {out.name}\n📁 ~/Desktop/AI-video-Generation/")
        print("🎉 Claymation octopus TAG campaign complete!")
    else:
        print("❌ Generation failed. Can adjust clay textures, timing, or octopus personality.")


if __name__ == "__main__":
    main()
