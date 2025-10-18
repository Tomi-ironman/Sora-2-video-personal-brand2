#!/usr/bin/env python3
"""
Create Culture & AI Video
Beautiful message about AI and culture
"""

from pathlib import Path
from rich.console import Console

console = Console()

# 15-second script about culture and AI
CULTURE_SCRIPT = """
Culture is the heartbeat of humanity. It's our stories, our traditions, our soul. 
AI doesn't erase culture—it amplifies it. It helps us preserve what makes us human, 
share our heritage across borders, and celebrate our diversity. Technology and tradition, 
hand in hand, creating a richer future for all.
"""

def create_culture_video():
    """Create the complete culture & AI video"""
    
    console.print("\n[bold cyan]🎬 Creating Culture & AI Video[/bold cyan]\n")
    
    # Paths
    image_path = Path("Tomi/Gemini_Generated_Image_paq9q1paq9q1paq9.png")
    narration_dir = Path("narrations")
    narration_dir.mkdir(exist_ok=True)
    audio_path = narration_dir / "culture_ai_narration.wav"
    
    # Check image exists
    if not image_path.exists():
        console.print(f"[red]❌ Image not found: {image_path}[/red]")
        return None
    
    console.print(f"[green]✅ Found image: {image_path}[/green]")
    console.print(f"\n[bold]📝 Script:[/bold]")
    console.print(f"[dim]{CULTURE_SCRIPT.strip()}[/dim]\n")
    
    # Step 1: Generate voice audio
    console.print("[cyan]Step 1: Generating voice narration...[/cyan]")
    
    try:
        from voice_providers.chatterbox_provider import ChatterboxProvider
        
        provider = ChatterboxProvider()
        
        # Generate with natural, warm tone
        console.print("[dim]Using your voice with natural tone...[/dim]")
        provider.generate_with_voice(
            text=CULTURE_SCRIPT.strip(),
            voice_name="Tomi_Zenyai",
            exaggeration=0.5,  # Natural, conversational
            output_path=audio_path
        )
        
        console.print(f"[green]✅ Voice generated: {audio_path}[/green]")
        
        # Get audio duration
        import wave
        with wave.open(str(audio_path), 'r') as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            duration = frames / float(rate)
            console.print(f"[cyan]Duration: {duration:.1f} seconds[/cyan]")
        
    except Exception as e:
        console.print(f"[red]❌ Voice generation failed: {e}[/red]")
        return None
    
    # Step 2: Create talking head video
    console.print("\n[cyan]Step 2: Creating talking head video...[/cyan]")
    console.print("[dim]Syncing your voice with the image...[/dim]")
    console.print("[dim]This will take 30-90 seconds...[/dim]\n")
    
    try:
        from create_talking_video import create_talking_video
        
        video_path = create_talking_video(
            image_path=str(image_path),
            audio_path=str(audio_path),
            output_path="talking_videos/culture_ai_video.mp4",
            enhancer="gfpgan"  # Enhanced quality
        )
        
        if video_path:
            console.print("\n[bold green]🎉 Culture & AI Video Complete![/bold green]\n")
            console.print(f"[cyan]📹 Video:[/cyan] {video_path}")
            console.print(f"[cyan]🎙️  Audio:[/cyan] {audio_path}")
            console.print(f"[cyan]📸 Image:[/cyan] {image_path}")
            
            # Show file size
            video_size = video_path.stat().st_size / (1024 * 1024)
            console.print(f"[cyan]📊 Size:[/cyan] {video_size:.1f} MB")
            
            console.print("\n[bold]🔊 To watch:[/bold]")
            console.print(f"   open {video_path}")
            
            # Auto-play
            console.print("\n[cyan]Playing video...[/cyan]")
            import subprocess
            try:
                subprocess.run(["open", str(video_path)], check=True)
            except:
                console.print("[yellow]Please open the video manually[/yellow]")
            
            return video_path
        else:
            console.print("[red]❌ Video creation failed[/red]")
            return None
            
    except Exception as e:
        console.print(f"[red]❌ Video creation failed: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return None

if __name__ == "__main__":
    import sys
    
    console.print("\n[bold cyan]🌍 Culture & AI - A Beautiful Message[/bold cyan]")
    console.print("[dim]Creating a 15-second video about technology and tradition[/dim]\n")
    
    result = create_culture_video()
    
    if result:
        console.print("\n[bold green]✅ Success! Your message is ready to share.[/bold green]")
        sys.exit(0)
    else:
        console.print("\n[red]❌ Video creation failed. Check errors above.[/red]")
        sys.exit(1)
