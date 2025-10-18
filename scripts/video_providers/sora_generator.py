#!/usr/bin/env python3
"""
Simple Sora 2 Video Generator
Generate videos using OpenAI's Sora model for personal brand content.
"""

import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

class SoraVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            console.print("[red]Error: OPENAI_API_KEY not found in .env file[/red]")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        # Save videos to Desktop/AI-video-Generation folder
        self.videos_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.videos_dir.mkdir(exist_ok=True)
    
    def generate_video(self, prompt, duration=10, size="1920x1080", quality="standard"):
        """Generate a video using Sora 2"""
        console.print(f"\n[cyan]🎬 Generating video with Sora 2...[/cyan]")
        console.print(f"[dim]Prompt: {prompt}[/dim]")
        console.print(f"[dim]Settings: {size}, {duration}s, {quality}[/dim]\n")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Generating video...", total=None)
                
                # Try the new Sora API endpoint
                try:
                    # This is the expected Sora API structure (when available)
                    response = self.client.videos.generations.create(
                        model="sora-1.0-turbo",
                        prompt=prompt,
                        size=size,
                        duration=duration,
                        quality=quality
                    )
                except AttributeError:
                    # Sora API not yet available, show informative message
                    console.print(f"[yellow]⚠️  Sora API not yet available in OpenAI Python library[/yellow]")
                    console.print(f"[dim]The Sora 2 API is still in limited preview.[/dim]")
                    console.print(f"[dim]Your prompt would be: {prompt}[/dim]")
                    console.print(f"[dim]Settings: {size}, {duration}s, {quality}[/dim]")
                    return None
                except Exception as e:
                    if "videos" in str(e).lower() or "sora" in str(e).lower():
                        console.print(f"[yellow]⚠️  Sora API access required[/yellow]")
                        console.print(f"[dim]You may need to join the Sora API waitlist or use a different model.[/dim]")
                        console.print(f"[dim]Error: {str(e)}[/dim]")
                        return None
                    else:
                        raise e
                
                progress.update(task, description="Video generated! Downloading...")
                
                # Download the video
                video_url = response.data[0].url
                video_filename = self.download_video(video_url, prompt)
                
                progress.update(task, description="Complete!")
            
            console.print(f"[green]✅ Video saved: {video_filename}[/green]")
            return video_filename
            
        except Exception as e:
            console.print(f"[red]❌ Error generating video: {str(e)}[/red]")
            return None
    
    def download_video(self, url, prompt):
        """Download video from URL"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_prompt = safe_prompt.replace(' ', '_')
        filename = f"sora_{timestamp}_{safe_prompt}.mp4"
        filepath = self.videos_dir / filename
        
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filepath
    
    def list_videos(self):
        """List all generated videos"""
        videos = list(self.videos_dir.glob("*.mp4"))
        
        if not videos:
            console.print("[yellow]No videos found. Generate your first video![/yellow]")
            return
        
        table = Table(title="Generated Videos")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Created", style="yellow")
        
        for video in sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True):
            size_mb = video.stat().st_size / (1024 * 1024)
            created = datetime.fromtimestamp(video.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            table.add_row(video.name, f"{size_mb:.1f} MB", created)
        
        console.print(table)
    
    def interactive_mode(self):
        """Interactive CLI mode"""
        console.print(Panel.fit(
            "[bold cyan]🎬 Sora 2 Video Generator[/bold cyan]\n"
            "[dim]Generate stunning videos for your personal brand[/dim]",
            border_style="cyan"
        ))
        
        while True:
            console.print("\n[bold]What would you like to do?[/bold]")
            console.print("1. Generate new video")
            console.print("2. List generated videos")
            console.print("3. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], default="1")
            
            if choice == "1":
                self.generate_interactive()
            elif choice == "2":
                self.list_videos()
            elif choice == "3":
                console.print("[cyan]👋 Goodbye![/cyan]")
                break
    
    def generate_interactive(self):
        """Interactive video generation"""
        console.print("\n[bold]Video Generation Settings[/bold]")
        
        prompt = Prompt.ask("Enter your video prompt")
        
        # Settings
        console.print("\n[dim]Optional settings (press Enter for defaults):[/dim]")
        
        size_options = ["1920x1080", "1080x1920", "1280x720"]
        size = Prompt.ask("Resolution", choices=size_options, default="1920x1080")
        
        duration = int(Prompt.ask("Duration (5-20 seconds)", default="10"))
        duration = max(5, min(20, duration))  # Clamp between 5-20
        
        quality_options = ["standard", "hd"]
        quality = Prompt.ask("Quality", choices=quality_options, default="standard")
        
        # Generate
        self.generate_video(prompt, duration, size, quality)

def main():
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        generator = SoraVideoGenerator()
        generator.generate_video(prompt)
    else:
        # Interactive mode
        generator = SoraVideoGenerator()
        generator.interactive_mode()

if __name__ == "__main__":
    main()
