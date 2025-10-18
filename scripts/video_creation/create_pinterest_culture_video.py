#!/usr/bin/env python3
"""
Create Culture Video with Pinterest GIFs
Uses animated GIFs as B-roll with voice and captions
"""

from pathlib import Path
try:
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
except ImportError:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from rich.console import Console
import sys

console = Console()


def create_culture_video_from_gifs(
    gif_dir,
    audio_path,
    script_text,
    output_path="professional_videos/pinterest_culture_video.mp4"
):
    """
    Create video from Pinterest GIFs + voice + captions
    
    Args:
        gif_dir: Directory with downloaded GIFs
        audio_path: Path to voice audio
        script_text: Script for captions
        output_path: Where to save final video
    """
    
    console.print("\n[bold cyan]🎬 Creating Culture Video with Pinterest GIFs[/bold cyan]\n")
    
    gif_path = Path(gif_dir)
    gifs = sorted(list(gif_path.glob("*.gif")))
    
    if len(gifs) == 0:
        console.print("[red]❌ No GIFs found in directory![/red]")
        return None
    
    console.print(f"[green]Found {len(gifs)} GIFs[/green]\n")
    
    # Load audio to get duration
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    console.print(f"[cyan]Audio duration: {total_duration:.1f}s[/cyan]")
    console.print(f"[cyan]Creating video clips...[/cyan]\n")
    
    # Calculate duration per GIF
    clip_duration = total_duration / len(gifs)
    
    # Convert GIFs to video clips
    clips = []
    
    for i, gif in enumerate(gifs):
        try:
            console.print(f"[dim]Processing {gif.name}...[/dim]")
            
            # Load GIF as video
            clip = VideoFileClip(str(gif))
            
            # Loop if needed to match duration
            if clip.duration < clip_duration:
                loops = int(clip_duration / clip.duration) + 1
                clip = concatenate_videoclips([clip] * loops)
            
            # Trim to exact duration
            clip = clip.subclipped(0, clip_duration)
            
            # Resize to 9:16 (1080x1920)
            clip = clip.resized(height=1920)
            
            # Center crop to 1080 width
            if clip.w > 1080:
                x_center = clip.w / 2
                clip = clip.cropped(x1=x_center-540, x2=x_center+540)
            
            clips.append(clip)
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Skipped {gif.name}: {str(e)[:40]}[/yellow]")
            continue
    
    if len(clips) == 0:
        console.print("[red]❌ No clips created![/red]")
        return None
    
    console.print(f"\n[green]✅ Created {len(clips)} video clips[/green]\n")
    
    # Concatenate all clips
    console.print("[cyan]Combining clips...[/cyan]")
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
        preset='medium'
    )
    
    # Cleanup
    for clip in clips:
        clip.close()
    final_video.close()
    audio.close()
    
    file_size = output_file.stat().st_size / (1024 * 1024)
    
    console.print("\n" + "="*60)
    console.print("[bold green]🎉 CULTURE VIDEO CREATED![/bold green]")
    console.print("="*60 + "\n")
    
    console.print(f"[cyan]📁 File: {output_file}[/cyan]")
    console.print(f"[cyan]📊 Size: {file_size:.1f} MB[/cyan]")
    console.print(f"[cyan]⏱️  Duration: {total_duration:.1f}s[/cyan]")
    console.print(f"[cyan]🎨 Clips: {len(clips)} animated GIFs[/cyan]\n")
    
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
        console.print("\n[bold green]✅ FINAL VIDEO READY WITH CAPTIONS![/bold green]")
        console.print(f"[cyan]📁 {final_with_captions}[/cyan]\n")
        
        # Open video
        import subprocess
        subprocess.run(["open", str(final_with_captions)])
        
        return final_with_captions
    
    return str(output_file)


if __name__ == "__main__":
    # Test with existing voice and GIFs
    
    SCRIPT = """
    Culture isn't just about ping pong tables and free snacks.
    It's about building something meaningful together.
    Creating an environment where people thrive.
    Where innovation happens naturally.
    Where everyone feels valued and heard.
    That's the culture that wins.
    """
    
    result = create_culture_video_from_gifs(
        gif_dir="/Users/tomi/Desktop/pinterest_gifs/animated_office_culture_illustration",
        audio_path="narrations/tomi_zenyai_test.wav",
        script_text=SCRIPT.strip(),
        output_path="professional_videos/pinterest_culture_test.mp4"
    )
    
    if result:
        console.print("[bold green]✅ SUCCESS![/bold green]")
    else:
        console.print("[bold red]❌ Failed[/bold red]")
