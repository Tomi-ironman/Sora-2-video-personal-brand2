#!/usr/bin/env python3
"""
Generate Cultural Voices Videos ONE BY ONE using the exact same method that worked before
"""

from sora2_direct_api import Sora2DirectAPI

def generate_icelandic_rimur():
    """Generate Icelandic Rímur video - 12 seconds"""
    generator = Sora2DirectAPI()
    
    prompt = """Breathtaking cinematic 12-second video of Icelandic Rímur vocal tradition. Epic Icelandic landscape at golden hour - dramatic black volcanic rocks, steaming geysers, Northern Lights dancing across star-filled sky, ancient Viking runestones, moss-covered lava fields, glacial ice formations reflecting aurora colors. 

AUDIO: Deep resonant male voice performing traditional Rímur chanting - ancient storytelling style with haunting melodic phrases. Cinematic orchestral score with ethereal strings and Nordic instruments. Atmospheric sound design: howling Arctic winds, distant echoing vocals, crackling geothermal activity, mystical ambient drones. Epic movie-quality audio mixing with spatial depth and reverb.

VISUALS: Cinematic shots, slow camera movements across otherworldly terrain, ethereal lighting. 4K cinematic quality, film-like color grading. Movie-level production value."""
    
    print("🎬 Creating Icelandic Rímur video with Sora 2...")
    print("🇮🇸 Culture: Icelandic Rímur - Ancient Storytelling Chants")
    print("📱 Format: 9:16 mobile (720x1280)")
    print("⏱️ Duration: 12 seconds")
    print("🎯 Style: Highly cinematic with Northern Lights")
    
    # Generate with Sora 2 using the exact same method that worked before
    result = generator.generate_video(
        prompt=prompt,
        seconds=12,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Icelandic Rímur video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        return result
    else:
        print("❌ Failed to generate Icelandic Rímur video")
        return None

def generate_norwegian_joik():
    """Generate Norwegian Joik video - 12 seconds"""
    generator = Sora2DirectAPI()
    
    prompt = """Mystical cinematic 12-second video of Norwegian Sami Joik tradition. Arctic tundra under brilliant Northern Lights, traditional Sami lavvu tent with warm firelight, reindeer silhouettes against aurora, snow-covered mountains, person in colorful traditional Sami clothing (gákti) with ancient frame drums.

AUDIO: Authentic Sami joik throat singing - rhythmic spiritual chanting with harmonic overtones. Traditional frame drum rhythms building intensity. Cinematic score with Nordic folk instruments, ethereal choir, and mystical soundscapes. Atmospheric sound design: Arctic wind through snow, crackling campfire, distant reindeer calls, aurora borealis sonic textures. Epic movie-quality audio with immersive spatial mixing.

VISUALS: Mystical atmosphere, aurora reflections on snow, intimate cultural moments. 4K cinematic quality, ethereal lighting. Movie-level production value."""
    
    print("🎬 Creating Norwegian Joik video with Sora 2...")
    print("🇳🇴 Culture: Norwegian Sami Joik - Arctic Throat Singing")
    print("📱 Format: 9:16 mobile (720x1280)")
    print("⏱️ Duration: 12 seconds")
    print("🎯 Style: Highly cinematic Arctic with Northern Lights")
    
    # Generate with Sora 2 using the exact same method that worked before
    result = generator.generate_video(
        prompt=prompt,
        seconds=12,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Norwegian Joik video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        return result
    else:
        print("❌ Failed to generate Norwegian Joik video")
        return None

def generate_tibetan_throat_singing():
    """Generate Tibetan Throat Singing video - 12 seconds"""
    generator = Sora2DirectAPI()
    
    prompt = """Spiritual cinematic 12-second video of Tibetan throat singing tradition. Majestic Himalayan monastery perched on mountain cliff, saffron-robed monks in meditation, colorful prayer flags fluttering in mountain wind, golden Buddha statues, burning incense creating mystical smoke, snow-capped peaks at sunrise.

AUDIO: Deep Tibetan throat singing with multiple harmonic overtones creating sacred resonance. Traditional singing bowls with crystalline tones, distant temple bells echoing through mountains. Cinematic orchestral score with Tibetan instruments, ethereal choir, and spiritual soundscapes. Atmospheric sound design: mountain winds through prayer flags, monastery chanting reverb, burning incense crackling, sacred ambience. Epic movie-quality audio with cathedral-like spatial depth.

VISUALS: Spiritual, serene, golden hour lighting, peaceful monastery life. 4K cinematic quality. Movie-level production value."""
    
    print("🎬 Creating Tibetan Throat Singing video with Sora 2...")
    print("🇹🇧 Culture: Tibetan Throat Singing - Himalayan Monastery")
    print("📱 Format: 9:16 mobile (720x1280)")
    print("⏱️ Duration: 12 seconds")
    print("🎯 Style: Highly cinematic monastery with golden hour")
    
    # Generate with Sora 2 using the exact same method that worked before
    result = generator.generate_video(
        prompt=prompt,
        seconds=12,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Tibetan Throat Singing video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        return result
    else:
        print("❌ Failed to generate Tibetan Throat Singing video")
        return None

def generate_moroccan_gnawa():
    """Generate Moroccan Gnawa video - 12 seconds"""
    generator = Sora2DirectAPI()
    
    prompt = """Vibrant cinematic 12-second video of Moroccan Gnawa tradition. Sahara Desert at sunset with golden sand dunes, traditional Gnawa musicians in colorful flowing robes, ornate Moroccan architecture with intricate geometric patterns, bustling medina markets, camel caravans silhouetted against desert sunset.

AUDIO: Hypnotic Gnawa vocals with call-and-response chanting building in intensity. Traditional karkaba metal castanets creating rhythmic percussion, sintir bass lute with deep resonant tones. Cinematic score with Middle Eastern instruments, desert winds, and mystical soundscapes. Atmospheric sound design: desert wind through sand dunes, camel bells, bustling medina ambience, crackling campfire. Epic movie-quality audio with immersive desert acoustics.

VISUALS: Warm desert colors, rhythmic camera movements. 4K cinematic quality. Movie-level production value."""
    
    print("🎬 Creating Moroccan Gnawa video with Sora 2...")
    print("🇲🇦 Culture: Moroccan Gnawa - Desert Rhythmic Tradition")
    print("📱 Format: 9:16 mobile (720x1280)")
    print("⏱️ Duration: 12 seconds")
    print("🎯 Style: Highly cinematic desert with warm colors")
    
    # Generate with Sora 2 using the exact same method that worked before
    result = generator.generate_video(
        prompt=prompt,
        seconds=12,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Moroccan Gnawa video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        return result
    else:
        print("❌ Failed to generate Moroccan Gnawa video")
        return None

def generate_greek_byzantine():
    """Generate Greek Byzantine Chanting video - 12 seconds"""
    generator = Sora2DirectAPI()
    
    prompt = """Divine cinematic 12-second video of Greek Byzantine chanting tradition. Ancient Greek Orthodox monastery on cliff overlooking azure Mediterranean Sea, white-washed buildings with brilliant blue domes, ancient olive groves, golden religious icons glowing in candlelight, monastery interior with stone arches, sunset over Greek islands.

AUDIO: Sacred Byzantine chanting - multiple male voices in perfect harmony creating heavenly resonance. Ancient liturgical melodies echoing through stone monastery with cathedral reverb. Cinematic orchestral score with Greek instruments, angelic choir, and Mediterranean soundscapes. Atmospheric sound design: gentle Mediterranean waves, monastery bells, olive leaves rustling, sacred candle flames flickering. Epic movie-quality audio with divine spatial acoustics.

VISUALS: Divine lighting, peaceful Mediterranean beauty. 4K cinematic quality. Movie-level production value."""
    
    print("🎬 Creating Greek Byzantine Chanting video with Sora 2...")
    print("🇬🇷 Culture: Greek Byzantine Chanting - Mediterranean Monastery")
    print("📱 Format: 9:16 mobile (720x1280)")
    print("⏱️ Duration: 12 seconds")
    print("🎯 Style: Highly cinematic Mediterranean with blue domes")
    
    # Generate with Sora 2 using the exact same method that worked before
    result = generator.generate_video(
        prompt=prompt,
        seconds=12,
        size="720x1280"
    )
    
    if result:
        print(f"🎉 SUCCESS! Greek Byzantine Chanting video created: {result.name}")
        print("📁 Location: ~/Desktop/AI-video-Generation/")
        return result
    else:
        print("❌ Failed to generate Greek Byzantine Chanting video")
        return None

def main():
    """Generate one cultural voice video at a time"""
    print("🌍 CULTURAL VOICES - ONE BY ONE GENERATION")
    print("Using the exact same method that worked before")
    print("=" * 50)
    
    # Ask which culture to generate
    cultures = {
        "1": ("Icelandic Rímur", generate_icelandic_rimur),
        "2": ("Norwegian Joik (Sami)", generate_norwegian_joik),
        "3": ("Tibetan Throat Singing", generate_tibetan_throat_singing),
        "4": ("Moroccan Gnawa", generate_moroccan_gnawa),
        "5": ("Greek Byzantine Chanting", generate_greek_byzantine)
    }
    
    print("Choose which culture to generate:")
    for key, (name, _) in cultures.items():
        print(f"{key}. {name}")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice in cultures:
        culture_name, generate_func = cultures[choice]
        print(f"\n🎵 Generating {culture_name}...")
        result = generate_func()
        
        if result:
            print(f"\n✅ {culture_name} video generated successfully!")
            print("🎬 Ready for your cultural voices showcase!")
        else:
            print(f"\n❌ Failed to generate {culture_name} video")
    else:
        print("❌ Invalid choice. Please run again and choose 1-5.")

if __name__ == "__main__":
    main()
