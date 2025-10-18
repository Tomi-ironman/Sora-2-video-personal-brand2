#!/usr/bin/env python3
"""
Pinterest Video Scraper
Downloads high-quality videos from Pinterest
Perfect for B-roll and culture videos!
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import requests
import time
from rich.console import Console
from rich.progress import Progress
import sys
import re

console = Console()


def scrape_pinterest_videos(query, num_videos=10, output_dir="/Users/tomi/Desktop/pinterest_videos"):
    """
    Scrape videos from Pinterest using Playwright + Network Interception
    
    Args:
        query: Search term (e.g., "creative workspace", "startup culture")
        num_videos: How many videos to download
        output_dir: Where to save videos
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Video Scraper[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[dim]Downloading {num_videos} high-quality videos...[/dim]\n")
    
    # Create output directory
    output_path = Path(output_dir) / query.replace(' ', '_')
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_videos = []
    video_urls_found = []
    
    with sync_playwright() as p:
        # Launch browser
        console.print("[cyan]Launching browser...[/cyan]")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Intercept network requests to catch video URLs
        def handle_response(response):
            url = response.url
            # Pinterest videos are served from v.pinimg.com or v1.pinimg.com
            if '.mp4' in url and ('v.pinimg.com' in url or 'v1.pinimg.com' in url):
                if url not in video_urls_found:
                    video_urls_found.append(url)
                    console.print(f"[green]🎥 Found video: {url[:60]}...[/green]")
        
        page.on("response", handle_response)
        
        # Go to Pinterest video search
        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}&rs=typed"
        console.print(f"[dim]Opening: {search_url}[/dim]\n")
        
        page.goto(search_url)
        time.sleep(3)
        
        # Scroll to load more pins
        console.print("[cyan]Loading pins...[/cyan]")
        for i in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
        
        # Find pins and hover over them to trigger video loads
        console.print("[cyan]Hovering over pins to load videos...[/cyan]")
        pins = page.query_selector_all('div[data-test-id="pin"]')
        
        console.print(f"[green]Found {len(pins)} pins, checking for videos...[/green]\n")
        
        for i, pin in enumerate(pins[:num_videos * 3]):  # Check 3x to find enough videos
            try:
                # Hover over pin to trigger video load
                pin.hover()
                time.sleep(1)  # Wait for video to load
                
                if len(video_urls_found) >= num_videos:
                    console.print(f"[green]Found {len(video_urls_found)} videos![/green]")
                    break
                    
            except:
                continue
        
        console.print(f"\n[cyan]Captured {len(video_urls_found)} video URLs from network![/cyan]\n")
        
        browser.close()
        
        # Download the captured videos
        if len(video_urls_found) == 0:
            console.print("[yellow]⚠️  No videos found. Try:[/yellow]")
            console.print('[dim]  • Add "video" to your search[/dim]')
            console.print('[dim]  • Try: "workspace video", "office tour", "aesthetic video"[/dim]')
            return []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading videos...", total=min(num_videos, len(video_urls_found)))
            
            for i, video_url in enumerate(video_urls_found[:num_videos]):
                try:
                    console.print(f"[dim]Downloading {i+1}/{min(num_videos, len(video_urls_found))}...[/dim]")
                    
                    # Download video
                    response = requests.get(video_url, timeout=30, stream=True)
                    
                    if response.status_code == 200:
                        # Save video
                        filename = f"{query.replace(' ', '_')}_{i + 1:03d}.mp4"
                        filepath = output_path / filename
                        
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
                        
                        if file_size > 0.05:  # Only count if > 50KB
                            downloaded_videos.append(str(filepath))
                            progress.update(task, advance=1)
                            console.print(f"[green]✓[/green] {filename} ({file_size:.1f} MB)")
                        else:
                            filepath.unlink()  # Delete tiny file
                            console.print(f"[dim]Skipped tiny file[/dim]")
                    
                except Exception as e:
                    console.print(f"[red]Failed: {str(e)[:50]}[/red]")
                    continue
    
    # Summary
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded_videos)} videos![/bold green]")
    console.print(f"[cyan]📁 Saved to: {output_path}/[/cyan]\n")
    
    if len(downloaded_videos) > 0:
        total_size = sum(Path(v).stat().st_size for v in downloaded_videos) / (1024 * 1024)
        console.print(f"[cyan]📊 Total size: {total_size:.1f} MB[/cyan]\n")
    
    return downloaded_videos


def download_pinterest_video_pins(pin_urls, output_dir="/Users/tomi/Desktop/pinterest_videos"):
    """
    Download videos from specific Pinterest pin URLs
    
    Args:
        pin_urls: List of Pinterest pin URLs
        output_dir: Where to save videos
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Pin Video Downloader[/bold cyan]")
    console.print(f"[yellow]Downloading {len(pin_urls)} pins...[/yellow]\n")
    
    output_path = Path(output_dir) / "pin_videos"
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        for i, pin_url in enumerate(pin_urls):
            try:
                console.print(f"[cyan]Opening pin {i+1}/{len(pin_urls)}...[/cyan]")
                page.goto(pin_url)
                time.sleep(2)
                
                # Find video on pin page
                video = page.query_selector('video')
                
                if video:
                    video_url = video.get_attribute('src')
                    
                    if not video_url:
                        sources = video.query_selector_all('source')
                        for source in sources:
                            video_url = source.get_attribute('src')
                            if video_url:
                                break
                    
                    if video_url and 'data:' not in video_url:
                        # Download
                        response = requests.get(video_url, timeout=30, stream=True)
                        
                        if response.status_code == 200:
                            filename = f"pin_video_{i+1:03d}.mp4"
                            filepath = output_path / filename
                            
                            with open(filepath, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            file_size = filepath.stat().st_size / (1024 * 1024)
                            console.print(f"[green]✓[/green] {filename} ({file_size:.1f} MB)")
                            downloaded.append(str(filepath))
                
            except Exception as e:
                console.print(f"[red]Failed: {str(e)[:60]}[/red]")
                continue
        
        browser.close()
    
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded)} videos![/bold green]")
    return downloaded


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Pinterest Video Scraper[/bold]\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python3 pinterest_video_scraper.py "search query" [num_videos]')
        console.print('  python3 pinterest_video_scraper.py --pins "url1" "url2" "url3"\n')
        console.print("[bold]Examples:[/bold]")
        console.print('  python3 pinterest_video_scraper.py "creative workspace video" 15')
        console.print('  python3 pinterest_video_scraper.py "startup culture video" 20')
        console.print('  python3 pinterest_video_scraper.py "modern office video" 10')
        console.print('  python3 pinterest_video_scraper.py --pins "https://pin.it/..." "https://pin.it/..."\n')
        console.print("[bold cyan]💡 Tips:[/bold cyan]")
        console.print('  • Add "video" to search terms for better results')
        console.print('  • Try: "aesthetic video", "vlog style", "cinematic"')
        console.print('  • Videos are typically 5-30 seconds (perfect for B-roll!)')
        sys.exit(1)
    
    if sys.argv[1] == "--pins":
        # Download from specific pins
        pin_urls = sys.argv[2:]
        download_pinterest_video_pins(pin_urls)
    else:
        # Search and download
        query = sys.argv[1]
        num_videos = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        scrape_pinterest_videos(query, num_videos)
