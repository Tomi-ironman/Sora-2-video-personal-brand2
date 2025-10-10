#!/usr/bin/env python3
"""
Zenyai Audio Professional Commercial - 8 Second Pain Point to Solution
Based on extensive research of audio professional workflows and pain points
"""

from sora2_direct_api import Sora2DirectAPI

def main():
    gen = Sora2DirectAPI()
    
    # Research-based commercial targeting audio professionals' biggest pain points
    prompt = """
Create an intense, relatable 8-second commercial in 9:16 vertical format targeting audio professionals in gaming, film, and commercial production. The style should be realistic, slightly gritty, and immediately recognizable to anyone who works in audio post-production.

VISUAL STYLE: Realistic cinematography with moody lighting - think dimly lit studios, multiple monitor glow, and the authentic look of late-night work sessions. Color palette should be desaturated with blue/orange contrast from monitor screens and warm desk lamps. Fast-paced editing with quick cuts that build tension.

TARGET AUDIENCE PAIN POINTS (from research):
- Spending hours searching through massive, disorganized audio libraries
- Frantically scrolling through endless file lists with cryptic names
- Working 3AM sessions with multiple coffee cups and energy drinks
- Dealing with poor file organization and missing metadata
- Racing against impossible deadlines while maintaining quality

SEQUENCE BREAKDOWN:

Beat 1 (0-2s): CHAOS MONTAGE - Quick cuts of the universal audio professional struggle:
- Close-up of tired eyes staring at multiple monitors showing Pro Tools, file browsers, and endless audio waveforms
- Hands frantically scrolling through thousands of poorly named audio files: "door_slam_01.wav", "footstep_take_47.wav", "ambience_thing.aiff"
- Clock showing 3:17 AM in corner of screen
- Multiple empty coffee cups and energy drink cans scattered around workspace
- Frustrated expression as someone types "WHERE IS THAT PERFECT FOOTSTEP SOUND??" in a search bar

Beat 2 (2-4s): THE BREAKING POINT - Escalating frustration:
- Rapid montage of clicking through folders: SFX > Footsteps > Concrete > Various > Misc > Old_Project_Backup > ???
- Split screen showing: Left side = chaotic file browser with 10,000+ unsorted files, Right side = timeline with empty audio tracks and looming deadline
- Close-up of hands rubbing temples in exhaustion
- Audio waveform visualization showing the stress (erratic, chaotic patterns)

Beat 3 (4-6s): THE SOLUTION MOMENT - Zenyai enters:
- Screen suddenly clears to clean, organized interface
- Person speaks into microphone with relief: "Find me a crisp footstep on concrete, medium pace, urban environment"
- INSTANT RESULTS: Perfect audio files appear immediately with rich metadata tags visible
- The same tired face now showing amazement and relief
- Clean, organized waveforms replace the chaos

Beat 4 (6-8s): THE TRANSFORMATION - New reality:
- Same workspace, but now organized and calm
- Multiple screens showing perfectly tagged, searchable audio libraries
- Person confidently dragging the perfect sound into timeline
- Text overlay appears: "Zenyai - AI-native Audio Asset Management. Stop searching. Start creating."
- Final shot: The person leaning back in chair with satisfied smile, project completed, clock now showing reasonable hour

TECHNICAL DETAILS: 720x1280 vertical format. Realistic lighting with authentic studio environments. Fast-paced editing for first 4 seconds, then slower, more confident pacing for the solution. Use actual audio software interfaces (Pro Tools, Logic, etc.) for authenticity. Include real sound designer workspace elements: multiple monitors, audio interfaces, studio monitors, cable management.

EMOTIONAL JOURNEY: Stress and frustration → Breaking point → Relief and amazement → Confidence and satisfaction. The commercial should make every audio professional think "That's exactly my life" in the first 4 seconds, then show them a better way.

CALL TO ACTION: "Stop searching. Start creating. Zenyai.io"
"""

    print("🎧 Generating Audio Professional Commercial...")
    print("🎯 Target: Gaming, Film & Commercial Audio Professionals")
    print("⚡ Pain Points: File chaos, search frustration, deadline stress")
    print("💡 Solution: AI-native audio asset management")
    print("🎬 Style: Realistic, gritty, authentic studio environments")
    
    # Generate the commercial
    result = gen.generate_video(prompt=prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"🎉 SUCCESS! Audio Professional Commercial created!")
        print("🔥 Features:")
        print("   ✅ Authentic audio professional pain points")
        print("   ✅ Realistic late-night studio environments")
        print("   ✅ Relatable file organization chaos")
        print("   ✅ Clear problem → solution narrative")
        print("   ✅ Professional audio software interfaces")
        print("   ✅ Emotional journey: Stress → Relief → Confidence")
        print("   ✅ Strong CTA: 'Stop searching. Start creating.'")
        print("   ✅ 8s, 9:16 format optimized for social media")
    else:
        print("❌ Failed to generate Audio Professional Commercial")

if __name__ == "__main__":
    main()
