#!/usr/bin/env python3
"""
Hybrid Video Generator
Combines FREE stock media (Pexels/Pixabay) with AI video generation (Sora/Runway)
This is your complete InVideo competitor with zero stock media costs!
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.table import Table
import openai

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent))

from media_providers.unified_media_manager import UnifiedMediaManager
from media_providers.ffmpeg_utils import FFmpegUtils

console = Console()

class HybridVideoGenerator:
    """
    Complete video generation system that intelligently combines:
    1. Free stock footage (Pexels/Pixabay) for B-roll
    2. AI-generated videos (Sora/Runway) for custom scenes
    3. Free audio (Freesound) for background music
    4. FREE voice cloning (Chatterbox) for narration
    5. FFmpeg for professional editing
    """
    
    def __init__(self):
        self.media_manager = UnifiedMediaManager()
        self.openai_client = None  # Only initialize when needed for Sora
        self.output_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.output_dir.mkdir(exist_ok=True)
        
        self.temp_dir = self.output_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize voice provider (Chatterbox)
        self.voice_provider = None
        try:
            from voice_providers.chatterbox_provider import ChatterboxProvider
            self.voice_provider = ChatterboxProvider()
            console.print("[green]✅ Chatterbox voice cloning ready[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Chatterbox not available: {e}[/yellow]")
            console.print("[dim]   See CHATTERBOX_SETUP.md for setup instructions[/dim]")
    
    def create_simple_script(self, topic: str, duration: int = 30, keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create simple script from keywords (NO GPT-4 needed!)
        Just search stock footage based on keywords - FREE!
        
        Args:
            topic: Main topic/title
            duration: Video duration in seconds
            keywords: List of keywords for stock footage search
        
        Returns:
            Simple script structure for video creation
        """
        console.print(f"\n[cyan]📝 Creating video: {topic}[/cyan]")
        
        # Auto-generate keywords if not provided
        if not keywords:
            keywords = [topic]
        
        # Split duration across keywords
        scene_duration = duration // len(keywords)
        
        scenes = [
            {
                'description': keyword,
                'duration': scene_duration,
                'type': 'stock',
                'keywords': [keyword]
            }
            for keyword in keywords
        ]
        
        return {
            'title': topic,
            'scenes': scenes,
            'voiceover_script': f"This video showcases {topic}.",
            'background_music_mood': 'upbeat'
        }
    
    def get_stock_footage(self, scene: Dict[str, Any], output_dir: Path) -> Optional[Path]:
        """Get stock footage for a scene"""
        keywords = scene.get('keywords', [scene.get('description')])
        
        console.print(f"   🔍 Searching stock footage: {keywords}")
        
        # Try to find video
        for keyword in keywords:
            results = self.media_manager.search_videos(keyword, num_results=3)
            if results:
                path = self.media_manager.download_media(results[0], output_dir)
                if path:
                    console.print(f"      ✅ Downloaded: {keyword}")
                    return path
        
        console.print(f"      ⚠️  No stock footage found")
        return None
    
    def generate_ai_video(self, scene: Dict[str, Any], output_dir: Path) -> Optional[Path]:
        """Generate AI video using Sora (THIS is where GPT-4/OpenAI is used!)"""
        console.print(f"   🎨 AI generation with Sora: {scene.get('description')}")
        
        # Initialize OpenAI client only when needed for Sora
        if not self.openai_client:
            try:
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            except Exception as e:
                console.print(f"[red]❌ OpenAI not configured: {e}[/red]")
                console.print("[yellow]   Falling back to stock footage[/yellow]")
                keywords = [scene.get('description')]
                results = self.media_manager.search_videos(keywords[0], num_results=3)
                if results:
                    return self.media_manager.download_media(results[0], output_dir)
                return None
        
        try:
            # TODO: Call Sora API here
            # prompt = scene.get('prompt', scene.get('description'))
            # video = self.openai_client.videos.generate(model="sora", prompt=prompt)
            # return video.save(output_dir)
            
            console.print(f"      ℹ️  Sora integration coming soon - using stock fallback")
            keywords = [scene.get('description')]
            results = self.media_manager.search_videos(keywords[0], num_results=3)
            if results:
                path = self.media_manager.download_media(results[0], output_dir)
                if path:
                    console.print(f"      ✅ Downloaded fallback footage")
                    return path
        except Exception as e:
            console.print(f"[red]❌ Sora generation failed: {e}[/red]")
        
        return None
    
    def create_complete_video(
        self,
        topic: str,
        duration: int = 30,
        use_ai_generation: bool = False,
        add_music: bool = True,
        add_voiceover: bool = False,
        voice_name: Optional[str] = None
    ) -> Optional[Path]:
        """
        Create a complete video from topic
        
        Args:
            topic: Video topic/concept
            duration: Target duration in seconds
            use_ai_generation: Use Sora/Runway for custom scenes
            add_music: Add background music
            add_voiceover: Add AI voiceover (uses Chatterbox if available)
            voice_name: Name of voice clone to use (optional)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')[:50]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            
            # Step 1: Create simple script (NO GPT-4!)
            task1 = progress.add_task("[cyan]Preparing video...", total=1)
            
            # Extract keywords from topic
            keywords = topic.split()
            script = self.create_simple_script(topic, duration, keywords[:5])  # Max 5 keywords
            
            progress.update(task1, completed=1)
            
            # Show script preview
            console.print(f"\n[bold]📋 Script Preview:[/bold]")
            console.print(f"[cyan]Title:[/cyan] {script.get('title')}")
            console.print(f"[cyan]Scenes:[/cyan] {len(script.get('scenes', []))}")
            
            # Step 2: Gather video clips
            task2 = progress.add_task("[cyan]Gathering footage...", total=len(script.get('scenes', [])))
            
            clips_dir = self.temp_dir / f"{timestamp}_clips"
            clips_dir.mkdir(exist_ok=True)
            
            video_clips = []
            
            for idx, scene in enumerate(script.get('scenes', [])):
                scene_type = scene.get('type', 'stock')
                
                if scene_type == 'stock' or not use_ai_generation:
                    # Get stock footage
                    clip_path = self.get_stock_footage(scene, clips_dir)
                else:
                    # Generate AI video
                    clip_path = self.generate_ai_video(scene, clips_dir)
                
                if clip_path:
                    # Trim to scene duration
                    scene_duration = scene.get('duration', 5)
                    trimmed_path = clips_dir / f"scene_{idx}_trimmed.mp4"
                    
                    try:
                        FFmpegUtils.trim_video(clip_path, trimmed_path, 0, scene_duration)
                        video_clips.append(trimmed_path)
                    except:
                        video_clips.append(clip_path)  # Use original if trim fails
                
                progress.update(task2, advance=1)
            
            if not video_clips:
                console.print("[red]❌ No video clips generated[/red]")
                return None
            
            console.print(f"\n[green]✅ Gathered {len(video_clips)} video clips[/green]")
            
            # Step 3: Get background music
            audio_path = None
            if add_music:
                task3 = progress.add_task("[cyan]Finding background music...", total=1)
                
                mood = script.get('background_music_mood', 'upbeat')
                audio_results = self.media_manager.search_audio(
                    query=f"{mood} background",
                    num_results=3,
                    duration_min=duration - 10,
                    duration_max=duration + 30,
                    audio_type='music'
                )
                
                if audio_results:
                    audio_dir = self.temp_dir / f"{timestamp}_audio"
                    audio_dir.mkdir(exist_ok=True)
                    audio_path = self.media_manager.download_media(audio_results[0], audio_dir)
                    
                    if audio_path:
                        console.print(f"[green]✅ Background music added[/green]")
                
                progress.update(task3, completed=1)
            
            # Step 3.5: Generate voiceover (if requested and available)
            voiceover_path = None
            if add_voiceover and self.voice_provider:
                task3_5 = progress.add_task("[cyan]Generating voiceover...", total=1)
                
                voiceover_script = script.get('voiceover_script', '')
                if voiceover_script:
                    voiceover_dir = self.temp_dir / f"{timestamp}_voiceover"
                    voiceover_dir.mkdir(exist_ok=True)
                    
                    try:
                        if voice_name:
                            voiceover_path = self.voice_provider.generate_with_voice(
                                text=voiceover_script,
                                voice_name=voice_name,
                                output_path=voiceover_dir / "narration.wav"
                            )
                        else:
                            voiceover_path = self.voice_provider.generate(
                                text=voiceover_script,
                                output_path=voiceover_dir / "narration.wav"
                            )
                        console.print(f"[green]✅ Voiceover generated with Chatterbox (FREE!)[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Voiceover generation failed: {e}[/yellow]")
                
                progress.update(task3_5, completed=1)
            elif add_voiceover and not self.voice_provider:
                console.print("[yellow]⚠️  Chatterbox not available for voiceover[/yellow]")
                console.print("[dim]   See CHATTERBOX_SETUP.md for setup[/dim]")
            
            # Step 4: Create final video
            task4 = progress.add_task("[cyan]Creating final video...", total=1)
            
            output_filename = f"{timestamp}_{safe_name}.mp4"
            output_path = self.output_dir / output_filename
            
            try:
                # Concatenate clips
                temp_concat = self.temp_dir / f"{timestamp}_concat.mp4"
                FFmpegUtils.concatenate_videos(video_clips, temp_concat)
                
                # Mix audio tracks (voiceover + background music)
                if voiceover_path and audio_path:
                    # Mix voiceover with background music
                    temp_with_voiceover = self.temp_dir / f"{timestamp}_with_voiceover.mp4"
                    FFmpegUtils.add_audio_to_video(
                        temp_concat,
                        voiceover_path,
                        temp_with_voiceover,
                        audio_volume=1.0  # Full volume for voiceover
                    )
                    temp_concat.unlink()
                    
                    # Add background music at lower volume
                    FFmpegUtils.add_audio_to_video(
                        temp_with_voiceover,
                        audio_path,
                        output_path,
                        audio_volume=0.2  # Low volume for background
                    )
                    temp_with_voiceover.unlink()
                    
                elif voiceover_path:
                    # Just voiceover, no music
                    FFmpegUtils.add_audio_to_video(
                        temp_concat,
                        voiceover_path,
                        output_path,
                        audio_volume=1.0
                    )
                    temp_concat.unlink()
                    
                elif audio_path:
                    # Just music, no voiceover
                    FFmpegUtils.add_audio_to_video(
                        temp_concat,
                        audio_path,
                        output_path,
                        audio_volume=0.3
                    )
                    temp_concat.unlink()
                else:
                    # No audio at all
                    temp_concat.rename(output_path)
                
                # Trim to exact duration
                if output_path.exists():
                    temp_final = self.temp_dir / f"{timestamp}_final.mp4"
                    FFmpegUtils.trim_video(output_path, temp_final, 0, duration)
                    output_path.unlink()
                    temp_final.rename(output_path)
                
                progress.update(task4, completed=1)
                
                console.print(f"\n[bold green]🎉 Video created successfully![/bold green]")
                console.print(f"[cyan]📁 Location:[/cyan] {output_path}")
                
                # Show details
                size_mb = output_path.stat().st_size / (1024 * 1024)
                console.print(f"[dim]Size: {size_mb:.1f} MB | Duration: ~{duration}s[/dim]")
                
                # Show cost savings
                console.print(f"\n[green]💰 Cost Breakdown:[/green]")
                console.print(f"   Stock footage: $0 (saved ~${len(video_clips) * 50})")
                console.print(f"   Background music: $0 (saved ~$50)")
                if voiceover_path:
                    console.print(f"   Voice cloning: $0 (saved ~$20) [Chatterbox]")
                console.print(f"   Video editing: $0 (saved ~$100)")
                console.print(f"   Script/Planning: $0 (NO GPT-4 needed!)")
                voiceover_savings = 20 if voiceover_path else 0
                console.print(f"   [bold]Total cost: $0 | Total saved: ${len(video_clips) * 50 + 150 + voiceover_savings}[/bold]")
                
                return output_path
                
            except Exception as e:
                console.print(f"[red]❌ Error creating video: {e}[/red]")
                return None
    
    def interactive_mode(self):
        """Interactive video creation"""
        console.print(Panel.fit(
            "[bold cyan]🎬 Hybrid Video Generator[/bold cyan]\n"
            "[dim]Combines FREE stock media with optional AI generation[/dim]\n"
            "[green]$0/month platform | Unlimited videos | Professional quality[/green]",
            border_style="cyan"
        ))
        
        # Get topic
        console.print("\n[bold]Video Creation Options:[/bold]")
        console.print("1. Quick generate from topic")
        console.print("2. Use preset template")
        console.print("3. Advanced custom settings")
        
        choice = Prompt.ask("Choose option", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            topic = Prompt.ask("\n[bold]What's your video topic?[/bold]", default="Productivity in the Modern Workplace")
            duration = int(Prompt.ask("[bold]Duration (seconds)[/bold]", default="30"))
            add_music = Confirm.ask("[bold]Add background music?[/bold]", default=True)
            
            self.create_complete_video(
                topic=topic,
                duration=duration,
                add_music=add_music
            )
        
        elif choice == "2":
            self.show_presets()
        
        else:
            console.print("[yellow]Advanced mode coming soon![/yellow]")
    
    def show_presets(self):
        """Show and run presets"""
        presets = {
            '1': {
                'name': 'Product Demo',
                'topic': 'Modern Product Demonstration',
                'duration': 30,
                'description': 'Professional product showcase'
            },
            '2': {
                'name': 'Explainer Video',
                'topic': 'How Technology Improves Productivity',
                'duration': 45,
                'description': 'Educational explainer format'
            },
            '3': {
                'name': 'Social Media',
                'topic': 'Quick Productivity Tip',
                'duration': 15,
                'description': 'Short-form social content'
            },
            '4': {
                'name': 'Company Culture',
                'topic': 'Modern Workplace Culture',
                'duration': 30,
                'description': 'Team and culture showcase'
            },
            '5': {
                'name': 'Testimonial',
                'topic': 'Customer Success Story',
                'duration': 30,
                'description': 'Customer testimonial format'
            }
        }
        
        table = Table(title="Video Presets")
        table.add_column("Option", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Description", style="dim")
        
        for key, preset in presets.items():
            table.add_row(
                key,
                preset['name'],
                f"{preset['duration']}s",
                preset['description']
            )
        
        console.print("\n")
        console.print(table)
        
        choice = Prompt.ask("\n[bold]Select preset[/bold]", choices=list(presets.keys()), default="1")
        
        preset = presets[choice]
        console.print(f"\n[cyan]Creating: {preset['name']}[/cyan]")
        
        self.create_complete_video(
            topic=preset['topic'],
            duration=preset['duration'],
            add_music=True
        )

def main():
    generator = HybridVideoGenerator()
    
    if len(sys.argv) > 1:
        # Command line mode
        topic = " ".join(sys.argv[1:])
        generator.create_complete_video(topic=topic, duration=30, add_music=True)
    else:
        # Interactive mode
        generator.interactive_mode()

if __name__ == "__main__":
    main()
