#!/usr/bin/env python3
"""
SMART Video Creator - Automatically detects topic and downloads relevant illustrations
"""

import subprocess
import os
from pathlib import Path
from step1_generate_voice import generate_voice_only
from rich.console import Console
import re

console = Console()


def detect_topic_from_script(script_text):
    """
    Intelligently detect the topic from the script
    Returns: (topic_name, search_query)
    """
    
    script_lower = script_text.lower()
    
    # Topic detection patterns
    topics = {
        'greek': {
            'keywords': ['greece', 'greek', 'athens', 'parthenon', 'sparta', 'mythology', 'zeus', 'apollo'],
            'query': 'greek art illustration ancient greece mythology'
        },
        'japanese': {
            'keywords': ['japan', 'japanese', 'tokyo', 'samurai', 'cherry blossom', 'zen', 'wabi-sabi'],
            'query': 'japanese art illustration traditional ukiyo-e'
        },
        'egyptian': {
            'keywords': ['egypt', 'egyptian', 'pyramid', 'pharaoh', 'nile', 'hieroglyph'],
            'query': 'egyptian art illustration ancient egypt pyramids'
        },
        'roman': {
            'keywords': ['rome', 'roman', 'caesar', 'colosseum', 'latin'],
            'query': 'roman art illustration ancient rome empire'
        },
        'chinese': {
            'keywords': ['china', 'chinese', 'beijing', 'dynasty', 'confucius', 'tao'],
            'query': 'chinese art illustration traditional ink painting'
        },
        'viking': {
            'keywords': ['viking', 'norse', 'odin', 'thor', 'scandinavia'],
            'query': 'viking art illustration norse mythology'
        },
        'indian': {
            'keywords': ['india', 'indian', 'hindu', 'buddha', 'sanskrit', 'taj mahal'],
            'query': 'indian art illustration traditional miniature painting'
        },
        'aztec': {
            'keywords': ['aztec', 'mayan', 'mexico', 'pyramid', 'mesoamerica'],
            'query': 'aztec art illustration mayan civilization'
        }
    }
    
    # Detect which topic
    for topic_name, topic_info in topics.items():
        for keyword in topic_info['keywords']:
            if keyword in script_lower:
                console.print(f"[green]🎯 Detected topic: {topic_name.upper()}[/green]")
                console.print(f"[dim]Search query: {topic_info['query']}[/dim]\n")
                return topic_name, topic_info['query']
    
    # Fallback: extract first meaningful word
    words = re.findall(r'\b[A-Z][a-z]+\b', script_text)
    if words:
        topic_name = words[0].lower()
        query = f"{topic_name} art illustration"
        console.print(f"[yellow]🔍 Guessed topic: {topic_name}[/yellow]")
        console.print(f"[dim]Search query: {query}[/dim]\n")
        return topic_name, query
    
    # Ultimate fallback
    return 'culture', 'cultural art illustration'


def download_topic_illustrations(topic_name, search_query, num_images=30):
    """
    Download illustrations for the specific topic
    """
    
    console.print(f"[bold cyan]🎨 Downloading {topic_name.upper()} illustrations[/bold cyan]\n")
    
    download_dir = f"pinterest_downloads/{topic_name}_illustrations"
    
    try:
        from pinterest_scraper import scrape_pinterest_images
        
        urls = scrape_pinterest_images(
            query=search_query,
            num_images=num_images,
            output_dir=download_dir
        )
        
        # Find the created directory
        base_path = Path(download_dir)
        subdirs = list(base_path.glob("*"))
        
        if subdirs:
            images_dir = subdirs[0]
            console.print(f"[green]✅ Downloaded to: {images_dir}[/green]\n")
            return str(images_dir)
        else:
            console.print(f"[red]❌ No images downloaded[/red]\n")
            return None
            
    except Exception as e:
        console.print(f"[red]❌ Download error: {str(e)}[/red]\n")
        return None


def create_smart_video(script_text, output_filename):
    """
    Create video with automatic topic detection and relevant illustrations
    
    Args:
        script_text: The script content
        output_filename: Output video filename (e.g., 'greek_culture.mp4')
    """
    
    console.print("\n[bold cyan]🎬 SMART VIDEO CREATOR[/bold cyan]\n")
    console.print(f"[yellow]Script length: {len(script_text)} characters[/yellow]\n")
    
    # STEP 1: Detect topic
    console.print("[bold]STEP 1: Detect Topic[/bold]\n")
    topic_name, search_query = detect_topic_from_script(script_text)
    
    # STEP 2: Generate voice
    console.print("[bold]STEP 2: Generate Voice[/bold]\n")
    voice_filename = f"narrations/{topic_name}_culture_voice.wav"
    
    voice_file = generate_voice_only(script_text, voice_filename)
    
    if not voice_file:
        console.print("\n[red]❌ Voice generation failed![/red]")
        return None
    
    # STEP 3: Download topic-specific illustrations
    console.print("\n[bold]STEP 3: Download Topic Illustrations[/bold]\n")
    images_dir = download_topic_illustrations(topic_name, search_query)
    
    if not images_dir or not Path(images_dir).exists():
        console.print(f"[red]❌ Could not download {topic_name} illustrations[/red]")
        return None
    
    # STEP 4: Create video
    console.print("\n[bold]STEP 4: Create Video[/bold]\n")
    
    from step2_create_video import create_video_from_voice
    
    result = create_video_from_voice(
        voice_file=voice_file,
        topic_for_images=topic_name,
        output_filename=output_filename,
        download_new_images=False,
        existing_images_dir=images_dir
    )
    
    if result:
        console.print(f"\n[bold green]🎉 VIDEO COMPLETE![/bold green]")
        console.print(f"[cyan]📁 {result}[/cyan]")
        console.print(f"[cyan]📁 Desktop: {output_filename}[/cyan]\n")
        console.print(f"[green]✅ Topic: {topic_name.upper()}[/green]")
        console.print(f"[green]✅ Illustrations: {topic_name}-specific[/green]")
        console.print(f"[green]✅ Style: Illustration/watercolor[/green]\n")
        return result
    else:
        console.print("\n[red]❌ Video creation failed[/red]")
        return None


if __name__ == "__main__":
    # Example: Greek culture
    script = "Greece! Ancient wisdom, eternal beauty!"
    
    console.print("[bold]🧪 Testing with Greek culture script[/bold]\n")
    
    result = create_smart_video(script, "greek_culture_smart.mp4")
    
    if result:
        console.print("[bold green]✅ SUCCESS![/bold green]")
    else:
        console.print("[bold red]❌ FAILED[/bold red]")
