#!/usr/bin/env python3
"""
Create Professional Voiceover Video
Your voice + B-roll footage = Professional content!
"""

from pathlib import Path
import subprocess
import requests
import json
import os
import colorsys
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

def get_video_thumbnail_colors(thumbnail_url):
    """Extract dominant colors from video thumbnail"""
    try:
        response = requests.get(thumbnail_url, timeout=5)
        img = Image.open(io.BytesIO(response.content))
        img = img.resize((100, 100))  # Downsize for speed
        img_array = np.array(img)
        
        # Get average RGB
        avg_color = img_array.mean(axis=(0, 1))
        
        # Convert to HSV for better comparison
        hsv = colorsys.rgb_to_hsv(avg_color[0]/255, avg_color[1]/255, avg_color[2]/255)
        return hsv
    except:
        return None

def color_difference(color1, color2):
    """Calculate color difference (0-1, higher = more different)"""
    if not color1 or not color2:
        return 1.0
    
    # HSV distance
    h_diff = min(abs(color1[0] - color2[0]), 1 - abs(color1[0] - color2[0]))
    s_diff = abs(color1[1] - color2[1])
    v_diff = abs(color1[2] - color2[2])
    
    return (h_diff * 2 + s_diff + v_diff) / 4

def search_pexels_videos(query, per_page=10):
    """Search Pexels for videos with metadata"""
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "landscape",
        "size": "large"  # Get larger for better quality
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        videos = response.json().get('videos', [])
        # Add source tag
        for v in videos:
            v['source'] = 'pexels'
        return videos
    return []

def search_pixabay_videos(query, per_page=10):
    """Search Pixabay for videos with metadata"""
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "per_page": per_page,
        "video_type": "all"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for hit in data.get('hits', []):
                # Convert Pixabay format to Pexels-like format
                video_files = []
                for key in ['large', 'medium', 'small']:
                    if key in hit['videos']:
                        video_files.append({
                            'quality': key,
                            'width': hit['videos'][key].get('width', 1920),
                            'height': hit['videos'][key].get('height', 1080),
                            'link': hit['videos'][key]['url']
                        })
                
                videos.append({
                    'id': hit['id'],
                    'duration': hit.get('duration', 10),
                    'video_files': video_files,
                    'image': hit.get('picture_id', ''),  # Thumbnail
                    'user': {'name': hit.get('user', 'Pixabay')},
                    'views': hit.get('views', 0),
                    'likes': hit.get('likes', 0),
                    'source': 'pixabay'
                })
            
            return videos
    except Exception as e:
        console.print(f"[yellow]Pixabay search failed: {e}[/yellow]")
    
    return []

def download_video(url, output_path):
    """Download video from URL"""
    console.print(f"[cyan]Downloading: {output_path.name}...[/cyan]")
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path

def create_voiceover_video(audio_path, output_path, search_queries=None, max_clip_duration=3, add_music=True, aspect_ratio="9:16"):
    """
    Create professional video with voiceover + B-roll
    
    Args:
        audio_path: Path to voiceover audio file
        output_path: Path for output video
        search_queries: List of search terms for B-roll (specific to topic!)
        max_clip_duration: Max seconds per clip (2-3 for better pacing, prevents freezing)
        add_music: Add background music for professional feel
        aspect_ratio: "9:16" for social media (portrait) or "16:9" for YouTube (landscape)
    """
    
    console.print("\n[bold cyan]🎬 Creating Professional Voiceover Video[/bold cyan]")
    console.print(f"[cyan]📱 Format: {aspect_ratio} ({'Portrait/Social Media' if aspect_ratio == '9:16' else 'Landscape/YouTube'})[/cyan]\n")
    
    # MORE search queries - SPECIFIC to Culture & AI theme
    # Need 10-15 clips for 23 seconds to prevent freezing!
    if not search_queries:
        search_queries = [
            "diverse people cultures",
            "traditional cultural art",
            "storytelling heritage",
            "global traditions",
            "artificial intelligence",
            "technology innovation",
            "cultural preservation",
            "world diversity",
            "community celebration",
            "digital culture",
            "future technology",
            "human connection"
        ]
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    audio_path = Path(audio_path)
    if not audio_path.exists():
        console.print(f"[red]❌ Audio file not found: {audio_path}[/red]")
        return None
    
    # Create temp directories
    temp_dir = Path("temp_voiceover")
    temp_dir.mkdir(exist_ok=True)
    
    broll_dir = temp_dir / "broll"
    broll_dir.mkdir(exist_ok=True)
    
    # Step 1: Use existing voice
    console.print("[bold]Step 1: Using your voice audio[/bold]")
    console.print(f"[green]✅ Voice audio: {audio_path}[/green]\n")
    
    # Get audio duration
    duration_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(duration_cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())
    
    console.print(f"[cyan]⏱️  Voiceover duration: {total_duration:.1f} seconds[/cyan]\n")
    
    # Step 2: Download B-roll videos (SMART CALCULATION!)
    console.print("[bold]Step 2: Downloading B-roll footage[/bold]")
    
    # INTELLIGENT CALCULATION: How many clips do we need?
    import math
    clips_needed = math.ceil(total_duration / max_clip_duration)
    
    # Add 1 extra for safety margin
    clips_needed += 1
    
    # Don't exceed available search queries
    clips_needed = min(clips_needed, len(search_queries))
    
    console.print(f"[bold cyan]📐 Math:[/bold cyan]")
    console.print(f"  Voiceover: {total_duration:.1f} seconds")
    console.print(f"  Max clip: {max_clip_duration:.1f} seconds")
    console.print(f"  Calculation: {total_duration:.1f} ÷ {max_clip_duration:.1f} = {total_duration/max_clip_duration:.2f}")
    console.print(f"  Videos needed: {clips_needed} clips\n")
    
    broll_videos = []
    total_downloaded_duration = 0
    
    previous_colors = []  # Track colors to avoid similar videos
    
    for i, query in enumerate(search_queries[:clips_needed]):
        console.print(f"\n[bold cyan]{i+1}/{clips_needed}: '{query}'[/bold cyan]")
        
        # Search BOTH providers
        pexels_videos = search_pexels_videos(query, per_page=10)
        pixabay_videos = search_pixabay_videos(query, per_page=10)
        
        all_videos = pexels_videos + pixabay_videos
        console.print(f"[dim]  Found {len(pexels_videos)} Pexels + {len(pixabay_videos)} Pixabay = {len(all_videos)} total[/dim]")
        
        if not all_videos:
            console.print(f"[yellow]⚠️  No videos found for '{query}'[/yellow]")
            continue
        
        # INTELLIGENT SELECTION: Score each video
        scored_videos = []
        
        for video in all_videos:
            score = 0
            reasons = []
            
            # 1. Duration check (prefer 5-20 second videos)
            duration = video.get('duration', 10)
            if 5 <= duration <= 20:
                score += 30
                reasons.append(f"duration={duration}s")
            elif duration > 20:
                score += 15
            
            # 2. Popularity (views/likes)
            views = video.get('views', 0)
            likes = video.get('likes', 0)
            if views > 10000:
                score += 20
                reasons.append(f"popular")
            if likes > 100:
                score += 10
            
            # 3. Quality (prefer HD)
            video_files = video.get('video_files', [])
            has_hd = any(vf.get('width', 0) >= 1920 for vf in video_files)
            if has_hd:
                score += 25
                reasons.append("HD")
            
            # 4. Color diversity (avoid similar colors)
            thumbnail = video.get('image', '')
            if thumbnail:
                video_color = get_video_thumbnail_colors(thumbnail)
                if video_color and previous_colors:
                    # Calculate difference from all previous videos
                    min_diff = min([color_difference(video_color, prev) for prev in previous_colors])
                    if min_diff > 0.3:  # Different enough
                        score += 15
                        reasons.append("unique-color")
                    elif min_diff < 0.15:  # Too similar
                        score -= 20
                        reasons.append("similar-color")
            
            # 5. Source bonus (Pexels tends to be higher quality)
            if video.get('source') == 'pexels':
                score += 5
            
            scored_videos.append({
                'video': video,
                'score': score,
                'reasons': reasons,
                'color': get_video_thumbnail_colors(video.get('image', ''))
            })
        
        # Sort by score (highest first)
        scored_videos.sort(key=lambda x: x['score'], reverse=True)
        
        # Pick the best video
        best = scored_videos[0]
        video = best['video']
        
        console.print(f"[green]  ✓ Best: {video.get('source', 'unknown').upper()} "
                     f"(score: {best['score']}) - {', '.join(best['reasons'][:3])}[/green]")
        
        # Download the best video
        video_files = video.get('video_files', [])
        hd_file = None
        
        # Get highest quality available
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
            broll_videos.append(video_path)
            total_downloaded_duration += max_clip_duration
            
            # Track color for next iteration
            if best['color']:
                previous_colors.append(best['color'])
            
            console.print(f"[green]✅ Downloaded (cumulative: {total_downloaded_duration:.1f}s)[/green]")
    
    if not broll_videos:
        console.print("[red]❌ No B-roll videos downloaded[/red]")
        return None
    
    console.print(f"\n[green]✅ Downloaded {len(broll_videos)} B-roll clips[/green]\n")
    
    # Step 3: Create video montage with seamless transitions
    console.print("[bold]Step 3: Creating seamless video montage[/bold]")
    
    # SMART CALCULATION: Each clip should be exactly this long
    clips_count = len(broll_videos)
    clip_duration = total_duration / clips_count
    
    # But cap at max_clip_duration
    if clip_duration > max_clip_duration:
        clip_duration = max_clip_duration
    
    console.print(f"[bold cyan]📐 Clip sizing:[/bold cyan]")
    console.print(f"  Total needed: {total_duration:.1f}s")
    console.print(f"  Clips: {clips_count}")
    console.print(f"  Each clip: {clip_duration:.1f}s")
    console.print(f"  Total coverage: {clips_count * clip_duration:.1f}s")
    
    # Verify we have enough coverage
    total_coverage = clips_count * clip_duration
    if total_coverage < total_duration:
        console.print(f"[yellow]⚠️  Coverage gap: {total_duration - total_coverage:.1f}s short![/yellow]")
        console.print(f"[yellow]   Extending last clip to fill gap...[/yellow]")
    else:
        console.print(f"[green]✅ Full coverage achieved![/green]")
    
    console.print()
    
    # Create concat file for FFmpeg
    concat_file = temp_dir / "concat.txt"
    trimmed_clips = []
    
    for i, video in enumerate(broll_videos):
        trimmed_path = broll_dir / f"trimmed_{i:02d}.mp4"
        
        # Get original video duration
        duration_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video)
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True)
        original_duration = float(result.stdout.strip())
        
        # Calculate this clip's duration
        this_clip_duration = clip_duration
        
        # If this is the last clip and we have a gap, extend it
        if i == len(broll_videos) - 1:
            total_so_far = (len(broll_videos) - 1) * clip_duration
            remaining = total_duration - total_so_far
            if remaining > clip_duration:
                this_clip_duration = remaining
                console.print(f"[yellow]  Extending final clip to {this_clip_duration:.1f}s[/yellow]")
        
        # SMART CROP + CINEMATIC COLOR GRADING
        # Determine output dimensions based on aspect ratio
        if aspect_ratio == "9:16":
            # Portrait for social media (TikTok, Instagram Reels, YouTube Shorts)
            output_width = 1080
            output_height = 1920
            # Smart crop: scale to height, then crop center width
            scale_filter = f"scale=-1:{output_height}:force_original_aspect_ratio=increase"
            crop_filter = f"crop={output_width}:{output_height}:(in_w-{output_width})/2:0"
        else:
            # Landscape for YouTube
            output_width = 1920
            output_height = 1080
            scale_filter = f"scale={output_width}:{output_height}:force_original_aspect_ratio=decrease,pad={output_width}:{output_height}:(ow-iw)/2:(oh-ih)/2"
            crop_filter = ""
        
        # Cinematic color grading
        color_filter = "eq=saturation=1.3:contrast=1.1:brightness=0.02,vignette=PI/4"
        
        # Combine filters
        if crop_filter:
            video_filter = f"{scale_filter},{crop_filter},{color_filter}"
        else:
            video_filter = f"{scale_filter},{color_filter}"
        
        if original_duration < this_clip_duration:
            # Loop video MULTIPLE times to ensure no freezing
            loops_needed = int(this_clip_duration / original_duration) + 2
            trim_cmd = [
                "ffmpeg", "-stream_loop", str(loops_needed),
                "-i", str(video),
                "-t", str(this_clip_duration),
                "-vf", video_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",  # Better quality
                "-an",  # Remove audio from video clips
                "-y", str(trimmed_path)
            ]
        else:
            # Trim video to exact duration with smart crop + color grading
            trim_cmd = [
                "ffmpeg",
                "-i", str(video),
                "-t", str(this_clip_duration),
                "-vf", video_filter,
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-an",  # Remove audio from video clips
                "-y", str(trimmed_path)
            ]
        
        subprocess.run(trim_cmd, capture_output=True, check=True)
        trimmed_clips.append(trimmed_path)
        console.print(f"[dim]  Clip {i+1}: {this_clip_duration:.1f}s[/dim]")
    
    # Create concat file
    with open(concat_file, 'w') as f:
        for clip in trimmed_clips:
            f.write(f"file '{clip.absolute()}'\n")
    
    # Concatenate videos
    concat_output = temp_dir / "video_no_audio.mp4"
    concat_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        "-y",
        str(concat_output)
    ]
    
    subprocess.run(concat_cmd, capture_output=True, check=True)
    console.print("[green]✅ B-roll montage created[/green]\n")
    
    # Step 4: Download background music (optional)
    music_path = None
    if add_music:
        console.print("\n[bold]Step 4: Adding background music[/bold]")
        try:
            # Search Pixabay for free background music
            pixabay_key = os.getenv('PIXABAY_API_KEY', '50169877-0f51f8bb1485fc7c948b8e10c')
            music_url = f"https://pixabay.com/api/?key={pixabay_key}&q=ambient+background&media_type=music&per_page=1"
            response = requests.get(music_url)
            if response.status_code == 200:
                data = response.json()
                if data.get('hits'):
                    music_url = data['hits'][0]['previewURL']
                    music_path = temp_dir / "background_music.mp3"
                    console.print(f"[cyan]Downloading background music...[/cyan]")
                    download_video(music_url, music_path)
                    console.print("[green]✅ Music downloaded[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not download music: {e}[/yellow]")
    
    # Step 5: Add voiceover + music (CRITICAL - ensure audio is properly merged!)
    console.print("\n[bold]Step 5: Adding YOUR voiceover + mixing audio[/bold]")
    console.print(f"[cyan]Voiceover: {audio_path}[/cyan]")
    
    if music_path and music_path.exists():
        console.print(f"[cyan]Music: {music_path}[/cyan]")
        # Mix voiceover (loud) + background music (quiet)
        final_cmd = [
            "ffmpeg",
            "-i", str(concat_output),  # Video
            "-i", str(audio_path),      # Voiceover (primary)
            "-i", str(music_path),      # Background music
            "-filter_complex",
            "[1:a]volume=1.0[voice];[2:a]volume=0.15,afade=t=in:d=2:curve=log,afade=t=out:st=" + str(total_duration-2) + ":d=2:curve=log[music];[voice][music]amix=inputs=2:duration=shortest[a]",
            "-map", "0:v:0",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-y",
            str(output)
        ]
    else:
        # Just voiceover, no music
        final_cmd = [
            "ffmpeg",
            "-i", str(concat_output),
            "-i", str(audio_path),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-y",
            str(output)
        ]
    
    result = subprocess.run(final_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        console.print(f"[red]❌ Audio merge failed![/red]")
        console.print(f"[dim]{result.stderr}[/dim]")
        return None
    
    console.print("[green]✅ Audio mixed successfully![/green]")
    
    console.print(f"\n[bold green]🎉 Professional video created![/bold green]")
    console.print(f"[cyan]📁 Saved to:[/cyan] {output}")
    
    # File size
    file_size = output.stat().st_size / (1024 * 1024)
    console.print(f"[cyan]📊 Size:[/cyan] {file_size:.1f} MB")
    console.print(f"[cyan]⏱️  Duration:[/cyan] {total_duration:.1f} seconds")
    
    console.print("\n[bold]🎬 Features:[/bold]")
    console.print("✅ Professional B-roll footage")
    console.print("✅ Your cloned voice")
    if aspect_ratio == "9:16":
        console.print("✅ Portrait HD (1080x1920) - Perfect for social media!")
    else:
        console.print("✅ Landscape HD (1920x1080) - Perfect for YouTube!")
    console.print("✅ Smart cropped & color graded")
    console.print("✅ Seamless transitions")
    
    # Open video
    console.print("\n[cyan]Opening video...[/cyan]")
    subprocess.run(["open", str(output)])
    
    # Cleanup
    console.print("\n[dim]Cleaning up temp files...[/dim]")
    import shutil
    shutil.rmtree(temp_dir)
    
    return output


if __name__ == "__main__":
    # OPTIMIZED search queries - MORE clips, SPECIFIC to Culture & AI narrative
    SEARCH_QUERIES = [
        "diverse people cultures",         # "Culture is the heartbeat"
        "traditional cultural art",        # "our stories"
        "heritage storytelling",           # "our traditions"
        "human soul emotions",             # "our soul"
        "artificial intelligence",         # "AI doesn't erase culture"
        "technology amplify culture",      # "it amplifies it"
        "preserve heritage",               # "preserve what makes us human"
        "global community",                # "share our heritage"
        "world diversity",                 # "across borders"
        "cultural celebration",            # "celebrate our diversity"
        "technology tradition",            # "Technology and tradition"
        "future together unity"            # "creating a richer future"
    ]
    
    console.print("\n[bold cyan]🌍 Culture & AI - Professional Voiceover Video (OPTIMIZED)[/bold cyan]")
    console.print("[dim]Your voice + relevant B-roll = Professional content[/dim]\n")
    
    # Use existing voice audio
    audio_file = "narrations/tomi_zenyai_test.wav"
    
    result = create_voiceover_video(
        audio_path=audio_file,
        output_path="professional_videos/culture_ai_SOCIAL_MEDIA.mp4",
        search_queries=SEARCH_QUERIES,
        max_clip_duration=4,  # 4 seconds max per clip (smart calculation!)
        add_music=True,  # Add cinematic background music
        aspect_ratio="9:16"  # Portrait for social media (TikTok, Instagram, Shorts)
    )
    
    if result:
        console.print("\n[bold green]✅ Your professional video is ready![/bold green]")
        console.print("\n[dim]This is how top creators make content![/dim]")
