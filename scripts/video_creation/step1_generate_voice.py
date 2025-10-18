#!/usr/bin/env python3
"""
STEP 1: Generate Voice ONLY
Wait for completion before creating video
"""

import requests
import time
from pathlib import Path
from rich.console import Console

console = Console()

VOICE_CLONE_API = "https://zenyai-voice-cloning-d73w32b5wq-uc.a.run.app/clone-voice"
REFERENCE_AUDIO_URL = "https://storage.googleapis.com/chatterbox-ai-models/voices/tomi_reference.wav"


def generate_voice_only(script_text, output_file="narrations/generated_voice.wav"):
    """
    Generate voice and WAIT for completion
    
    Returns:
        Path to audio file if successful, None if failed
    """
    
    console.print("\n[bold cyan]🎙️  STEP 1: VOICE GENERATION ONLY[/bold cyan]\n")
    console.print(f"[yellow]Script length: {len(script_text)} characters[/yellow]")
    console.print(f"[yellow]Output: {output_file}[/yellow]\n")
    console.print(f"[dim]Script preview:[/dim]")
    console.print(f"[dim]{script_text[:150]}...[/dim]\n")
    
    # Try with VERY long timeout for longer scripts
    timeout_seconds = 600  # 10 minutes
    
    console.print(f"[cyan]📡 Calling voice API (timeout: {timeout_seconds}s)...[/cyan]")
    console.print("[dim]This may take a while for longer scripts...[/dim]\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            VOICE_CLONE_API,
            json={
                "reference_audio_url": REFERENCE_AUDIO_URL,
                "text": script_text
            },
            timeout=timeout_seconds
        )
        
        elapsed = time.time() - start_time
        console.print(f"[dim]API response time: {elapsed:.1f}s[/dim]")
        
        if response.status_code != 200:
            console.print(f"[red]❌ API Error ({response.status_code})[/red]")
            console.print(f"[dim]{response.text[:300]}[/dim]")
            return None
        
        result = response.json()
        
        if not result.get("success"):
            console.print(f"[red]❌ Generation failed: {result.get('error', 'Unknown')}[/red]")
            return None
        
        audio_url = result["audio_url"]
        console.print(f"[green]✅ Voice generated successfully![/green]")
        console.print(f"[dim]Audio URL: {audio_url[:80]}...[/dim]\n")
        
        # Download the audio
        console.print("[cyan]📥 Downloading audio file...[/cyan]")
        audio_response = requests.get(audio_url, timeout=60)
        audio_response.raise_for_status()
        
        # Save file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(audio_response.content)
        
        file_size = len(audio_response.content)
        console.print(f"[green]✅ Audio saved![/green]")
        console.print(f"[cyan]📁 Location: {output_path}[/cyan]")
        console.print(f"[dim]Size: {file_size / 1024:.1f} KB[/dim]\n")
        
        # Play it
        console.print("[cyan]🔊 Opening audio...[/cyan]")
        import subprocess
        subprocess.run(['open', str(output_path)])
        
        console.print(f"\n[bold green]✅ STEP 1 COMPLETE![/bold green]")
        console.print(f"[cyan]Voice file ready: {output_path}[/cyan]\n")
        console.print(f"[yellow]Next: Run step2_create_video.py to create the video[/yellow]\n")
        
        return str(output_path)
        
    except requests.Timeout:
        elapsed = time.time() - start_time
        console.print(f"\n[red]❌ Timeout after {elapsed:.1f}s[/red]")
        console.print(f"[yellow]⚠️  The API is taking too long for this script length[/yellow]")
        console.print(f"[yellow]⚠️  Try a shorter script or contact the API team[/yellow]\n")
        return None
        
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]\n")
        return None


if __name__ == "__main__":
    # Test with Japanese culture script
    script = """One thing AI can't take away from us is Japanese culture.

Cherry blossoms bloom for just two weeks. A reminder that beauty is fleeting.

Tea ceremony. Four hundred years of mindfulness in every gesture.

Wabi-sabi. Finding perfection in imperfection.

Calligraphy. Where discipline meets art.

This is culture. Timeless. Human. Irreplaceable."""
    
    result = generate_voice_only(script, "narrations/japanese_culture_api.wav")
    
    if result:
        console.print("[bold green]SUCCESS! Ready for Step 2.[/bold green]")
    else:
        console.print("[bold red]FAILED. Check API or try shorter script.[/bold red]")
