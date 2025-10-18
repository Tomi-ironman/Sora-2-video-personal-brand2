"""
Fantasy Cutaway Generator for attention-grabbing B-roll sequences.
Inspired by colorful, surreal, game-like visuals for short-form content.
"""
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from veo3_generator import Veo3VideoGenerator
import subprocess

console = Console()

class FantasyCutawayGenerator:
    def __init__(self):
        self.veo_generator = Veo3VideoGenerator()
        
    def get_cutaway_presets(self) -> Dict[str, str]:
        """Predefined fantasy cutaway concepts inspired by user examples"""
        return {
            "neon_lantern_alley": """
            Magical floating lantern orbs in a mystical alley, glowing orange and teal lights,
            soft volumetric fog, friendly round creatures with big eyes silhouetted against warm light,
            dreamy parallax movement, Studio Ghibli meets cyberpunk aesthetic, 
            vertical 9:16 composition, cinematic lighting, ultra-saturated colors
            """,
            
            "bioluminescent_forest": """
            Enchanted forest with purple and green bioluminescent mushrooms and plants,
            glowing spores floating like particles, massive friendly creature silhouette,
            pink and teal color palette, soft bloom effects, magical atmosphere,
            vertical 9:16 composition, dreamy depth of field, fantasy game aesthetic
            """,
            
            "solar_red_noir": """
            Stark red background field, dramatic black silhouette figure with glowing orange eyes,
            bold graphic novel style, high contrast lighting, minimalist composition,
            vertical 9:16 format, noir meets sci-fi aesthetic, striking visual impact
            """,
            
            "teal_crimson_lounge": """
            Sophisticated figure in glasses holding wine glass, teal and crimson color scheme,
            glossy rim lighting, deep red background, glass reflections and refractions,
            film noir meets modern art, vertical 9:16 composition, moody atmospheric lighting
            """,
            
            "orbital_drift": """
            Vintage car floating in space above Earth, cosmic aurora ribbons,
            deep blue and purple nebula, retro-futuristic aesthetic, 
            vertical 9:16 composition, dreamy space atmosphere, nostalgic sci-fi vibes
            """,
            
            "sound_wave_ocean": """
            Cinematic ocean made of glowing sound waves, neon blue and purple colors,
            waves crashing in rhythm, particle effects, audio visualization aesthetic,
            vertical 9:16 composition, electronic music video style, hypnotic movement
            """,
            
            "crystal_equalizer": """
            Massive 3D crystal equalizer towers rising and shattering into particles,
            rainbow holographic effects, electronic music visualization,
            vertical 9:16 composition, futuristic club aesthetic, dynamic motion
            """,
            
            "mythic_library": """
            Ancient library where books emit visible sound auras, floating pages,
            warm golden and blue lighting, magical knowledge visualization,
            vertical 9:16 composition, fantasy meets technology aesthetic
            """
        }
    
    def generate_cutaway(self, preset_name: str, duration: float = 1.5, aspect_ratio: str = "9:16") -> Optional[str]:
        """Generate a single fantasy cutaway clip"""
        presets = self.get_cutaway_presets()
        
        if preset_name not in presets:
            console.print(f"[red]❌ Unknown preset: {preset_name}[/red]")
            return None
        
        base_prompt = presets[preset_name]
        
        # Enhanced prompt for maximum visual impact
        enhanced_prompt = f"""
        FANTASY CUTAWAY SEQUENCE - MAXIMUM VISUAL IMPACT:
        
        {base_prompt.strip()}
        
        CRITICAL REQUIREMENTS:
        - Ultra-saturated, vibrant colors for scroll-stopping impact
        - Smooth, hypnotic camera movement (slow zoom, gentle drift)
        - Duration: {duration} seconds of pure visual magic
        - NO text, NO characters, NO dialogue - pure abstract beauty
        - Game-like, otherworldly aesthetic
        - Perfect for short-form content hooks
        
        TECHNICAL SPECS:
        - {aspect_ratio} vertical format optimized for mobile
        - 720p resolution with crisp detail
        - Seamless loop potential for smooth transitions
        - High contrast and saturation for attention-grabbing
        - Cinematic depth and atmosphere
        """
        
        console.print(f"[cyan]🎨 Generating fantasy cutaway: {preset_name}[/cyan]")
        
        return self.veo_generator.generate_video(
            prompt=enhanced_prompt,
            aspect_ratio=aspect_ratio,
            resolution="720p",
            use_character_consistency=False  # No character needed for abstract cutaways
        )
    
    def generate_multiple_cutaways(self, preset_names: List[str], duration: float = 1.5) -> List[str]:
        """Generate multiple cutaway clips"""
        cutaway_paths = []
        
        for preset in preset_names:
            path = self.generate_cutaway(preset, duration)
            if path:
                cutaway_paths.append(path)
                console.print(f"[green]✅ Generated: {preset}[/green]")
            else:
                console.print(f"[red]❌ Failed: {preset}[/red]")
        
        return cutaway_paths


def _ffmpeg_exists() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def create_attention_timeline(main_video_path: str, cutaway_paths: List[str], output_path: str) -> str:
    """
    Assemble timeline with alternating main video and fantasy cutaways.
    Pattern: main(2.5s) → cutaway(1.2s) → main(2.5s) → cutaway(1.2s) → main(2s)
    """
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        
        console.print("[cyan]🎬 Assembling attention-grabbing timeline...[/cyan]")
        
        # Load main video
        main_clip = VideoFileClip(main_video_path)
        total_duration = main_clip.duration
        
        # Load cutaway clips
        
        if not cutaway_clips:
            console.print("[yellow]⚠️  No cutaway clips available, returning original video[/yellow]")
            return main_video_path
        
        # Create timeline segments (strict 2s alternation)
        segments = []
        current_time = 0
        cutaway_index = 0

        # Pattern: main(2s) → cutaway(2s) → main(2s) → cutaway(2s) → main(rest)
        segment_durations = [2.0, 2.0, 2.0, 2.0]  # Remaining time handled after loop
        
        for i, duration in enumerate(segment_durations):
            if current_time >= total_duration:
                break
                
            if i % 2 == 0:  # Main video segments
                end_time = min(current_time + duration, total_duration)
                segment = main_clip.subclip(current_time, end_time)
                segments.append(segment)
                current_time = end_time
            else:  # Cutaway segments
                if cutaway_index < len(cutaway_clips):
                    cutaway = cutaway_clips[cutaway_index]
                    # Trim cutaway to exactly 2s where possible
                    cutaway_segment = cutaway.subclip(0, min(2.0, cutaway.duration))
                    segments.append(cutaway_segment)
                    cutaway_index += 1
        
        # Add remaining main video if any
        if current_time < total_duration:
            final_segment = main_clip.subclip(current_time, total_duration)
            segments.append(final_segment)
        
        # Concatenate all segments
        final_video = concatenate_videoclips(segments, method="compose")
        
        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        final_video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        
        # Cleanup
        main_clip.close()
        for clip in cutaway_clips:
            clip.close()
        final_video.close()
        
        console.print(f"[green]✅ Attention-grabbing video created: {output_path.name}[/green]")
        return str(output_path)
        
    except ImportError:
        console.print("[yellow]⚠️ MoviePy not available, trying ffmpeg fallback for timeline assembly...[/yellow]")
        
        if not _ffmpeg_exists():
            console.print("[red]❌ Neither MoviePy nor ffmpeg available. Install MoviePy or ffmpeg to assemble timeline.")
            return main_video_path
        
        try:
            # Prepare temp directory
            tmp_dir = Path(tempfile.gettempdir()) / "attention_build"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            parts = []

            def cut_segment(src: str, start: float, dur: float, index: int) -> Path:
                out = tmp_dir / f"seg_{index:02d}.mp4"
                # Use keyframe-accurate cutting with re-encode for reliability
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(max(0.0, start)),
                    "-i", src,
                    "-t", str(dur),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    str(out)
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return out

            # Probe main video duration using ffprobe
            def probe_duration(p: str) -> float:
                try:
                    result = subprocess.run([
                        "ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p
                    ], capture_output=True, text=True, check=True)
                    return float(result.stdout.strip())
                except Exception:
                    return 8.0  # fallback
            
            total = probe_duration(main_video_path)
            start = 0.0
            seg_idx = 0

            # main 2s
            if start < total:
                parts.append(cut_segment(main_video_path, start, min(2.0, total - start), seg_idx)); seg_idx += 1
                start += 2.0
            
            # cutaway 1 (2s)
            if cutaway_paths:
                parts.append(cut_segment(cutaway_paths[0], 0.0, 2.0, seg_idx)); seg_idx += 1
            
            # main next 2s
            if start < total:
                parts.append(cut_segment(main_video_path, start, min(2.0, total - start), seg_idx)); seg_idx += 1
                start += 2.0
            
            # cutaway 2 (2s) if available
            if len(cutaway_paths) > 1:
                parts.append(cut_segment(cutaway_paths[1], 0.0, 2.0, seg_idx)); seg_idx += 1
            
            # append rest of main
            if start < total:
                parts.append(cut_segment(main_video_path, start, max(0.5, total - start), seg_idx)); seg_idx += 1

            # Write concat list
            concat_file = tmp_dir / "concat.txt"
            with open(concat_file, "w") as f:
                for p in parts:
                    f.write(f"file '{p.as_posix()}'\n")

            # Concat
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cmd_concat = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
                "-c", "copy", str(output_path)
            ]
            subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            console.print(f"[green]✅ Attention-grabbing video created (ffmpeg): {output_path.name}[/green]")
            return str(output_path)
        except Exception as e:
            console.print(f"[red]❌ ffmpeg assembly failed: {e}[/red]")
            return main_video_path
    except Exception as e:
        console.print(f"[red]❌ Timeline assembly failed: {e}[/red]")
        return main_video_path


# Preset combinations for different moods
ATTENTION_PRESETS = {
    "neon_magic": ["neon_lantern_alley", "sound_wave_ocean"],
    "forest_dreams": ["bioluminescent_forest", "mythic_library"],
    "noir_future": ["solar_red_noir", "teal_crimson_lounge"],
    "cosmic_vibes": ["orbital_drift", "crystal_equalizer"],
    "full_spectrum": ["neon_lantern_alley", "bioluminescent_forest", "sound_wave_ocean"]
}
