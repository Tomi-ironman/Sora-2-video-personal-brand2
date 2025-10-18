#!/usr/bin/env python3
"""
Complete Video Generator with Voice Cloning API
1. Generate voice using API
2. Download fresh illustrations
3. Create video with super fast hook + zoom effects
"""

import subprocess
import os
from pathlib import Path
from voice_cloning_api import clone_voice
from rich.console import Console

console = Console()


def create_video_with_voice_api(
    script_text,
    topic,
    output_filename,
    images_dir=None,
    download_new_images=True
):
    """
    Complete video creation pipeline
    
    Args:
        script_text: The script to narrate
        topic: Topic for image search (e.g., "japanese art illustration")
        output_filename: Name for the final video
        images_dir: Use existing images (optional)
        download_new_images: Download fresh images
    """
    
    console.print("\n[bold cyan]🎬 COMPLETE VIDEO GENERATOR[/bold cyan]\n")
    console.print(f"[yellow]Topic: {topic}[/yellow]")
    console.print(f"[yellow]Output: {output_filename}[/yellow]\n")
    
    # Step 1: Generate voice using API
    console.print("[bold]Step 1: Generate Voice[/bold]")
    voice_file = f"narrations/{topic.replace(' ', '_')}_voice.wav"
    
    voice_path = clone_voice(script_text, voice_file)
    
    if not voice_path:
        console.print("[red]❌ Voice generation failed![/red]")
        return None
    
    # Step 2: Download images if needed
    if download_new_images:
        console.print("\n[bold]Step 2: Download Fresh Illustrations[/bold]")
        
        from pinterest_scraper import scrape_pinterest_images
        
        download_dir = f"pinterest_downloads/{topic.replace(' ', '_')}"
        
        urls = scrape_pinterest_images(
            query=topic,
            num_images=30,
            output_dir=download_dir
        )
        
        images_dir = Path(download_dir) / topic.replace(' ', '_')
    
    # Step 3: Create video with hook + zoom
    console.print("\n[bold]Step 3: Create Video with Hook + Zoom[/bold]\n")
    
    output_file = f"professional_videos/{output_filename}"
    temp_dir = Path("temp_clips")
    temp_dir.mkdir(exist_ok=True)
    
    # Get image files
    image_files = sorted(list(Path(images_dir).glob("*.jpg")))
    
    if len(image_files) == 0:
        console.print(f"[red]❌ No images found in {images_dir}[/red]")
        return None
    
    console.print(f"[green]✅ Found {len(image_files)} images[/green]")
    
    # Video structure - SUPER FAST HOOK
    hook_clips = min(20, len(image_files) - 8)
    hook_duration = 0.15  # 150ms per clip = FAST
    story_clips = min(8, len(image_files) - hook_clips)
    story_duration = 2.2
    
    console.print(f"\n[cyan]📊 Video Structure:[/cyan]")
    console.print(f"   🔥 HOOK: {hook_clips} clips @ {hook_duration}s = SUPER FAST")
    console.print(f"   🎥 STORY: {story_clips} clips @ {story_duration}s with ZOOM\n")
    
    # Create HOOK clips (fast, no zoom)
    console.print("[cyan]🔥 Creating hook clips...[/cyan]")
    hook_list = []
    for i in range(hook_clips):
        img = image_files[i]
        output_clip = temp_dir / f"hook_{i:03d}.mp4"
        
        cmd = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-loop', '1',
            '-i', str(img),
            '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:v', 'libx264',
            '-t', str(hook_duration),
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            str(output_clip)
        ]
        subprocess.run(cmd, check=True)
        hook_list.append(output_clip)
    
    console.print(f"[green]✅ Created {len(hook_list)} hook clips[/green]")
    
    # Create STORY clips (with zoom)
    console.print("\n[cyan]🎥 Creating story clips with zoom...[/cyan]")
    story_list = []
    for i in range(story_clips):
        img_idx = hook_clips + i
        if img_idx >= len(image_files):
            break
        img = image_files[img_idx]
        output_clip = temp_dir / f"story_{i:03d}.mp4"
        
        zoom_filter = f'zoompan=z=\'min(zoom+0.0005,1.15)\':d={int(story_duration * 30)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920'
        
        cmd = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-loop', '1',
            '-i', str(img),
            '-vf', f'scale=1200:2150:force_original_aspect_ratio=increase,{zoom_filter}',
            '-c:v', 'libx264',
            '-t', str(story_duration),
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            str(output_clip)
        ]
        subprocess.run(cmd, check=True)
        story_list.append(output_clip)
    
    console.print(f"[green]✅ Created {len(story_list)} story clips[/green]")
    
    # Concatenate clips
    console.print("\n[cyan]🔗 Combining clips...[/cyan]")
    concat_file = 'concat_list.txt'
    with open(concat_file, 'w') as f:
        for clip in hook_list + story_list:
            f.write(f"file '{clip.absolute()}'\n")
    
    Path("professional_videos").mkdir(exist_ok=True)
    
    temp_video = "temp_video_no_audio.mp4"
    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        temp_video
    ]
    subprocess.run(cmd, check=True)
    
    # Add audio
    console.print("[cyan]🎙️  Adding audio...[/cyan]")
    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', temp_video,
        '-i', voice_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_file
    ]
    subprocess.run(cmd, check=True)
    
    # Clean up
    console.print("[cyan]🧹 Cleaning up...[/cyan]")
    os.remove(concat_file)
    os.remove(temp_video)
    for clip in hook_list + story_list:
        clip.unlink()
    temp_dir.rmdir()
    
    console.print(f"\n[bold green]✅ VIDEO CREATED![/bold green]")
    console.print(f"[cyan]📁 {output_file}[/cyan]\n")
    
    # Copy to desktop
    desktop_path = os.path.expanduser(f'~/Desktop/{output_filename}')
    subprocess.run(['cp', output_file, desktop_path])
    console.print(f"[green]✅ Copied to Desktop: {output_filename}[/green]\n")
    
    # Open video
    subprocess.run(['open', output_file])
    
    return output_file


if __name__ == "__main__":
    # Example: Create a new Japanese culture video with API voice
    
    script = """One thing AI can't take away from us is Japanese culture.

Cherry blossoms bloom for just two weeks. A reminder that beauty is fleeting.

Tea ceremony. Four hundred years of mindfulness in every gesture.

Wabi-sabi. Finding perfection in imperfection.

Calligraphy. Where discipline meets art.

This is culture. Timeless. Human. Irreplaceable."""
    
    create_video_with_voice_api(
        script_text=script,
        topic="japanese art illustration watercolor",
        output_filename="japanese_culture_API_voice.mp4",
        download_new_images=True
    )
