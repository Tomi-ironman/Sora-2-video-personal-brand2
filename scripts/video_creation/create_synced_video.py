#!/usr/bin/env python3
"""
Smart Video-Narration Sync
Matches B-roll to exactly what you're saying at each moment!
"""

from pathlib import Path
import subprocess
import requests
import json
import os
import colorsys
import math
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from rich.console import Console
import numpy as np
from PIL import Image
import io

console = Console()

# Load environment variables
load_dotenv()

# API keys
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'Xx747gOZoWryJBlB3Q70KVzqeEDxE5YkrWjokSQ3vHzZvDAXY6fOCr8r')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '50169877-0f51f8bb1485fc7c948b8e10c')

# Import video selection functions from create_voiceover_video
from create_voiceover_video import (
    get_video_thumbnail_colors,
    color_difference,
    search_pexels_videos,
    search_pixabay_videos,
    download_video
)

def parse_script_segments(script_text, total_duration):
    """
    Parse script into time-based segments with UNIQUE search queries
    
    Args:
        script_text: Full narration text
        total_duration: Total audio duration in seconds
        
    Returns:
        List of segments with [start_time, end_time, text, search_query]
    """
    
    # Split script into sentences
    import re
    sentences = re.split(r'[.!?]+', script_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Calculate time per sentence (evenly distributed)
    time_per_sentence = total_duration / len(sentences)
    
    segments = []
    previous_queries = []  # Track queries to ensure uniqueness
    
    for i, sentence in enumerate(sentences):
        start_time = i * time_per_sentence
        end_time = (i + 1) * time_per_sentence
        
        # Generate UNIQUE search query from sentence keywords
        search_query = extract_visual_keywords(sentence, previous_queries)
        previous_queries.append(search_query)
        
        segments.append({
            'start': start_time,
            'end': end_time,
            'duration': end_time - start_time,
            'text': sentence,
            'search_query': search_query
        })
    
    return segments

def extract_visual_keywords(text, previous_queries=[]):
    """
    Extract visual keywords from text for video search
    ENSURES UNIQUE QUERIES to avoid duplicate videos!
    
    Examples:
    "Culture is the heartbeat of humanity" → "cultural diversity people"
    "AI doesn't erase culture" → "artificial intelligence technology"
    "our traditions" → "traditional heritage customs"
    """
    
    text_lower = text.lower()
    
    # Keyword mapping: text phrases → visual search terms (with variations!)
    keyword_map = {
        # Culture keywords (multiple variations)
        'culture': ['cultural diversity people', 'world cultures celebration', 'ethnic traditions global'],
        'heartbeat': ['heartbeat rhythm pulse', 'life energy vibrant', 'living breathing dynamic'],
        'humanity': ['human diversity world', 'people together global', 'mankind unity earth'],
        'stories': ['storytelling narrative people', 'oral tradition telling', 'sharing stories community'],
        'traditions': ['traditional cultural heritage', 'customs rituals ancient', 'cultural practices historical'],
        'soul': ['emotional soul spiritual', 'inner spirit essence', 'deep feelings human'],
        
        # AI/Tech keywords
        'ai': ['artificial intelligence technology', 'AI machine learning future', 'digital AI innovation'],
        "doesn't erase": ['technology preserve culture', 'digital preservation heritage', 'tech enhancing tradition'],
        'amplifies': ['amplify enhance empower', 'strengthen boost improve', 'magnify increase elevate'],
        'technology': ['modern technology innovation', 'digital tech future', 'technological advancement'],
        'preserve': ['preservation heritage protect', 'conserve tradition maintain', 'safeguard cultural legacy'],
        
        # Unity keywords
        'share': ['sharing community together', 'exchange knowledge global', 'connect people worldwide'],
        'heritage': ['cultural heritage legacy', 'ancestral traditions history', 'historical culture roots'],
        'borders': ['global world international', 'across nations worldwide', 'borderless unity earth'],
        'celebrate': ['celebration festival joy', 'cultural celebration dancing', 'happy festive gathering'],
        'diversity': ['cultural diversity variety', 'multicultural different people', 'varied ethnic groups'],
        
        # Future keywords
        'future': ['future innovation progress', 'tomorrow advancement technology', 'next generation evolving'],
        'hand in hand': ['hands together unity', 'cooperation collaboration teamwork', 'partnership working together'],
        'richer': ['abundance prosperity vibrant', 'colorful rich diverse', 'thriving flourishing dynamic']
    }
    
    # Find matching keywords and pick a variation that hasn't been used
    matched_terms = []
    for keyword, visual_terms in keyword_map.items():
        if keyword in text_lower:
            # Pick a variation that's different from previous queries
            for term in visual_terms:
                if term not in previous_queries:
                    matched_terms.append(term)
                    break
            else:
                # All variations used, use first one
                matched_terms.append(visual_terms[0])
    
    # If no specific match, extract nouns/adjectives
    if not matched_terms:
        words = text_lower.split()
        visual_words = [w for w in words if len(w) > 4 and w not in ['doesn', 'makes', 'human', 'what', 'that', 'this']]
        matched_terms = [' '.join(visual_words[:3])] if visual_words else ['people culture world']
    
    # Return first matched term that's unique
    for term in matched_terms:
        if term not in previous_queries:
            return term
    
    # Fallback: add variation number to make it unique
    base_term = matched_terms[0] if matched_terms else 'culture people'
    return f"{base_term} variation"

def create_synced_video(
    audio_path,
    script_text,
    output_path,
    aspect_ratio="9:16",
    add_music=True
):
    """
    Create video with B-roll synced to narration content!
    
    Args:
        audio_path: Path to audio file
        script_text: Full script text (for semantic matching)
        output_path: Output video path
        aspect_ratio: "9:16" or "16:9"
        add_music: Add background music
    """
    
    console.print("\n[bold cyan]🎬 Creating Smart-Synced Video[/bold cyan]")
    console.print("[cyan]📱 Matching B-roll to narration content![/cyan]\n")
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    audio_path = Path(audio_path)
    if not audio_path.exists():
        console.print(f"[red]❌ Audio file not found: {audio_path}[/red]")
        return None
    
    # Create temp directories
    temp_dir = Path("temp_synced")
    temp_dir.mkdir(exist_ok=True)
    
    broll_dir = temp_dir / "broll"
    broll_dir.mkdir(exist_ok=True)
    
    # Get audio duration
    console.print("[bold]Step 1: Analyzing audio & script[/bold]")
    duration_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(duration_cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())
    
    console.print(f"[cyan]⏱️  Audio duration: {total_duration:.1f} seconds[/cyan]")
    
    # Parse script into time-based segments
    segments = parse_script_segments(script_text, total_duration)
    
    console.print(f"\n[bold cyan]📝 Script Breakdown:[/bold cyan]")
    for i, seg in enumerate(segments):
        console.print(f"  [{seg['start']:.1f}s-{seg['end']:.1f}s] \"{seg['text'][:50]}...\" → [cyan]{seg['search_query']}[/cyan]")
    
    # Download B-roll for each segment
    console.print(f"\n[bold]Step 2: Downloading synced B-roll[/bold]\n")
    
    previous_colors = []
    downloaded_video_ids = []  # Track video IDs to prevent duplicates
    broll_videos = []
    
    for i, segment in enumerate(segments):
        console.print(f"[bold cyan]{i+1}/{len(segments)}: {segment['search_query']}[/bold cyan]")
        console.print(f"[dim]  Time: {segment['start']:.1f}s-{segment['end']:.1f}s | \"{segment['text'][:60]}...\"[/dim]")
        
        # Search both providers with segment-specific query
        pexels_videos = search_pexels_videos(segment['search_query'], per_page=10)
        pixabay_videos = search_pixabay_videos(segment['search_query'], per_page=10)
        
        all_videos = pexels_videos + pixabay_videos
        console.print(f"[dim]  Found {len(all_videos)} total videos[/dim]")
        
        if not all_videos:
            console.print(f"[yellow]⚠️  No videos, using fallback[/yellow]")
            # Fallback to generic search
            all_videos = search_pexels_videos("culture people", per_page=5)
        
        # Score and select best video (skip duplicates!)
        scored_videos = []
        
        for video in all_videos:
            video_id = video.get('id')
            
            # Skip if we already downloaded this video
            if video_id in downloaded_video_ids:
                continue
            
            score = 0
            reasons = []
            
            # Duration check
            duration = video.get('duration', 10)
            if 5 <= duration <= 20:
                score += 30
                reasons.append(f"duration={duration}s")
            
            # Popularity
            if video.get('views', 0) > 10000:
                score += 20
                reasons.append("popular")
            
            # Quality
            has_hd = any(vf.get('width', 0) >= 1920 for vf in video.get('video_files', []))
            if has_hd:
                score += 25
                reasons.append("HD")
            
            # Color diversity
            thumbnail = video.get('image', '')
            if thumbnail:
                video_color = get_video_thumbnail_colors(thumbnail)
                if video_color and previous_colors:
                    min_diff = min([color_difference(video_color, prev) for prev in previous_colors])
                    if min_diff > 0.3:
                        score += 15
                        reasons.append("unique-color")
                    elif min_diff < 0.15:
                        score -= 20
            
            # Source bonus
            if video.get('source') == 'pexels':
                score += 5
            
            scored_videos.append({
                'video': video,
                'score': score,
                'reasons': reasons,
                'color': get_video_thumbnail_colors(video.get('image', ''))
            })
        
        # Pick best
        scored_videos.sort(key=lambda x: x['score'], reverse=True)
        best = scored_videos[0]
        video = best['video']
        
        console.print(f"[green]  ✓ Best: {video.get('source', 'unknown').upper()} "
                     f"(score: {best['score']})[/green]")
        
        # Download video
        video_files = video.get('video_files', [])
        hd_file = None
        
        for quality in ['hd', 'large', 'sd', 'medium']:
            for vf in video_files:
                if vf.get('quality', '').lower() == quality or vf.get('width', 0) >= 1920:
                    hd_file = vf
                    break
            if hd_file:
                break
        
        if not hd_file and video_files:
            hd_file = video_files[0]
        
        if hd_file:
            video_url = hd_file['link']
            video_path = broll_dir / f"clip_{i:02d}.mp4"
            download_video(video_url, video_path)
            
            # Track this video ID to prevent duplicates
            video_id = video.get('id')
            if video_id:
                downloaded_video_ids.append(video_id)
            
            # Store with segment info
            segment['video_path'] = video_path
            broll_videos.append(segment)
            
            if best['color']:
                previous_colors.append(best['color'])
            
            console.print(f"[green]✅ Downloaded[/green]\n")
    
    # Create video with synced timing
    console.print("[bold]Step 3: Creating synced montage[/bold]\n")
    
    # Process each video clip with exact timing
    trimmed_clips = []
    
    for i, segment in enumerate(broll_videos):
        trimmed_path = broll_dir / f"trimmed_{i:02d}.mp4"
        video = segment['video_path']
        clip_duration = segment['duration']
        
        # Determine output dimensions
        if aspect_ratio == "9:16":
            output_width = 1080
            output_height = 1920
            scale_filter = f"scale=-1:{output_height}:force_original_aspect_ratio=increase"
            crop_filter = f"crop={output_width}:{output_height}:(in_w-{output_width})/2:0"
        else:
            output_width = 1920
            output_height = 1080
            scale_filter = f"scale={output_width}:{output_height}:force_original_aspect_ratio=decrease,pad={output_width}:{output_height}:(ow-iw)/2:(oh-ih)/2"
            crop_filter = ""
        
        # Color grading
        color_filter = "eq=saturation=1.3:contrast=1.1:brightness=0.02,vignette=PI/4"
        
        # Combine filters
        if crop_filter:
            video_filter = f"{scale_filter},{crop_filter},{color_filter}"
        else:
            video_filter = f"{scale_filter},{color_filter}"
        
        # Get original duration
        duration_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "default=noprint_wrappers=1:nokey=1", str(video)]
        result = subprocess.run(duration_cmd, capture_output=True, text=True)
        original_duration = float(result.stdout.strip())
        
        if original_duration < clip_duration:
            loops = int(clip_duration / original_duration) + 2
            trim_cmd = [
                "ffmpeg", "-stream_loop", str(loops),
                "-i", str(video), "-t", str(clip_duration),
                "-vf", video_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-an", "-y", str(trimmed_path)
            ]
        else:
            trim_cmd = [
                "ffmpeg", "-i", str(video), "-t", str(clip_duration),
                "-vf", video_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-an", "-y", str(trimmed_path)
            ]
        
        subprocess.run(trim_cmd, capture_output=True, check=True)
        trimmed_clips.append(trimmed_path)
        console.print(f"[dim]  Clip {i+1}: {clip_duration:.1f}s → \"{segment['text'][:40]}...\"[/dim]")
    
    # Concatenate
    concat_file = temp_dir / "concat.txt"
    with open(concat_file, 'w') as f:
        for clip in trimmed_clips:
            f.write(f"file '{clip.absolute()}'\n")
    
    concat_output = temp_dir / "video_no_audio.mp4"
    concat_cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy",
        "-y", str(concat_output)
    ]
    subprocess.run(concat_cmd, capture_output=True, check=True)
    console.print("[green]✅ Montage created[/green]\n")
    
    # Add music (optional)
    music_path = None
    if add_music:
        console.print("[bold]Step 4: Adding background music[/bold]")
        try:
            music_url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q=ambient+background&media_type=music&per_page=1"
            response = requests.get(music_url)
            if response.status_code == 200:
                data = response.json()
                if data.get('hits'):
                    music_url = data['hits'][0]['previewURL']
                    music_path = temp_dir / "background_music.mp3"
                    download_video(music_url, music_path)
                    console.print("[green]✅ Music downloaded[/green]\n")
        except:
            pass
    
    # Final mix
    console.print("[bold]Step 5: Adding voiceover + mixing[/bold]")
    
    if music_path and music_path.exists():
        final_cmd = [
            "ffmpeg",
            "-i", str(concat_output),
            "-i", str(audio_path),
            "-i", str(music_path),
            "-filter_complex",
            f"[1:a]volume=1.0[voice];[2:a]volume=0.15,afade=t=in:d=2:curve=log,afade=t=out:st={total_duration-2}:d=2:curve=log[music];[voice][music]amix=inputs=2:duration=shortest[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-y", str(output)
        ]
    else:
        final_cmd = [
            "ffmpeg",
            "-i", str(concat_output),
            "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-y", str(output)
        ]
    
    subprocess.run(final_cmd, capture_output=True, check=True)
    
    console.print(f"\n[bold green]🎉 Smart-Synced Video Created![/bold green]")
    console.print(f"[cyan]📁 Saved to:[/cyan] {output}")
    
    file_size = output.stat().st_size / (1024 * 1024)
    console.print(f"[cyan]📊 Size:[/cyan] {file_size:.1f} MB")
    console.print(f"[cyan]⏱️  Duration:[/cyan] {total_duration:.1f} seconds")
    
    console.print("\n[bold]✨ Smart Features:[/bold]")
    console.print("✅ B-roll matched to narration content")
    console.print("✅ Each clip synced to what you're saying")
    console.print("✅ Intelligent video selection")
    console.print(f"✅ {aspect_ratio} format")
    
    # Open
    console.print("\n[cyan]Opening video...[/cyan]")
    subprocess.run(["open", str(output)])
    
    # Cleanup
    console.print("\n[dim]Cleaning up...[/dim]")
    import shutil
    shutil.rmtree(temp_dir)
    
    return output


if __name__ == "__main__":
    # Culture & AI script
    SCRIPT = """
    Culture is the heartbeat of humanity. It's our stories, our traditions, our soul.
    AI doesn't erase culture, it amplifies it. It helps us preserve what makes us human,
    share our heritage across borders, and celebrate our diversity.
    Technology and tradition, hand in hand, creating a richer future for all.
    """
    
    console.print("\n[bold cyan]🌍 Culture & AI - Smart-Synced Video[/bold cyan]")
    console.print("[dim]B-roll matched to narration content![/dim]\n")
    
    result = create_synced_video(
        audio_path="narrations/tomi_zenyai_test.wav",
        script_text=SCRIPT.strip(),
        output_path="professional_videos/culture_ai_SYNCED_v2.mp4",
        aspect_ratio="9:16",
        add_music=True
    )
    
    if result:
        console.print("\n[bold green]✅ Your smart-synced video is ready![/bold green]")
        console.print("\n[dim]B-roll perfectly matched to what you're saying![/dim]")
