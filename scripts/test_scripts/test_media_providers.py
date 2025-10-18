#!/usr/bin/env python3
"""
Test Script for Free Media Providers
Tests all 5 free APIs: Pexels, Pixabay, Unsplash, Freesound, FFmpeg
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from media_providers import (
    PexelsProvider,
    PixabayProvider,
    FreesoundProvider,
    UnsplashProvider
)
from media_providers.ffmpeg_utils import FFmpegUtils
from media_providers.unified_media_manager import UnifiedMediaManager

console = Console()

def test_ffmpeg():
    """Test FFmpeg installation"""
    console.print("\n[bold cyan]Testing FFmpeg...[/bold cyan]")
    
    if FFmpegUtils.check_ffmpeg_installed():
        console.print("[green]✅ FFmpeg is installed and working[/green]")
        return True
    else:
        console.print("[red]❌ FFmpeg not found. Install with: brew install ffmpeg[/red]")
        return False

def test_pexels():
    """Test Pexels API"""
    console.print("\n[bold cyan]Testing Pexels API...[/bold cyan]")
    
    try:
        provider = PexelsProvider()
        results = provider.search_videos(query="ocean waves", per_page=3)
        
        videos = results.get('videos', [])
        if videos:
            console.print(f"[green]✅ Pexels API working - Found {len(videos)} videos[/green]")
            console.print(f"   Example: {videos[0].get('user', {}).get('name')} - Duration: {videos[0].get('duration')}s")
            return True
        else:
            console.print("[yellow]⚠️  Pexels API returned no results[/yellow]")
            return False
            
    except RuntimeError as e:
        console.print(f"[red]❌ Pexels Error: {e}[/red]")
        console.print("[dim]   Set PEXELS_API_KEY in .env file[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Pexels Error: {e}[/red]")
        return False

def test_pixabay():
    """Test Pixabay API"""
    console.print("\n[bold cyan]Testing Pixabay API...[/bold cyan]")
    
    try:
        provider = PixabayProvider()
        results = provider.search_videos(query="nature", per_page=3)
        
        videos = results.get('hits', [])
        if videos:
            console.print(f"[green]✅ Pixabay API working - Found {len(videos)} videos[/green]")
            console.print(f"   Example: Video ID {videos[0].get('id')} - Duration: {videos[0].get('duration')}s")
            return True
        else:
            console.print("[yellow]⚠️  Pixabay API returned no results[/yellow]")
            return False
            
    except RuntimeError as e:
        console.print(f"[red]❌ Pixabay Error: {e}[/red]")
        console.print("[dim]   Set PIXABAY_API_KEY in .env file[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Pixabay Error: {e}[/red]")
        return False

def test_unsplash():
    """Test Unsplash API"""
    console.print("\n[bold cyan]Testing Unsplash API...[/bold cyan]")
    
    try:
        provider = UnsplashProvider()
        results = provider.search_photos(query="technology", per_page=3)
        
        photos = results.get('results', [])
        if photos:
            console.print(f"[green]✅ Unsplash API working - Found {len(photos)} images[/green]")
            console.print(f"   Example: {photos[0].get('user', {}).get('name')} - {photos[0].get('width')}x{photos[0].get('height')}px")
            return True
        else:
            console.print("[yellow]⚠️  Unsplash API returned no results[/yellow]")
            return False
            
    except RuntimeError as e:
        console.print(f"[red]❌ Unsplash Error: {e}[/red]")
        console.print("[dim]   Set UNSPLASH_ACCESS_KEY in .env file[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Unsplash Error: {e}[/red]")
        return False

def test_freesound():
    """Test Freesound API"""
    console.print("\n[bold cyan]Testing Freesound API...[/bold cyan]")
    
    try:
        provider = FreesoundProvider()
        results = provider.search_sounds(query="ambient music", page_size=3)
        
        sounds = results.get('results', [])
        if sounds:
            console.print(f"[green]✅ Freesound API working - Found {len(sounds)} sounds[/green]")
            console.print(f"   Example: {sounds[0].get('name')} - Duration: {sounds[0].get('duration'):.1f}s")
            return True
        else:
            console.print("[yellow]⚠️  Freesound API returned no results[/yellow]")
            return False
            
    except RuntimeError as e:
        console.print(f"[red]❌ Freesound Error: {e}[/red]")
        console.print("[dim]   Set FREESOUND_API_KEY in .env file[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Freesound Error: {e}[/red]")
        return False

def test_unified_manager():
    """Test Unified Media Manager"""
    console.print("\n[bold cyan]Testing Unified Media Manager...[/bold cyan]")
    
    try:
        manager = UnifiedMediaManager()
        
        # Test video search
        videos = manager.search_videos("sunset", num_results=2)
        console.print(f"[green]✅ Video search: {len(videos)} results[/green]")
        
        # Test image search
        images = manager.search_images("workspace", num_results=2)
        console.print(f"[green]✅ Image search: {len(images)} results[/green]")
        
        # Test audio search
        audio = manager.search_audio("calm music", num_results=2)
        console.print(f"[green]✅ Audio search: {len(audio)} results[/green]")
        
        console.print("[green]✅ Unified Manager working perfectly![/green]")
        return True
        
    except RuntimeError as e:
        console.print(f"[red]❌ Unified Manager Error: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Unified Manager Error: {e}[/red]")
        return False

def main():
    console.print(Panel.fit(
        "[bold cyan]🎬 Free Media Providers Test Suite[/bold cyan]\n"
        "[dim]Testing Pexels, Pixabay, Unsplash, Freesound, FFmpeg[/dim]",
        border_style="cyan"
    ))
    
    results = {
        'FFmpeg': test_ffmpeg(),
        'Pexels': test_pexels(),
        'Pixabay': test_pixabay(),
        'Unsplash': test_unsplash(),
        'Freesound': test_freesound(),
        'Unified Manager': test_unified_manager()
    }
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold]Test Summary:[/bold]")
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "[green]✅ PASS[/green]" if result else "[red]❌ FAIL[/red]"
        console.print(f"  {status}  {name}")
    
    console.print("="*60)
    console.print(f"\n[bold]Results: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("[green bold]🎉 All systems operational![/green bold]")
    elif passed > 0:
        console.print("[yellow]⚠️  Some providers need API keys. See setup guide.[/yellow]")
    else:
        console.print("[red]❌ No providers configured. Run setup first.[/red]")
    
    # Next steps
    if passed < total:
        console.print("\n[bold cyan]Next Steps:[/bold cyan]")
        console.print("1. Get API keys from:")
        if not results['Pexels']:
            console.print("   • Pexels: https://www.pexels.com/api/new/")
        if not results['Pixabay']:
            console.print("   • Pixabay: https://pixabay.com/api/docs/")
        if not results['Unsplash']:
            console.print("   • Unsplash: https://unsplash.com/oauth/applications")
        if not results['Freesound']:
            console.print("   • Freesound: https://freesound.org/apiv2/apply/")
        if not results['FFmpeg']:
            console.print("   • FFmpeg: brew install ffmpeg")
        
        console.print("\n2. Add keys to .env file:")
        console.print("   PEXELS_API_KEY=your_key")
        console.print("   PIXABAY_API_KEY=your_key")
        console.print("   UNSPLASH_ACCESS_KEY=your_key")
        console.print("   FREESOUND_API_KEY=your_key")
        
        console.print("\n3. Run this test again to verify")

if __name__ == "__main__":
    main()
