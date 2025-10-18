#!/usr/bin/env python3
"""
Mixed Media Downloader - Downloads BOTH static illustrations and animated GIFs
Uses 3X search strategy for GIFs to ensure we find enough animated content
"""

from pinterest_scraper import scrape_pinterest_images
from pinterest_gif_downloader import PinterestGIFDownloader
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
import time

console = Console()


def download_mixed_media(
    topic,
    num_static=20,
    num_gifs=5,
    output_dir=None
):
    """
    Download mixed media: static illustrations + animated GIFs
    
    Args:
        topic: Topic name (e.g., "greek culture")
        num_static: Number of static illustrations to download
        num_gifs: Number of GIFs to attempt (will search 3x this amount)
        output_dir: Output directory (auto-generated if None)
    
    Returns:
        dict with paths to static images and GIFs
    """
    
    console.print(f"\n[bold cyan]🎨 MIXED MEDIA DOWNLOADER[/bold cyan]")
    console.print(f"[yellow]Topic: {topic}[/yellow]")
    console.print(f"[yellow]Target: {num_static} static + {num_gifs} GIFs[/yellow]\n")
    
    if output_dir is None:
        output_dir = f"pinterest_downloads/mixed_{topic.replace(' ', '_')}"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = {
        'topic': topic,
        'static_images': [],
        'gifs': [],
        'all_media': [],
        'output_dir': str(output_path)
    }
    
    # STEP 1: Download static illustrations (fast and reliable)
    console.print("[bold cyan]━━━ STEP 1: Static Illustrations ━━━[/bold cyan]\n")
    
    static_query = f"{topic} art illustration"
    console.print(f"[cyan]🖼️  Downloading {num_static} static illustrations...[/cyan]")
    console.print(f"[dim]Query: {static_query}[/dim]\n")
    
    try:
        urls = scrape_pinterest_images(
            query=static_query,
            num_images=num_static,
            output_dir=output_dir
        )
        
        # Find downloaded images
        static_dir = output_path / static_query.replace(' ', '_')
        if static_dir.exists():
            static_images = list(static_dir.glob("*.jpg")) + list(static_dir.glob("*.png"))
            results['static_images'] = [str(img) for img in static_images]
            console.print(f"[green]✅ Downloaded {len(static_images)} static images[/green]\n")
    
    except Exception as e:
        console.print(f"[red]❌ Static download error: {str(e)[:100]}[/red]\n")
    
    # STEP 2: Download GIFs (3X search strategy since they're rare)
    console.print("[bold cyan]━━━ STEP 2: Animated GIFs (3X Strategy) ━━━[/bold cyan]\n")
    
    # Search 3X more pins to find enough GIFs
    search_multiplier = 3
    pins_to_check = num_gifs * search_multiplier
    
    gif_query = f"{topic} gif art illustration animated"
    console.print(f"[cyan]🎬 Searching for {num_gifs} GIFs (checking {pins_to_check} pins)...[/cyan]")
    console.print(f"[dim]Query: {gif_query}[/dim]")
    console.print(f"[dim]Strategy: 3X search to compensate for GIF rarity[/dim]\n")
    
    gif_downloader = PinterestGIFDownloader(f"{output_dir}/gifs")
    
    # Import search functionality
    from playwright.sync_api import sync_playwright
    
    pin_urls = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            search_url = f"https://www.pinterest.com/search/pins/?q={gif_query.replace(' ', '%20')}"
            page.goto(search_url)
            time.sleep(3)
            
            # Scroll MORE to load enough pins for 3X strategy
            for i in range(10):  # More scrolling = more pins
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                if i % 3 == 0:
                    console.print(f"[dim]  Loading more pins... ({i+1}/10)[/dim]")
            
            # Extract pin URLs
            links = page.query_selector_all('a[href*="/pin/"]')
            for link in links:
                href = link.get_attribute('href')
                if href and '/pin/' in href:
                    full_url = f"https://www.pinterest.com{href}" if href.startswith('/') else href
                    pin_urls.append(full_url)
            
            browser.close()
        
        # Remove duplicates and take enough for 3X strategy
        pin_urls = list(set(pin_urls))[:pins_to_check]
        
        console.print(f"[green]✅ Found {len(pin_urls)} pins to check for GIFs[/green]\n")
        
        # Check each pin for animated content
        gifs_found = []
        
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Finding GIFs (target: {num_gifs})...", total=num_gifs)
            
            for pin_url in pin_urls:
                if len(gifs_found) >= num_gifs:
                    break
                
                console.print(f"[dim]Checking pin {len(gifs_found)+1}/{num_gifs}...[/dim]")
                
                result = gif_downloader.download_animated_from_pin(pin_url, convert_videos=True)
                
                if result:
                    gifs_found.append(result['local_path'])
                    progress.update(task, advance=1)
                    console.print(f"[green]  ✅ GIF {len(gifs_found)}/{num_gifs} found![/green]")
                
                # Rate limiting
                time.sleep(2)
        
        results['gifs'] = gifs_found
        console.print(f"\n[green]✅ Found {len(gifs_found)} GIFs[/green]\n")
    
    except Exception as e:
        console.print(f"[red]❌ GIF download error: {str(e)[:100]}[/red]\n")
    
    # STEP 3: Combine media intelligently
    console.print("[bold cyan]━━━ STEP 3: Organizing Mixed Media ━━━[/bold cyan]\n")
    
    # Strategy: Sprinkle GIFs throughout static images
    all_media = []
    
    if results['gifs'] and results['static_images']:
        # Mix: Start with GIF, then static, sprinkle more GIFs throughout
        gif_positions = [0]  # First item is a GIF
        
        # Calculate where to place remaining GIFs
        if len(results['gifs']) > 1 and len(results['static_images']) > 0:
            spacing = len(results['static_images']) // (len(results['gifs']) - 1) if len(results['gifs']) > 1 else 0
            for i in range(1, len(results['gifs'])):
                pos = i * spacing
                gif_positions.append(pos)
        
        # Build mixed list
        gif_idx = 0
        static_idx = 0
        
        for i in range(len(results['static_images']) + len(results['gifs'])):
            if i in gif_positions and gif_idx < len(results['gifs']):
                all_media.append({
                    'path': results['gifs'][gif_idx],
                    'type': 'gif'
                })
                gif_idx += 1
            elif static_idx < len(results['static_images']):
                all_media.append({
                    'path': results['static_images'][static_idx],
                    'type': 'static'
                })
                static_idx += 1
    
    elif results['static_images']:
        # Fallback: only static
        all_media = [{'path': img, 'type': 'static'} for img in results['static_images']]
    
    results['all_media'] = all_media
    
    # Summary
    console.print(f"[bold green]✅ MIXED MEDIA READY![/bold green]\n")
    console.print(f"[cyan]📊 Media Composition:[/cyan]")
    console.print(f"[cyan]  • Static images: {len(results['static_images'])}[/cyan]")
    console.print(f"[cyan]  • Animated GIFs: {len(results['gifs'])}[/cyan]")
    console.print(f"[cyan]  • Total media: {len(all_media)}[/cyan]\n")
    
    if all_media:
        console.print(f"[cyan]🎬 Media Order (first 10):[/cyan]")
        for i, item in enumerate(all_media[:10], 1):
            icon = "🎬" if item['type'] == 'gif' else "🖼️"
            filename = Path(item['path']).name[:40]
            console.print(f"  {i}. {icon} {filename}")
        
        if len(all_media) > 10:
            console.print(f"  ... and {len(all_media) - 10} more")
    
    console.print(f"\n[cyan]📁 Output: {output_path}/[/cyan]\n")
    
    return results


if __name__ == "__main__":
    # Example: Download mixed media for Greek culture
    results = download_mixed_media(
        topic="greek culture",
        num_static=18,  # Enough for video
        num_gifs=3,     # A few GIFs sprinkled in
    )
    
    console.print(f"\n[bold]✅ Download Complete![/bold]")
    console.print(f"[green]Ready for video creation with mixed static + animated content![/green]\n")
