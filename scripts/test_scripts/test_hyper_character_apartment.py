#!/usr/bin/env python3
"""
Sora 2 text-to-video: 9:16, 4s clip, hyper-detailed character description in high-rise apartment.
Note: Sora API currently does not allow reproducing a real person's likeness via image input.
This uses a very specific text description to bias towards the desired look.
"""
from sora2_direct_api import Sora2DirectAPI

def main():
    generator = Sora2DirectAPI()

    # Sora 2 supports seconds in {4, 8, 12}. We'll use 4s per request.
    seconds = 4
    size = "720x1280"  # 9:16 portrait supported size

    # Hyper-detailed character description and scene (long-form to improve consistency)
    prompt = (
        "A single-take portrait shot of a young professional man speaking directly to camera in a luxurious high-rise apartment at dusk. "
        "He is seated, centered in the frame, with city skyline bokeh lights glowing through the floor-to-ceiling windows behind him. "
        "Camera is locked-off, portrait 9:16, subtle natural lens breathing only. "
        "Character appearance: a young adult male with warm medium-to-dark brown skin, balanced oval-to-square facial structure, prominent but smooth cheekbones, well-defined jawline with a slightly squared chin, proportionate forehead, defined temples, and clean, even skin texture with gentle highlights across the brow and cheek planes. "
        "Hair: short, tidy, modern fade-style sides with a natural, slightly curly top; hairline clean and symmetrical; no stray flyaways. "
        "Eyebrows: dark, moderately thick with a natural arch; eyes: warm, intelligent brown with a soft reflect from key light; eye shape slightly almond with a calm, focused gaze tracking the camera lens; eyelids show subtle, realistic blinking; gentle micro-movements convey attentive listening and confidence. "
        "Nose: straight bridge with subtle, natural curvature; nostrils proportionate and symmetrical; tip neither bulbous nor pinched. "
        "Mouth and lips: full but proportionate, well-contoured vermilion border; natural hydration sheen; corners rest neutrally and lift slightly during emphasis; lip-synchronization is precise with the spoken line. "
        "Teeth appear briefly during certain phonemes as natural, well-aligned, not exaggeratedly white. "
        "Ears proportionate, with realistic occlusion by hair at the temples; neck musculature subtly visible during micro-gestures; clavicle and shoulder line relaxed and confident. "
        "Wardrobe: contemporary professional-casual button-down in a neutral tone (mid-gray or soft charcoal), neat collar, no logos, matte fabric; a simple, tasteful necklace or accessory may be present but must not dominate. "
        "Lighting: cinematic three-point with practicals in background; warm key from camera-left at about 45 degrees, soft fill from camera-right maintaining gentle contrast ratio ~2:1, and a very soft edge/hair light to create separation. "
        "Color palette: warm skin tones balanced against cooler city blues and magentas in the skyline; white balance consistent; no color shifts across frames. "
        "Background: high-rise apartment interior—clean modern lines, minimalist furniture silhouettes; distant city skyline with blue/magenta dusk gradient; tasteful ambient practicals (lamp or LED strip) in soft orange; strong depth separation with shallow DOF; no jump cuts, no scene changes. "
        "Performance and movement: natural micro-expressions, subtle breathing, very slight head motion (no bobbing), minimal hand gestures near chest height if visible; direct eye contact with lens throughout; delivery confident, articulate, and energized without feeling staged. "
        "Audio and lip sync: synchronized dialogue; mouth shapes match phonemes accurately; consonants and vowels feel physically plausible; no audio drift. "
        "Voice direction (narration content): 'In a world full of noise, precision storytelling cuts through. When visuals and sound move together with intention, your message doesn’t just inform—it resonates.' "
        "Timing: keep the shot concise and focused within four seconds; no camera cuts; no zooms; micro dolly push of 1-2% maximum is acceptable. "
        "Technical: render as 9:16 portrait 720x1280; high detail but natural; no excessive sharpening; motion stable; no artifacts; lighting consistent across frames; keep framing waist-up or chest-up; maintain identity coherence from first to last frame; avoid uncanny valley. "
        "Style: grounded realism with cinematic polish; avoid cartoonish effects; no dramatic VFX; focus on the human presence and professional environment."
    )

    print("🎬 Generating 4s high-rise apartment clip (9:16, Sora 2)...")
    result = generator.generate_video(prompt=prompt, seconds=seconds, size=size)

    if result:
        print(f"✅ Saved: {result.name}\n📁 ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Generation failed. If rate-limited or moderated, we can soften phrasing and retry.")

if __name__ == "__main__":
    main()
