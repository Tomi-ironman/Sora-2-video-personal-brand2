#!/usr/bin/env python3
"""
Create Greek Culture Video with EMOTIONAL Voice
"""

import subprocess
from pathlib import Path
from step1_generate_voice import generate_voice_only
from rich.console import Console

console = Console()

# Read the emotional script
script_file = "scripts/greek_culture_emotional.txt"
with open(script_file, 'r') as f:
    script = f.read()

console.print("\n[bold cyan]🇬🇷 GREEK CULTURE VIDEO - EMOTIONAL VERSION[/bold cyan]\n")
console.print(f"[yellow]Script with emotional cues:[/yellow]")
console.print(f"[dim]{script[:200]}...[/dim]\n")

# STEP 1: Generate voice with emotional script
console.print("[bold]STEP 1: Generating EMOTIONAL voice...[/bold]\n")

voice_file = generate_voice_only(script, "narrations/greek_culture_emotional.wav")

if not voice_file:
    console.print("\n[red]❌ Voice generation failed![/red]")
    console.print("[yellow]The API may be taking too long. Try again or use shorter script.[/yellow]")
    exit(1)

console.print(f"\n[bold green]✅ Voice ready: {voice_file}[/bold green]")
console.print("\n[yellow]Next: Download Greek illustrations and create video...[/yellow]\n")

# Download Greek culture illustrations
console.print("[bold]Downloading Greek culture illustrations...[/bold]\n")

try:
    from pinterest_scraper import scrape_pinterest_images
    
    urls = scrape_pinterest_images(
        query="greek art illustration ancient greece mythology",
        num_images=30,
        output_dir="pinterest_downloads/greek_culture"
    )
    
    images_dir = "pinterest_downloads/greek_culture/greek_art_illustration_ancient_greece_mythology"
except:
    console.print("[yellow]⚠️  Pinterest scraper not available, using fallback images[/yellow]\n")
    images_dir = "pinterest_downloads/japanese_art_v2/japanese_traditional_art_watercolor_painting_illustration_ukiyo-e_style"

# STEP 2: Create video
console.print("\n[bold]STEP 2: Creating video with emotional voice...[/bold]\n")

from step2_create_video import create_video_from_voice

result = create_video_from_voice(
    voice_file=voice_file,
    topic_for_images="greek_culture",
    output_filename="greek_culture_emotional.mp4",
    download_new_images=False,
    existing_images_dir=images_dir
)

if result:
    console.print(f"\n[bold green]🎉 GREEK CULTURE VIDEO COMPLETE![/bold green]")
    console.print(f"[cyan]📁 {result}[/cyan]")
    console.print(f"[cyan]📁 Desktop: greek_culture_emotional.mp4[/cyan]\n")
else:
    console.print("\n[red]❌ Video creation failed[/red]")
