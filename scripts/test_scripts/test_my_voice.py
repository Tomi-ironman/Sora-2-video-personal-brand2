#!/usr/bin/env python3
"""
Test Tomi's Voice - Generate Speech from Script
"""

from pathlib import Path
from rich.console import Console

console = Console()

# Culture & AI script (15 seconds)
SCRIPT = """
Culture is the heartbeat of humanity. It's our stories, our traditions, our soul. 
AI doesn't erase culture, it amplifies it. It helps us preserve what makes us human, 
share our heritage across borders, and celebrate our diversity. Technology and tradition, 
hand in hand, creating a richer future for all.
"""

def test_voice():
    """Generate speech with Tomi's voice"""
    
    console.print("\n[bold cyan]🎙️ Testing Your Voice with Zenyai Script[/bold cyan]\n")
    
    try:
        # Import Chatterbox
        from voice_providers.chatterbox_provider import ChatterboxProvider
        
        # Initialize
        console.print("[cyan]Initializing Chatterbox...[/cyan]")
        provider = ChatterboxProvider()
        
        # First, clone the voice if not already done
        console.print("[cyan]Setting up your voice: Tomi_Zenyai[/cyan]")
        try:
            provider.clone_voice(
                name="Tomi_Zenyai",
                audio_sample_path=Path("voice_samples/tomi_zenyai.wav"),
                description="Tomi's voice for Zenyai"
            )
            console.print("[green]✅ Voice cloned[/green]")
        except Exception as e:
            console.print(f"[yellow]Voice may already be cloned: {e}[/yellow]")
        
        # Show script
        console.print("\n[bold]📝 Script:[/bold]")
        console.print(f"[dim]{SCRIPT.strip()}[/dim]")
        
        # Generate speech
        console.print("\n[cyan]Generating speech with your voice...[/cyan]")
        
        output_dir = Path("narrations")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "culture_ai_narration.wav"
        
        audio = provider.generate_with_voice(
            text=SCRIPT.strip(),
            voice_name="Tomi_Zenyai",
            exaggeration=0.5,  # Natural tone
            output_path=output_path
        )
        
        console.print(f"\n[bold green]✅ Speech generated successfully![/bold green]")
        console.print(f"[cyan]📁 Saved to:[/cyan] {audio}")
        console.print(f"[cyan]📊 File size:[/cyan] {audio.stat().st_size / 1024:.1f} KB")
        
        # Show how to play
        console.print("\n[bold]🔊 To listen:[/bold]")
        console.print(f"   [dim]open {audio}[/dim]")
        console.print(f"   [dim]# Or: afplay {audio}[/dim]")
        
        # Try to play automatically
        console.print("\n[cyan]Playing audio...[/cyan]")
        import subprocess
        try:
            subprocess.run(["afplay", str(audio)], check=True)
            console.print("[green]✅ Playback complete![/green]")
        except:
            console.print("[yellow]⚠️  Couldn't auto-play. Open the file manually.[/yellow]")
        
        console.print("\n[bold green]🎉 Your voice works perfectly![/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Create videos with your voice:")
        console.print("   [dim]python3 hybrid_video_generator.py 'Zenyai Demo'[/dim]")
        console.print("2. Generate custom narrations:")
        console.print("   [dim]Use provider.generate_with_voice(...)[/dim]")
        
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Chatterbox not installed: {e}[/red]")
        console.print("\n[yellow]⚠️  You need to setup Python 3.11 first[/yellow]")
        console.print("\n[bold]Quick Setup (5 minutes):[/bold]")
        console.print("1. [dim]./setup_python311.sh[/dim]")
        console.print("2. [dim]conda activate chatterbox[/dim]")
        console.print("3. [dim]cd chatterbox && pip install -e .[/dim]")
        console.print("4. [dim]python3 test_my_voice.py[/dim]")
        console.print("\nSee: CHATTERBOX_SETUP.md or YOUR_VOICE_READY.md")
        
        # Show the script that will be generated
        console.print("\n[bold]📝 Script that will be generated:[/bold]")
        console.print(f"[dim]{SCRIPT.strip()}[/dim]")
        
        return False
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return False

if __name__ == "__main__":
    import sys
    success = test_voice()
    sys.exit(0 if success else 1)
