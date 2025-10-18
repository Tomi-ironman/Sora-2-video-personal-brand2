#!/usr/bin/env python3
"""
Zenyai Musical Note Café - Warm Cartoonish Aesthetic
A heartwarming story of finding home in Zenyai
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Comprehensive prompt inspired by the reference images
    prompt = """
Create an 8-second heartwarming animated video in 9:16 vertical format with a rough, painterly aesthetic that looks hand-painted with visible brushstrokes. The visual style should feel like traditional oil painting or watercolor - NOT 3D or overly polished. Think rough canvas texture, imperfect edges, and organic paint application.

VISUAL STYLE: Rough, textured painting style with visible brushstrokes and canvas texture. Colors should feel mixed on a palette - golden yellows, warm browns, muted oranges, and cream whites with subtle color variations and imperfections. Lighting should be dramatic and painterly, like natural light in a traditional painting. Avoid smooth gradients - use rough color transitions and visible paint texture. The animation should feel like a living painting, not a cartoon.

MAIN CHARACTER: A musical note painted with rough brushstrokes, not smooth or 3D. The note should have painterly texture and feel hand-drawn with visible paint application. Simple features but painted in an artistic, mature way - not childlike or overly cute.

SETTING: A rustic café interior painted with heavy brushstrokes and texture. Weathered wooden beams, rough plaster walls, aged furniture with paint texture visible. Think of an old European attic café with character and imperfections. Everything should look hand-painted with visible canvas texture and brushwork.

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): The musical note floats gently outside the café window, looking wistful and searching. Golden hour light bathes the scene. The note presses against the glass, peering inside at the warm, inviting interior. Soft piano melody begins. The note's expression shows longing and hope.

Beat 2 (2-4s): The café door opens with a gentle chime, and the musical note floats inside, eyes widening with wonder. The interior is bathed in warm amber light from lanterns and window light. Other musical elements (treble clefs, bass clefs) sit at tables like café patrons, creating a sense of community. The note looks around, amazed.

Beat 3 (4-6s): The musical note finds an empty spot at a cozy table by the window. As it settles in, it begins to glow softly with contentment. The note speaks directly to the camera with warmth and sincerity: "I needed a place to stay, and now I've found a home in Zenyai." The lighting becomes even warmer, more golden.

Beat 4 (6-8s): The note turns to face the camera fully, with a gentle, inviting smile. The café around it pulses with soft, musical energy. The note concludes with heartfelt warmth: "Join me today." As the note speaks, elegant painted text appears on screen in warm, handwritten style: "Zenyai - AI-native Audio Asset Management. Tag smarter. Sync faster. Collaborate in the cloud." The text should have the same rough, painterly texture as the rest of the scene, integrated naturally into the warm atmosphere.

TECHNICAL DETAILS: 720x1280 vertical format. Rough, painterly animation with visible brushstrokes throughout. Heavy texture overlay to simulate canvas. Imperfect edges and organic paint application. NO smooth 3D surfaces or clean digital lines. Everything should look hand-painted with traditional media. Muted, earthy color palette with paint mixing effects.

EMOTIONAL TONE: Mature, warm, and authentic - like a classic European painting. Avoid childish or overly cute aesthetics. The roughness should add character and sophistication, not messiness. Think of a cozy artist's studio or old bookshop atmosphere.
"""

    print("🎵 Generating Musical Note Café Story...")
    print("☕ Style: Warm cartoonish with golden hour lighting")
    print("🎨 Colors: Golden yellows, amber oranges, soft purples")
    print("💫 Message: 'I needed a place to stay, found home in Zenyai'")
    print("🏠 Tone: Nostalgic, warm, welcoming, emotionally resonant")
    
    # Generate the video
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Musical Note Café story created!")
        print("🔥 Features:")
        print("   ✅ Warm, authentic cartoonish aesthetic")
        print("   ✅ Musical note character with personality")
        print("   ✅ Cozy café setting with golden hour lighting")
        print("   ✅ Heartfelt message: 'Found home in Zenyai'")
        print("   ✅ Spoken CTA: 'Join me today'")
        print("   ✅ Nostalgic, emotionally resonant tone")
        print("   ✅ 8s, 9:16 format optimized for social media")
    else:
        print("❌ Failed to generate Musical Note Café video")

if __name__ == "__main__":
    main()
