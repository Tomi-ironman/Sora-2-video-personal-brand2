#!/usr/bin/env python3
"""
Cultural Voices Video Generator
Creates a stunning 60-second video showcasing 5 ancient vocal traditions
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from sora2_direct_api import Sora2DirectAPI

# Load environment variables
load_dotenv()

console = Console()

class CulturalVoicesGenerator:
    def __init__(self):
        self.sora = Sora2DirectAPI()
        self.output_dir = Path.home() / "Desktop" / "AI-video-Generation" / "Cultural-Voices"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_voices_of_earth_video(self):
        """Generate 5 separate 12-second videos for each cultural tradition"""
        
        console.print(Panel.fit(
            "[bold cyan]🎵 VOICES OF THE EARTH[/bold cyan]\n"
            "[dim]5 Ancient Vocal Traditions • 12 Seconds Each • Cinematic Beauty[/dim]",
            border_style="cyan"
        ))
        
        # Define each cultural segment as separate 12-second videos
        segments = [
            {
                "name": "Icelandic Rímur",
                "prompt": """Breathtaking cinematic 12-second video of Icelandic Rímur vocal tradition. Epic Icelandic landscape at golden hour - dramatic black volcanic rocks, steaming geysers, Northern Lights dancing across star-filled sky, ancient Viking runestones, moss-covered lava fields, glacial ice formations reflecting aurora colors. Deep resonant male voice performing traditional Rímur chanting - ancient storytelling style with haunting melodic phrases, accompanied by wind sounds and distant echoing. Cinematic shots, slow camera movements across otherworldly terrain, ethereal lighting. 4K cinematic quality, film-like color grading."""
            },
            {
                "name": "Norwegian Joik (Sami)",
                "prompt": """Mystical cinematic 12-second video of Norwegian Sami Joik tradition. Arctic tundra under brilliant Northern Lights, traditional Sami lavvu tent with warm firelight, reindeer silhouettes against aurora, snow-covered mountains, person in colorful traditional Sami clothing (gákti) with ancient frame drums. Authentic Sami joik throat singing - rhythmic spiritual chanting with overtones, accompanied by traditional drum beats. Mystical atmosphere, aurora reflections on snow, intimate cultural moments. 4K cinematic quality, ethereal lighting."""
            },
            {
                "name": "Tibetan Throat Singing", 
                "prompt": """Spiritual cinematic 12-second video of Tibetan throat singing tradition. Majestic Himalayan monastery perched on mountain cliff, saffron-robed monks in meditation, colorful prayer flags fluttering in mountain wind, golden Buddha statues, burning incense creating mystical smoke, snow-capped peaks at sunrise. Deep Tibetan throat singing with multiple harmonic overtones, accompanied by singing bowls and distant temple bells. Spiritual, serene, golden hour lighting, peaceful monastery life. 4K cinematic quality."""
            },
            {
                "name": "Moroccan Gnawa",
                "prompt": """Vibrant cinematic 12-second video of Moroccan Gnawa tradition. Sahara Desert at sunset with golden sand dunes, traditional Gnawa musicians in colorful flowing robes, ornate Moroccan architecture with intricate geometric patterns, bustling medina markets, camel caravans silhouetted against desert sunset. Hypnotic Gnawa vocals with call-and-response style, accompanied by karkaba metal castanets and sintir bass lute creating rhythmic patterns. Warm desert colors, rhythmic camera movements. 4K cinematic quality."""
            },
            {
                "name": "Greek Byzantine Chanting",
                "prompt": """Divine cinematic 12-second video of Greek Byzantine chanting tradition. Ancient Greek Orthodox monastery on cliff overlooking azure Mediterranean Sea, white-washed buildings with brilliant blue domes, ancient olive groves, golden religious icons glowing in candlelight, monastery interior with stone arches, sunset over Greek islands. Sacred Byzantine chanting - multiple male voices in perfect harmony, ancient liturgical melodies echoing through stone monastery. Divine lighting, peaceful Mediterranean beauty. 4K cinematic quality."""
            }
        ]
        
        generated_videos = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            for i, segment in enumerate(segments, 1):
                console.print(f"\n[cyan]🎬 Generating {segment['name']} ({i}/5)...[/cyan]")
                
                # Generate 12-second video for this culture
                video_path = self.sora.generate_video(
                    prompt=segment['prompt'],
                    seconds=12,
                    size="1280x720"  # Landscape format (16:9 aspect ratio)
                )
                
                if video_path and Path(video_path).exists():
                    # Move to our cultural voices directory with proper naming
                    culture_name = segment['name'].replace(' ', '_').replace('(', '').replace(')', '').lower()
                    final_path = self.output_dir / f"{i:02d}_{culture_name}_{timestamp}.mp4"
                    Path(video_path).rename(final_path)
                    
                    generated_videos.append({
                        "culture": segment['name'],
                        "file_path": str(final_path),
                        "order": i
                    })
                    
                    console.print(f"[green]✅ {segment['name']} saved: {final_path.name}[/green]")
                else:
                    console.print(f"[red]❌ Failed to generate {segment['name']}[/red]")
            
            if generated_videos:
                # Save metadata for all segments
                metadata = {
                    "title": "Voices of the Earth - 5 Ancient Vocal Traditions",
                    "total_segments": len(generated_videos),
                    "duration_per_segment": "12 seconds",
                    "total_duration": f"{len(generated_videos) * 12} seconds",
                    "segments": generated_videos,
                    "generated_at": datetime.now().isoformat(),
                    "output_directory": str(self.output_dir)
                }
                
                metadata_path = self.output_dir / f"voices_of_earth_metadata_{timestamp}.json"
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                console.print(f"\n[dim]📄 Metadata saved: {metadata_path}[/dim]")
                
                return generated_videos
            else:
                console.print("[red]❌ No videos were generated successfully[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]❌ Error generating videos: {str(e)}[/red]")
            return None

def main():
    """Main function to generate the cultural voices video"""
    
    console.print(Panel.fit(
        "[bold magenta]🌍 CULTURAL VOICES VIDEO GENERATOR[/bold magenta]\n"
        "[dim]Creating stunning cinematic showcase of world vocal traditions[/dim]",
        border_style="magenta"
    ))
    
    generator = CulturalVoicesGenerator()
    
    try:
        # Generate the cultural videos
        generated_videos = generator.generate_voices_of_earth_video()
        
        if generated_videos:
            video_list = "\n".join([f"• {video['culture']}" for video in generated_videos])
            console.print(Panel.fit(
                f"[bold green]🎉 SUCCESS![/bold green]\n\n"
                f"[cyan]📹 Videos Generated:[/cyan] {len(generated_videos)}/5\n"
                f"[cyan]📁 Location:[/cyan] ~/Desktop/AI-video-Generation/Cultural-Voices/\n"
                f"[cyan]⏱️  Duration:[/cyan] 12 seconds each (60 seconds total)\n"
                f"[cyan]🎵 Cultures Generated:[/cyan]\n{video_list}\n\n"
                f"[dim]Ready for your cultural voices showcase![/dim]\n"
                f"[dim]You can combine these 5 videos in sequence for the full experience.[/dim]",
                border_style="green"
            ))
        else:
            console.print(Panel.fit(
                "[bold red]❌ GENERATION FAILED[/bold red]\n\n"
                "[yellow]Please check your API key and try again[/yellow]",
                border_style="red"
            ))
            
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Generation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {str(e)}[/red]")

if __name__ == "__main__":
    main()
