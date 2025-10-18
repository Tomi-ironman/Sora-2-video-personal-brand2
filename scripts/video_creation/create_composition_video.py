#!/usr/bin/env python3
"""
Complete pipeline: Music Composition Video
1. Generate voice with API
2. Download mixed media (static + GIFs)
3. Create video with text emphasis
"""

from step1_generate_voice import generate_voice_only
from mixed_media_downloader import download_mixed_media
from create_video_with_text_emphasis import create_video_with_emphasis
from rich.console import Console

console = Console()

# Read the composition script
with open('scripts/music_composition.txt', 'r') as f:
    script = f.read()

console.print("\n[bold cyan]🎵 MUSIC COMPOSITION VIDEO - COMPLETE PIPELINE[/bold cyan]\n")
console.print(f"[yellow]Script:[/yellow]")
console.print(f"[dim]{script}[/dim]\n")
console.print(f"[cyan]Length: {len(script)} characters[/cyan]\n")

# STEP 1: Generate Voice
console.print("[bold cyan]━━━ STEP 1: Generate Voice with API ━━━[/bold cyan]\n")

voice_file = generate_voice_only(script, "narrations/composition_voice.wav")

if not voice_file:
    console.print("\n[red]❌ Voice generation failed![/red]")
    console.print("[yellow]The API may have issues. Check with your team.[/yellow]")
    exit(1)

console.print(f"\n[bold green]✅ Voice ready: {voice_file}[/bold green]\n")

# STEP 2: Download Mixed Media
console.print("[bold cyan]━━━ STEP 2: Download Mixed Media ━━━[/bold cyan]\n")

media_results = download_mixed_media(
    topic="music composition production",
    num_static=18,
    num_gifs=3,
    output_dir="pinterest_downloads/mixed_music_composition"
)

console.print(f"\n[bold green]✅ Media downloaded![/bold green]")
console.print(f"[cyan]  • Static: {len(media_results['static_images'])}[/cyan]")
console.print(f"[cyan]  • GIFs: {len(media_results['gifs'])}[/cyan]\n")

# STEP 3: Create Video with Text Emphasis
console.print("[bold cyan]━━━ STEP 3: Create Video with Text Emphasis ━━━[/bold cyan]\n")

video_file = create_video_with_emphasis(
    media_dir="pinterest_downloads/mixed_music_composition",
    voice_file=voice_file,
    script_text=script,
    output_filename="music_composition_final.mp4"
)

console.print(f"\n[bold green]🎉 COMPOSITION VIDEO COMPLETE![/bold green]")
console.print(f"[cyan]📁 {video_file}[/cyan]")
console.print(f"[cyan]📁 Desktop: music_composition_final.mp4[/cyan]\n")

console.print("[bold]✅ Full pipeline executed successfully![/bold]\n")
