#!/usr/bin/env python3
"""
Create Cinematic Video from Pinterest Images
Converts static images into dynamic video with Ken Burns effects
"""

from pathlib import Path
try:
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
except ImportError:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from rich.console import Console
import sys

console = Console()


def create_cinematic_video_from_images(
    image_dir,
    audio_path,
    script_text,
    output_path="professional_videos/pinterest_cinematic_video.mp4",
    seconds_per_image=3.0  # How long each image shows
):
    """
    Create cinematic video from Pinterest images with Ken Burns effects
    
    Args:
        image_dir: Directory with downloaded images
        audio_path: Path to voice audio
        script_text: Script for captions
        output_path: Where to save final video
        seconds_per_image: Duration for each image (default 3 seconds)
    """
    
    console.print("\n[bold cyan]🎬 Creating Cinematic Video from Pinterest Images[/bold cyan]\n")
    
    # Load audio to get duration FIRST
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    console.print(f"[cyan]Audio duration: {total_duration:.1f}s[/cyan]")
    
    # Calculate how many images we NEED
    images_needed = int(total_duration / seconds_per_image) + 1
    
    console.print(f"[yellow]Images needed: {images_needed} (at {seconds_per_image}s each)[/yellow]\n")
    
    # Check available images
    image_path = Path(image_dir)
    available_images = sorted(list(image_path.glob("*.jpg")) + list(image_path.glob("*.png")))
    
    if len(available_images) == 0:
        console.print("[red]❌ No images found in directory![/red]")
        return None
    
    console.print(f"[green]Found {len(available_images)} images available[/green]")
    
    # Check if we have enough images
    if len(available_images) < images_needed:
        console.print(f"[bold red]⚠️  WARNING: Need {images_needed} images but only have {len(available_images)}![/bold red]")
        console.print(f"[yellow]Downloading more images...[/yellow]\n")
        
        # Extract search query from directory name
        search_query = image_path.name.replace('_', ' ')
        
        # Download more images
        import subprocess
        subprocess.run([
            "python3", "pinterest_scraper.py",
            search_query,
            str(images_needed + 5)  # Download a few extra
        ])
        
        # Reload images
        available_images = sorted(list(image_path.glob("*.jpg")) + list(image_path.glob("*.png")))
        console.print(f"[green]Now have {len(available_images)} images[/green]\n")
    
    # Use exactly the number of images we need (no repeats!)
    images = available_images[:images_needed]
    
    console.print(f"[cyan]Using {len(images)} unique images[/cyan]")
    console.print(f"[cyan]Creating cinematic clips...[/cyan]\n")
    
    # Calculate duration per image
    clip_duration = seconds_per_image
    
    # Create video clips from images with Ken Burns effect
    clips = []
    
    for i, img in enumerate(images):
        try:
            console.print(f"[dim]Processing {img.name}...[/dim]")
            
            # Load image
            clip = ImageClip(str(img), duration=clip_duration)
            
            # Resize to 9:16 (1080x1920)
            clip = clip.resized(height=1920)
            
            # Center crop to 1080 width if needed
            if clip.w > 1080:
                x_center = clip.w / 2
                clip = clip.cropped(x1=x_center-540, x2=x_center+540)
            elif clip.w < 1080:
                # If too narrow, resize to fit width
                clip = clip.resized(width=1080)
                # Then crop height if needed
                if clip.h > 1920:
                    y_center = clip.h / 2
                    clip = clip.cropped(y1=y_center-960, y2=y_center+960)
            
            # Add Ken Burns effect (slow zoom in)
            def zoom_effect(t):
                # Zoom from 1.0 to 1.1 over the duration
                zoom = 1.0 + (0.1 * t / clip_duration)
                return zoom
            
            clip = clip.resized(lambda t: zoom_effect(t))
            
            # Add fade in/out
            if i == 0:
                clip = clip.fadein(0.5)
            if i == len(images) - 1:
                clip = clip.fadeout(0.5)
            
            clips.append(clip)
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Skipped {img.name}: {str(e)[:40]}[/yellow]")
            continue
    
    if len(clips) == 0:
        console.print("[red]❌ No clips created![/red]")
        return None
    
    console.print(f"\n[green]✅ Created {len(clips)} cinematic clips[/green]\n")
    
    # Concatenate all clips with crossfade
    console.print("[cyan]Combining clips with transitions...[/cyan]")
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Add audio
    console.print("[cyan]Adding voiceover...[/cyan]")
    final_video = final_video.with_audio(audio)
    
    # Export
    console.print(f"[cyan]Exporting to {output_path}...[/cyan]\n")
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    final_video.write_videofile(
        str(output_file),
        codec='libx264',
        audio_codec='aac',
        fps=24,
        preset='medium',
        bitrate='8000k'  # High quality
    )
    
    # Cleanup
    for clip in clips:
        clip.close()
    final_video.close()
    audio.close()
    
    file_size = output_file.stat().st_size / (1024 * 1024)
    
    console.print("\n" + "="*60)
    console.print("[bold green]🎉 CINEMATIC VIDEO CREATED![/bold green]")
    console.print("="*60 + "\n")
    
    console.print(f"[cyan]📁 File: {output_file}[/cyan]")
    console.print(f"[cyan]📊 Size: {file_size:.1f} MB[/cyan]")
    console.print(f"[cyan]⏱️  Duration: {total_duration:.1f}s[/cyan]")
    console.print(f"[cyan]🎨 Clips: {len(clips)} cinematic images[/cyan]\n")
    
    # Now add captions
    console.print("[bold]Adding captions...[/bold]\n")
    
    from add_captions import add_captions_to_video
    
    captioned_output = output_file.parent / f"{output_file.stem}_WITH_CAPTIONS.mp4"
    
    final_with_captions = add_captions_to_video(
        video_path=str(output_file),
        output_path=str(captioned_output),
        audio_path=audio_path,
        script_text=script_text,
        style="modern"
    )
    
    if final_with_captions:
        console.print("\n[bold green]✅ FINAL CINEMATIC VIDEO READY![/bold green]")
        console.print(f"[cyan]📁 {final_with_captions}[/cyan]\n")
        
        # Open video
        import subprocess
        subprocess.run(["open", str(final_with_captions)])
        
        return final_with_captions
    
    return str(output_file)


if __name__ == "__main__":
    # Create video with Afrofuturism sci-fi images
    
    SCRIPT = """
    Culture isn't just about ping pong tables and free snacks.
    It's about building something meaningful together.
    Creating an environment where people thrive.
    Where innovation happens naturally.
    Where everyone feels valued and heard.
    That's the culture that wins.
    """
    
    result = create_cinematic_video_from_images(
        image_dir="/Users/tomi/Desktop/pinterest_images/afrofuturism_sci-fi_concept_art",
        audio_path="narrations/tomi_zenyai_test.wav",
        script_text=SCRIPT.strip(),
        output_path="professional_videos/afrofuturism_culture_video.mp4"
    )
    
    if result:
        console.print("[bold green]✅ SUCCESS![/bold green]")
    else:
        console.print("[bold red]❌ Failed[/bold red]")
