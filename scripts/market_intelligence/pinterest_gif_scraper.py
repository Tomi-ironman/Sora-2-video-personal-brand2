#!/usr/bin/env python3
"""
Pinterest GIF Scraper
Downloads animated GIFs from Pinterest - Perfect for B-roll!
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import requests
import time
from rich.console import Console
from rich.progress import Progress
import sys

console = Console()


def scrape_pinterest_gifs(query, num_gifs=20, output_dir="/Users/tomi/Desktop/pinterest_gifs"):
    """
    Scrape GIFs from Pinterest
    
    Args:
        query: Search term (e.g., "workspace aesthetic", "office culture")
        num_gifs: How many GIFs to download
        output_dir: Where to save GIFs
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest GIF Scraper[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[dim]Downloading {num_gifs} animated GIFs...[/dim]\n")
    
    # Create output directory
    output_path = Path(output_dir) / query.replace(' ', '_')
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_gifs = []
    
    with sync_playwright() as p:
        # Launch browser
        console.print("[cyan]Launching browser...[/cyan]")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Search for GIFs on Pinterest - try multiple search strategies
        search_queries = [
            f"{query} animated gif",
            f"{query} gif animation",
            f"{query} moving"
        ]
        
        gif_urls = []
        
        for search_term in search_queries:
            if len(gif_urls) >= num_gifs:
                break
                
            search_url = f"https://www.pinterest.com/search/pins/?q={search_term.replace(' ', '%20')}"
            console.print(f"[dim]Searching: {search_term}...[/dim]")
            
            page.goto(search_url)
            time.sleep(3)
            
            # Scroll to load more content
            for i in range(10):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1.5)
            
            # Get page content and extract GIF URLs
            page_content = page.content()
            
            # Find all .gif URLs in the page
            import re
            found_gifs = re.findall(r'https://i\.pinimg\.com/originals/[^"\']+\.gif', page_content)
            gif_urls.extend(found_gifs)
        
        # Remove duplicates
        gif_urls = list(set(gif_urls))
        
        console.print(f"\n[cyan]Extracting GIF URLs from page...[/cyan]")
        
        console.print(f"[green]Found {len(gif_urls)} unique GIF URLs![/green]\n")
        
        if len(gif_urls) == 0:
            console.print("[yellow]⚠️  No GIFs found. Try different search terms.[/yellow]")
            browser.close()
            return []
        
        # Download GIFs
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=min(num_gifs, len(gif_urls)))
            
            for i, gif_url in enumerate(gif_urls[:num_gifs]):
                try:
                    console.print(f"[dim]Downloading {i+1}/{min(num_gifs, len(gif_urls))}...[/dim]")
                    
                    # Download GIF
                    response = requests.get(gif_url, timeout=15, stream=True)
                    
                    if response.status_code == 200:
                        filename = f"{query.replace(' ', '_')}_{i + 1:03d}.gif"
                        filepath = output_path / filename
                        
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
                        
                        if file_size > 0.01:  # Only count if > 10KB
                            downloaded_gifs.append(str(filepath))
                            progress.update(task, advance=1)
                            console.print(f"[green]✓[/green] {filename} ({file_size:.1f} MB)")
                        else:
                            filepath.unlink()  # Delete tiny file
                            console.print(f"[dim]Skipped tiny file[/dim]")
                    
                except Exception as e:
                    console.print(f"[red]Failed: {str(e)[:50]}[/red]")
                    continue
        
        browser.close()
    
    # Summary
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded_gifs)} GIFs![/bold green]")
    console.print(f"[cyan]📁 Saved to: {output_path}/[/cyan]\n")
    
    if len(downloaded_gifs) > 0:
        total_size = sum(Path(g).stat().st_size for g in downloaded_gifs) / (1024 * 1024)
        console.print(f"[cyan]📊 Total size: {total_size:.1f} MB[/cyan]\n")
    
    return downloaded_gifs


def convert_gifs_to_videos(gif_dir, output_dir="/Users/tomi/Desktop/pinterest_videos_from_gifs"):
    """
    Convert downloaded GIFs to MP4 videos
    Perfect for video editing!
    """
    
    console.print(f"\n[bold cyan]🎬 Converting GIFs to Videos[/bold cyan]\n")
    
    gif_path = Path(gif_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    gifs = list(gif_path.glob("*.gif"))
    
    if len(gifs) == 0:
        console.print("[yellow]No GIFs found to convert[/yellow]")
        return []
    
    console.print(f"[cyan]Found {len(gifs)} GIFs to convert...[/cyan]\n")
    
    converted = []
    
    try:
        from moviepy.editor import VideoFileClip
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Converting...", total=len(gifs))
            
            for gif in gifs:
                try:
                    # Convert GIF to MP4
                    clip = VideoFileClip(str(gif))
                    
                    output_file = output_path / f"{gif.stem}.mp4"
                    
                    clip.write_videofile(
                        str(output_file),
                        codec='libx264',
                        audio=False,
                        verbose=False,
                        logger=None
                    )
                    
                    clip.close()
                    
                    file_size = output_file.stat().st_size / (1024 * 1024)
                    console.print(f"[green]✓[/green] {output_file.name} ({file_size:.1f} MB)")
                    
                    converted.append(str(output_file))
                    progress.update(task, advance=1)
                    
                except Exception as e:
                    console.print(f"[red]Failed {gif.name}: {str(e)[:40]}[/red]")
                    continue
        
        console.print(f"\n[bold green]✅ Converted {len(converted)} GIFs to videos![/bold green]")
        console.print(f"[cyan]📁 Saved to: {output_path}/[/cyan]\n")
        
        return converted
        
    except ImportError:
        console.print("[yellow]⚠️  moviepy not installed[/yellow]")
        console.print("[cyan]Install with: pip install moviepy[/cyan]")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Pinterest GIF Scraper[/bold]\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python3 pinterest_gif_scraper.py "search query" [num_gifs]')
        console.print('  python3 pinterest_gif_scraper.py --convert "gif_directory"\n')
        console.print("[bold]Examples:[/bold]")
        console.print('  python3 pinterest_gif_scraper.py "creative workspace" 30')
        console.print('  python3 pinterest_gif_scraper.py "office culture" 25')
        console.print('  python3 pinterest_gif_scraper.py "startup vibes" 20')
        console.print('  python3 pinterest_gif_scraper.py --convert "pinterest_gifs/workspace"\n')
        console.print("[bold cyan]💡 Tips:[/bold cyan]")
        console.print('  • GIFs are perfect for B-roll!')
        console.print('  • Convert to MP4 for easier editing')
        console.print('  • Loop them for longer clips')
        sys.exit(1)
    
    if sys.argv[1] == "--convert":
        # Convert GIFs to videos
        gif_dir = sys.argv[2]
        convert_gifs_to_videos(gif_dir)
    else:
        # Search and download GIFs
        query = sys.argv[1]
        num_gifs = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        
        result = scrape_pinterest_gifs(query, num_gifs)
        
        if len(result) > 0:
            console.print("\n[bold]Want to convert to videos?[/bold]")
            console.print(f'[dim]python3 pinterest_gif_scraper.py --convert "pinterest_gifs/{query.replace(" ", "_")}"[/dim]')
