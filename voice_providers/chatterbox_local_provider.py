#!/usr/bin/env python3
"""
Chatterbox Local Voice Provider
Uses Chatterbox models downloaded locally
"""

import torch
import torchaudio
from pathlib import Path
from rich.console import Console
import sys

console = Console()


class ChatterboxLocalProvider:
    """
    Voice provider using Chatterbox models locally
    """
    
    def __init__(self):
        self.model_path = Path.home() / ".cache/huggingface/hub/models--ResembleAI--chatterbox"
        self.model = None
        self.device = "cpu"  # Use CPU for now
        
    def load_model(self):
        """
        Load Chatterbox model from local cache
        """
        console.print("[cyan]Loading Chatterbox model from local cache...[/cyan]")
        
        if not self.model_path.exists():
            console.print(f"[red]❌ Model not found at: {self.model_path}[/red]")
            console.print("[yellow]Models need to be downloaded first[/yellow]")
            return False
        
        try:
            # For now, just verify the model files exist
            model_files = list(self.model_path.glob("**/*.safetensors"))
            if len(model_files) == 0:
                console.print("[red]❌ No model files found[/red]")
                return False
            
            console.print(f"[green]✅ Found {len(model_files)} model files[/green]")
            console.print("[dim]Model loading ready (full inference not yet implemented)[/dim]")
            
            self.model = "placeholder"  # Placeholder until full implementation
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error loading model: {str(e)[:100]}[/red]")
            return False
    
    def generate_voice(self, text, reference_audio_path, output_path):
        """
        Generate voice using Chatterbox
        
        Args:
            text: Text to convert to speech
            reference_audio_path: Path to reference voice
            output_path: Where to save generated audio
        
        Returns:
            Path to generated audio or None
        """
        
        console.print(f"\n[bold cyan]🎙️  Generating Voice Locally[/bold cyan]\n")
        console.print(f"Text: {text[:60]}...")
        console.print(f"Reference: {reference_audio_path}")
        
        # Load model if not already loaded
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            console.print("\n[yellow]⚠️  Full Chatterbox inference not yet implemented[/yellow]")
            console.print("[dim]Using fallback: copying reference audio as placeholder[/dim]\n")
            
            # For now, just copy the reference audio as a placeholder
            # This will be replaced with actual Chatterbox inference
            import shutil
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            ref_path = Path(reference_audio_path)
            if ref_path.exists():
                shutil.copy(ref_path, output_file)
                console.print(f"[green]✅ Placeholder audio created: {output_file}[/green]\n")
                return str(output_file)
            else:
                console.print(f"[red]❌ Reference audio not found: {ref_path}[/red]\n")
                return None
                
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)[:100]}[/red]\n")
            return None
    
    def generate_with_voice(self, text, voice_name="Tomi_Zenyai", exaggeration=0.5, output_path="output.wav"):
        """
        Generate voice with specific voice name (for compatibility)
        
        Args:
            text: Text to convert to speech
            voice_name: Voice to use
            exaggeration: Voice exaggeration level
            output_path: Where to save audio
        
        Returns:
            Path to generated audio file
        """
        
        # Use default reference voice
        reference_audio = "narrations/tomi_zenyai_test.wav"
        
        return self.generate_voice(text, reference_audio, output_path)


if __name__ == "__main__":
    # Test the provider
    console.print("\n[bold cyan]🧪 Testing Chatterbox Local Provider[/bold cyan]\n")
    
    provider = ChatterboxLocalProvider()
    
    # Test model loading
    console.print("[bold]1. Model Loading Test[/bold]")
    if provider.load_model():
        console.print("[green]✅ Model loading successful[/green]\n")
    else:
        console.print("[red]❌ Model loading failed[/red]\n")
        sys.exit(1)
    
    # Test voice generation
    console.print("[bold]2. Voice Generation Test[/bold]")
    
    test_text = """
    Culture isn't just about ping pong tables and free snacks.
    It's about building something meaningful together.
    """
    
    result = provider.generate_voice(
        text=test_text.strip(),
        reference_audio_path="narrations/tomi_zenyai_test.wav",
        output_path="narrations/local_test.wav"
    )
    
    if result:
        console.print(f"[bold green]✅ Test successful![/bold green]")
        console.print(f"[cyan]Audio saved to: {result}[/cyan]\n")
        console.print("[yellow]Note: This is using placeholder audio until full Chatterbox inference is implemented[/yellow]\n")
    else:
        console.print("[bold red]❌ Test failed![/bold red]\n")
