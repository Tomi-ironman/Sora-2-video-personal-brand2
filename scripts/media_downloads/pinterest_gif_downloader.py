#!/usr/bin/env python3
"""
Pinterest GIF/Animated Media Downloader
Specifically retrieves animated content (GIFs or MP4/WebM videos that act like GIFs)
Following the agent instruction set for reliable GIF detection
"""

import requests
import re
import json
import time
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

console = Console()


class PinterestGIFDownloader:
    """Smart Pinterest GIF downloader with type detection"""
    
    def __init__(self, output_dir="pinterest_gifs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def extract_media_urls_from_pin(self, pin_url):
        """
        Extract media URLs from a Pinterest pin page
        Returns: list of candidate media URLs
        """
        console.print(f"[cyan]🔍 Analyzing pin: {pin_url[:50]}...[/cyan]")
        
        media_urls = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(pin_url, timeout=10000)
                page.wait_for_timeout(2000)
                
                # Get page content
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Method 1: Look for og:video meta tags
                og_video = soup.find('meta', property='og:video')
                if og_video and og_video.get('content'):
                    media_urls.append(og_video['content'])
                    console.print(f"[dim]  Found og:video[/dim]")
                
                # Method 2: Look for og:image meta tags (might be animated)
                og_image = soup.find('meta', property='og:image')
                if og_image and og_image.get('content'):
                    media_urls.append(og_image['content'])
                    console.print(f"[dim]  Found og:image[/dim]")
                
                # Method 3: Extract from JSON-LD
                json_ld = soup.find('script', type='application/ld+json')
                if json_ld:
                    try:
                        data = json.loads(json_ld.string)
                        if 'video' in data:
                            media_urls.append(data['video'].get('contentUrl', ''))
                        if 'image' in data:
                            if isinstance(data['image'], list):
                                media_urls.extend(data['image'])
                            else:
                                media_urls.append(data['image'])
                        console.print(f"[dim]  Found JSON-LD data[/dim]")
                    except:
                        pass
                
                # Method 4: Look for video elements in page
                video_elements = page.query_selector_all('video source')
                for video_el in video_elements:
                    src = video_el.get_attribute('src')
                    if src:
                        media_urls.append(src)
                        console.print(f"[dim]  Found video element[/dim]")
                
            except Exception as e:
                console.print(f"[yellow]  ⚠️  Could not load pin: {str(e)[:50]}[/yellow]")
            
            browser.close()
        
        # Clean and deduplicate URLs
        media_urls = [url for url in media_urls if url and url.startswith('http')]
        media_urls = list(set(media_urls))  # Remove duplicates
        
        return media_urls
    
    def check_media_type(self, url):
        """
        Check if URL is GIF, animated video, or static image
        Returns: ('gif'|'animated_video'|'static_image', content_type, size_mb)
        """
        try:
            # HEAD request to check Content-Type without downloading
            response = self.session.head(url, allow_redirects=True, timeout=10)
            
            content_type = response.headers.get('content-type', '').lower()
            content_length = int(response.headers.get('content-length', 0))
            size_mb = content_length / (1024 * 1024)
            
            # Classify based on Content-Type
            if 'image/gif' in content_type:
                return 'gif', content_type, size_mb
            elif 'video/mp4' in content_type or 'video/webm' in content_type:
                # Short videos are likely GIF replacements
                if size_mb < 20:  # Less than 20MB = probably a GIF-like clip
                    return 'animated_video', content_type, size_mb
                else:
                    return 'video_too_large', content_type, size_mb
            elif 'image/' in content_type:
                return 'static_image', content_type, size_mb
            else:
                return 'unknown', content_type, size_mb
                
        except Exception as e:
            console.print(f"[dim]  ⚠️  Could not check type: {str(e)[:50]}[/dim]")
            return 'error', '', 0
    
    def download_media(self, url, output_path):
        """Download media from URL to output path"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            console.print(f"[red]  ❌ Download failed: {str(e)[:50]}[/red]")
            return False
    
    def convert_video_to_gif(self, video_path, gif_path):
        """Convert MP4/WebM to GIF using ffmpeg"""
        console.print(f"[cyan]  🔄 Converting to GIF...[/cyan]")
        
        try:
            cmd = [
                'ffmpeg', '-y', '-i', str(video_path),
                '-vf', 'fps=15,scale=640:-1:flags=lanczos',
                '-loop', '0',
                str(gif_path)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Remove original video
            video_path.unlink()
            
            return True
        except Exception as e:
            console.print(f"[red]  ❌ Conversion failed: {str(e)[:50]}[/red]")
            return False
    
    def download_animated_from_pin(self, pin_url, convert_videos=True):
        """
        Download animated content from a Pinterest pin
        
        Args:
            pin_url: Pinterest pin URL
            convert_videos: If True, convert MP4/WebM to GIF
        
        Returns:
            dict with download info or None
        """
        # Extract media URLs
        media_urls = self.extract_media_urls_from_pin(pin_url)
        
        if not media_urls:
            console.print(f"[yellow]  ⚠️  No media found[/yellow]")
            return None
        
        console.print(f"[green]  ✅ Found {len(media_urls)} candidate URL(s)[/green]")
        
        # Check each URL and find animated content
        animated_media = []
        
        for url in media_urls:
            media_type, content_type, size_mb = self.check_media_type(url)
            
            if media_type == 'gif':
                animated_media.append({
                    'url': url,
                    'type': 'gif',
                    'content_type': content_type,
                    'size_mb': size_mb,
                    'priority': 1  # Prefer true GIFs
                })
                console.print(f"[green]  ✅ GIF found ({size_mb:.1f}MB)[/green]")
            
            elif media_type == 'animated_video':
                animated_media.append({
                    'url': url,
                    'type': 'animated_video',
                    'content_type': content_type,
                    'size_mb': size_mb,
                    'priority': 2  # Fallback to videos
                })
                console.print(f"[cyan]  🎥 Animated video found ({size_mb:.1f}MB)[/cyan]")
        
        if not animated_media:
            console.print(f"[yellow]  ⚠️  No animated content found (only static images)[/yellow]")
            return None
        
        # Sort by priority (GIFs first) and size (prefer larger = better quality)
        animated_media.sort(key=lambda x: (x['priority'], -x['size_mb']))
        best_media = animated_media[0]
        
        # Generate output filename
        pin_id = re.search(r'/pin/(\d+)', pin_url)
        if pin_id:
            base_name = f"pin_{pin_id.group(1)}"
        else:
            base_name = f"pin_{int(time.time())}"
        
        # Download
        if best_media['type'] == 'gif':
            output_path = self.output_dir / f"{base_name}.gif"
            console.print(f"[cyan]  📥 Downloading GIF...[/cyan]")
        else:
            ext = '.mp4' if 'mp4' in best_media['content_type'] else '.webm'
            output_path = self.output_dir / f"{base_name}{ext}"
            console.print(f"[cyan]  📥 Downloading video...[/cyan]")
        
        if self.download_media(best_media['url'], output_path):
            console.print(f"[green]  ✅ Saved: {output_path.name}[/green]")
            
            # Convert video to GIF if requested
            if best_media['type'] == 'animated_video' and convert_videos:
                gif_path = output_path.with_suffix('.gif')
                if self.convert_video_to_gif(output_path, gif_path):
                    output_path = gif_path
                    console.print(f"[green]  ✅ Converted to GIF: {gif_path.name}[/green]")
            
            return {
                'source_url': pin_url,
                'media_type': best_media['type'],
                'media_url': best_media['url'],
                'local_path': str(output_path),
                'content_type': best_media['content_type'],
                'size_mb': best_media['size_mb']
            }
        
        return None


def search_and_download_gifs(query, num_gifs=10, convert_videos=True):
    """
    Search Pinterest for a topic and download animated content
    
    Args:
        query: Search query (e.g., "greek art illustration")
        num_gifs: Number of animated items to download
        convert_videos: Convert MP4/WebM to GIF
    """
    console.print(f"\n[bold cyan]🎨 Pinterest GIF Downloader[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[yellow]Target: {num_gifs} animated items[/yellow]\n")
    
    downloader = PinterestGIFDownloader(f"pinterest_gifs/{query.replace(' ', '_')}")
    
    # Get Pinterest search results
    console.print("[cyan]🔍 Searching Pinterest...[/cyan]\n")
    
    pin_urls = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        page.goto(search_url)
        time.sleep(3)
        
        # Scroll to load more pins
        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
        
        # Extract pin URLs
        links = page.query_selector_all('a[href*="/pin/"]')
        for link in links:
            href = link.get_attribute('href')
            if href and '/pin/' in href:
                full_url = f"https://www.pinterest.com{href}" if href.startswith('/') else href
                pin_urls.append(full_url)
        
        browser.close()
    
    # Remove duplicates
    pin_urls = list(set(pin_urls))[:num_gifs * 3]  # Get 3x to account for filtering
    
    console.print(f"[green]✅ Found {len(pin_urls)} pins to check[/green]\n")
    
    # Download animated content
    downloaded = []
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading animated content...", total=num_gifs)
        
        for pin_url in pin_urls:
            if len(downloaded) >= num_gifs:
                break
            
            console.print(f"\n[bold]Pin {len(downloaded)+1}/{num_gifs}[/bold]")
            
            result = downloader.download_animated_from_pin(pin_url, convert_videos)
            
            if result:
                downloaded.append(result)
                progress.update(task, advance=1)
            
            # Rate limiting
            time.sleep(2)
    
    # Summary
    console.print(f"\n[bold green]✅ Downloaded {len(downloaded)} animated items![/bold green]")
    console.print(f"[cyan]📁 Saved to: {downloader.output_dir}/[/cyan]\n")
    
    # Stats
    gifs = sum(1 for d in downloaded if d['media_type'] == 'gif')
    videos = len(downloaded) - gifs
    
    console.print(f"[green]  • True GIFs: {gifs}[/green]")
    console.print(f"[cyan]  • Videos converted: {videos}[/cyan]\n")
    
    return downloaded


if __name__ == "__main__":
    # Example: Download Greek art animated illustrations
    results = search_and_download_gifs(
        query="greek art illustration animated",
        num_gifs=10,
        convert_videos=True  # Convert MP4s to GIFs
    )
    
    console.print("[bold]📊 Results:[/bold]")
    for i, result in enumerate(results, 1):
        console.print(f"{i}. {result['local_path']} ({result['size_mb']:.1f}MB)")
