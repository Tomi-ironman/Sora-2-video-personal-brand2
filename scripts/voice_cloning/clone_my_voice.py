#!/usr/bin/env python3
"""
Clone Tomi's Voice for Zenyai Videos
Run this once to set up your voice for all future videos
"""

from pathlib import Path
from rich.console import Console

console = Console()

def clone_voice():
    """Clone voice from audio sample"""
    
    console.print("\n[bold cyan]🎙️ Cloning Your Voice...[/bold cyan]\n")
    
    try:
        # Import Chatterbox
        from voice_providers.chatterbox_provider import ChatterboxProvider
        
        # Initialize provider
        console.print("[cyan]Initializing Chatterbox...[/cyan]")
        provider = ChatterboxProvider()
        
        # Clone voice
        console.print("[cyan]Cloning voice from: voice_samples/tomi_zenyai.wav[/cyan]")
        provider.clone_voice(
            name="Tomi_Zenyai",
            audio_sample_path=Path("voice_samples/tomi_zenyai.wav"),
            description="Tomi's voice for Zenyai videos"
        )
        
        console.print("[green]✅ Voice cloned successfully![/green]")
        
        # Generate test
        console.print("\n[cyan]Generating test narration...[/cyan]")
        test_text = "Welcome to Zenyai, the AI-powered audio storage platform for professionals. This is my voice."
        
        narrations_dir = Path("narrations")
        narrations_dir.mkdir(exist_ok=True)
        
        test_output = provider.generate_with_voice(
            text=test_text,
            voice_name="Tomi_Zenyai",
            output_path=narrations_dir / "tomi_voice_test.wav"
        )
        
        console.print(f"[green]✅ Test narration saved: {test_output}[/green]")
        
        # Show how to use
        console.print("\n[bold green]🎉 Your voice is ready![/bold green]\n")
        console.print("[bold]How to use in videos:[/bold]")
        console.print("1. Create video with your voice:")
        console.print("   [dim]python3 hybrid_video_generator.py \"Zenyai Demo\"[/dim]")
        console.print("   [dim]# When prompted, add voiceover: YES[/dim]")
        console.print("   [dim]# Voice name: Tomi_Zenyai[/dim]")
        console.print("")
        console.print("2. Or programmatically:")
        console.print("   [dim]generator.create_complete_video([/dim]")
        console.print("   [dim]    topic='Zenyai Product Demo',[/dim]")
        console.print("   [dim]    add_voiceover=True,[/dim]")
        console.print("   [dim]    voice_name='Tomi_Zenyai'[/dim]")
        console.print("   [dim])[/dim]")
        console.print("")
        console.print("[bold]Voice name:[/bold] [green]Tomi_Zenyai[/green]")
        console.print("[bold]Source audio:[/bold] voice_samples/tomi_zenyai.wav (1m 25s)")
        console.print("[bold]Test output:[/bold] narrations/tomi_voice_test.wav")
        console.print("")
        console.print("[dim]Listen to the test to verify quality![/dim]")
        
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Chatterbox not installed: {e}[/red]")
        console.print("\n[yellow]Setup required (10 minutes):[/yellow]")
        console.print("1. Run: [dim]./setup_python311.sh[/dim]")
        console.print("2. Activate: [dim]conda activate chatterbox[/dim]")
        console.print("3. Install: [dim]cd chatterbox && pip install -e .[/dim]")
        console.print("4. Run this script again")
        console.print("\nSee: CHATTERBOX_SETUP.md")
        return False
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return False

if __name__ == "__main__":
    import sys
    success = clone_voice()
    sys.exit(0 if success else 1)
