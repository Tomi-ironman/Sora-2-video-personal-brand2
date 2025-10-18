#!/usr/bin/env python3
"""
Pinterest Image Scraper
Downloads high-quality creative images from Pinterest
Perfect for B-roll, reference, and culture videos
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import requests
import time
from rich.console import Console
from rich.progress import Progress
import sys

console = Console()


def scrape_pinterest_images(query, num_images=20, output_dir="/Users/tomi/Desktop/pinterest_images"):
    """
    Scrape images from Pinterest using Playwright
    
    Args:
        query: Search term (e.g., "creative workspace", "culture videos")
        num_images: How many images to download
        output_dir: Where to save images
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Image Scraper[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[dim]Downloading {num_images} high-quality images...[/dim]\n")
    
    # Create output directory
    output_path = Path(output_dir) / query.replace(' ', '_')
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_images = []
    
    with sync_playwright() as p:
        # Launch browser
        console.print("[cyan]Launching browser...[/cyan]")
        browser = p.chromium.launch(headless=False)  # Set to True for background
        page = browser.new_page()
        
        # Go to Pinterest search
        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        console.print(f"[dim]Opening: {search_url}[/dim]\n")
        
        page.goto(search_url)
        time.sleep(3)  # Wait for page load
        
        # Scroll to load more images
        console.print("[cyan]Loading images...[/cyan]")
        for i in range(5):  # Scroll 5 times to load more
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
        
        # Find all image elements
        console.print("[cyan]Finding images...[/cyan]\n")
        
        # Pinterest uses different selectors, try multiple
        image_selectors = [
            'img[src*="pinimg.com"]',
            'img[alt]',
            'div[data-test-id="pin"] img'
        ]
        
        all_images = []
        for selector in image_selectors:
            try:
                images = page.query_selector_all(selector)
                all_images.extend(images)
            except:
                continue
        
        console.print(f"[green]Found {len(all_images)} images[/green]\n")
        
        # Download images with quality control
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=num_images)
            
            downloaded = 0
            checked = 0
            
            for img in all_images:
                if downloaded >= num_images:
                    break
                
                if checked >= num_images * 3:  # Check up to 3x to find quality images
                    break
                
                try:
                    checked += 1
                    
                    # Get image URL
                    img_url = img.get_attribute('src')
                    
                    if not img_url or 'data:image' in img_url:
                        continue
                    
                    # Get high-res version (Pinterest uses 'originals' for full size)
                    if '236x' in img_url:
                        img_url = img_url.replace('236x', 'originals')
                    elif '474x' in img_url:
                        img_url = img_url.replace('474x', 'originals')
                    
                    # Download image
                    response = requests.get(img_url, timeout=10)
                    
                    if response.status_code == 200:
                        # Quality control: Check file size
                        file_size = len(response.content)
                        
                        # Skip tiny images (likely low quality or thumbnails)
                        if file_size < 50000:  # Less than 50KB
                            console.print(f"[dim]Skipped: Too small ({file_size/1024:.0f}KB)[/dim]")
                            continue
                        
                        # Skip huge files (might be corrupted or wrong format)
                        if file_size > 20000000:  # More than 20MB
                            console.print(f"[dim]Skipped: Too large ({file_size/1024/1024:.1f}MB)[/dim]")
                            continue
                        
                        # Save image
                        ext = 'jpg' if 'jpeg' in img_url or 'jpg' in img_url else 'png'
                        filename = f"{query.replace(' ', '_')}_{downloaded + 1:03d}.{ext}"
                        filepath = output_path / filename
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        # Verify image can be opened (quality check)
                        try:
                            from PIL import Image
                            with Image.open(filepath) as test_img:
                                width, height = test_img.size
                                
                                # Skip low resolution images
                                if width < 500 or height < 500:
                                    filepath.unlink()
                                    console.print(f"[dim]Skipped: Low res ({width}x{height})[/dim]")
                                    continue
                        except:
                            filepath.unlink()
                            console.print(f"[dim]Skipped: Corrupted image[/dim]")
                            continue
                        
                        downloaded_images.append(str(filepath))
                        downloaded += 1
                        
                        progress.update(task, advance=1)
                        console.print(f"[green]✓[/green] {filename} ({file_size/1024:.0f}KB, {width}x{height})")
                        
                except Exception as e:
                    console.print(f"[dim]Skipped: {str(e)[:50]}[/dim]")
                    continue
    
    # Summary
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded_images)} images![/bold green]")
    console.print(f"[cyan]📁 Saved to: {output_path}/[/cyan]\n")
    
    return downloaded_images


def download_pinterest_boards(board_url, num_images=50, output_dir="pinterest_boards"):
    """
    Download all images from a Pinterest board
    Perfect for culture/aesthetic collections
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Board Downloader[/bold cyan]")
    console.print(f"[yellow]Board: {board_url}[/yellow]\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(board_url)
        time.sleep(3)
        
        # Scroll to load all pins
        console.print("[cyan]Loading board...[/cyan]")
        for i in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
        
        # Find images
        images = page.query_selector_all('img[src*="pinimg.com"]')
        
        console.print(f"[green]Found {len(images)} pins[/green]\n")
        
        downloaded = 0
        
        for img in images[:num_images]:
            try:
                img_url = img.get_attribute('src')
                
                if not img_url or 'data:image' in img_url:
                    continue
                
                # Get high-res
                img_url = img_url.replace('236x', 'originals').replace('474x', 'originals')
                
                response = requests.get(img_url, timeout=10)
                
                if response.status_code == 200:
                    filename = f"board_pin_{downloaded + 1:03d}.jpg"
                    filepath = output_path / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    console.print(f"[green]✓[/green] {filename}")
                    downloaded += 1
                    
            except Exception as e:
                continue
        
        browser.close()
    
    console.print(f"\n[bold green]✅ Downloaded {downloaded} images from board![/bold green]")
    return downloaded


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Pinterest Image Scraper[/bold]\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python3 pinterest_scraper.py "search query" [num_images]')
        console.print('  python3 pinterest_scraper.py --board "board_url" [num_images]\n')
        console.print("[bold]Examples:[/bold]")
        console.print('  python3 pinterest_scraper.py "creative workspace" 30')
        console.print('  python3 pinterest_scraper.py "culture aesthetic" 50')
        console.print('  python3 pinterest_scraper.py "modern office vibes" 20')
        console.print('  python3 pinterest_scraper.py --board "https://pinterest.com/board/..." 50')
        sys.exit(1)
    
    if sys.argv[1] == "--board":
        # Download from board
        board_url = sys.argv[2]
        num_images = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        download_pinterest_boards(board_url, num_images)
    else:
        # Search and download
        query = sys.argv[1]
        num_images = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        scrape_pinterest_images(query, num_images)
