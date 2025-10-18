#!/usr/bin/env python3
"""
Automatic Video Generator
Uses free media providers to create complete videos from text prompts
Combines: Pexels/Pixabay (B-roll) + Freesound (music) + FFmpeg (editing)
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel

load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from media_providers.unified_media_manager import UnifiedMediaManager

console = Console()

class AutoVideoGenerator:
    def __init__(self):
        self.manager = UnifiedMediaManager()
        self.output_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.temp_dir = self.output_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_video(
        self,
        concept: str,
        keywords: list,
        duration: int = 30,
        include_music: bool = True
    ):
        """
        Generate a complete video from concept and keywords
        
        Args:
            concept: Video concept/title (e.g., "Productivity Tips")
            keywords: List of visual keywords (e.g., ["office work", "laptop", "coffee"])
            duration: Target video duration in seconds
            include_music: Whether to add background music
        """
        console.print(f"\n[bold cyan]🎬 Creating Video: {concept}[/bold cyan]\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in concept if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')[:50]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            
            # Step 1: Search for B-roll videos
            task1 = progress.add_task("[cyan]Searching for B-roll footage...", total=len(keywords))
            
            video_clips = []
            clips_per_keyword = max(1, duration // (len(keywords) * 5))  # Rough calculation
            
            for keyword in keywords:
                console.print(f"   🔍 Searching: {keyword}")
                
                # Search videos
                results = self.manager.search_videos(keyword, num_results=clips_per_keyword)
                
                # Download first result
                if results:
                    clip_dir = self.temp_dir / f"{timestamp}_clips"
                    clip_dir.mkdir(exist_ok=True)
                    
                    path = self.manager.download_media(results[0], clip_dir)
                    if path:
                        video_clips.append(path)
                        console.print(f"      ✅ Downloaded clip for '{keyword}'")
                
                progress.update(task1, advance=1)
            
            if not video_clips:
                console.print("[red]❌ No video clips found. Try different keywords.[/red]")
                return None
            
            console.print(f"\n[green]✅ Downloaded {len(video_clips)} video clips[/green]")
            
            # Step 2: Search for background music (if requested)
            audio_path = None
            if include_music:
                task2 = progress.add_task("[cyan]Finding background music...", total=None)
                
                audio_results = self.manager.search_audio(
                    query="upbeat background",
                    num_results=3,
                    duration_min=duration - 10,
                    duration_max=duration + 30,
                    audio_type='music'
                )
                
                if audio_results:
                    audio_dir = self.temp_dir / f"{timestamp}_audio"
                    audio_dir.mkdir(exist_ok=True)
                    
                    audio_path = self.manager.download_media(audio_results[0], audio_dir)
                    if audio_path:
                        console.print(f"[green]✅ Downloaded background music[/green]")
                
                progress.update(task2, completed=True)
            
            # Step 3: Create final video
            task3 = progress.add_task("[cyan]Creating final video...", total=None)
            
            output_filename = f"{timestamp}_{safe_name}.mp4"
            output_path = self.output_dir / output_filename
            
            try:
                final_video = self.manager.create_video_from_assets(
                    video_clips=video_clips,
                    audio_path=audio_path,
                    output_path=output_path,
                    target_duration=duration
                )
                
                progress.update(task3, completed=True)
                
                console.print(f"\n[bold green]🎉 Video created successfully![/bold green]")
                console.print(f"[cyan]📁 Location: {final_video}[/cyan]")
                
                # Show file size
                size_mb = final_video.stat().st_size / (1024 * 1024)
                console.print(f"[dim]Size: {size_mb:.1f} MB[/dim]")
                
                return final_video
                
            except Exception as e:
                console.print(f"[red]❌ Error creating video: {e}[/red]")
                return None
    
    def interactive_mode(self):
        """Interactive mode for creating videos"""
        console.print(Panel.fit(
            "[bold cyan]🎬 Automatic Video Generator[/bold cyan]\n"
            "[dim]Create complete videos from text using free stock media[/dim]",
            border_style="cyan"
        ))
        
        # Get concept
        concept = Prompt.ask("\n[bold]What's your video concept?[/bold]", default="Productivity Tips")
        
        # Get keywords
        console.print("\n[bold]Enter visual keywords[/bold] [dim](comma-separated)[/dim]")
        console.print("[dim]Example: office work, laptop typing, coffee break[/dim]")
        keywords_input = Prompt.ask("Keywords")
        keywords = [k.strip() for k in keywords_input.split(',')]
        
        # Get duration
        duration = int(Prompt.ask("\n[bold]Video duration[/bold] (seconds)", default="30"))
        
        # Music option
        include_music = Prompt.ask("\n[bold]Include background music?[/bold]", choices=["yes", "no"], default="yes") == "yes"
        
        # Generate
        self.generate_video(
            concept=concept,
            keywords=keywords,
            duration=duration,
            include_music=include_music
        )
    
    def quick_generate(self, preset: str):
        """Quick generate with presets"""
        presets = {
            'productivity': {
                'concept': 'Productivity Tips',
                'keywords': ['office desk', 'laptop work', 'coffee morning', 'notebook writing'],
                'duration': 30
            },
            'tech': {
                'concept': 'Tech Innovation',
                'keywords': ['coding computer', 'technology workspace', 'modern office', 'startup team'],
                'duration': 30
            },
            'lifestyle': {
                'concept': 'Modern Lifestyle',
                'keywords': ['city life', 'coffee shop', 'urban workspace', 'creative work'],
                'duration': 30
            },
            'business': {
                'concept': 'Business Growth',
                'keywords': ['business meeting', 'office teamwork', 'professional workspace', 'success celebration'],
                'duration': 30
            }
        }
        
        if preset in presets:
            config = presets[preset]
            console.print(f"[cyan]Using preset: {preset.upper()}[/cyan]")
            return self.generate_video(
                concept=config['concept'],
                keywords=config['keywords'],
                duration=config['duration']
            )
        else:
            console.print(f"[red]Unknown preset: {preset}[/red]")
            console.print(f"[dim]Available: {', '.join(presets.keys())}[/dim]")
            return None

def main():
    generator = AutoVideoGenerator()
    
    if len(sys.argv) > 1:
        # Command line mode with preset
        preset = sys.argv[1]
        generator.quick_generate(preset)
    else:
        # Interactive mode
        generator.interactive_mode()

if __name__ == "__main__":
    main()
