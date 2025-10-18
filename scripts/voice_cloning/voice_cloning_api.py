#!/usr/bin/env python3
"""
Voice Cloning API - Production Ready
Uses Zenyai Voice Cloning Service
"""

import requests
import time
from pathlib import Path
from rich.console import Console

console = Console()

# Production endpoint
VOICE_CLONE_API = "https://zenyai-voice-cloning-d73w32b5wq-uc.a.run.app/clone-voice"
REFERENCE_AUDIO_URL = "https://storage.googleapis.com/chatterbox-ai-models/voices/tomi_reference.wav"


def clone_voice(text, output_file="narrations/cloned_voice.wav", timeout=600):
    """
    Clone voice using production API
    
    Args:
        text: Script text to convert to speech
        output_file: Where to save the audio file
        timeout: Max wait time in seconds (default 10 minutes)
    
    Returns:
        Path to downloaded audio file
    """
    
    console.print("\n[bold cyan]🎙️  Voice Cloning API[/bold cyan]\n")
    console.print(f"[yellow]Script length: {len(text)} characters[/yellow]")
    console.print(f"[yellow]Script: {text[:100]}...[/yellow]\n")
    
    # Make API request
    console.print("[cyan]📡 Calling voice cloning API...[/cyan]")
    
    try:
        response = requests.post(
            VOICE_CLONE_API,
            json={
                "reference_audio_url": REFERENCE_AUDIO_URL,
                "text": text
            },
            timeout=timeout
        )
        
        # Check response
        console.print(f"[dim]Status code: {response.status_code}[/dim]")
        
        if response.status_code != 200:
            console.print(f"[red]❌ API Error ({response.status_code})[/red]")
            console.print(f"[dim]Response: {response.text[:500]}[/dim]")
            return None
        
        result = response.json()
        
        if not result.get("success"):
            console.print(f"[red]❌ API Error: {result.get('error', 'Unknown error')}[/red]")
            console.print(f"[dim]Full response: {result}[/dim]")
            return None
        
        audio_url = result["audio_url"]
        console.print(f"[green]✅ Voice cloned successfully![/green]")
        console.print(f"[dim]Audio URL: {audio_url}[/dim]\n")
        
        # Download the audio file
        console.print("[cyan]📥 Downloading audio...[/cyan]")
        audio_response = requests.get(audio_url, timeout=60)
        audio_response.raise_for_status()
        
        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(audio_response.content)
        
        file_size = len(audio_response.content)
        console.print(f"[green]✅ Audio downloaded![/green]")
        console.print(f"[cyan]📁 Saved to: {output_path}[/cyan]")
        console.print(f"[dim]Size: {file_size / 1024:.1f} KB[/dim]\n")
        
        return str(output_path)
        
    except requests.Timeout:
        console.print(f"[red]❌ Timeout: Voice cloning took longer than {timeout}s[/red]")
        return None
        
    except requests.RequestException as e:
        console.print(f"[red]❌ API Error: {str(e)}[/red]")
        return None
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        return None


def test_voice_cloning():
    """Test the voice cloning API"""
    
    test_script = """
    One thing AI can't take away from us is Japanese culture.
    Cherry blossoms bloom for just two weeks. A reminder that beauty is fleeting.
    Tea ceremony. Four hundred years of mindfulness in every gesture.
    Wabi-sabi. Finding perfection in imperfection.
    This is culture. Timeless. Human. Irreplaceable.
    """
    
    output_file = "narrations/test_voice_api.wav"
    
    console.print("\n[bold]🧪 Testing Voice Cloning API[/bold]\n")
    
    result = clone_voice(test_script.strip(), output_file)
    
    if result:
        console.print(f"\n[bold green]✅ TEST PASSED![/bold green]")
        console.print(f"[cyan]Audio file: {result}[/cyan]\n")
        
        # Try to play it
        import subprocess
        console.print("[cyan]🔊 Opening audio...[/cyan]")
        subprocess.run(['open', result])
    else:
        console.print("\n[bold red]❌ TEST FAILED[/bold red]\n")


if __name__ == "__main__":
    test_voice_cloning()
