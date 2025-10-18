#!/usr/bin/env python3
"""
Personal Brand Video Creator
Pattern: YOU → Hook → Text → Visual → YOU → Text → Visual → YOU
Maximum personalization with your face in the video!
"""

import subprocess
import os
from pathlib import Path
from rich.console import Console
import re
import random
try:
    from .style_engine import load_style, style_filter_for_visual, text_draw_params
except Exception:
    # Fallback when running as a script without package context
    from style_engine import load_style, style_filter_for_visual, text_draw_params

console = Console()


class PersonalVideoCreator:
    """Create personal brand videos with your footage interspersed"""
    
    def __init__(self, personal_video_path):
        self.personal_video = Path(personal_video_path)
        self.temp_dir = Path("temp_personal_clips")
        self.temp_dir.mkdir(exist_ok=True)
    
    def cut_personal_video(self, segment_duration=1.5):
        """
        Cut personal video into segments
        
        Args:
            segment_duration: Duration of each segment in seconds
        
        Returns:
            List of paths to personal video segments
        """
        console.print(f"\n[cyan]✂️  Cutting personal video into segments...[/cyan]")
        console.print(f"[dim]Source: {self.personal_video.name}[/dim]\n")
        
        # Get video duration
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(self.personal_video)
        ], capture_output=True, text=True, check=True)
        
        duration = float(result.stdout.strip())
        num_segments = int(duration / segment_duration)
        
        console.print(f"[green]Duration: {duration:.1f}s[/green]")
        console.print(f"[green]Creating {num_segments} segments @ {segment_duration}s each[/green]\n")
        
        segments = []
        
        for i in range(num_segments):
            start_time = i * segment_duration
            output_path = self.temp_dir / f"personal_{i:03d}.mp4"
            
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-ss', str(start_time),
                '-i', str(self.personal_video),
                '-t', str(segment_duration),
                '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                '-an',  # Remove audio from personal clips!
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True)
            segments.append(output_path)
        console.print(f"[green]✅ Created {len(segments)} personal video segments[/green]\n")
        return segments


def create_text_slide(text, duration, output_path, font_size=120, position="center"):
    """Create text slide with vertical stacked words (one word per line)."""
    words = [w for w in text.split() if w]
    # Enforce vertical stacking: each word on its own line
    multiline_text = '\n'.join(words)
    multiline_text = multiline_text.replace("'", "'\\''").replace(":", "\\:")
    
    font_options = [
        '/System/Library/Fonts/Supplemental/Helvetica Neue Thin.ttc',
        '/System/Library/Fonts/SF-Pro-Text-Light.otf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Supplemental/Arial.ttf'
    ]
    
    font_file = None
    for font_path in font_options:
        if Path(font_path).exists():
            font_file = font_path
            break
    
    if not font_file:
        font_file = '/System/Library/Fonts/Supplemental/Arial.ttf'
    
    # Positioning
    if position == "top":
        y_expr = "(h*0.18)"
    elif position == "bottom":
        y_expr = "(h*0.75)"
    else:
        y_expr = "(h-text_h)/2"

    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'lavfi',
        '-i', f'color=c=black:s=1080x1920:d={duration}',
        '-vf', f"drawtext=text='{multiline_text}':fontcolor=white:fontsize={font_size}:x=(w-text_w)/2:y={y_expr}:line_spacing=30:fontfile={font_file}",
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True)


def analyze_script_for_emphasis(script_text):
    """Find phrases to emphasize"""
    sentences = re.split(r'([.!?]+)', script_text)
    
    result = []
    for i in range(0, len(sentences)-1, 2):
        if sentences[i].strip():
            sentence = sentences[i].strip()
            if i+1 < len(sentences):
                sentence += sentences[i+1]
            result.append(sentence)
    
    emphasis_phrases = []
    
    for sentence in result:
        should_emphasize = False
        
        if '!' in sentence or '?' in sentence:
            should_emphasize = True
        elif len(sentence.strip()) < 50 and len(sentence.strip()) > 10:
            should_emphasize = True
        
        power_words = ['never', 'always', 'only', 'must', "can't", "won't", 
                      'impossible', 'forever', 'timeless', 'eternal', 'absolute']
        if any(word in sentence.lower() for word in power_words):
            should_emphasize = True
        
        if should_emphasize:
            emphasis_phrases.append(sentence.strip())
    
    return emphasis_phrases


def create_personal_brand_video(
    personal_video_path,
    media_dir,
    voice_file,
    script_text,
    output_filename,
    hook_duration=0.15,
    story_duration=2.2,
    text_duration=1.5,
    personal_duration=1.5,
    style_name=None,
    style=None,
    seed=None,
    randomize=True
):
    """
    Create personal brand video with YOU in it!
    
    Pattern:
    1. First 1 sec: YOU (personal intro)
    2. Hook: Fast visuals
    3. Then cycle: Text → Visual → YOU → Text → Visual → YOU
    """
    
    console.print("\n[bold cyan]🎬 PERSONAL BRAND VIDEO CREATOR[/bold cyan]\n")
    console.print(f"[yellow]Your video: {Path(personal_video_path).name}[/yellow]")
    console.print(f"[yellow]Pattern: YOU → Hook → Text → Visual → YOU → Text → Visual → YOU[/yellow]\n")

    # Load style (overrides)
    active_style = style or load_style(style_name)
    pacing = active_style.get('pacing', {})
    hook_duration = float(pacing.get('hook_duration', hook_duration))
    story_duration = float(pacing.get('story_duration', story_duration))
    text_duration = float(pacing.get('text_duration', text_duration))
    personal_duration = float(pacing.get('personal_duration', personal_duration))
    txt_params = text_draw_params(active_style)
    grade_filter = style_filter_for_visual(active_style)
    
    # RNG
    rng = random.Random(seed) if seed is not None else random.Random()

    # Cut personal video
    creator = PersonalVideoCreator(personal_video_path)
    personal_segments = creator.cut_personal_video(segment_duration=personal_duration)
    
    # Analyze script
    emphasis_phrases = analyze_script_for_emphasis(script_text)
    console.print(f"[green]✅ Found {len(emphasis_phrases)} emphasis phrases[/green]\n")
    
    # Load media
    media_path = Path(media_dir)
    static_images = []
    gifs = []
    
    for subdir in media_path.glob("*"):
        if subdir.is_dir() and 'gifs' not in subdir.name.lower():
            static_images.extend(list(subdir.glob("*.jpg")))
            static_images.extend(list(subdir.glob("*.png")))
    
    gif_dir = media_path / "gifs"
    if gif_dir.exists():
        gifs = list(gif_dir.glob("*.gif"))
    
    # Randomize media order if requested
    if randomize:
        rng.shuffle(static_images)
        rng.shuffle(gifs)
    else:
        static_images.sort()
        gifs.sort()
    
    console.print(f"[cyan]📊 Media:[/cyan]")
    console.print(f"[cyan]   • Static images: {len(static_images)}[/cyan]")
    console.print(f"[cyan]   • GIFs: {len(gifs)}[/cyan]")
    console.print(f"[cyan]   • Your clips: {len(personal_segments)}[/cyan]\n")
    
    # Build clip sequence
    temp_dir = Path("temp_personal_final")
    temp_dir.mkdir(exist_ok=True)
    
    all_clips = []
    
    # 1. OPENING: Random personal clip (1 sec) for variety
    console.print("[yellow]🎬 Opening with YOU![/yellow]")
    opening_clip = temp_dir / "opening_you.mp4"
    opening_idx = 0
    if randomize and len(personal_segments) > 1:
        opening_idx = rng.randrange(0, min(4, len(personal_segments)))  # favor early variations
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', str(personal_segments[opening_idx]),
        '-t', '1.0',
        '-an',  # No audio from personal clips
        '-c:v', 'copy',
        str(opening_clip)
    ], check=True)
    all_clips.append(opening_clip)
    
    # 2. HOOK: Fast visuals (10 clips)
    console.print("[yellow]🔥 Creating hook...[/yellow]")
    hook_count = min(10, len(static_images))
    
    for i in range(hook_count):
        output_clip = temp_dir / f"hook_{i:03d}.mp4"
        # Randomly decide to use a GIF if available
        use_gif = bool(gifs) and (randomize and rng.random() < 0.5)
        if use_gif:
            gif_src = rng.choice(gifs)
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-i', str(gif_src),
                '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                '-t', str(hook_duration),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        else:
            # Static image
            vf = f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920'
            if grade_filter:
                vf = vf + "," + grade_filter
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-loop', '1',
                '-i', str(static_images[i % len(static_images)]),
                '-vf', vf,
                '-t', str(hook_duration),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(output_clip)
            ]
        
        subprocess.run(cmd, check=True)
        all_clips.append(output_clip)
    
    console.print(f"[green]✅ Hook complete ({hook_count} clips)[/green]\n")
    
    # 3. STORY: Cycle Text → Visual → YOU
    console.print("[yellow]📝 Creating story with YOU interspersed...[/yellow]\n")
    
    media_idx = hook_count
    # Build randomized order for personal segments, excluding opening_idx first occurrence
    personal_order = list(range(len(personal_segments)))
    if randomize:
        rng.shuffle(personal_order)
    # Ensure opening_idx appears later in sequence (skip the first instance)
    if opening_idx in personal_order:
        personal_order.remove(opening_idx)
    personal_iter = iter(personal_order)
    
    for i, emphasis_text in enumerate(emphasis_phrases):
        # Text slide
        text_clip = temp_dir / f"text_{i:03d}.mp4"
        console.print(f"[dim]  📝 Text: \"{emphasis_text[:30]}...\"[/dim]")
        create_text_slide(emphasis_text, text_duration, text_clip, font_size=txt_params.get('fontsize',120), position=txt_params.get('position','center'))
        all_clips.append(text_clip)
        
        # Visual clip (if we have media left)
        if media_idx < len(static_images):
            visual_clip = temp_dir / f"visual_{i:03d}.mp4"
            
            zoom_filter = f'zoompan=z=\'min(zoom+0.0005,1.15)\':d={int(story_duration * 30)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920'
            vf_visual = f'scale=1200:2150:force_original_aspect_ratio=increase,{zoom_filter}'
            if grade_filter:
                vf_visual = vf_visual + "," + grade_filter
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-loop', '1',
                '-i', str(static_images[media_idx]),
                '-vf', vf_visual,
                '-t', str(story_duration),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                str(visual_clip)
            ]
            subprocess.run(cmd, check=True)
            all_clips.append(visual_clip)
            media_idx += 1
        
        # YOUR PERSONAL CLIP
        try:
            next_personal_idx = next(personal_iter)
            console.print(f"[green]  🎬 YOU (clip {next_personal_idx})[/green]")
            all_clips.append(personal_segments[next_personal_idx])
        except StopIteration:
            pass
    
    console.print(f"\n[green]✅ Created {len(all_clips)} total clips[/green]\n")
    
    # Concatenate
    console.print("[cyan]🔗 Combining all clips...[/cyan]")
    concat_file = 'concat_personal_brand.txt'
    with open(concat_file, 'w') as f:
        for clip in all_clips:
            f.write(f"file '{clip.absolute()}'\n")
    
    Path("professional_videos").mkdir(exist_ok=True)
    
    temp_video = "temp_personal_brand_no_audio.mp4"
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
    console.print("[cyan]🎙️  Adding YOUR voice...[/cyan]")
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
    for clip in temp_dir.glob("*.mp4"):
        if clip.name.startswith(('hook_', 'text_', 'visual_', 'opening_')):
            clip.unlink()
    temp_dir.rmdir()
    
    console.print(f"\n[bold green]🎉 PERSONAL BRAND VIDEO CREATED![/bold green]")
    console.print(f"[cyan]📁 {output_file}[/cyan]\n")
    
    # Copy to desktop
    desktop_path = os.path.expanduser(f'~/Desktop/{output_filename}')
    subprocess.run(['cp', output_file, desktop_path])
    console.print(f"[green]✅ Copied to Desktop: {output_filename}[/green]\n")
    
    # Summary
    console.print(f"[bold]📊 Video Composition:[/bold]")
    console.print(f"[green]   • Opening: YOU (1s)[/green]")
    console.print(f"[green]   • Hook: {hook_count} fast clips[/green]")
    console.print(f"[green]   • Story: Text → Visual → YOU (cycling)[/green]")
    console.print(f"[green]   • Your appearances: {personal_idx} times[/green]")
    console.print(f"[green]   • Total clips: {len(all_clips)}[/green]\n")
    
    # Open
    subprocess.run(['open', output_file])
    
    return output_file


if __name__ == "__main__":
    # Test with music composition
    script = """Music composition. Where creativity meets discipline!

The blank page. Every composer's greatest fear!

But here's the truth. You don't need perfect inspiration!

Start with a simple melody. Just four notes!

Build it. Layer it. Transform it!

This is how masterpieces are born. One note at a time!"""
    
    create_personal_brand_video(
        personal_video_path="Tomi/Hyperrealistic_Music_Creation_Video.mp4",
        media_dir="pinterest_downloads/mixed_music_composition",
        voice_file="narrations/composition_voice.wav",
        script_text=script,
        output_filename="composition_with_tomi.mp4"
    )
