#!/usr/bin/env python3
"""
Create video with intelligent text emphasis slides
Analyzes script to insert black screens with key phrases for maximum impact
"""

import subprocess
import os
import re
from pathlib import Path
from rich.console import Console

console = Console()


class ScriptAnalyzer:
    """Intelligently analyze script to find phrases worth emphasizing"""
    
    def __init__(self, script_text):
        self.script = script_text
        self.sentences = self._split_into_sentences()
    
    def _split_into_sentences(self):
        """Split script into sentences, preserving punctuation"""
        # Split on . ! ? but keep the punctuation
        sentences = re.split(r'([.!?]+)', self.script)
        
        # Combine sentence with its punctuation
        result = []
        for i in range(0, len(sentences)-1, 2):
            if sentences[i].strip():
                sentence = sentences[i].strip()
                if i+1 < len(sentences):
                    sentence += sentences[i+1]
                result.append(sentence)
        
        return result
    
    def find_emphasis_phrases(self):
        """
        Intelligently find phrases that should be emphasized with text-only slides
        
        Criteria:
        - Exclamation marks (strong emotion)
        - Questions (engagement)
        - Short, punchy statements (<50 chars)
        - Key words: "never", "always", "only", "must", "can't", etc.
        """
        emphasis_phrases = []
        
        for sentence in self.sentences:
            should_emphasize = False
            reason = ""
            
            # Check for exclamation (strong emotion)
            if '!' in sentence:
                should_emphasize = True
                reason = "exclamation"
            
            # Check for question (engagement)
            elif '?' in sentence:
                should_emphasize = True
                reason = "question"
            
            # Check for short punchy statement (impact)
            elif len(sentence.strip()) < 50 and len(sentence.strip()) > 10:
                should_emphasize = True
                reason = "short_punchy"
            
            # Check for power words
            power_words = ['never', 'always', 'only', 'must', "can't", "won't", 
                          'impossible', 'forever', 'timeless', 'eternal', 'absolute']
            if any(word in sentence.lower() for word in power_words):
                should_emphasize = True
                reason = "power_word"
            
            if should_emphasize:
                emphasis_phrases.append({
                    'text': sentence.strip(),
                    'reason': reason,
                    'length': len(sentence.strip())
                })
        
        return emphasis_phrases
    
    def create_emphasis_plan(self, total_clips):
        """
        Create a plan for where to insert text emphasis slides
        Returns list of: {'type': 'visual'/'text', 'content': ...}
        """
        emphasis_phrases = self.find_emphasis_phrases()
        
        if not emphasis_phrases:
            # No emphasis needed, all visual
            return [{'type': 'visual', 'index': i} for i in range(total_clips)]
        
        # Strategy: Alternate visual and text for emphasis phrases
        # Start with visual (hook), then mix in text
        plan = []
        
        # Reserve first 10 for hook (all visual, fast)
        hook_count = min(10, total_clips - len(emphasis_phrases))
        for i in range(hook_count):
            plan.append({'type': 'visual', 'index': i})
        
        # After hook: alternate visual and text
        remaining_visuals = total_clips - hook_count
        emphasis_idx = 0
        visual_idx = hook_count
        
        # Intelligent mixing: visual → text → visual → text
        for i in range(remaining_visuals):
            # Add visual
            if visual_idx < total_clips:
                plan.append({'type': 'visual', 'index': visual_idx})
                visual_idx += 1
            
            # Add text emphasis (if we have more phrases)
            if emphasis_idx < len(emphasis_phrases):
                plan.append({
                    'type': 'text',
                    'content': emphasis_phrases[emphasis_idx]['text'],
                    'reason': emphasis_phrases[emphasis_idx]['reason']
                })
                emphasis_idx += 1
        
        return plan


def create_text_slide(text, duration, output_path, font_size=120):
    """
    Create a black slide with large, elegant, stacked text
    
    Args:
        text: Text to display
        duration: Duration in seconds
        output_path: Where to save the clip
        font_size: Font size for text (default 120 for big impact)
    """
    # Aggressive line breaking - 1-2 words per line for vertical stack
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        # Break after just 1-2 words for vertical stacking
        if len(current_line) >= 2:
            lines.append(' '.join(current_line))
            current_line = []
    
    # Add any remaining words
    if current_line:
        lines.append(' '.join(current_line))
    
    # If only one line, try to split by comma or other punctuation
    if len(lines) == 1 and ',' in lines[0]:
        parts = lines[0].split(',')
        lines = [p.strip() + (',' if i < len(parts)-1 else '') for i, p in enumerate(parts)]
    
    # Join lines with newline for vertical stacking
    multiline_text = '\\n'.join(lines)
    
    # Escape special characters for ffmpeg
    multiline_text = multiline_text.replace("'", "'\\''").replace(":", "\\:")
    
    # Use thin, elegant font (Helvetica Neue Light or SF Pro Text Light)
    # Try multiple font paths for compatibility
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
    
    # Create text slide with larger font, more line spacing, centered
    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'lavfi',
        '-i', f'color=c=black:s=1080x1920:d={duration}',
        '-vf', f"drawtext=text='{multiline_text}':fontcolor=white:fontsize={font_size}:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=30:fontfile={font_file}",
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True)


def create_video_with_emphasis(
    media_dir,
    voice_file,
    script_text,
    output_filename,
    hook_duration=0.15,
    story_duration=2.2,
    text_duration=1.5
):
    """
    Create video with intelligent text emphasis slides
    
    Args:
        media_dir: Directory with media files
        voice_file: Path to voice audio
        script_text: The actual script text for analysis
        output_filename: Output filename
        hook_duration: Duration per clip in hook
        story_duration: Duration per visual clip in story
        text_duration: Duration for text-only slides
    """
    
    console.print("\n[bold cyan]🎬 VIDEO WITH TEXT EMPHASIS[/bold cyan]\n")
    console.print(f"[yellow]Analyzing script for emphasis opportunities...[/yellow]\n")
    
    # Analyze script
    analyzer = ScriptAnalyzer(script_text)
    emphasis_phrases = analyzer.find_emphasis_phrases()
    
    console.print(f"[green]✅ Found {len(emphasis_phrases)} phrases to emphasize:[/green]")
    for i, phrase in enumerate(emphasis_phrases, 1):
        console.print(f"  {i}. \"{phrase['text'][:50]}...\" ({phrase['reason']})")
    console.print()
    
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
    
    static_images.sort()
    gifs.sort()
    
    console.print(f"[cyan]📊 Media: {len(static_images)} static + {len(gifs)} GIFs[/cyan]\n")
    
    # Create emphasis plan
    total_media = len(static_images) + len(gifs)
    plan = analyzer.create_emphasis_plan(total_media)
    
    console.print(f"[cyan]📋 Video Plan: {len(plan)} total clips[/cyan]")
    hook_clips = sum(1 for p in plan if p['type'] == 'visual' and p.get('index', 0) < 10)
    text_clips = sum(1 for p in plan if p['type'] == 'text')
    visual_clips = sum(1 for p in plan if p['type'] == 'visual')
    
    console.print(f"[cyan]   🔥 Hook: {hook_clips} visual clips (fast)[/cyan]")
    console.print(f"[cyan]   🎥 Story: {visual_clips - hook_clips} visual clips[/cyan]")
    console.print(f"[cyan]   📝 Emphasis: {text_clips} text-only slides[/cyan]\n")
    
    # Create temp directory
    temp_dir = Path("temp_emphasis_clips")
    temp_dir.mkdir(exist_ok=True)
    
    # Process all clips according to plan
    all_clips = []
    media_idx = 0
    
    console.print("[cyan]🎬 Creating clips...[/cyan]\n")
    
    for i, item in enumerate(plan):
        output_clip = temp_dir / f"clip_{i:03d}.mp4"
        
        if item['type'] == 'text':
            # Create text emphasis slide
            console.print(f"[yellow]  📝 Text slide: \"{item['content'][:40]}...\"[/yellow]")
            create_text_slide(item['content'], text_duration, output_clip)
            all_clips.append(output_clip)
        
        else:
            # Create visual clip (GIF or static)
            if media_idx >= total_media:
                break
            
            # Prefer GIF first, then static
            if media_idx == 0 and gifs:
                media_path = gifs[0]
                media_type = 'gif'
                media_idx += 1
            elif media_idx - len(gifs) < len(static_images):
                media_path = static_images[media_idx - len(gifs)]
                media_type = 'static'
                media_idx += 1
            else:
                continue
            
            # Determine if this is hook or story
            is_hook = item.get('index', 0) < 10
            duration = hook_duration if is_hook else story_duration
            
            if media_type == 'gif':
                console.print(f"[dim]  🎬 GIF clip ({duration}s)[/dim]")
                cmd = [
                    'ffmpeg', '-y', '-loglevel', 'error',
                    '-stream_loop', '-1',
                    '-i', str(media_path),
                    '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-t', str(duration),
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-r', '30',
                    str(output_clip)
                ]
            else:
                if is_hook:
                    # No zoom in hook
                    cmd = [
                        'ffmpeg', '-y', '-loglevel', 'error',
                        '-loop', '1',
                        '-i', str(media_path),
                        '-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                        '-t', str(duration),
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-r', '30',
                        str(output_clip)
                    ]
                else:
                    # Zoom in story
                    zoom_filter = f'zoompan=z=\'min(zoom+0.0005,1.15)\':d={int(duration * 30)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920'
                    cmd = [
                        'ffmpeg', '-y', '-loglevel', 'error',
                        '-loop', '1',
                        '-i', str(media_path),
                        '-vf', f'scale=1200:2150:force_original_aspect_ratio=increase,{zoom_filter}',
                        '-t', str(duration),
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-r', '30',
                        str(output_clip)
                    ]
            
            subprocess.run(cmd, check=True)
            all_clips.append(output_clip)
    
    console.print(f"\n[green]✅ Created {len(all_clips)} clips[/green]\n")
    
    # Concatenate
    console.print("[cyan]🔗 Combining all clips...[/cyan]")
    concat_file = 'concat_emphasis_list.txt'
    with open(concat_file, 'w') as f:
        for clip in all_clips:
            f.write(f"file '{clip.absolute()}'\n")
    
    Path("professional_videos").mkdir(exist_ok=True)
    
    temp_video = "temp_emphasis_no_audio.mp4"
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
    for clip in all_clips:
        clip.unlink()
    temp_dir.rmdir()
    
    console.print(f"\n[bold green]✅ VIDEO WITH TEXT EMPHASIS CREATED![/bold green]")
    console.print(f"[cyan]📁 {output_file}[/cyan]\n")
    
    # Copy to desktop
    desktop_path = os.path.expanduser(f'~/Desktop/{output_filename}')
    subprocess.run(['cp', output_file, desktop_path])
    console.print(f"[green]✅ Copied to Desktop: {output_filename}[/green]\n")
    
    # Open
    subprocess.run(['open', output_file])
    
    return output_file


if __name__ == "__main__":
    # Test with Greek culture
    script = "Greece! Ancient wisdom, eternal beauty!"
    
    create_video_with_emphasis(
        media_dir="pinterest_downloads/mixed_greek_culture",
        voice_file="narrations/greek_very_short.wav",
        script_text=script,
        output_filename="greek_with_text_emphasis.mp4"
    )
