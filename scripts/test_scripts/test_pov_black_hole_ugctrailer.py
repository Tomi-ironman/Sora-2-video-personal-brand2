#!/usr/bin/env python3
"""
Zenyai POV UGC Trailer: BLACK HOLE (hyper‑real, violent audio impact)
Fast 8s, 9:16. Selfie-style astronaut addressing camera mid‑catastrophe.
"""

from sora2_direct_api import Sora2DirectAPI


def main():
    gen = Sora2DirectAPI()

    prompt = """
Photoreal, cinematic VFX look in 9:16, 8 seconds, four 2‑second beats. Selfie POV with a helmet‑cam reflection and subtle lens grime. Handheld shake, auto‑exposure, sensor noise in shadows, realistic motion blur, violent low‑frequency rumbles, metallic stress, air hiss, debris pings. Dynamic range with deep blacks and specular highlights from starlight. Readable on‑screen captions.

Beat 1 (0‑2s): Selfie POV of an astronaut spinning toward a massive black hole. Gravitational lensing warps the background; suit HUD flickers. The astronaut shouts over the roar. On‑screen text (subtitle style): 'Okay—listen—this is bad!'

Beat 2 (2‑4s): The spin stabilizes for a split second; micro‑debris lashes the visor with sharp pings. Violent audio design: bassy horizon roar + metallic creaks + clipped radio static. The astronaut talks DIRECTLY to the viewer: 'Before I stretch into spaghetti, hear me.' On‑screen text: 'I need you to know this.'

Beat 3 (4‑6s): Helmet HUD overlays a minimal UI with waveform/timeline motifs syncing to the chaos. The astronaut (urgent, to camera): 'If this is it… make every second sound like it matters.' Sound layers slam in: VO clarity, whooshes, sub‑harmonic rattle, crystalline highs—all motion‑matched. On‑screen text: 'Make sound that holds.'

Beat 4 (6‑8s): Final drop—camera yanks as gravity grips. Hard vignette; stars smear. The astronaut whispers: 'Before I stretch into spaghetti…' Then a hard audio hit and cut to black. On‑screen text: 'Link in bio.'

Technical: 720x1280 vertical. Hyper‑real textures, visor scratches, suit fabric weave. Aggressive but readable motion; no flicker; crisp captions; impactful transitions between beats; violent but cinematic audio mix with clean VO riding above the chaos.
"""

    print("🎬 Generating POV 'Black Hole' UGC‑style trailer (8s, 9:16)…")
    out = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    if out:
        print(f"✅ Saved: {out.name}\n📁 ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Generation failed. We can adjust intensity, shake, or captions and retry.")


if __name__ == "__main__":
    main()
