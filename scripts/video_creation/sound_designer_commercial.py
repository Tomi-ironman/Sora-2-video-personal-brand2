#!/usr/bin/env python3
"""
Zenyai Sound Designer Commercial - "The Search That Never Ends"
Based on extensive research of sound designer pain points and workflow frustrations
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Research-based commercial targeting sound designers' biggest pain point: file organization hell
    prompt = """
Create an intense, relatable 8-second commercial in 9:16 vertical format targeting sound designers who are drowning in disorganized audio libraries. The style should be realistic and gritty, capturing the authentic frustration of late-night studio work and the relief of finding the perfect solution.

VISUAL STYLE: Realistic cinematography with moody, dimly lit studio environments. Color palette should be desaturated blues and oranges from multiple monitor glow, with warm desk lamp lighting. Fast-paced, anxiety-inducing editing for the first 4 seconds, then smooth, confident pacing for the solution.

TARGET AUDIENCE RESEARCH FINDINGS:
- Sound designers spend HOURS searching through massive, disorganized audio libraries
- They have thousands of poorly named files: "door_slam_01.wav", "step_thing.aiff", "walk_sound_final_FINAL.wav"
- They work late nights (2-3 AM) under deadline pressure
- They settle for mediocre sounds because they can't find the perfect ones they KNOW they have
- File organization is described as "extremely messy and unorganized" - needing "the sound design equivalent of Marie Kondo"

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): THE ENDLESS SEARCH - Authentic frustration:
- Close-up of bloodshot, tired eyes staring at multiple monitors showing Pro Tools and file browsers
- Clock in corner showing 2:47 AM
- Rapid scrolling through thousands of cryptically named audio files:
  "Footsteps_concrete_01.wav"
  "step_thing.aiff" 
  "walk_sound_final_FINAL.wav"
  "urban_footstep_take_47.wav"
  "concrete_step_OLD_VERSION.aiff"
- Frustrated typing in search bar: "WHERE IS THAT PERFECT URBAN FOOTSTEP??"
- Search returns 847 results, all useless

Beat 2 (2-4s): THE BREAKING POINT - Escalating desperation:
- Split screen: Left = chaotic file browser with 10,000+ poorly organized files, Right = empty Pro Tools timeline with looming deadline timer
- Rapid montage of clicking through nested folders: SFX > Footsteps > Concrete > Various > Misc > Old_Projects > Backup > ??? > More_Sounds > Random_Stuff
- Close-up of hands frantically scrolling, then stopping to rub temples in exhaustion
- Multiple empty coffee cups and energy drink cans scattered around workspace
- Audio waveform visualization showing chaotic, erratic patterns representing the stress

Beat 3 (4-6s): THE SOLUTION MOMENT - Zenyai enters with AI magic:
- Screen suddenly transitions to clean, organized Zenyai interface
- Same exhausted person speaks into microphone with desperate hope: "Find me a crisp concrete footstep, urban environment, medium pace, professional quality"
- INSTANT RESULTS: Perfect audio files appear immediately with rich, descriptive metadata tags visible:
  "Urban_Concrete_Footstep_Medium_Pace_Crisp_Professional_44kHz_Stereo.wav"
  Tags: #urban #concrete #footstep #medium-pace #crisp #professional #outdoor #city
- The tired face transforms to amazement and relief
- Clean, organized waveforms replace the chaos

Beat 4 (6-8s): THE TRANSFORMATION - New reality of organized bliss:
- Same workspace, but now calm and organized
- Multiple screens showing perfectly tagged, searchable Zenyai audio libraries
- Person confidently dragging the perfect sound into Pro Tools timeline
- Sound waveform appears clean and professional in the timeline
- Text overlay appears in clean, modern font: "Zenyai - AI-native Audio Asset Management. Stop searching. Start creating."
- Final shot: The person leaning back in chair with satisfied smile, project progress bar showing completion, clock now showing a reasonable hour (7:23 PM)

TECHNICAL DETAILS: 720x1280 vertical format. Authentic studio lighting with multiple monitor glow. Use real audio software interfaces (Pro Tools, Logic Pro, file browsers) for maximum authenticity. Include genuine sound designer workspace elements: audio interfaces, studio monitors, cable management, acoustic treatment. The editing should feel frantic and stressful for the first 4 seconds, then become smooth and confident.

EMOTIONAL JOURNEY: Exhausted frustration → Desperate searching → Breaking point → Hope → Relief → Confidence → Satisfaction. Every sound designer should think "That's my exact life!" in the first 4 seconds.

CALL TO ACTION: "Stop searching. Start creating. Zenyai.io"

AUTHENTIC DETAILS: Include real file naming conventions that sound designers will recognize, actual folder structures they use, and the specific language they use to describe their pain points. This should feel like someone secretly filmed their worst day and then showed them the solution.
"""

    print("🎧 Generating Sound Designer Commercial - 'The Search That Never Ends'...")
    print("🎯 Target: Sound Designers drowning in file organization hell")
    print("⚡ Core Pain Point: Hours wasted searching through disorganized libraries")
    print("💡 Solution: AI-native audio asset management with semantic search")
    print("🎬 Style: Authentic late-night studio frustration → relief")
    print("📊 Based on: Extensive research from Reddit, forums, and industry blogs")
    
    # Generate the commercial
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Sound Designer Commercial created!")
        print("🔥 Research-Based Features:")
        print("   ✅ Authentic file organization nightmare (2:47 AM scenario)")
        print("   ✅ Real file naming conventions sound designers recognize")
        print("   ✅ Actual folder structure chaos they experience daily")
        print("   ✅ Semantic search solution: 'Find crisp concrete footstep...'")
        print("   ✅ Instant results with rich metadata tagging")
        print("   ✅ Emotional journey: Frustration → Relief → Confidence")
        print("   ✅ Professional studio environment authenticity")
        print("   ✅ Strong CTA: 'Stop searching. Start creating.'")
        print("   ✅ 8s, 9:16 format optimized for social media")
        print("")
        print("🎯 This commercial directly addresses the #1 pain point from our research:")
        print("   'Library management can be the difference between finding that")
        print("   perfect sound vs. settling for something mediocre.'")
    else:
        print("❌ Failed to generate Sound Designer Commercial")

if __name__ == "__main__":
    main()
