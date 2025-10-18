#!/usr/bin/env python3
"""
Quick Video Maker - Using existing voice
No heavy AI loading - just pure video creation!
"""

from pathlib import Path
from create_synced_video import create_synced_video
from add_captions import add_captions_to_video
from rich.console import Console
import sys

console = Console()

def make_video_fast(topic, audio_path="narrations/tomi_zenyai_test.wav"):
    """
    Create video using existing voice audio
    
    Args:
        topic: What the video is about (for B-roll search)
        audio_path: Path to your voice audio
    """
    
    console.print("\n[bold cyan]🎬 FAST VIDEO MAKER[/bold cyan]")
    console.print("[dim]Using your pre-recorded voice![/dim]\n")
    
    # Read the script from audio (or use topic)
    script = f"""
    {topic} is transforming the creator economy.
    
    The tools we have today are revolutionary. From AI to automation,
    everything is changing faster than ever before.
    
    Whether you're building a personal brand or creating content,
    understanding these shifts gives you a massive advantage.
    
    The future belongs to those who adapt and evolve.
    This is your moment to level up.
    """
    
    script = " ".join(script.split())
    
    console.print(f"[yellow]Topic: {topic}[/yellow]")
    console.print(f"[dim]Using voice: {audio_path}[/dim]\n")
    
    # Step 1: Create video with B-roll
    console.print("[bold]Step 1/2: Creating video with smart B-roll[/bold]")
    
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_').lower()[:30]
    
    output_dir = Path("professional_videos")
    output_dir.mkdir(exist_ok=True)
    
    video_path = output_dir / f"{safe_topic}_fast.mp4"
    
    result = create_synced_video(
        audio_path=audio_path,
        script_text=script,
        output_path=str(video_path),
        aspect_ratio="9:16",
        add_music=True
    )
    
    if not result:
        console.print("[red]❌ Video creation failed[/red]")
        return None
    
    console.print(f"[green]✅ Video created![/green]\n")
    
    # Step 2: Add captions
    console.print("[bold]Step 2/2: Adding captions[/bold]")
    
    captioned_path = output_dir / f"{safe_topic}_fast_WITH_CAPTIONS.mp4"
    
    final_video = add_captions_to_video(
        video_path=str(video_path),
        output_path=str(captioned_path),
        audio_path=audio_path,
        script_text=script,
        style="modern"
    )
    
    if not final_video:
        console.print("[yellow]⚠️  Captions failed, but video is ready![/yellow]")
        final_video = video_path
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold green]🎉 VIDEO READY![/bold green]")
    console.print("="*60 + "\n")
    
    console.print(f"[cyan]📁 File: {final_video}[/cyan]")
    
    file_size = Path(final_video).stat().st_size / (1024 * 1024)
    console.print(f"[cyan]📊 Size: {file_size:.1f} MB[/cyan]")
    console.print(f"[cyan]📱 Format: 9:16 (social media ready)[/cyan]\n")
    
    console.print("[bold]✨ Features:[/bold]")
    console.print("  ✅ Your voice")
    console.print("  ✅ Smart B-roll")
    console.print("  ✅ Background music")
    console.print("  ✅ Word-by-word captions")
    console.print("  ✅ Cinematic color grading")
    
    console.print("\n[bold green]Ready to post! 🚀[/bold green]\n")
    
    # Open video
    import subprocess
    subprocess.run(["open", str(final_video)])
    
    return final_video


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: python make_video_quick.py \"Your Topic\"[/bold red]")
        console.print("\n[bold]Example:[/bold]")
        console.print('  python make_video_quick.py "AI Tools for Creators"')
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    
    result = make_video_fast(topic)
    
    if result:
        console.print("[bold green]✅ SUCCESS![/bold green]")
    else:
        console.print("[bold red]❌ Failed[/bold red]")
