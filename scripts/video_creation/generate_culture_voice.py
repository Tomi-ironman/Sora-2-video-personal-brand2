#!/usr/bin/env python3
"""
Generate Culture & AI Voice Narration
"""

from pathlib import Path
from rich.console import Console

console = Console()

# 15-second script about culture and AI
CULTURE_SCRIPT = """
Culture is the heartbeat of humanity. It's our stories, our traditions, our soul. AI doesn't erase culture, it amplifies it. It helps us preserve what makes us human, share our heritage across borders, and celebrate our diversity. Technology and tradition, hand in hand, creating a richer future for all.
"""

console.print("\n[bold cyan]🎙️ Generating Culture & AI Narration[/bold cyan]\n")
console.print(f"[bold]Script:[/bold]\n[dim]{CULTURE_SCRIPT.strip()}[/dim]\n")

try:
    from voice_providers.chatterbox_provider import ChatterboxProvider
    
    provider = ChatterboxProvider()
    
    narration_dir = Path("narrations")
    narration_dir.mkdir(exist_ok=True)
    audio_path = narration_dir / "culture_ai_narration.wav"
    
    console.print("[cyan]Generating with your voice...[/cyan]")
    
    provider.generate_with_voice(
        text=CULTURE_SCRIPT.strip(),
        voice_name="Tomi_Zenyai",
        exaggeration=0.5,
        output_path=audio_path
    )
    
    console.print(f"[green]✅ Voice generated: {audio_path}[/green]")
    
    # Get duration
    import wave
    with wave.open(str(audio_path), 'r') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        duration = frames / float(rate)
        console.print(f"[cyan]Duration: {duration:.1f} seconds[/cyan]")
    
    console.print("\n[green]✅ Ready for video creation![/green]")
    
except Exception as e:
    console.print(f"[red]❌ Error: {e}[/red]")
    import traceback
    traceback.print_exc()
