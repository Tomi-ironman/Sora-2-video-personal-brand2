#!/usr/bin/env python3
"""
Create Talking Head Videos with SadTalker
Lip-sync your cloned voice to any photo!
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def create_talking_video(
    image_path: str,
    audio_path: str,
    output_path: str = None,
    enhancer: str = "gfpgan"
):
    """
    Create a talking head video from an image and audio
    
    Args:
        image_path: Path to your photo (headshot recommended)
        audio_path: Path to audio file (your cloned voice)
        output_path: Where to save the video (optional)
        enhancer: Face enhancement ('gfpgan' or 'none')
    """
    
    console.print("\n[bold cyan]🎬 Creating Talking Head Video with SadTalker[/bold cyan]\n")
    
    # Check if SadTalker is set up
    sadtalker_dir = Path("SadTalker")
    if not sadtalker_dir.exists():
        console.print("[red]❌ SadTalker not found![/red]")
        console.print("Run setup first")
        return None
    
    # Check inputs
    image_path = Path(image_path)
    audio_path = Path(audio_path)
    
    if not image_path.exists():
        console.print(f"[red]❌ Image not found: {image_path}[/red]")
        return None
    
    if not audio_path.exists():
        console.print(f"[red]❌ Audio not found: {audio_path}[/red]")
        return None
    
    # Set output path
    if output_path is None:
        output_dir = Path("talking_videos")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"talking_{image_path.stem}.mp4"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]📸 Image:[/cyan] {image_path}")
    console.print(f"[cyan]🎙️  Audio:[/cyan] {audio_path}")
    console.print(f"[cyan]💾 Output:[/cyan] {output_path}")
    console.print("")
    
    # Run SadTalker inference
    console.print("[cyan]🎬 Generating talking video...[/cyan]")
    console.print("[dim]This may take 1-3 minutes for the first run (downloading models)[/dim]")
    console.print("")
    
    os.chdir("SadTalker")
    
    # Build command
    cmd = [
        "python",
        "inference.py",
        "--driven_audio", f"../{audio_path}",
        "--source_image", f"../{image_path}",
        "--result_dir", f"../{output_path.parent}",
        "--enhancer", enhancer,
        "--still",  # Less head movement for professional look
        "--preprocess", "full"  # Full preprocessing for best quality
    ]
    
    import subprocess
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        os.chdir("..")
        
        # Find the generated video
        result_files = list(output_path.parent.glob("*.mp4"))
        if result_files:
            latest_video = max(result_files, key=lambda p: p.stat().st_mtime)
            
            # Rename to our desired output
            if latest_video != output_path:
                latest_video.rename(output_path)
            
            console.print(f"\n[bold green]✅ Talking video created![/bold green]")
            console.print(f"[cyan]📁 Saved to:[/cyan] {output_path}")
            
            file_size = output_path.stat().st_size / (1024 * 1024)
            console.print(f"[cyan]📊 Size:[/cyan] {file_size:.1f} MB")
            
            console.print("\n[bold]🔊 To watch:[/bold]")
            console.print(f"   open {output_path}")
            
            return output_path
        else:
            console.print("[red]❌ Video not generated[/red]")
            return None
            
    except subprocess.CalledProcessError as e:
        os.chdir("..")
        console.print(f"[red]❌ Error: {e}[/red]")
        console.print(f"[dim]{e.stderr}[/dim]")
        return None
    except Exception as e:
        os.chdir("..")
        console.print(f"[red]❌ Error: {e}[/red]")
        return None

def interactive_mode():
    """Interactive mode for creating talking videos"""
    
    console.print("\n[bold cyan]🎬 SadTalker - Create Talking Head Videos[/bold cyan]\n")
    
    # Get image
    console.print("[bold]Step 1: Your Photo[/bold]")
    console.print("Provide a clear headshot (front-facing, good lighting)")
    image_path = Prompt.ask("Image path")
    
    if not Path(image_path).exists():
        console.print(f"[red]❌ Image not found: {image_path}[/red]")
        return
    
    # Get audio
    console.print("\n[bold]Step 2: Your Audio[/bold]")
    console.print("Use your cloned voice or any audio file")
    
    # Suggest the test audio
    test_audio = Path("narrations/tomi_zenyai_test.wav")
    if test_audio.exists():
        console.print(f"[dim]💡 Suggestion: {test_audio}[/dim]")
    
    audio_path = Prompt.ask("Audio path", default=str(test_audio) if test_audio.exists() else "")
    
    if not Path(audio_path).exists():
        console.print(f"[red]❌ Audio not found: {audio_path}[/red]")
        return
    
    # Enhancement
    console.print("\n[bold]Step 3: Face Enhancement[/bold]")
    enhancer = Prompt.ask(
        "Enhance face quality?",
        choices=["yes", "no"],
        default="yes"
    )
    enhancer = "gfpgan" if enhancer == "yes" else "none"
    
    # Create video
    result = create_talking_video(
        image_path=image_path,
        audio_path=audio_path,
        enhancer=enhancer
    )
    
    if result:
        console.print("\n[bold green]🎉 Your talking video is ready![/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Watch the video")
        console.print("2. Use in your Zenyai marketing")
        console.print("3. Create more with different scripts")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        if len(sys.argv) >= 3:
            create_talking_video(
                image_path=sys.argv[1],
                audio_path=sys.argv[2],
                output_path=sys.argv[3] if len(sys.argv) > 3 else None
            )
        else:
            console.print("[red]Usage: python create_talking_video.py <image> <audio> [output][/red]")
    else:
        # Interactive mode
        interactive_mode()
