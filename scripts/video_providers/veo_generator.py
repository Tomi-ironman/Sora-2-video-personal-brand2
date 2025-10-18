#!/usr/bin/env python3
"""
Google Veo 2 Video Generator
Generate hyper-realistic videos using Google's Veo 2 model for personal brand content.
"""

import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

class VeoVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            console.print("[red]Error: GOOGLE_AI_API_KEY not found in .env file[/red]")
            console.print("[dim]Get your API key from: https://aistudio.google.com/app/apikey[/dim]")
            sys.exit(1)
        
        genai.configure(api_key=self.api_key)
        # Save videos to Desktop/AI-video-Generation folder
        self.videos_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.videos_dir.mkdir(exist_ok=True)
    
    def generate_video(self, prompt, duration=30, aspect_ratio="16:9", quality="high"):
        """Generate a video using Google Veo 2"""
        console.print(f"\n[cyan]🎬 Generating video with Google Veo 2...[/cyan]")
        console.print(f"[dim]Prompt: {prompt}[/dim]")
        console.print(f"[dim]Settings: {aspect_ratio}, {duration}s, {quality} quality[/dim]\n")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Generating video...", total=None)
                
                # Try Google's video generation
                try:
                    # This is the expected Google Veo API structure
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    
                    # Enhanced prompt for better video generation
                    enhanced_prompt = f"""
                    Create a {duration}-second hyper-realistic video with the following description:
                    
                    {prompt}
                    
                    Technical requirements:
                    - Aspect ratio: {aspect_ratio}
                    - Duration: {duration} seconds
                    - Quality: {quality}
                    - Style: Hyper-realistic, professional, cinematic
                    - Camera movement: Smooth, professional
                    - Lighting: Professional, well-lit
                    - Focus: Sharp, clear details
                    """
                    
                    response = model.generate_content(enhanced_prompt)
                    
                    # Note: Google's video generation API is still evolving
                    # This is a placeholder for when the API becomes available
                    console.print(f"[yellow]⚠️  Google Veo 2 API integration in progress[/yellow]")
                    console.print(f"[dim]Google's video generation API is being integrated.[/dim]")
                    console.print(f"[green]✅ Your enhanced prompt:[/green]")
                    console.print(f"[dim]{enhanced_prompt}[/dim]")
                    
                    return None
                    
                except Exception as e:
                    if "video" in str(e).lower() or "veo" in str(e).lower():
                        console.print(f"[yellow]⚠️  Google Veo 2 API access required[/yellow]")
                        console.print(f"[dim]Video generation may require special API access.[/dim]")
                        console.print(f"[dim]Error: {str(e)}[/dim]")
                        return None
                    else:
                        # Try alternative approach with Gemini for video planning
                        progress.update(task, description="Creating video concept with Gemini...")
                        return self.create_video_concept(prompt, duration, aspect_ratio, quality)
                        
        except Exception as e:
            console.print(f"[red]❌ Error generating video: {str(e)}[/red]")
            return None
    
    def create_video_concept(self, prompt, duration, aspect_ratio, quality):
        """Create a detailed video concept using Gemini"""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            concept_prompt = f"""
            Create a detailed video production concept for a {duration}-second personal brand video.
            
            Original concept: {prompt}
            
            Please provide:
            1. Detailed shot breakdown (every 3-5 seconds)
            2. Camera angles and movements
            3. Lighting setup recommendations
            4. Props and set design
            5. Color palette and mood
            6. Audio/music suggestions
            7. Post-production effects
            8. Technical specifications for {aspect_ratio} aspect ratio
            
            Make this hyper-realistic and professional for personal branding.
            """
            
            response = model.generate_content(concept_prompt)
            
            # Save the concept to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_')
            concept_filename = f"video_concept_{timestamp}_{safe_prompt}.txt"
            concept_filepath = self.videos_dir / concept_filename
            
            with open(concept_filepath, 'w') as f:
                f.write(f"Video Concept Generated: {datetime.now()}\n")
                f.write(f"Original Prompt: {prompt}\n")
                f.write(f"Duration: {duration}s | Aspect Ratio: {aspect_ratio} | Quality: {quality}\n")
                f.write("="*80 + "\n\n")
                f.write(response.text)
            
            console.print(f"[green]✅ Video concept saved: {concept_filename}[/green]")
            console.print(f"[cyan]📋 Detailed production plan created![/cyan]")
            
            # Display a preview of the concept
            console.print(f"\n[bold]Video Concept Preview:[/bold]")
            preview = response.text[:500] + "..." if len(response.text) > 500 else response.text
            console.print(f"[dim]{preview}[/dim]")
            
            return concept_filepath
            
        except Exception as e:
            console.print(f"[red]❌ Error creating video concept: {str(e)}[/red]")
            return None
    
    def list_concepts(self):
        """List all generated video concepts"""
        concepts = list(self.videos_dir.glob("video_concept_*.txt"))
        videos = list(self.videos_dir.glob("*.mp4"))
        
        if not concepts and not videos:
            console.print("[yellow]No video concepts or videos found. Generate your first concept![/yellow]")
            return
        
        if concepts:
            table = Table(title="Generated Video Concepts")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="green")
            table.add_column("Created", style="yellow")
            
            for concept in sorted(concepts, key=lambda x: x.stat().st_mtime, reverse=True):
                size_kb = concept.stat().st_size / 1024
                created = datetime.fromtimestamp(concept.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                table.add_row(concept.name, f"{size_kb:.1f} KB", created)
            
            console.print(table)
        
        if videos:
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
            "[bold cyan]🎬 Google Veo 2 Video Generator[/bold cyan]\n"
            "[dim]Generate hyper-realistic videos for your personal brand[/dim]",
            border_style="cyan"
        ))
        
        while True:
            console.print("\n[bold]What would you like to do?[/bold]")
            console.print("1. Generate new video concept")
            console.print("2. List generated concepts & videos")
            console.print("3. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], default="1")
            
            if choice == "1":
                self.generate_interactive()
            elif choice == "2":
                self.list_concepts()
            elif choice == "3":
                console.print("[cyan]👋 Goodbye![/cyan]")
                break
    
    def generate_interactive(self):
        """Interactive video generation"""
        console.print("\n[bold]Video Generation Settings[/bold]")
        
        prompt = Prompt.ask("Enter your video prompt")
        
        # Settings
        console.print("\n[dim]Optional settings (press Enter for defaults):[/dim]")
        
        aspect_options = ["16:9", "9:16", "1:1", "4:3"]
        aspect_ratio = Prompt.ask("Aspect ratio", choices=aspect_options, default="16:9")
        
        duration = int(Prompt.ask("Duration (5-60 seconds)", default="30"))
        duration = max(5, min(60, duration))  # Clamp between 5-60
        
        quality_options = ["standard", "high", "ultra"]
        quality = Prompt.ask("Quality", choices=quality_options, default="high")
        
        # Generate
        self.generate_video(prompt, duration, aspect_ratio, quality)

def main():
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        generator = VeoVideoGenerator()
        generator.generate_video(prompt)
    else:
        # Interactive mode
        generator = VeoVideoGenerator()
        generator.interactive_mode()

if __name__ == "__main__":
    main()
