#!/usr/bin/env python3
"""
Generate ZenyAI UGC B-roll video using Sora 2
8 seconds with 2-second frame segments, personable and realistic
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    generator = Sora2DirectAPI()
    
    # ZenyAI UGC B-roll prompt for Sora 2
    zenyai_ugc_prompt = """
    A dynamic 8-second UGC-style B-roll video showcasing ZenyAI, an innovative AI technology company.
    
    SEQUENCE BREAKDOWN (2-second segments):
    
    Segment 1 (0-2s): Close-up of hands typing on a modern laptop showing AI interface
    - Warm, natural lighting in a contemporary workspace
    - Coffee cup and notebook visible
    - Screen displays sleek AI dashboard with ZenyAI branding
    - Organic, purposeful typing movements
    
    Segment 2 (2-4s): Medium shot of diverse team members collaborating
    - Modern office environment with glass walls
    - People pointing at screens, discussing AI concepts
    - Whiteboard with technical diagrams in background
    - Authentic conversations and natural gestures
    
    Segment 3 (4-6s): Screen capture style showing AI content generation
    - ZenyAI platform creating content in real-time
    - Progress indicators and smooth interface animations
    - Text or visual content being generated
    - Satisfying creation process visualization
    
    Segment 4 (6-8s): Wide shot of team celebrating breakthrough moment
    - Genuine excitement and collaboration
    - High-fives and positive energy
    - Modern office with city skyline view
    - Golden hour lighting through floor-to-ceiling windows
    
    UGC STYLE ELEMENTS:
    - Authentic, documentary-style cinematography
    - Handheld camera feel with subtle natural movement
    - Warm, inviting color palette
    - Real human emotions and interactions
    - Professional but approachable atmosphere
    - Modern tech startup aesthetic
    
    BRAND INTEGRATION:
    - ZenyAI logo subtly visible on screens
    - Clean, modern design language
    - Innovation and collaboration themes
    - Human-centered AI development story
    
    TECHNICAL REQUIREMENTS:
    - 9:16 vertical format optimized for social media
    - Smooth transitions between segments
    - Consistent color grading throughout
    - High-quality, crisp visuals
    - Natural ambient sound design
    
    EMOTIONAL TONE:
    - Inspiring and motivational
    - Authentic and relatable
    - Confident innovation
    - Team-oriented collaboration
    - Future-forward technology focus
    """
    
    print("🎬 Creating ZenyAI UGC B-roll with Sora 2...")
    print("🏢 Company: ZenyAI - AI Technology Innovation")
    print("📱 Format: 9:16 vertical (720x1280)")
    print("⏱️ Duration: 8 seconds with 2s segments")
    print("🎯 Style: UGC, authentic, highly realistic")
    
    # Generate with Sora 2
    result = generator.generate_video(
        prompt=zenyai_ugc_prompt,
        seconds=8,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! ZenyAI UGC B-roll created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        print("🔥 Features:")
        print("   ✅ UGC-style authentic storytelling")
        print("   ✅ 2-second segment structure")
        print("   ✅ Tech startup aesthetic")
        print("   ✅ Team collaboration focus")
        print("   ✅ ZenyAI brand integration")
        print("   ✅ 9:16 social media format")
        print("   ✅ Natural, personable feel")
    else:
        print("❌ Failed to generate ZenyAI UGC video")

if __name__ == "__main__":
    main()
