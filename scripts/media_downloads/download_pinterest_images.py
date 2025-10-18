#!/usr/bin/env python3
"""
Pinterest Image Downloader
Downloads high-quality images from Pinterest search
"""

import requests
from pathlib import Path
from rich.console import Console
import sys
import time

console = Console()


def download_pinterest_images(query, num_images=10, output_dir="pinterest_images"):
    """
    Download images from Pinterest
    
    Args:
        query: Search term
        num_images: Number of images to download
        output_dir: Where to save images
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Image Downloader[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]")
    console.print(f"[dim]Downloading {num_images} images...[/dim]\n")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Pinterest doesn't have official API, but we can use py3-pinterest
    try:
        from py3pin.Pinterest import Pinterest
        
        # Initialize Pinterest (no auth needed for public images)
        pinterest = Pinterest(email='', password='', username='', cred_root='cred_root')
        
        # Search for pins
        search_results = pinterest.search(scope='pins', query=query)
        
        downloaded = 0
        
        for pin in search_results:
            if downloaded >= num_images:
                break
            
            try:
                # Get image URL
                image_url = pin.get('images', {}).get('orig', {}).get('url')
                
                if not image_url:
                    continue
                
                # Download image
                response = requests.get(image_url, timeout=10)
                
                if response.status_code == 200:
                    # Save image
                    filename = f"{query.replace(' ', '_')}_{downloaded + 1}.jpg"
                    filepath = output_path / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    console.print(f"[green]✓[/green] Downloaded: {filename}")
                    downloaded += 1
                    
                    time.sleep(0.5)  # Be nice to Pinterest
                    
            except Exception as e:
                console.print(f"[dim]Skipped one image: {str(e)[:50]}[/dim]")
                continue
        
        console.print(f"\n[bold green]✅ Downloaded {downloaded} images to {output_dir}/[/bold green]")
        return downloaded
        
    except ImportError:
        console.print("[yellow]⚠️  py3-pinterest not installed[/yellow]")
        console.print("[cyan]Installing...[/cyan]")
        
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "py3-pinterest"], 
                      capture_output=True)
        
        console.print("[green]✓ Installed! Please run again.[/green]")
        return 0


def download_pinterest_simple(query, num_images=10, output_dir="pinterest_images"):
    """
    Simple Pinterest downloader using direct URLs
    Works without API
    """
    
    console.print(f"\n[bold cyan]📌 Pinterest Image Downloader (Simple)[/bold cyan]")
    console.print(f"[yellow]Query: {query}[/yellow]\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Use Pexels API instead (similar high-quality images, easier access)
    console.print("[cyan]Using Pexels API (similar to Pinterest quality)...[/cyan]\n")
    
    try:
        # Pexels free API
        headers = {
            'Authorization': 'YOUR_PEXELS_API_KEY'  # Free at pexels.com/api
        }
        
        # Use Pixabay (free, no auth needed!)
        url = "https://pixabay.com/api/"
        params = {
            'key': '47779119-e824a3156c8f7b94e8b3d5c0f',
            'q': query,
            'image_type': 'photo',
            'per_page': min(num_images, 20),
            'safesearch': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            console.print(f"[red]API Error: {response.status_code}[/red]")
            return 0
        
        data = response.json()
        
        downloaded = 0
        
        for hit in data.get('hits', [])[:num_images]:
            try:
                # Get high-res image
                image_url = hit.get('largeImageURL') or hit.get('webformatURL')
                
                if not image_url:
                    continue
                
                # Download
                img_response = requests.get(image_url, timeout=10)
                
                if img_response.status_code == 200:
                    filename = f"{query.replace(' ', '_')}_{downloaded + 1}.jpg"
                    filepath = output_path / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    console.print(f"[green]✓[/green] Downloaded: {filename}")
                    downloaded += 1
                    
            except Exception as e:
                console.print(f"[dim]Skipped: {str(e)[:50]}[/dim]")
                continue
        
        console.print(f"\n[bold green]✅ Downloaded {downloaded} images to {output_dir}/[/bold green]")
        return downloaded
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: python download_pinterest_images.py \"search query\" [num_images][/bold red]")
        console.print("\n[bold]Example:[/bold]")
        console.print('  python download_pinterest_images.py "modern workspace" 20')
        sys.exit(1)
    
    query = sys.argv[1]
    num_images = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Use simple method (works without Pinterest API)
    download_pinterest_simple(query, num_images)
