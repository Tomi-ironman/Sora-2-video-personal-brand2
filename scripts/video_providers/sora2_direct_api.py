#!/usr/bin/env python3
"""
Sora 2 Direct API Generator
Uses the actual Sora 2 REST API endpoints for video generation with image-to-video support.
"""

import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import base64

# Load environment variables
load_dotenv()

console = Console()

class Sora2DirectAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            console.print("[red]Error: OPENAI_API_KEY not found in .env file[/red]")
            sys.exit(1)
        
        self.base_url = "https://api.openai.com/v1/videos"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Save videos to Desktop/AI-video-Generation folder
        self.videos_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.videos_dir.mkdir(exist_ok=True)
        
        # Reference images directory
        self.reference_dir = Path(__file__).parent / "Reference Character"
    
    def generate_video_with_image(self, image_path: str, prompt: str, seconds: int = 8, size: str = "720x1280"):
        """Generate a video using Sora 2 with image reference (image-to-video)"""
        console.print(f"\n[cyan]🎬 Generating image-to-video with Sora 2...[/cyan]")
        console.print(f"[cyan]📸 Using image: {Path(image_path).name}[/cyan]")
        console.print(f"[dim]Prompt: {prompt}[/dim]")
        console.print(f"[dim]Settings: {size}, {seconds}s[/dim]\n")
        
        try:
            # Prepare the multipart form data
            files = {
                'model': (None, 'sora-2'),
                'prompt': (None, prompt),
                'seconds': (None, str(seconds)),
                'size': (None, size),
                'input_reference': (Path(image_path).name, open(image_path, 'rb'), 'image/jpeg')
            }
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Creating video job...", total=None)
                
                # Create video generation job
                response = requests.post(self.base_url, headers=self.headers, files=files)
                
                # Close the file
                files['input_reference'][1].close()
                
                if response.status_code != 200:
                    console.print(f"[red]❌ API Error: {response.status_code}[/red]")
                    console.print(f"[red]{response.text}[/red]")
                    return None
                
                job_data = response.json()
                video_id = job_data['id']
                
                console.print(f"[green]✅ Video job created: {video_id}[/green]")
                progress.update(task, description=f"Generating video... (ID: {video_id})")
                
                # Poll for completion
                while True:
                    status_response = requests.get(f"{self.base_url}/{video_id}", headers=self.headers)
                    if status_response.status_code != 200:
                        console.print(f"[red]❌ Status check failed: {status_response.text}[/red]")
                        return None
                    
                    status_data = status_response.json()
                    current_status = status_data['status']
                    progress_pct = status_data.get('progress', 0)
                    
                    if current_status == 'completed':
                        progress.update(task, description="Video completed! Downloading...")
                        break
                    elif current_status == 'failed':
                        error_info = status_data.get('error', {})
                        console.print(f"[red]❌ Video generation failed: {error_info}[/red]")
                        return None
                    else:
                        progress.update(task, description=f"Generating... {progress_pct}% ({current_status})")
                        time.sleep(5)  # Wait 5 seconds before next check
                
                # Download the completed video
                download_response = requests.get(f"{self.base_url}/{video_id}/content", headers=self.headers)
                if download_response.status_code != 200:
                    console.print(f"[red]❌ Download failed: {download_response.text}[/red]")
                    return None
                
                # Save video file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')
                filename = f"sora2_{timestamp}_{safe_prompt}.mp4"
                filepath = self.videos_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(download_response.content)
                
                progress.update(task, description="Complete!")
            
            console.print(f"[green]✅ Video saved: {filename}[/green]")
            console.print(f"[cyan]📁 Location: ~/Desktop/AI-video-Generation/[/cyan]")
            return filepath
            
        except Exception as e:
            console.print(f"[red]❌ Error generating video: {str(e)}[/red]")
            return None
    
    def generate_video(self, prompt: str, seconds: int = 8, size: str = "720x1280"):
        """Generate a video using Sora 2 (text-to-video)"""
        console.print(f"\n[cyan]🎬 Generating video with Sora 2...[/cyan]")
        console.print(f"[dim]Prompt: {prompt}[/dim]")
        console.print(f"[dim]Settings: {size}, {seconds}s[/dim]\n")
        
        try:
            data = {
                'model': 'sora-2',
                'prompt': prompt,
                'seconds': str(seconds),
                'size': size
            }
            
            # Add Content-Type header for JSON
            headers = self.headers.copy()
            headers['Content-Type'] = 'application/json'
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Creating video job...", total=None)
                
                # Create video generation job
                response = requests.post(self.base_url, headers=headers, json=data)
                
                if response.status_code != 200:
                    console.print(f"[red]❌ API Error: {response.status_code}[/red]")
                    console.print(f"[red]{response.text}[/red]")
                    return None
                
                job_data = response.json()
                video_id = job_data['id']
                
                console.print(f"[green]✅ Video job created: {video_id}[/green]")
                progress.update(task, description=f"Generating video... (ID: {video_id})")
                
                # Poll for completion
                while True:
                    status_response = requests.get(f"{self.base_url}/{video_id}", headers=self.headers)
                    if status_response.status_code != 200:
                        console.print(f"[red]❌ Status check failed: {status_response.text}[/red]")
                        return None
                    
                    status_data = status_response.json()
                    current_status = status_data['status']
                    progress_pct = status_data.get('progress', 0)
                    
                    if current_status == 'completed':
                        progress.update(task, description="Video completed! Downloading...")
                        break
                    elif current_status == 'failed':
                        error_info = status_data.get('error', {})
                        console.print(f"[red]❌ Video generation failed: {error_info}[/red]")
                        return None
                    else:
                        progress.update(task, description=f"Generating... {progress_pct}% ({current_status})")
                        time.sleep(5)  # Wait 5 seconds before next check
                
                # Download the completed video
                download_response = requests.get(f"{self.base_url}/{video_id}/content", headers=self.headers)
                if download_response.status_code != 200:
                    console.print(f"[red]❌ Download failed: {download_response.text}[/red]")
                    return None
                
                # Save video file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')
                filename = f"sora2_{timestamp}_{safe_prompt}.mp4"
                filepath = self.videos_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(download_response.content)
                
                progress.update(task, description="Complete!")
            
            console.print(f"[green]✅ Video saved: {filename}[/green]")
            console.print(f"[cyan]📁 Location: ~/Desktop/AI-video-Generation/[/cyan]")
            return filepath
            
        except Exception as e:
            console.print(f"[red]❌ Error generating video: {str(e)}[/red]")
            return None
    
    def generate_talking_avatar_from_image(self, image_name: str, dialogue: str = "", seconds: int = 8):
        """Generate a talking avatar video from a specific reference image"""
        image_path = self.reference_dir / image_name
        
        if not image_path.exists():
            console.print(f"[red]❌ Image not found: {image_path}[/red]")
            console.print(f"[dim]Available images in Reference Character/:[/dim]")
            for img in self.reference_dir.glob("*"):
                if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    console.print(f"[dim]  - {img.name}[/dim]")
            return None
        
        # Create a simple prompt for talking avatar
        if dialogue:
            prompt = f"""
            Animate this person speaking with natural lip synchronization and facial expressions.
            The person should speak this dialogue with perfect lip sync:
            "{dialogue}"
            
            Keep the original background and composition exactly as shown in the reference image.
            Only animate the mouth, eyes, and subtle head movements for natural speech.
            Maintain the exact identity, facial features, and appearance from the reference image.
            """
        else:
            prompt = """
            Animate this person speaking naturally with realistic facial expressions and lip movements.
            Keep the original background and composition exactly as shown in the reference image.
            Only animate the mouth, eyes, and subtle head movements for natural speech.
            Maintain the exact identity, facial features, and appearance from the reference image.
            """
        
        return self.generate_video_with_image(
            image_path=str(image_path),
            prompt=prompt,
            seconds=seconds,
            size="720x1280"  # 9:16 aspect ratio for mobile
        )

def main():
    generator = Sora2DirectAPI()
    
    console.print(Panel.fit(
        "[bold cyan]🎬 Sora 2 Direct API Generator[/bold cyan]\n"
        "[dim]Generate videos using the real Sora 2 API with image-to-video support[/dim]",
        border_style="cyan"
    ))
    
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        generator.generate_video(prompt)
    else:
        # Interactive mode
        while True:
            console.print("\n[bold]What would you like to do?[/bold]")
            console.print("1. Generate talking avatar from your image")
            console.print("2. Generate text-to-video")
            console.print("3. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], default="1")
            
            if choice == "1":
                # List available images
                images = list(generator.reference_dir.glob("*"))
                image_files = [img for img in images if img.suffix.lower() in ['.jpg', '.jpeg', '.png']]
                
                if not image_files:
                    console.print(f"[red]No images found in {generator.reference_dir}[/red]")
                    continue
                
                console.print("\n[bold]Available reference images:[/bold]")
                for i, img in enumerate(image_files, 1):
                    console.print(f"{i}. {img.name}")
                
                img_choice = Prompt.ask("Choose image number", default="1")
                try:
                    selected_image = image_files[int(img_choice) - 1]
                    dialogue = Prompt.ask("Enter dialogue (optional)", default="")
                    seconds = int(Prompt.ask("Duration in seconds (4-20)", default="8"))
                    
                    generator.generate_talking_avatar_from_image(
                        image_name=selected_image.name,
                        dialogue=dialogue,
                        seconds=max(4, min(20, seconds))
                    )
                except (ValueError, IndexError):
                    console.print("[red]Invalid selection[/red]")
                    
            elif choice == "2":
                prompt = Prompt.ask("Enter your video prompt")
                seconds = int(Prompt.ask("Duration in seconds (4-20)", default="8"))
                size = Prompt.ask("Size (720x1280, 1024x1024, 1280x720)", default="720x1280")
                
                generator.generate_video(prompt, max(4, min(20, seconds)), size)
                
            elif choice == "3":
                console.print("[cyan]👋 Goodbye![/cyan]")
                break

if __name__ == "__main__":
    main()
