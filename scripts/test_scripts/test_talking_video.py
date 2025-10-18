#!/usr/bin/env python3
"""
Quick test script for generating a talking video with your character
"""

from veo3_generator import Veo3VideoGenerator

def main():
    generator = Veo3VideoGenerator()
    
    # Test dialogue about sound design (matching your expertise)
    dialogue = """
    Hey everyone! I'm excited to share how AI is revolutionizing sound design for video creators. 
    With tools like ZenyAI, you can now generate professional sound effects and music that perfectly 
    sync with your video content. No more spending hours searching for the right audio - 
    just describe what you need and let AI create it for you! This is the future of content creation.
    """
    
    print("🎬 Generating talking video with your character...")
    print(f"📝 Dialogue: {dialogue[:100]}...")
    
    # Generate the talking video
    generator.generate_talking_video(
        dialogue_text=dialogue,
        aspect_ratio="9:16"
    )

if __name__ == "__main__":
    main()
