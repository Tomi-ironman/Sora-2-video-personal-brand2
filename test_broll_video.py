#!/usr/bin/env python3
"""
Test script for generating professional videos with B-roll and titles
"""

from veo3_generator import Veo3VideoGenerator

def main():
    generator = Veo3VideoGenerator()
    
    # Main concept for the video
    main_concept = """
    Professional storyteller and audio creator discussing the profound power of storytelling 
    through audio and sound design. Exploring how creative audio storytelling creates the 
    deepest human connections and transforms how we communicate with audiences in the digital age.
    """
    
    # Dialogue for the main presenter
    dialogue = """
    You know, there's something magical about storytelling through audio. When you combine 
    a compelling narrative with the right sounds, music, and audio design, you create something 
    that goes straight to the heart. I've spent years in this studio crafting audio experiences, 
    and I can tell you - there's no more powerful way to connect with people than through 
    an audio story. When someone puts on headphones and hears your story, complete with 
    immersive soundscapes and emotional music, you're not just telling them something - 
    you're making them feel it. That's the magic of creative audio storytelling. 
    It's intimate, it's personal, and it creates connections that last.
    """
    
    # Custom B-roll scenes focused on storytelling and audio connection
    b_roll_scenes = [
        "Close-up of hands crafting audio stories on mixing console with warm lighting",
        "Studio monitor speakers playing emotional music with visible sound wave patterns",
        "Computer screen showing audio storytelling software with narrative waveforms",
        "Professional microphone capturing intimate storytelling moments",
        "Headphones resting on desk suggesting personal audio connection",
        "Audio interface with warm glowing lights creating storytelling atmosphere",
        "Books and creative materials scattered around studio suggesting narrative inspiration",
        "Close-up of audio meters responding to emotional storytelling content"
    ]
    
    # Custom titles focused on storytelling and human connection
    titles = [
        "The Power of Audio Storytelling",
        "Creating Human Connections",
        "Stories That Touch Hearts",
        "The Magic of Sound & Narrative",
        "Intimate Audio Experiences"
    ]
    
    print("🎬 Generating image-to-video animation...")
    print("📸 Animating your reference photo with dialogue")
    print(f"📝 Concept: {main_concept[:100]}...")
    print(f"🗣️ Dialogue: {dialogue[:100]}...")
    print("🎯 NO titles or B-roll - just your photo coming to life")
    
    # Generate the image-to-video animation
    generator.generate_image_to_video(
        main_concept=main_concept,
        dialogue_text=dialogue,
        aspect_ratio="9:16"
    )

if __name__ == "__main__":
    main()
