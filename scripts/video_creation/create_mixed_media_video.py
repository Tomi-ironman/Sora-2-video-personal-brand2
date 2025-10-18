#!/usr/bin/env python3
"""
Create video with mixed media (static images + GIFs)
GIFs play naturally, static images use zoom effects
"""

import subprocess
import os
from pathlib import Path
from rich.console import Console

console = Console()


def create_mixed_media_video(
    media_dir,
    voice_file,
    output_filename,
    hook_duration=0.15,
    story_duration=2.2
):
    """
    Create video from mixed static + GIF media
    
    Args:
        media_dir: Directory containing subdirs with images and gifs
        voice_file: Path to voice audio file
        output_filename: Output video filename
        hook_duration: Duration per clip in hook (seconds)
        story_duration: Duration per clip in story (seconds)
    """
    
    console.print("\n[bold cyan]🎬 MIXED MEDIA VIDEO CREATOR[/bold cyan]\n")
    console.print(f"[yellow]Media dir: {media_dir}[/yellow]")
    console.print(f"[yellow]Voice: {voice_file}[/yellow]")
    console.print(f"[yellow]Output: {output_filename}[/yellow]\n")
    
    media_path = Path(media_dir)
    
    # Find all media files
    static_images = []
    gifs = []
    
    # Look for static images
    for subdir in media_path.glob("*"):
        if subdir.is_dir() and 'gifs' not in subdir.name.lower():
            static_images.extend(list(subdir.glob("*.jpg")))
            static_images.extend(list(subdir.glob("*.png")))
    
    # Look for GIFs
    gif_dir = media_path / "gifs"
    if gif_dir.exists():
        gifs = list(gif_dir.glob("*.gif"))
    
    console.print(f"[green]✅ Found {len(static_images)} static images[/green]")
    console.print(f"[green]✅ Found {len(gifs)} GIFs[/green]\n")
    
    if len(static_images) == 0 and len(gifs) == 0:
        console.print("[red]❌ No media found![/red]")
        return None
    
    # Sort for consistency
    static_images.sort()
    gifs.sort()
    
    # Mix media: GIF first, then intersperse GIFs among static
    all_media = []
    
    if gifs:
        # Start with a GIF for impact
        all_media.append({'path': gifs[0], 'type': 'gif'})
        remaining_gifs = gifs[1:]
    else:
        remaining_gifs = []
    
    # Calculate positions for remaining GIFs
    if remaining_gifs and static_images:
        spacing = len(static_images) // len(remaining_gifs) if len(remaining_gifs) > 0 else len(static_images)
        gif_positions = [spacing * (i + 1) for i in range(len(remaining_gifs))]
    else:
        gif_positions = []
    
    # Intersperse GIFs among static images
    static_idx = 0
    gif_idx = 0
    
    for i in range(len(static_images)):
        # Check if we should insert a GIF at this position
        if i in gif_positions and gif_idx < len(remaining_gifs):
            all_media.append({'path': remaining_gifs[gif_idx], 'type': 'gif'})
            gif_idx += 1
        
        # Add static image
        if static_idx < len(static_images):
            all_media.append({'path': static_images[static_idx], 'type': 'static'})
            static_idx += 1
    
    console.print(f"[cyan]📊 Video Structure:[/cyan]")
    console.print(f"[cyan]   Total clips: {len(all_media)}[/cyan]")
    
    # Split into hook and story
    hook_clips = min(10, len(all_media) - 8)
    story_clips = len(all_media) - hook_clips
    
    console.print(f"[cyan]   🔥 HOOK: {hook_clips} clips @ {hook_duration}s each[/cyan]")
    console.print(f"[cyan]   🎥 STORY: {story_clips} clips @ {story_duration}s each[/cyan]\n")
    
    # Create temp directory
    temp_dir = Path("temp_mixed_clips")
    temp_dir.mkdir(exist_ok=True)
    
    # Process HOOK clips
    console.print("[cyan]🔥 Creating hook clips...[/cyan]")
    hook_list = []
    
    for i in range(hook_clips):
        media = all_media[i]
        output_clip = temp_dir / f"hook_{i:03d}.mp4"
        
        if media['type'] == 'gif':
            # GIF: Play naturally, no zoom
            console.print(f"[dim]  Hook {i+1}: GIF (natural playback)[/dim]")
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-i', str(media['path']),
                '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                '-c:v', 'libx264',
                '-t', str(hook_duration),
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        else:
            # Static: No zoom in hook (too fast)
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-loop', '1',
                '-i', str(media['path']),
                '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                '-c:v', 'libx264',
                '-t', str(hook_duration),
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        
        subprocess.run(cmd, check=True)
        hook_list.append(output_clip)
    
    console.print(f"[green]✅ {len(hook_list)} hook clips created[/green]\n")
    
    # Process STORY clips
    console.print("[cyan]🎥 Creating story clips...[/cyan]")
    story_list = []
    
    for i in range(story_clips):
        media_idx = hook_clips + i
        if media_idx >= len(all_media):
            break
        
        media = all_media[media_idx]
        output_clip = temp_dir / f"story_{i:03d}.mp4"
        
        if media['type'] == 'gif':
            # GIF: Loop and play naturally for story duration
            console.print(f"[dim]  Story {i+1}: GIF (looping)[/dim]")
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-stream_loop', '-1',  # Loop infinitely
                '-i', str(media['path']),
                '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                '-c:v', 'libx264',
                '-t', str(story_duration),
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        else:
            # Static: Use zoom effect
            zoom_filter = f'zoompan=z=\'min(zoom+0.0005,1.15)\':d={int(story_duration * 30)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920'
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-loop', '1',
                '-i', str(media['path']),
                '-vf', f'scale=1200:2150:force_original_aspect_ratio=increase,{zoom_filter}',
                '-c:v', 'libx264',
                '-t', str(story_duration),
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        
        subprocess.run(cmd, check=True)
        story_list.append(output_clip)
    
    console.print(f"[green]✅ {len(story_list)} story clips created[/green]\n")
    
    # Concatenate all clips
    console.print("[cyan]🔗 Combining clips...[/cyan]")
    concat_file = 'concat_mixed_list.txt'
    with open(concat_file, 'w') as f:
        for clip in hook_list + story_list:
            f.write(f"file '{clip.absolute()}'\n")
    
    Path("professional_videos").mkdir(exist_ok=True)
    
    temp_video = "temp_mixed_video_no_audio.mp4"
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
    console.print("[cyan]🎙️  Adding voice...[/cyan]")
    output_file = f"professional_videos/{output_filename}"
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
    
    console.print(f"\n[bold green]✅ MIXED MEDIA VIDEO CREATED![/bold green]")
    console.print(f"[cyan]📁 {output_file}[/cyan]\n")
    
    # Copy to desktop
    desktop_path = os.path.expanduser(f'~/Desktop/{output_filename}')
    subprocess.run(['cp', output_file, desktop_path])
    console.print(f"[green]✅ Copied to Desktop: {output_filename}[/green]\n")
    
    # Open video
    console.print("[cyan]🎬 Opening video...[/cyan]")
    subprocess.run(['open', output_file])
    
    return output_file


if __name__ == "__main__":
    # Create Greek culture video with mixed media
    create_mixed_media_video(
        media_dir="pinterest_downloads/mixed_greek_culture",
        voice_file="narrations/greek_very_short.wav",
        output_filename="greek_culture_mixed_media.mp4"
    )
