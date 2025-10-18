#!/usr/bin/env python3
"""
Chatterbox Voice Cloning Test
Tests Chatterbox installation and basic functionality
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_chatterbox():
    """Test Chatterbox voice cloning"""
    
    console.print(Panel.fit(
        "[bold cyan]🎙️ Chatterbox Voice Cloning Test[/bold cyan]\n"
        "[dim]Testing FREE voice generation and cloning[/dim]",
        border_style="cyan"
    ))
    
    try:
        # Check Python version
        import sys
        py_version = sys.version_info
        
        console.print(f"\n[cyan]Python Version:[/cyan] {py_version.major}.{py_version.minor}.{py_version.micro}")
        
        if py_version.major == 3 and py_version.minor not in [10, 11]:
            console.print("[yellow]⚠️  Warning: Chatterbox requires Python 3.10 or 3.11[/yellow]")
            console.print(f"[yellow]   You have Python {py_version.major}.{py_version.minor}[/yellow]")
            console.print("\n[bold]Setup Instructions:[/bold]")
            console.print("1. Install conda: https://docs.conda.io/en/latest/miniconda.html")
            console.print("2. Create environment: conda create -n chatterbox python=3.11 -y")
            console.print("3. Activate: conda activate chatterbox")
            console.print("4. Install: cd chatterbox && pip install -e .")
            console.print("\nSee CHATTERBOX_SETUP.md for detailed instructions")
            return False
        
        # Try to import Chatterbox
        console.print("\n[cyan]Testing imports...[/cyan]")
        
        from voice_providers.chatterbox_provider import ChatterboxProvider
        console.print("[green]✅ ChatterboxProvider imported successfully[/green]")
        
        # Initialize provider
        console.print("\n[cyan]Initializing Chatterbox...[/cyan]")
        provider = ChatterboxProvider()
        console.print(f"[green]✅ Chatterbox initialized on device: {provider.device}[/green]")
        
        # Test text-to-speech
        console.print("\n[cyan]Testing voice generation...[/cyan]")
        
        test_text = "Hello! This is a test of Chatterbox voice generation for Zenyai."
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        audio_path = provider.generate(
            text=test_text,
            output_path=output_dir / "test_chatterbox.wav"
        )
        
        console.print(f"[green]✅ Generated speech: {audio_path}[/green]")
        
        # Check file size
        size_kb = audio_path.stat().st_size / 1024
        console.print(f"[dim]   File size: {size_kb:.1f} KB[/dim]")
        
        # Test voice library
        console.print("\n[cyan]Testing voice library...[/cyan]")
        voices = provider.list_voices()
        console.print(f"[green]✅ Voice library ready ({len(voices)} voices)[/green]")
        
        # Success summary
        console.print("\n" + "="*60)
        console.print("[bold green]🎉 All tests passed![/bold green]")
        console.print("\n[bold]Chatterbox is ready to use![/bold]")
        console.print(f"  • Device: {provider.device}")
        console.print(f"  • Model: {'Multilingual (23 languages)' if provider.multilingual else 'English only'}")
        console.print(f"  • Test audio: {audio_path}")
        console.print("="*60)
        
        console.print("\n[bold cyan]Next Steps:[/bold cyan]")
        console.print("1. Record your voice sample (10-30 seconds)")
        console.print("2. Clone your voice:")
        console.print("   [dim]provider.clone_voice('Your_Name', Path('sample.wav'))[/dim]")
        console.print("3. Generate with your voice:")
        console.print("   [dim]provider.generate_with_voice(text='...', voice_name='Your_Name')[/dim]")
        console.print("\nSee CHATTERBOX_SETUP.md for detailed guide!")
        
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Import Error: {e}[/red]")
        console.print("\n[bold]Chatterbox not installed.[/bold]")
        console.print("Follow these steps:")
        console.print("1. Create Python 3.11 environment")
        console.print("2. cd chatterbox && pip install -e .")
        console.print("3. Run this test again")
        console.print("\nSee CHATTERBOX_SETUP.md for full instructions")
        return False
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return False

if __name__ == "__main__":
    success = test_chatterbox()
    sys.exit(0 if success else 1)
