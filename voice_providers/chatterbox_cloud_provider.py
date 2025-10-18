#!/usr/bin/env python3
"""
Chatterbox Cloud Voice Provider
Uses Google Cloud Run API for voice cloning
"""

import requests
from pathlib import Path
from rich.console import Console
import time

console = Console()


class ChatterboxCloudProvider:
    """
    Voice provider using Chatterbox from Google Cloud Run
    """
    
    def __init__(self):
        self.base_url = "https://zenyai-voice-cloning-d73w32b5wq-uc.a.run.app"
        self.health_endpoint = f"{self.base_url}/health"
        self.clone_endpoint = f"{self.base_url}/clone-voice"
        self.clone_stream_endpoint = f"{self.base_url}/clone-voice-stream"
        
        # Reference voice URL (your cloned voice sample)
        # TODO: Upload your reference voice to GCS and update this URL
        self.reference_voice_url = "https://storage.googleapis.com/chatterbox-ai-models/voices/tomi_zenyai_reference.wav"
    
    def check_health(self):
        """
        Check if the service is running
        """
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_voice(self, text, output_path, reference_audio_url=None):
        """
        Generate voice using Chatterbox Cloud API
        
        Args:
            text: Text to convert to speech
            output_path: Where to save the audio
            reference_audio_url: URL to reference voice (optional)
        
        Returns:
            Path to generated audio file or None if failed
        """
        
        console.print("[cyan]Connecting to Chatterbox Cloud...[/cyan]")
        
        # Check health first
        if not self.check_health():
            console.print("[yellow]⚠️  Chatterbox service not responding[/yellow]")
            return None
        
        console.print("[green]✅ Service connected[/green]")
        console.print(f"[cyan]Generating voice ({len(text)} characters)...[/cyan]")
        
        # Use reference voice URL if not provided
        if reference_audio_url is None:
            reference_audio_url = self.reference_voice_url
        
        # Prepare request
        payload = {
            "reference_audio_url": reference_audio_url,
            "text": text
        }
        
        try:
            # Make request to clone voice
            console.print("[dim]Sending request to cloud (first request may take 30-60s for model loading)...[/dim]")
            
            response = requests.post(
                self.clone_endpoint,
                json=payload,
                timeout=180  # 3 minutes timeout (model loading + generation)
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    # Get the audio URL from response
                    audio_url = result.get('audio_url')
                    
                    if not audio_url:
                        console.print(f"[red]❌ No audio URL in response[/red]")
                        return None
                    
                    console.print(f"[green]✅ Voice generated in cloud![/green]")
                    console.print(f"[dim]Downloading from: {audio_url[:60]}...[/dim]")
                    
                    # Download the audio file
                    audio_response = requests.get(audio_url, timeout=30)
                    
                    if audio_response.status_code == 200:
                        # Save audio file
                        output_file = Path(output_path)
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_file, 'wb') as f:
                            f.write(audio_response.content)
                        
                        file_size = output_file.stat().st_size / 1024  # KB
                        
                        # Verify it's actually audio (should be > 10KB for real audio)
                        if file_size < 10:
                            console.print(f"[yellow]⚠️  File too small ({file_size:.1f}KB) - likely not real audio[/yellow]")
                            output_file.unlink()  # Delete invalid file
                            return None
                        
                        console.print(f"[green]✅ Voice downloaded successfully![/green]")
                        console.print(f"[dim]Size: {file_size:.1f}KB[/dim]")
                        
                        return str(output_file)
                    else:
                        console.print(f"[red]❌ Failed to download audio: {audio_response.status_code}[/red]")
                        return None
                else:
                    console.print(f"[red]❌ API returned error: {result.get('error', 'Unknown error')}[/red]")
                    return None
            else:
                console.print(f"[red]❌ API Error: {response.status_code}[/red]")
                console.print(f"[dim]{response.text[:200]}[/dim]")
                return None
                
        except requests.exceptions.Timeout:
            console.print("[red]❌ Request timeout (voice generation taking too long)[/red]")
            return None
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)[:100]}[/red]")
            return None
    
    def generate_with_voice(self, text, voice_name="Tomi_Zenyai", exaggeration=0.5, output_path="output.wav"):
        """
        Generate voice with specific voice name (for compatibility)
        
        Args:
            text: Text to convert to speech
            voice_name: Voice to use (currently only supports Tomi_Zenyai)
            exaggeration: Voice exaggeration level (not used in cloud version)
            output_path: Where to save audio
        
        Returns:
            Path to generated audio file
        """
        
        return self.generate_voice(text, output_path)


if __name__ == "__main__":
    # Test the provider
    console.print("\n[bold cyan]🎙️  Testing Chatterbox Cloud Provider[/bold cyan]\n")
    
    provider = ChatterboxCloudProvider()
    
    # Test health
    console.print("[bold]1. Health Check[/bold]")
    if provider.check_health():
        console.print("[green]✅ Service is healthy[/green]\n")
    else:
        console.print("[red]❌ Service is down[/red]\n")
        exit(1)
    
    # Test voice generation
    console.print("[bold]2. Voice Generation Test[/bold]")
    
    test_text = """
    Culture isn't just about ping pong tables and free snacks.
    It's about building something meaningful together.
    Creating an environment where people thrive.
    """
    
    result = provider.generate_voice(
        text=test_text.strip(),
        output_path="narrations/cloud_test.wav"
    )
    
    if result:
        console.print(f"\n[bold green]✅ Test successful![/bold green]")
        console.print(f"[cyan]Audio saved to: {result}[/cyan]\n")
    else:
        console.print("\n[bold red]❌ Test failed![/bold red]\n")
