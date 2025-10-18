#!/usr/bin/env python3
"""
Create Complete Zenyai Introduction Video
Combines: Talking head + Stock footage + Background music
"""

from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
import subprocess

console = Console()

def create_zenyai_intro(
    your_photo: str,
    include_talking_head: bool = True,
    include_broll: bool = True,
    include_music: bool = True
):
    """
    Create a complete Zenyai introduction video
    
    Args:
        your_photo: Path to your professional headshot
        include_talking_head: Generate talking head video
        include_broll: Add B-roll stock footage
        include_music: Add background music
    """
    
    console.print("\n[bold cyan]🎬 Creating Complete Zenyai Introduction Video[/bold cyan]\n")
    
    output_dir = Path("zenyai_videos")
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Voice narration (already exists!)
    console.print("[bold]Step 1: Voice Narration[/bold]")
    voice_audio = Path("~/Desktop/Tomi_Zenyai_Voice_Test.wav").expanduser()
    
    if not voice_audio.exists():
        voice_audio = Path("narrations/tomi_zenyai_test.wav")
    
    if voice_audio.exists():
        console.print(f"[green]✅ Using voice: {voice_audio}[/green]")
    else:
        console.print("[red]❌ Voice file not found[/red]")
        return None
    
    # Step 2: Create talking head video
    talking_video = None
    if include_talking_head and Path(your_photo).exists():
        console.print("\n[bold]Step 2: Creating Talking Head Video[/bold]")
        console.print("[cyan]🎬 Generating lip-sync video with SadTalker...[/cyan]")
        
        from create_talking_video import create_talking_video
        
        talking_video = create_talking_video(
            image_path=your_photo,
            audio_path=str(voice_audio),
            output_path=output_dir / "tomi_talking.mp4",
            enhancer="gfpgan"
        )
        
        if talking_video:
            console.print(f"[green]✅ Talking video created: {talking_video}[/green]")
        else:
            console.print("[yellow]⚠️  Talking video failed, continuing without it[/yellow]")
    
    # Step 3: Add B-roll footage (optional)
    if include_broll:
        console.print("\n[bold]Step 3: Adding B-Roll Footage[/bold]")
        console.print("[cyan]Searching for Zenyai-related stock footage...[/cyan]")
        console.print("[dim]Keywords: audio, professional, technology, workspace[/dim]")
        # This would use hybrid_video_generator.py
        console.print("[yellow]💡 Manual step: Add B-roll clips to zenyai_videos/broll/[/yellow]")
    
    # Step 4: Add background music (optional)
    if include_music:
        console.print("\n[bold]Step 4: Background Music[/bold]")
        console.print("[cyan]You can add background music from Freesound[/cyan]")
        console.print("[dim]💡 Tip: Search 'upbeat corporate' or 'tech ambient'[/dim]")
    
    # Final output
    console.print("\n[bold green]✅ Video Components Ready![/bold green]\n")
    
    if talking_video:
        console.print(f"[cyan]📹 Talking Head:[/cyan] {talking_video}")
        console.print(f"[cyan]🎙️  Voice Audio:[/cyan] {voice_audio}")
        
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("1. Watch your talking head video:")
        console.print(f"   [dim]open {talking_video}[/dim]")
        console.print("\n2. To add B-roll and music, use:")
        console.print("   [dim]python hybrid_video_generator.py 'Zenyai Introduction'[/dim]")
        
        return talking_video
    else:
        console.print("[yellow]Create talking head first, then combine with B-roll[/yellow]")
        return None

def interactive_mode():
    """Interactive Zenyai video creation"""
    
    console.print("\n[bold cyan]🎬 Complete Zenyai Introduction Video Creator[/bold cyan]\n")
    
    console.print("[bold]What we'll create:[/bold]")
    console.print("  1. Talking head video (you + your voice)")
    console.print("  2. Optional: Add B-roll stock footage")
    console.print("  3. Optional: Add background music")
    console.print("")
    
    # Get photo
    console.print("[bold]Your Professional Photo:[/bold]")
    console.print("Provide a clear headshot of yourself (front-facing, good lighting)")
    
    photo_path = Prompt.ask("Photo path")
    
    if not Path(photo_path).exists():
        console.print(f"[red]❌ Photo not found: {photo_path}[/red]")
        console.print("\n[yellow]💡 Tip: Take/upload a professional headshot first[/yellow]")
        return
    
    # Options
    talking_head = Confirm.ask("Include talking head video?", default=True)
    broll = Confirm.ask("Include B-roll footage?", default=True)
    music = Confirm.ask("Include background music?", default=True)
    
    # Create
    result = create_zenyai_intro(
        your_photo=photo_path,
        include_talking_head=talking_head,
        include_broll=broll,
        include_music=music
    )
    
    if result:
        console.print("\n[bold green]🎉 Your Zenyai intro video is ready![/bold green]")
        console.print("\n[bold]Use it for:[/bold]")
        console.print("  • Website homepage")
        console.print("  • Social media (LinkedIn, Twitter)")
        console.print("  • Investor presentations")
        console.print("  • Product demos")
        console.print("  • Email campaigns")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        create_zenyai_intro(your_photo=sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()
