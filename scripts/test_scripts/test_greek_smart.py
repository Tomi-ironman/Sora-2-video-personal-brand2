#!/usr/bin/env python3
"""Test smart video with Greek topic"""

from create_video_smart import detect_topic_from_script, download_topic_illustrations
from step2_create_video import create_video_from_voice
from rich.console import Console

console = Console()

# Greek script
script = "Greece! Ancient wisdom, eternal beauty!"

console.print("\n[bold cyan]🇬🇷 TESTING SMART GREEK VIDEO[/bold cyan]\n")

# Auto-detect topic
console.print("[bold]Detecting topic...[/bold]")
topic_name, search_query = detect_topic_from_script(script)

console.print(f"[green]✅ Topic: {topic_name}[/green]")
console.print(f"[green]✅ Query: {search_query}[/green]\n")

# Download GREEK illustrations (not Japanese!)
console.print("[bold]Downloading GREEK illustrations...[/bold]\n")
images_dir = download_topic_illustrations(topic_name, search_query, num_images=25)

if images_dir:
    console.print(f"[green]✅ Greek images: {images_dir}[/green]\n")
    
    # Create video with GREEK images
    console.print("[bold]Creating video with GREEK images...[/bold]\n")
    create_video_from_voice(
        voice_file='narrations/greek_very_short.wav',
        topic_for_images=topic_name,
        output_filename='greek_culture_CORRECT.mp4',
        download_new_images=False,
        existing_images_dir=images_dir
    )
else:
    console.print("[red]❌ Failed to download Greek images[/red]")
