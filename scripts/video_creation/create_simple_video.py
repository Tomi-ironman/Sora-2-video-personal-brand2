#!/usr/bin/env python3
"""
Create Simple Video - Image + Voice (No Lip-Sync)
Fast alternative - generates in seconds!
"""

from pathlib import Path
import subprocess
from rich.console import Console

console = Console()

def create_simple_video(image_path, audio_path, output_path):
    """
    Create video with static image and audio
    FAST: Generates in 5-10 seconds!
    """
    
    console.print("\n[bold cyan]🎬 Creating Simple Video (Fast!)[/bold cyan]\n")
    
    image = Path(image_path)
    audio = Path(audio_path)
    output = Path(output_path)
    
    if not image.exists():
        console.print(f"[red]❌ Image not found: {image}[/red]")
        return None
    
    if not audio.exists():
        console.print(f"[red]❌ Audio not found: {audio}[/red]")
        return None
    
    output.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]📸 Image:[/cyan] {image}")
    console.print(f"[cyan]🎙️  Audio:[/cyan] {audio}")
    console.print(f"[cyan]💾 Output:[/cyan] {output}")
    console.print("")
    
    # Get audio duration
    duration_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio)
    ]
    
    try:
        result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        console.print(f"[cyan]⏱️  Duration:[/cyan] {duration:.1f} seconds")
    except:
        duration = 15
        console.print(f"[yellow]Using default duration: {duration}s[/yellow]")
    
    # Create video with FFmpeg
    console.print("\n[cyan]🎬 Generating video...[/cyan]")
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", str(image),
        "-i", str(audio),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-y",
        str(output)
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
        
        console.print(f"\n[bold green]✅ Video created successfully![/bold green]")
        console.print(f"[cyan]📁 Saved to:[/cyan] {output}")
        
        # File size
        file_size = output.stat().st_size / (1024 * 1024)
        console.print(f"[cyan]📊 Size:[/cyan] {file_size:.1f} MB")
        
        console.print("\n[bold]🔊 To watch:[/bold]")
        console.print(f"   open {output}")
        
        # Auto-play
        console.print("\n[cyan]Playing video...[/cyan]")
        subprocess.run(["open", str(output)])
        
        return output
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return None

if __name__ == "__main__":
    # Culture & AI video
    console.print("\n[bold cyan]🌍 Culture & AI Video - Simple Version[/bold cyan]")
    console.print("[dim]Static image + your voice (generates in seconds!)[/dim]\n")
    
    result = create_simple_video(
        image_path="Tomi/Gemini_Generated_Image_paq9q1paq9q1paq9.png",
        audio_path="narrations/tomi_zenyai_test.wav",
        output_path="simple_videos/culture_ai.mp4"
    )
    
    if result:
        console.print("\n[bold green]🎉 Your video is ready![/bold green]")
        console.print("\n[dim]This is a simple version (no lip-sync)[/dim]")
        console.print("[dim]For lip-sync version, wait for SadTalker to finish[/dim]")
