#!/usr/bin/env python3
"""
Download Illustrated/Animated GIFs from Pinterest
Perfect for your illustration aesthetic style
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import requests
import time
from rich.console import Console
from rich.progress import Progress

console = Console()

def download_illustrated_gifs(query, num_gifs=30, output_dir="animated_illustrations"):
    """
    Download animated illustration GIFs from Pinterest
    
    Args:
        query: Search term (e.g., "animated illustration", "motion graphics gif")
        num_gifs: How many GIFs to download
        output_dir: Where to save GIFs
    """
    
    console.print(f"\n[bold cyan]🎨 Illustrated GIF Downloader[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[dim]Downloading {num_gifs} animated illustrations...[/dim]\n")
    
    # Create output directory
    output_path = Path(output_dir) / query.replace(' ', '_')
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_gifs = []
    
    with sync_playwright() as p:
        # Launch browser
        console.print("[cyan]Launching browser...[/cyan]")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Go to Pinterest search
        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        console.print(f"[dim]Opening: {search_url}[/dim]\n")
        
        page.goto(search_url)
        time.sleep(4)  # Wait for page load
        
        # Scroll to load more images
        console.print("[cyan]Loading GIFs...[/cyan]")
        for i in range(8):  # More scrolls to find GIFs
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
        
        # Find all image/video elements (GIFs can be either)
        console.print("[cyan]Finding animated content...[/cyan]\n")
        
        # Pinterest shows GIFs as images or videos
        selectors = [
            'img[src*=".gif"]',
            'img[src*="pinimg.com"]',
            'video source',
            'div[data-test-id="pin"] img'
        ]
        
        all_media = []
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                all_media.extend(elements)
            except:
                continue
        
        console.print(f"[green]Found {len(all_media)} media items[/green]\n")
        
        # Download GIFs
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=num_gifs)
            
            downloaded = 0
            checked = 0
            
            for media in all_media:
                if downloaded >= num_gifs:
                    break
                
                if checked >= num_gifs * 5:  # Check up to 5x to find GIFs
                    break
                
                try:
                    checked += 1
                    
                    # Get media URL
                    media_url = media.get_attribute('src')
                    
                    if not media_url or 'data:image' in media_url:
                        continue
                    
                    # Check if it's a GIF or looks like one
                    is_gif = '.gif' in media_url.lower()
                    
                    # Try to get high-res version
                    if '236x' in media_url:
                        media_url = media_url.replace('236x', 'originals')
                    elif '474x' in media_url:
                        media_url = media_url.replace('474x', 'originals')
                    
                    # Download
                    response = requests.get(media_url, timeout=15)
                    
                    if response.status_code == 200:
                        file_size = len(response.content)
                        
                        # GIFs can be larger
                        if is_gif:
                            if file_size < 100000:  # Skip tiny GIFs (less than 100KB)
                                console.print(f"[dim]Skipped: Too small ({file_size/1024:.0f}KB)[/dim]")
                                continue
                            
                            if file_size > 50000000:  # Skip huge files (more than 50MB)
                                console.print(f"[dim]Skipped: Too large ({file_size/1024/1024:.1f}MB)[/dim]")
                                continue
                            
                            # Save GIF
                            filename = f"{query.replace(' ', '_')}_{downloaded + 1:03d}.gif"
                            filepath = output_path / filename
                            
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            downloaded_gifs.append(str(filepath))
                            downloaded += 1
                            
                            progress.update(task, advance=1)
                            console.print(f"[green]✓[/green] {filename} ({file_size/1024:.0f}KB)")
                        
                        else:
                            # Skip non-GIF for this downloader
                            continue
                        
                except Exception as e:
                    console.print(f"[dim]Skipped: {str(e)[:50]}[/dim]")
                    continue
        
        browser.close()
    
    # Summary
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded_gifs)} animated GIFs![/bold green]")
    console.print(f"[cyan]📁 Saved to: {output_path}/[/cyan]\n")
    
    return downloaded_gifs


# Best search queries for illustrated GIFs
ILLUSTRATION_GIF_QUERIES = [
    # General animated illustration
    "animated illustration gif",
    "motion graphics illustration",
    "2d animation illustration loop",
    "illustrated animation gif",
    
    # Specific artists (like Lorenzo Mercanti)
    "lorenzo mercanti gif",
    "illustration animation gif artist",
    "hand drawn animation gif",
    
    # Style-specific
    "minimalist animation gif",
    "abstract animation illustration",
    "geometric animation gif",
    "surreal animation gif art",
    
    # Future/past themes (as you mentioned)
    "futuristic illustration animation",
    "retro animation gif illustration",
    "vintage animation illustration",
    "sci fi animation gif art",
    
    # Japanese style (to match your current content)
    "japanese animation gif illustration",
    "asian art animation gif",
    "ukiyo-e style animation",
]


if __name__ == "__main__":
    console.print("\n[bold]🎨 ILLUSTRATION GIF FINDER[/bold]\n")
    console.print("[yellow]Best search queries for your style:[/yellow]\n")
    
    for i, query in enumerate(ILLUSTRATION_GIF_QUERIES[:10], 1):
        console.print(f"  {i}. [cyan]{query}[/cyan]")
    
    console.print("\n[dim]Usage: python3 download_illustration_gifs.py[/dim]\n")
    
    # Example: Download some animated illustrations
    print("Starting download with: 'animated illustration gif'")
    download_illustrated_gifs("animated illustration gif", num_gifs=20)
