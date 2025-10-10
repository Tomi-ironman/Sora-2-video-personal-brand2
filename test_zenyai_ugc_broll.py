#!/usr/bin/env python3
"""
Generate UGC B-roll video about ZenyAI using Google Veo 3
8-10 seconds total with 2-second frame segments
Personable, highly realistic content showcasing the company
"""

from veo3_generator import Veo3VideoGenerator

def main():
    generator = Veo3VideoGenerator()
    
    # ZenyAI UGC B-roll concept - personable and realistic
    zenyai_concept = """
    Create a dynamic UGC-style B-roll video showcasing ZenyAI, an innovative AI company.
    
    VISUAL STORYTELLING SEQUENCE (8-10 seconds total):
    
    FRAME 1 (0-2s): Close-up of hands typing on a sleek laptop with ZenyAI branding visible on screen
    - Modern workspace with warm lighting
    - Coffee cup and notebook nearby
    - Screen shows AI interface or dashboard
    - Natural, organic hand movements
    
    FRAME 2 (2-4s): Medium shot of a diverse team collaborating in a modern office
    - People pointing at screens, discussing AI concepts
    - Whiteboards with diagrams and flowcharts
    - Natural conversations and gestures
    - Bright, inspiring workspace atmosphere
    
    FRAME 3 (4-6s): Close-up of AI-generated content being created in real-time
    - Screen capture style showing ZenyAI platform in action
    - Text or images being generated
    - Progress bars and interface elements
    - Smooth, satisfying creation process
    
    FRAME 4 (6-8s): Wide shot of the founder/team celebrating a breakthrough
    - Authentic excitement and joy
    - High-fives or fist bumps
    - Modern office with city view
    - Golden hour lighting through windows
    
    OPTIONAL FRAME 5 (8-10s): Product showcase montage
    - Quick cuts of ZenyAI features
    - Mobile and desktop interfaces
    - Happy users interacting with the platform
    - End with ZenyAI logo reveal
    """
    
    # Enhanced prompt for UGC authenticity
    ugc_prompt = f"""
    {zenyai_concept}
    
    UGC STYLE REQUIREMENTS:
    - Authentic, documentary-style cinematography
    - Natural lighting with warm, inviting tones
    - Handheld camera feel with subtle movement
    - Real people, genuine emotions and interactions
    - Modern tech startup aesthetic
    - Diverse, inclusive team representation
    - Professional but approachable atmosphere
    
    TECHNICAL SPECS:
    - 9:16 vertical format for social media
    - Each segment transitions smoothly (2-second intervals)
    - High-quality, crisp visuals
    - Consistent color grading throughout
    - Natural sound design and ambient audio
    - No overly polished or artificial elements
    
    BRAND ELEMENTS:
    - ZenyAI branding subtly integrated
    - Modern, clean design language
    - Innovation and collaboration themes
    - Future-forward technology focus
    - Human-centered AI development story
    
    EMOTIONAL TONE:
    - Inspiring and motivational
    - Authentic and relatable
    - Confident but humble
    - Innovative and forward-thinking
    - Team-oriented and collaborative
    """
    
    print("🎬 Creating ZenyAI UGC B-roll video with Veo 3...")
    print("🏢 Company: ZenyAI (https://www.zenyai.io/)")
    print("📱 Format: 9:16 vertical")
    print("⏱️ Duration: 8-10 seconds with 2s frame segments")
    print("🎯 Style: UGC, personable, highly realistic")
    
    # Generate the UGC B-roll video
    result = generator.generate_video(
        prompt=ugc_prompt,
        aspect_ratio="9:16",
        resolution="720p",
        use_character_consistency=False  # Focus on company/product, not specific character
    )
    
    if result:
        print(f"🎉 SUCCESS! ZenyAI UGC B-roll created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        print("🔥 Features:")
        print("   ✅ UGC-style authentic cinematography")
        print("   ✅ 2-second frame segments")
        print("   ✅ Modern tech startup aesthetic")
        print("   ✅ 9:16 vertical format")
        print("   ✅ ZenyAI branding integration")
        print("   ✅ Collaborative team storytelling")
    else:
        print("❌ Failed to generate ZenyAI UGC video")
        print("💡 If quota issues persist, we can try Sora 2 text-to-video approach")

if __name__ == "__main__":
    main()
