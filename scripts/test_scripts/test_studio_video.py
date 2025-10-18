#!/usr/bin/env python3
"""
Test script for generating professional studio videos with exact environment match
"""

from veo3_generator import Veo3VideoGenerator

def main():
    generator = Veo3VideoGenerator()
    
    # Test concept about sound design in your professional studio
    video_concept = """
    Professional sound designer explaining the future of AI-powered audio creation 
    in a modern audio production studio. Demonstrating expertise in sound design 
    and video production technology.
    """
    
    dialogue = """
    Welcome to my studio! Today I want to show you how AI is transforming sound design. 
    Behind me, you can see my professional audio setup with studio monitors and acoustic treatment. 
    This is where I create the sounds that bring videos to life. With AI tools like the ones we're building, 
    creators can now generate professional-quality audio that perfectly matches their vision.
    """
    
    print("🎬 Generating professional studio video...")
    print("🏢 Using exact environment match from your reference setup")
    print(f"📝 Concept: {video_concept[:100]}...")
    print(f"🗣️ Dialogue: {dialogue[:100]}...")
    
    # Generate the professional studio video
    generator.generate_professional_studio_video(
        video_concept=video_concept,
        dialogue_text=dialogue,
        aspect_ratio="9:16"
    )

if __name__ == "__main__":
    main()
