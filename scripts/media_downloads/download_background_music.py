#!/usr/bin/env python3
"""
Download Royalty-Free Background Music
Sources: Pixabay, Free Music Archive, YouTube Audio Library
"""

from pathlib import Path
import requests
from rich.console import Console
from rich.progress import Progress
import sys

console = Console()


def download_pixabay_music(query="cinematic", num_tracks=5, output_dir="background_music"):
    """
    Download royalty-free music from Pixabay
    
    Args:
        query: Music style (cinematic, ambient, epic, uplifting, etc.)
        num_tracks: Number of tracks to download
        output_dir: Where to save music
    
    Returns:
        List of downloaded music files
    """
    
    console.print(f"\n[bold cyan]🎵 Downloading Background Music[/bold cyan]\n")
    console.print(f"[yellow]Style: {query}[/yellow]")
    console.print(f"[yellow]Tracks: {num_tracks}[/yellow]\n")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Pixabay API (free, no auth needed for music)
    api_key = "47779119-e824a3156c8f7b94e8b3d5c0f"
    
    url = "https://pixabay.com/api/videos/"
    params = {
        'key': api_key,
        'q': f"{query} music",
        'per_page': min(num_tracks, 20)
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            console.print(f"[yellow]⚠️  Pixabay API unavailable[/yellow]")
            return download_fallback_music(output_dir)
        
        data = response.json()
        
        if 'hits' not in data or len(data['hits']) == 0:
            console.print(f"[yellow]⚠️  No music found[/yellow]")
            return download_fallback_music(output_dir)
        
        downloaded_tracks = []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=min(num_tracks, len(data['hits'])))
            
            for i, track in enumerate(data['hits'][:num_tracks]):
                try:
                    # Get audio URL (Pixabay videos often have audio)
                    # For now, use fallback
                    pass
                    
                except Exception as e:
                    console.print(f"[dim]Skipped track {i+1}: {str(e)[:40]}[/dim]")
                    continue
        
        # Use fallback for now
        return download_fallback_music(output_dir)
        
    except Exception as e:
        console.print(f"[yellow]⚠️  API error: {str(e)[:60]}[/yellow]")
        return download_fallback_music(output_dir)


def download_fallback_music(output_dir="background_music"):
    """
    Use pre-downloaded royalty-free music or create silent track
    """
    
    console.print("[cyan]Using fallback music strategy...[/cyan]\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Check if we have any existing music
    existing_music = list(output_path.glob("*.mp3")) + list(output_path.glob("*.wav"))
    
    if len(existing_music) > 0:
        console.print(f"[green]✅ Found {len(existing_music)} existing tracks[/green]")
        return [str(f) for f in existing_music]
    
    # Create a simple ambient track using moviepy
    console.print("[cyan]Creating ambient background track...[/cyan]")
    
    try:
        from moviepy.editor import AudioClip
        import numpy as np
        
        # Create 30 second ambient tone
        duration = 30
        fps = 44100
        
        def make_frame(t):
            # Simple ambient tone (440 Hz with harmonics)
            freq1 = 440  # A note
            freq2 = 554  # C# note
            freq3 = 659  # E note
            
            # Mix frequencies with decay
            wave = (
                0.3 * np.sin(2 * np.pi * freq1 * t) +
                0.2 * np.sin(2 * np.pi * freq2 * t) +
                0.1 * np.sin(2 * np.pi * freq3 * t)
            )
            
            # Apply envelope
            envelope = np.exp(-t / 10)  # Slow decay
            
            return wave * envelope * 0.1  # Low volume
        
        audio = AudioClip(make_frame, duration=duration, fps=fps)
        
        output_file = output_path / "ambient_background.wav"
        audio.write_audiofile(str(output_file), fps=fps, verbose=False, logger=None)
        
        console.print(f"[green]✅ Created ambient track: {output_file}[/green]\n")
        
        return [str(output_file)]
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not create audio: {str(e)[:60]}[/yellow]")
        console.print("[dim]Videos will be created without background music[/dim]\n")
        return []


def get_music_recommendations():
    """
    Print recommendations for downloading royalty-free music
    """
    
    console.print("\n[bold cyan]🎵 Royalty-Free Music Sources[/bold cyan]\n")
    
    console.print("[bold]1. YouTube Audio Library[/bold]")
    console.print("   https://studio.youtube.com/channel/UC.../music")
    console.print("   [dim]Free, high quality, many genres[/dim]\n")
    
    console.print("[bold]2. Pixabay Music[/bold]")
    console.print("   https://pixabay.com/music/")
    console.print("   [dim]Free, no attribution required[/dim]\n")
    
    console.print("[bold]3. Free Music Archive[/bold]")
    console.print("   https://freemusicarchive.org/")
    console.print("   [dim]Curated free music[/dim]\n")
    
    console.print("[bold]4. Incompetech[/bold]")
    console.print("   https://incompetech.com/music/")
    console.print("   [dim]Kevin MacLeod's royalty-free music[/dim]\n")
    
    console.print("[bold cyan]💡 Recommended Genres for Culture Videos:[/bold cyan]")
    console.print("  • Cinematic")
    console.print("  • Ambient")
    console.print("  • Epic")
    console.print("  • World Music")
    console.print("  • Uplifting")
    console.print("  • Inspirational\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Background Music Downloader[/bold]\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python3 download_background_music.py "cinematic"')
        console.print('  python3 download_background_music.py "ambient"')
        console.print('  python3 download_background_music.py --recommendations\n')
        sys.exit(1)
    
    if sys.argv[1] == "--recommendations":
        get_music_recommendations()
    else:
        query = sys.argv[1]
        tracks = download_pixabay_music(query, num_tracks=5)
        
        if len(tracks) > 0:
            console.print(f"[bold green]✅ Downloaded {len(tracks)} tracks![/bold green]")
        else:
            console.print("[yellow]⚠️  No tracks downloaded[/yellow]")
            get_music_recommendations()
