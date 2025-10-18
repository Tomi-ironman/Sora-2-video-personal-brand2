#!/usr/bin/env python3
"""
Single attempt to generate ZenyAI UGC content with Gemini/Veo 3
No retry logic - just one clean attempt
"""

from veo3_generator import Veo3VideoGenerator

def main():
    # Create generator without retry logic
    generator = Veo3VideoGenerator()
    
    # ZenyAI UGC prompt for Gemini/Veo 3
    zenyai_ugc_prompt = """
    Create a dynamic UGC-style B-roll video showcasing ZenyAI, an innovative AI technology company.
    
    SEQUENCE (8-10 seconds with 2-second segments):
    
    Segment 1 (0-2s): Close-up of hands typing on laptop with ZenyAI interface
    - Modern workspace with warm lighting
    - Coffee cup and notebook visible
    - Screen shows AI dashboard with clean design
    - Natural, purposeful typing movements
    
    Segment 2 (2-4s): Team collaboration in modern office
    - Diverse team members discussing AI concepts
    - Pointing at screens and whiteboards
    - Glass walls and contemporary furniture
    - Authentic conversations and gestures
    
    Segment 3 (4-6s): AI content generation in real-time
    - ZenyAI platform creating content live
    - Progress bars and smooth animations
    - Text or visuals being generated
    - Satisfying creation process
    
    Segment 4 (6-8s): Team celebrating breakthrough
    - Genuine excitement and high-fives
    - Modern office with city skyline view
    - Golden hour lighting through windows
    - Positive energy and collaboration
    
    UGC STYLE:
    - Authentic, documentary cinematography
    - Handheld camera feel with natural movement
    - Warm, inviting color palette
    - Real human emotions and interactions
    - Professional but approachable atmosphere
    - Modern tech startup aesthetic
    
    BRAND ELEMENTS:
    - ZenyAI branding subtly integrated
    - Clean, modern design language
    - Innovation and collaboration themes
    - Human-centered AI development
    
    TECHNICAL:
    - 9:16 vertical format for social media
    - Smooth transitions between segments
    - High-quality, crisp visuals
    - Natural ambient sound
    - Consistent color grading
    """
    
    print("🎬 Single attempt: ZenyAI UGC with Gemini/Veo 3...")
    print("🏢 Company: ZenyAI")
    print("📱 Format: 9:16 vertical")
    print("⏱️ Duration: 8-10 seconds")
    print("🎯 Style: UGC, authentic, realistic")
    print("⚠️ No retries - single clean attempt")
    
    # Single attempt with Veo 3 - no retry logic
    try:
        result = generator.generate_video(
            prompt=zenyai_ugc_prompt,
            aspect_ratio="9:16",
            resolution="720p",
            use_character_consistency=False
        )
        
        if result:
            print(f"🎉 SUCCESS! ZenyAI UGC created: {result.name}")
            print("📁 Location: ~/Desktop/AI-video-Generation/")
            print("✅ Gemini/Veo 3 working properly")
        else:
            print("❌ Failed - Gemini/Veo 3 returned None")
            
    except Exception as e:
        print(f"❌ Gemini/Veo 3 Error: {str(e)}")
        print("💡 This confirms service issues - let's check status online")

if __name__ == "__main__":
    main()
