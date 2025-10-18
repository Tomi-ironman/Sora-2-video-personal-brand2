#!/usr/bin/env python3
"""
Create Talking Video with Wav2Lip
Fast lip-sync generation!
"""

from pathlib import Path
import subprocess
from rich.console import Console

console = Console()

def create_wav2lip_video(image_path, audio_path, output_path):
    """
    Create lip-synced video using Wav2Lip
    FAST: 10-30 seconds!
    """
    
    console.print("\n[bold cyan]🎬 Creating Talking Video with Wav2Lip[/bold cyan]\n")
    
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
    
    # Run Wav2Lip
    console.print("[cyan]🎬 Generating lip-synced video...[/cyan]")
    console.print("[dim]This will take 10-30 seconds[/dim]\n")
    
    wav2lip_cmd = [
        "python",
        "Wav2Lip/inference.py",
        "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
        "--face", str(image),
        "--audio", str(audio),
        "--outfile", str(output),
        "--fps", "25",
        "--pads", "0", "10", "0", "0",
        "--face_det_batch_size", "16",
        "--wav2lip_batch_size", "128",
        "--resize_factor", "1"
    ]
    
    try:
        result = subprocess.run(
            wav2lip_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if output.exists():
            console.print(f"\n[bold green]✅ Talking video created![/bold green]")
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
        else:
            console.print("[red]❌ Video not generated[/red]")
            console.print(f"[dim]{result.stdout}[/dim]")
            return None
            
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        console.print(f"[yellow]stdout:[/yellow]\n[dim]{e.stdout}[/dim]")
        console.print(f"[yellow]stderr:[/yellow]\n[dim]{e.stderr}[/dim]")
        return None

if __name__ == "__main__":
    # Culture & AI video
    console.print("\n[bold cyan]🌍 Culture & AI - Wav2Lip Version[/bold cyan]")
    console.print("[dim]Fast lip-sync generation (10-30 seconds!)[/dim]\n")
    
    result = create_wav2lip_video(
        image_path="Tomi/Gemini_Generated_Image_paq9q1paq9q1paq9.png",
        audio_path="narrations/tomi_zenyai_test.wav",
        output_path="wav2lip_videos/culture_ai.mp4"
    )
    
    if result:
        console.print("\n[bold green]🎉 Your talking video is ready![/bold green]")
        console.print("\n[bold]Features:[/bold]")
        console.print("✅ Accurate lip-sync")
        console.print("✅ Generated in seconds")
        console.print("✅ Ready to share!")
