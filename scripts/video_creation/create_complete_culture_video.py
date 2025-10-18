#!/usr/bin/env python3
"""
Complete Culture Video Generator
Topic → Script → Voice → Visuals → Final Video

Usage:
    python3 create_complete_culture_video.py "German Culture"
    python3 create_complete_culture_video.py "Japanese Samurai Culture"
    python3 create_complete_culture_video.py "African Tribal Traditions"
"""

from pathlib import Path
from rich.console import Console
import sys
import subprocess

console = Console()


def generate_culture_script(topic, duration_seconds=23):
    """
    Generate a DREAMY, FUTURISTIC script about a culture topic
    Blends past + future to inspire imagination
    
    Args:
        topic: Culture topic (e.g., "German Culture", "Japanese Samurai")
        duration_seconds: Target duration in seconds
    
    Returns:
        Script text
    """
    
    # Calculate approximate words needed (2.5 words per second)
    target_words = int(duration_seconds * 2.5)
    
    # Generate DREAMY script that blends past + future
    script = f"""
    Imagine {topic} reimagined for tomorrow.
    Where ancient traditions meet futuristic dreams.
    The past whispers secrets to the future.
    Every ritual, every dance, every story transformed.
    This is culture evolving, breathing, alive.
    A bridge between what was and what could be.
    Dream with us. The future remembers the past.
    """
    
    # Clean up
    script = " ".join(script.split()).strip()
    
    return script


def generate_voice_with_chatterbox(script_text, voice_name="Tomi_Zenyai", output_path="narrations/generated_voice.wav"):
    """
    Generate voice using Chatterbox Cloud API
    
    Args:
        script_text: Text to convert to speech
        voice_name: Voice to use
        output_path: Where to save audio
    
    Returns:
        Path to generated audio file
    """
    
    console.print("\n[bold cyan]🎙️  Generating Voice with Chatterbox Cloud[/bold cyan]\n")
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Use Chatterbox Cloud API
        from voice_providers.chatterbox_cloud_provider import ChatterboxCloudProvider
        
        console.print("[cyan]Connecting to Google Cloud Run...[/cyan]")
        
        provider = ChatterboxCloudProvider()
        
        result = provider.generate_voice(
            text=script_text,
            output_path=str(output_file)
        )
        
        if result:
            console.print(f"[green]✅ Voice generated from cloud: {output_file}[/green]\n")
            return str(output_file)
        else:
            raise Exception("Cloud API failed")
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Cloud API error: {str(e)[:60]}[/yellow]")
        console.print("[yellow]Using fallback test voice...[/yellow]\n")
        
        # Fallback to test voice
        fallback = Path("narrations/tomi_zenyai_test.wav")
        if fallback.exists():
            return str(fallback)
        else:
            console.print("[red]❌ No voice available![/red]")
            return None


def download_pinterest_visuals(topic, num_items=30, use_gifs=True):
    """
    Download Pinterest visuals for the topic
    OPTIMIZED: Blends past + future with artistic aesthetic
    
    Args:
        topic: Search topic
        num_items: Number of items to download
        use_gifs: If True, download GIFs; if False, download images
    
    Returns:
        Path to downloaded visuals directory
    """
    
    console.print(f"\n[bold cyan]📌 Downloading Pinterest Visuals[/bold cyan]\n")
    
    # SMART SEARCH: Blend past + future with artistic aesthetic
    # Use multiple optimized search terms to get the BEST visuals
    
    aesthetic_keywords = [
        "futuristic concept art",
        "sci-fi illustration",
        "digital painting",
        "cinematic art",
        "fantasy architecture",
        "dreamlike aesthetic",
        "surreal artistic",
        "painted illustration"
    ]
    
    # Create optimized search query
    if use_gifs:
        # For GIFs: Focus on animated, artistic, futuristic
        search_query = f"{topic} futuristic animated concept art illustration"
        script = "pinterest_gif_scraper.py"
    else:
        # For Images: Focus on painted, cinematic, blend of past/future
        search_query = f"{topic} futuristic concept art digital painting cinematic"
        script = "pinterest_scraper.py"
    
    console.print(f"[cyan]Search Strategy: Past + Future Aesthetic[/cyan]")
    console.print(f"[cyan]Query: {search_query}[/cyan]")
    console.print(f"[cyan]Type: {'Animated GIFs' if use_gifs else 'Cinematic Images'}[/cyan]\n")
    
    # Download
    result = subprocess.run(
        ["python3", script, search_query, str(num_items)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Determine output directory
        safe_query = search_query.replace(' ', '_')
        
        if use_gifs:
            visual_dir = f"/Users/tomi/Desktop/pinterest_gifs/{safe_query}"
        else:
            visual_dir = f"/Users/tomi/Desktop/pinterest_images/{safe_query}"
        
        console.print(f"[green]✅ Visuals downloaded to: {visual_dir}[/green]\n")
        return visual_dir
    else:
        console.print(f"[red]❌ Download failed: {result.stderr[:100]}[/red]")
        return None


def create_final_video(visual_dir, audio_path, script_text, topic, use_gifs=True):
    """
    Create final video with visuals, voice, and captions
    
    Args:
        visual_dir: Directory with visuals
        audio_path: Path to voice audio
        script_text: Script for captions
        topic: Video topic (for filename)
        use_gifs: Whether using GIFs or images
    
    Returns:
        Path to final video
    """
    
    console.print(f"\n[bold cyan]🎬 Creating Final Video[/bold cyan]\n")
    
    # Create safe filename
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_').lower()[:30]
    
    output_path = f"professional_videos/{safe_topic}_complete.mp4"
    
    # Choose creation method based on visual type
    if use_gifs:
        from create_pinterest_culture_video import create_culture_video_from_gifs
        
        result = create_culture_video_from_gifs(
            gif_dir=visual_dir,
            audio_path=audio_path,
            script_text=script_text,
            output_path=output_path
        )
    else:
        from create_cinematic_image_video import create_cinematic_video_from_images
        
        result = create_cinematic_video_from_images(
            image_dir=visual_dir,
            audio_path=audio_path,
            script_text=script_text,
            output_path=output_path,
            seconds_per_image=3.0
        )
    
    return result


def create_complete_culture_video(topic, use_gifs=True, duration=23):
    """
    Complete pipeline: Topic → Script → Voice → Visuals → Video
    
    Args:
        topic: Culture topic
        use_gifs: Use GIFs (True) or static images (False)
        duration: Target duration in seconds
    
    Returns:
        Path to final video
    """
    
    console.print("\n" + "="*60)
    console.print("[bold cyan]🎬 COMPLETE CULTURE VIDEO GENERATOR[/bold cyan]")
    console.print("="*60 + "\n")
    
    console.print(f"[yellow]Topic: {topic}[/yellow]")
    console.print(f"[yellow]Type: {'Animated GIFs' if use_gifs else 'Static Images'}[/yellow]")
    console.print(f"[yellow]Duration: {duration}s[/yellow]\n")
    
    # Step 1: Generate script
    console.print("[bold]Step 1/4: Generating Script[/bold]")
    script = generate_culture_script(topic, duration)
    
    console.print(f"[green]✅ Script created ({len(script.split())} words)[/green]")
    console.print(f"\n[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    console.print(f"[yellow]{script}[/yellow]")
    console.print(f"[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")
    
    # Step 2: Generate voice
    console.print("[bold]Step 2/4: Generating Voice[/bold]")
    
    # Create unique audio filename
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_').lower()[:30]
    audio_path = f"narrations/{safe_topic}_voice.wav"
    
    voice_file = generate_voice_with_chatterbox(script, output_path=audio_path)
    
    if not voice_file:
        console.print("[red]❌ Voice generation failed![/red]")
        return None
    
    # Step 3: Download visuals
    console.print("[bold]Step 3/4: Downloading Visuals[/bold]")
    
    visual_dir = download_pinterest_visuals(topic, num_items=30, use_gifs=use_gifs)
    
    if not visual_dir:
        console.print("[red]❌ Visual download failed![/red]")
        return None
    
    # Step 4: Create final video
    console.print("[bold]Step 4/4: Creating Final Video[/bold]")
    
    final_video = create_final_video(visual_dir, voice_file, script, topic, use_gifs)
    
    if final_video:
        console.print("\n" + "="*60)
        console.print("[bold green]🎉 COMPLETE VIDEO READY![/bold green]")
        console.print("="*60 + "\n")
        
        console.print(f"[cyan]📁 File: {final_video}[/cyan]")
        console.print(f"[cyan]🎨 Topic: {topic}[/cyan]")
        console.print(f"[cyan]🎙️  Voice: Your cloned voice[/cyan]")
        console.print(f"[cyan]📌 Source: Pinterest[/cyan]")
        console.print(f"[cyan]✨ Features: Captions, transitions, music[/cyan]\n")
        
        # Open video
        import subprocess
        subprocess.run(["open", str(final_video)])
        
        return final_video
    else:
        console.print("[red]❌ Video creation failed![/red]")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold]Complete Culture Video Generator[/bold]\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python3 create_complete_culture_video.py "Culture Topic" [--images]\n')
        console.print("[bold]Examples:[/bold]")
        console.print('  python3 create_complete_culture_video.py "German Culture"')
        console.print('  python3 create_complete_culture_video.py "Japanese Samurai Culture"')
        console.print('  python3 create_complete_culture_video.py "African Tribal Traditions"')
        console.print('  python3 create_complete_culture_video.py "Mexican Day of the Dead" --images\n')
        console.print("[bold cyan]💡 Tips:[/bold cyan]")
        console.print('  • Default: Uses animated GIFs')
        console.print('  • Add --images flag for static images with Ken Burns effect')
        console.print('  • Automatically generates script, voice, and visuals')
        console.print('  • Creates professional 9:16 video with captions')
        sys.exit(1)
    
    topic = sys.argv[1]
    use_gifs = "--images" not in sys.argv
    
    result = create_complete_culture_video(topic, use_gifs=use_gifs)
    
    if result:
        console.print("[bold green]✅ SUCCESS![/bold green]")
    else:
        console.print("[bold red]❌ FAILED![/bold red]")
