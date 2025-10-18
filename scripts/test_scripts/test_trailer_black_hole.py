#!/usr/bin/env python3
"""
Zenyai Trailer: BLACK HOLE (fast-paced 8s, 9:16)
Four 2s beats. Film-quality stylized animation. Ends with brand lock.
"""

from sora2_direct_api import Sora2DirectAPI


def main():
    gen = Sora2DirectAPI()

    prompt = (
        "Stylized, film‑quality animated trailer in 9:16, 8 seconds, four 2‑second beats. "
        "Hand‑painted cinematic look, volumetric lighting, rich bokeh, particle atmospherics, "
        "physically‑based rendering feel, premium color grading, stable motion. "
        "High dynamic range with deep blacks and luminous highlights. Crisp yet organic edges. "
        "Readable overlay text. Synced cinematic audio and impactful sound design. "
        "\n\n"
        "Beat 1 (0‑2s): Extreme wide of a lone astronaut hovering at the rim of a colossal black hole. "
        "Event‑horizon lensing bends starlight into shimmering rings; slow stardust spirals. "
        "Camera: slow push‑in. On‑screen text: 'On the edge of everything…'"
        "\n\n"
        "Beat 2 (2‑4s): Closer—gloves extend; the suit HUD flickers with waveform and timeline motifs. "
        "Particles arc like musical notes stretching into gravity. Bass‑rich ambience swells. "
        "On‑screen text: 'You still need sound that holds.'"
        "\n\n"
        "Beat 3 (4‑6s): The astronaut taps a floating UI node—layers of sound snap into sync: "
        "clear voice, textural whooshes, sub‑harmonic rumbles, delicate high‑end crystals. "
        "Motion‑matched sound that follows the camera move. On‑screen text: 'Prototype to polished—fast.'"
        "\n\n"
        "Beat 4 (6‑8s): Calm within the chaos: a still pocket forms. The brand lockup appears tastefully "
        "on a soft purple→blue gradient: stylized black Zenyai symbol with subtle glow. "
        "On‑screen text: 'Zenyai — Create cinematic audio faster.' CTA (VO): 'For filmmakers and game devs. Try Zenyai today.'"
        "\n\n"
        "Technical: 720x1280 vertical, fast pacing, zero flicker, smooth transitions between beats, "
        "legible text, tasteful lens blooms, restrained film grain."
    )

    print("🎬 Generating 'Black Hole' Zenyai trailer (8s, 9:16)…")
    out = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    if out:
        print(f"✅ Saved: {out.name}\n📁 ~/Desktop/AI-video-Generation/")
    else:
        print("❌ Generation failed. We can iterate copy/visuals and retry.")


if __name__ == "__main__":
    main()
