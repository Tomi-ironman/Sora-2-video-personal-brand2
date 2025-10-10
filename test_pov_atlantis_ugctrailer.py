#!/usr/bin/env python3
"""
Zenyai POV UGC Trailer: ATLANTIS CHASE (hyper‑real, violent audio energy)
Fast 8s, 9:16. Selfie-style diver addressing camera while chased in Atlantis.
"""

from sora2_direct_api import Sora2DirectAPI


def main():
    gen = Sora2DirectAPI()

    prompt = """
Photoreal, cinematic underwater VFX in 9:16, 8 seconds, four 2‑second beats. Selfie POV via dive mask/helmet‑cam with micro‑bubbles, lens droplets, refractive distortion, caustics dancing on ruins. Handheld shake, auto‑exposure compensating for shafts of light. Aggressive underwater sound design: muffled low‑end rumbles, pressure groans, creature clicks, gear creaks, regulator breaths, debris pings.

Beat 1 (0‑2s): Selfie POV—diver bolts through bioluminescent ruins of Atlantis, rain‑like silt and luminous algae streak past. Distant leviathan silhouette hunting. The diver shouts to camera through regulator: 'If I cut out—listen!'

Beat 2 (2‑4s): Corners turn tight; columns whip by; micro‑debris pings the mask. Violent audio surge: sub‑booms, stone shear, creature echolocation. The diver: 'You don’t have time—make sound that holds when everything breaks.' On‑screen subtitle: 'Make sound that holds.'

Beat 3 (4‑6s): Quick stabilization—HUD‑like overlay shows minimal waveform/timeline motifs syncing to motion; silt pulses to bass. The diver: 'Prototype to polished—fast. Adaptive stems. Iterate under pressure.' Layers slam in: VO clarity, transient whooshes, granular lows, crystalline highs—motion‑matched to kicks and turns.

Beat 4 (6‑8s): Final sprint into a cathedral‑like vault; the leviathan breaches frame—massive, awe‑terrifying. Camera jolts; particles explode. The diver (urgent, darkly funny) looks right into lens: 'Link in bio.' Hard hit, tiny after‑ring, hold one beat on the diver’s eyes.

Technical: 720x1280 vertical. Hyper‑real textures: mask scratches, neoprene weave, ancient stone erosion, bioluminescent particulate. No flicker. Crisp subtitle readability. Smooth but urgent transitions. Violent yet cinematic mix with clean VO above chaos.
"""

    print("🎬 Generating POV 'Atlantis Chase' UGC‑style trailer (8s, 9:16)…")
    out = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    if out:
        print(f"✅ Saved: {out.name}\n📁 ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Generation failed. We can adjust intensity, debris, or captions and retry.")


if __name__ == "__main__":
    main()
