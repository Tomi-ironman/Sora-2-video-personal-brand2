#!/usr/bin/env python3
"""
STEP 2: Create Video Using Pre-Generated Voice
Run this AFTER step1_generate_voice.py completes
"""

import subprocess
import os
from pathlib import Path
from rich.console import Console

console = Console()


def create_video_from_voice(
    voice_file,
    topic_for_images,
    output_filename,
    download_new_images=True,
    existing_images_dir=None
):
    """
    Create video using existing voice file
    
    Args:
        voice_file: Path to the voice file (from Step 1)
        topic_for_images: Topic for image search
        output_filename: Name for final video
        download_new_images: Download fresh images
        existing_images_dir: Use existing images instead
    """
    
    console.print("\n[bold cyan]🎬 STEP 2: CREATE VIDEO[/bold cyan]\n")
    console.print(f"[yellow]Voice file: {voice_file}[/yellow]")
    console.print(f"[yellow]Output: {output_filename}[/yellow]\n")
    
    # Verify voice file exists
    if not Path(voice_file).exists():
        console.print(f"[red]❌ Voice file not found: {voice_file}[/red]")
        console.print(f"[yellow]Run step1_generate_voice.py first![/yellow]\n")
        return None
    
    console.print(f"[green]✅ Voice file found![/green]\n")
    
    # Download or use existing images
    if download_new_images and not existing_images_dir:
        console.print("[bold]Downloading Fresh Illustrations[/bold]")
        
        from pinterest_scraper import scrape_pinterest_images
        
        download_dir = f"pinterest_downloads/{topic_for_images.replace(' ', '_')}"
        
        urls = scrape_pinterest_images(
            query=topic_for_images,
            num_images=30,
            output_dir=download_dir
        )
        
        images_dir = Path(download_dir) / topic_for_images.replace(' ', '_')
    else:
        images_dir = Path(existing_images_dir) if existing_images_dir else None
    
    if not images_dir or not images_dir.exists():
        console.print(f"[red]❌ Images directory not found[/red]")
        return None
    
    # Create video with hook + zoom
    console.print("\n[bold]Creating Video with Hook + Zoom[/bold]\n")
    
    output_file = f"professional_videos/{output_filename}"
    temp_dir = Path("temp_clips")
    temp_dir.mkdir(exist_ok=True)
    
    # Get image files
    image_files = sorted(list(images_dir.glob("*.jpg")))
    
    if len(image_files) == 0:
        console.print(f"[red]❌ No images found in {images_dir}[/red]")
        return None
    
    console.print(f"[green]✅ Found {len(image_files)} images[/green]")
    
    # Video structure
    hook_clips = min(20, len(image_files) - 8)
    hook_duration = 0.15  # SUPER FAST
    story_clips = min(8, len(image_files) - hook_clips)
    story_duration = 2.2
    
    console.print(f"\n[cyan]📊 Video Structure:[/cyan]")
    console.print(f"   🔥 HOOK: {hook_clips} clips @ {hook_duration}s")
    console.print(f"   🎥 STORY: {story_clips} clips @ {story_duration}s with ZOOM\n")
    
    # Create HOOK clips
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
        
        if (i + 1) % 5 == 0:
            console.print(f"   Created {i + 1}/{hook_clips}...")
    
    console.print(f"[green]✅ {len(hook_list)} hook clips created[/green]")
    
    # Create STORY clips with zoom
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
    
    console.print(f"[green]✅ {len(story_list)} story clips created[/green]")
    
    # Concatenate clips
    console.print("\n[cyan]🔗 Combining all clips...[/cyan]")
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
    console.print("[cyan]🎙️  Adding voice audio...[/cyan]")
    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', temp_video,
        '-i', voice_file,
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
    console.print("[cyan]🎬 Opening video...[/cyan]")
    subprocess.run(['open', output_file])
    
    console.print(f"\n[bold green]✅ STEP 2 COMPLETE![/bold green]")
    console.print(f"[cyan]Video ready: {output_file}[/cyan]\n")
    
    return output_file


if __name__ == "__main__":
    # Use the voice file from Step 1
    voice_file = "narrations/japanese_culture_api.wav"
    
    # Check if voice file exists
    if not Path(voice_file).exists():
        console.print(f"\n[yellow]⚠️  Voice file not found: {voice_file}[/yellow]")
        console.print(f"[yellow]Run step1_generate_voice.py first![/yellow]\n")
    else:
        create_video_from_voice(
            voice_file=voice_file,
            topic_for_images="japanese art illustration watercolor",
            output_filename="japanese_culture_API_final.mp4",
            download_new_images=True
        )
