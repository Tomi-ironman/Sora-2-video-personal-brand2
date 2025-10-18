#!/usr/bin/env python3
"""
Add Auto-Captions to Videos
Word-by-word captions like TikTok/Instagram Reels!
"""

from pathlib import Path
import subprocess
import json
from rich.console import Console

console = Console()

def transcribe_audio_with_whisper(audio_path):
    """
    Transcribe audio with word-level timestamps using Whisper
    """
    
    console.print("[bold]Transcribing audio with Whisper...[/bold]")
    
    try:
        # Use whisper for transcription with word timestamps
        cmd = [
            "whisper",
            str(audio_path),
            "--model", "base",
            "--output_format", "json",
            "--language", "en",
            "--word_timestamps", "True",
            "--output_dir", "temp_captions"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Read the JSON output
            json_file = Path("temp_captions") / f"{Path(audio_path).stem}.json"
            if json_file.exists():
                with open(json_file, 'r') as f:
                    data = json.load(f)
                console.print("[green]✅ Transcription complete![/green]")
                return data
        
    except FileNotFoundError:
        console.print("[yellow]⚠️  Whisper not installed, using script text instead[/yellow]")
    
    return None

def create_srt_from_script(script_text, total_duration):
    """
    Create SRT captions from script text with estimated timing
    """
    
    import re
    
    # Split into words
    words = re.findall(r'\b\w+\b|\S', script_text)
    
    # Calculate time per word
    time_per_word = total_duration / len(words)
    
    srt_content = []
    
    for i, word in enumerate(words):
        if not word.strip():
            continue
        
        start_time = i * time_per_word
        end_time = (i + 1) * time_per_word
        
        # Format as SRT
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        srt_content.append(f"{i+1}\n")
        srt_content.append(f"{start_str} --> {end_str}\n")
        srt_content.append(f"{word}\n\n")
    
    return ''.join(srt_content)

def create_srt_from_whisper(whisper_data):
    """
    Create SRT from Whisper word-level timestamps
    """
    
    srt_content = []
    idx = 1
    
    for segment in whisper_data.get('segments', []):
        for word_data in segment.get('words', []):
            word = word_data.get('word', '').strip()
            start = word_data.get('start', 0)
            end = word_data.get('end', 0)
            
            if not word:
                continue
            
            start_str = format_srt_time(start)
            end_str = format_srt_time(end)
            
            srt_content.append(f"{idx}\n")
            srt_content.append(f"{start_str} --> {end_str}\n")
            srt_content.append(f"{word}\n\n")
            
            idx += 1
    
    return ''.join(srt_content)

def format_srt_time(seconds):
    """
    Format seconds as SRT timestamp (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def add_captions_to_video(
    video_path,
    output_path,
    audio_path=None,
    script_text=None,
    style="modern"
):
    """
    Add auto-captions to video
    
    Args:
        video_path: Input video
        output_path: Output with captions
        audio_path: Audio file for transcription (optional)
        script_text: Script text for fallback timing
        style: Caption style ("modern", "minimal", "bold")
    """
    
    console.print("\n[bold cyan]📝 Adding Auto-Captions[/bold cyan]\n")
    
    video_path = Path(video_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    temp_dir = Path("temp_captions")
    temp_dir.mkdir(exist_ok=True)
    
    # Get video duration
    duration_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    result = subprocess.run(duration_cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())
    
    # Try Whisper transcription first
    srt_content = None
    
    if audio_path:
        whisper_data = transcribe_audio_with_whisper(audio_path)
        if whisper_data:
            srt_content = create_srt_from_whisper(whisper_data)
            console.print("[green]✅ Using Whisper word-level timing[/green]")
    
    # Fallback to script-based timing
    if not srt_content and script_text:
        srt_content = create_srt_from_script(script_text, total_duration)
        console.print("[yellow]Using script-based timing[/yellow]")
    
    if not srt_content:
        console.print("[red]❌ No captions generated[/red]")
        return None
    
    # Save SRT file
    srt_file = temp_dir / "captions.srt"
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    console.print(f"[green]✅ SRT created: {len(srt_content.splitlines())} lines[/green]\n")
    
    # Define caption styles
    styles = {
        "modern": {
            # TikTok/Instagram style - word by word, yellow/white
            "force_style": (
                "FontName=Arial Black,"
                "FontSize=32,"
                "PrimaryColour=&H00FFFF&,"  # Yellow
                "OutlineColour=&H000000&,"   # Black outline
                "BackColour=&H80000000,"     # Semi-transparent black
                "Bold=1,"
                "Outline=2,"
                "Shadow=0,"
                "Alignment=2,"  # Bottom center
                "MarginV=80"
            )
        },
        "minimal": {
            # Clean white text
            "force_style": (
                "FontName=Arial,"
                "FontSize=28,"
                "PrimaryColour=&HFFFFFF&,"  # White
                "OutlineColour=&H000000&,"   # Black outline
                "Bold=0,"
                "Outline=1,"
                "Shadow=1,"
                "Alignment=2,"
                "MarginV=60"
            )
        },
        "bold": {
            # Big bold text
            "force_style": (
                "FontName=Impact,"
                "FontSize=40,"
                "PrimaryColour=&HFFFFFF&,"  # White
                "OutlineColour=&H000000&,"   # Black outline
                "Bold=1,"
                "Outline=3,"
                "Shadow=2,"
                "Alignment=2,"
                "MarginV=100"
            )
        }
    }
    
    selected_style = styles.get(style, styles["modern"])
    
    console.print(f"[cyan]Applying '{style}' caption style...[/cyan]")
    
    # Burn captions into video with FFmpeg
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vf", f"subtitles={srt_file}:force_style='{selected_style['force_style']}'",
        "-c:a", "copy",  # Copy audio
        "-y",
        str(output_path)
    ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        console.print(f"\n[bold green]🎉 Captions added successfully![/bold green]")
        console.print(f"[cyan]📁 Saved to:[/cyan] {output_path}")
        
        file_size = output_path.stat().st_size / (1024 * 1024)
        console.print(f"[cyan]📊 Size:[/cyan] {file_size:.1f} MB")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        return output_path
    else:
        console.print(f"[red]❌ Error adding captions[/red]")
        console.print(f"[dim]{result.stderr}[/dim]")
        return None


if __name__ == "__main__":
    console.print("\n[bold cyan]📝 Testing Auto-Captions[/bold cyan]\n")
    
    # Test script
    SCRIPT = """
    Culture is the heartbeat of humanity. It's our stories, our traditions, our soul.
    AI doesn't erase culture, it amplifies it. It helps us preserve what makes us human,
    share our heritage across borders, and celebrate our diversity.
    Technology and tradition, hand in hand, creating a richer future for all.
    """
    
    # Add captions to the synced video
    result = add_captions_to_video(
        video_path="professional_videos/culture_ai_SYNCED_v2.mp4",
        output_path="professional_videos/culture_ai_WITH_CAPTIONS.mp4",
        audio_path="narrations/tomi_zenyai_test.wav",
        script_text=SCRIPT.strip(),
        style="modern"  # Try: "modern", "minimal", or "bold"
    )
    
    if result:
        console.print("\n[bold green]✅ Video with captions ready![/bold green]")
        console.print("\n[bold]🎬 Caption styles available:[/bold]")
        console.print("  • modern  - TikTok/Instagram style (yellow, word-by-word)")
        console.print("  • minimal - Clean white text")
        console.print("  • bold    - Big impact text")
        
        # Open video
        subprocess.run(["open", str(result)])
