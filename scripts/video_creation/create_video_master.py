#!/usr/bin/env python3
"""
MASTER VIDEO AUTOMATION
Complete end-to-end: Script → Voice → Media → Personal Footage → Final Video

Just provide a script and topic - everything else is automatic!
"""

from pathlib import Path
from rich.console import Console
from step1_generate_voice import generate_voice_only
from mixed_media_downloader import download_mixed_media
from create_personal_brand_video import create_personal_brand_video
import random
import time
import json

console = Console()


class MasterVideoAutomation:
    """Complete automation system for creating personal brand videos"""
    
    def __init__(self, tomi_folder="Tomi"):
        self.tomi_folder = Path(tomi_folder)
        console.print(f"\n[bold cyan]🎬 MASTER VIDEO AUTOMATION[/bold cyan]\n")
    
    def get_available_personal_videos(self):
        """Get all videos from Tomi folder"""
        if not self.tomi_folder.exists():
            console.print(f"[yellow]⚠️  Tomi folder not found: {self.tomi_folder}[/yellow]")
            return []
        
        videos = list(self.tomi_folder.glob("*.mp4")) + list(self.tomi_folder.glob("*.mov"))
        
        console.print(f"[green]✅ Found {len(videos)} personal videos in Tomi folder:[/green]")
        for i, video in enumerate(videos, 1):
            console.print(f"[dim]  {i}. {video.name}[/dim]")
        console.print()
        
        return videos
    
    def select_best_video(self, topic, available_videos):
        """
        Select best personal video for the topic
        For now: random selection, but you can add smart matching later
        """
        if not available_videos:
            return None
        
        # Smart matching could go here based on topic keywords
        # Randomize selection each run for variety
        selected = random.choice(available_videos)
        
        console.print(f"[cyan]🎯 Selected personal video: {selected.name}[/cyan]")
        console.print(f"[dim]Topic: {topic}[/dim]\n")
        
        return selected
    
    def create_complete_video(
        self,
        script_text,
        topic,
        output_filename,
        generate_voice=True,
        download_media=True,
        style_name=None,
        seed=None,
        randomize=True
    ):
        """
        Complete automation pipeline
        
        Args:
            script_text: The script to narrate
            topic: Topic for visual search (e.g., "music composition")
            output_filename: Final video filename
            generate_voice: Generate new voice or use existing
            download_media: Download new media or use existing
        
        Returns:
            Path to final video
        """
        
        console.print(f"[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]")
        console.print(f"[bold]📋 PROJECT: {output_filename}[/bold]")
        console.print(f"[bold]📝 Topic: {topic}[/bold]")
        console.print(f"[bold]📏 Script length: {len(script_text)} chars[/bold]")
        console.print(f"[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")
        
        # STEP 1: Get personal videos
        console.print("[bold cyan]━━━ STEP 1: Personal Footage ━━━[/bold cyan]\n")
        available_videos = self.get_available_personal_videos()
        
        if not available_videos:
            console.print("[red]❌ No personal videos found in Tomi folder![/red]")
            console.print("[yellow]Please add videos to the Tomi/ folder[/yellow]\n")
            return None
        
        selected_video = self.select_best_video(topic, available_videos)
        
        # STEP 2: Generate voice
        console.print("[bold cyan]━━━ STEP 2: Voice Generation ━━━[/bold cyan]\n")
        
        voice_filename = f"narrations/{topic.replace(' ', '_')}_voice.wav"
        
        if generate_voice:
            voice_file = generate_voice_only(script_text, voice_filename)
            
            if not voice_file:
                console.print("\n[red]❌ Voice generation failed![/red]")
                return None
            
            console.print(f"\n[bold green]✅ Voice ready: {voice_file}[/bold green]\n")
        else:
            voice_file = voice_filename
            console.print(f"[yellow]Using existing voice: {voice_file}[/yellow]\n")
        
        # STEP 3: Download media
        console.print("[bold cyan]━━━ STEP 3: Topic-Specific Media ━━━[/bold cyan]\n")
        
        media_dir = f"pinterest_downloads/mixed_{topic.replace(' ', '_')}"
        
        if download_media:
            media_results = download_mixed_media(
                topic=topic,
                num_static=18,
                num_gifs=3,
                output_dir=media_dir
            )
            
            console.print(f"\n[bold green]✅ Media downloaded![/bold green]")
            console.print(f"[cyan]  • Static: {len(media_results['static_images'])}[/cyan]")
            console.print(f"[cyan]  • GIFs: {len(media_results['gifs'])}[/cyan]\n")
        else:
            console.print(f"[yellow]Using existing media: {media_dir}[/yellow]\n")
        
        # STEP 4: Create final video
        console.print("[bold cyan]━━━ STEP 4: Final Video Assembly ━━━[/bold cyan]\n")
        
        # default seed (time-based) ensures varied outputs per run
        if seed is None:
            seed = int(time.time() * 1000) % 2_147_483_647

        # choose random style if none provided and randomize enabled
        if style_name is None and randomize:
            try:
                styles_dir = Path(__file__).resolve().parents[2] / "styles"
                index_path = styles_dir / "index.json"
                if index_path.exists():
                    with open(index_path, 'r') as f:
                        names = json.load(f)
                    if names:
                        style_name = random.choice(names)
                        console.print(f"[cyan]🎨 Using random style: {style_name}[/cyan]")
            except Exception:
                pass

        video_file = create_personal_brand_video(
            personal_video_path=str(selected_video),
            media_dir=media_dir,
            voice_file=voice_file,
            script_text=script_text,
            output_filename=output_filename,
            style_name=style_name,
            seed=seed,
            randomize=randomize
        )
        
        # Success summary
        console.print(f"\n[bold green]" + "="*50 + "[/bold green]")
        console.print(f"[bold green]🎉 AUTOMATION COMPLETE![/bold green]")
        console.print(f"[bold green]" + "="*50 + "[/bold green]\n")
        
        console.print(f"[bold]📊 Summary:[/bold]")
        console.print(f"[green]  ✅ Personal footage: {selected_video.name}[/green]")
        console.print(f"[green]  ✅ Voice: Generated with API[/green]")
        console.print(f"[green]  ✅ Visuals: Topic-matched ({topic})[/green]")
        console.print(f"[green]  ✅ Final video: {output_filename}[/green]")
        console.print(f"[green]  ✅ Location: Desktop + professional_videos/[/green]\n")
        
        return video_file


def create_video_from_script(script_text, topic, output_name, style_name=None, seed=None, randomize=True):
    """
    Simple wrapper - just provide script, topic, and output name!
    Everything else is automated!
    """
    automation = MasterVideoAutomation()
    
    return automation.create_complete_video(
        script_text=script_text,
        topic=topic,
        output_filename=output_name,
        style_name=style_name,
        seed=seed,
        randomize=randomize
    )


if __name__ == "__main__":
    # Example: Create a video about music composition
    
    script = """Music composition. Where creativity meets discipline!

The blank page. Every composer's greatest fear!

But here's the truth. You don't need perfect inspiration!

Start with a simple melody. Just four notes!

Build it. Layer it. Transform it!

This is how masterpieces are born. One note at a time!"""
    
    console.print("\n[bold]🧪 TESTING MASTER AUTOMATION[/bold]\n")
    
    create_video_from_script(
        script_text=script,
        topic="music composition production",
        output_name="composition_master_test.mp4"
    )
