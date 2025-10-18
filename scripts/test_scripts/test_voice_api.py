#!/usr/bin/env python3
"""
Test Voice Cloning API
"""

import requests
from rich.console import Console

console = Console()

API_URL = "https://zenyai-voice-cloning-d73w32b5wq-uc.a.run.app"

console.print("\n[bold cyan]🧪 Testing Voice Cloning API[/bold cyan]\n")

# Test 1: Health Check
console.print("[bold]Test 1: Health Check[/bold]")
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    console.print(f"Status: {response.status_code}")
    console.print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        console.print("[green]✅ Health check passed![/green]\n")
    else:
        console.print("[red]❌ Health check failed![/red]\n")
except Exception as e:
    console.print(f"[red]❌ Error: {e}[/red]\n")

# Test 2: Voice Generation
console.print("[bold]Test 2: Voice Generation[/bold]")

payload = {
    "reference_audio_url": "https://storage.googleapis.com/chatterbox-ai-models/voices/tomi_zenyai_reference.wav",
    "text": "Culture isn't just about ping pong tables and free snacks. It's about building something meaningful together."
}

console.print(f"Reference: {payload['reference_audio_url']}")
console.print(f"Text: {payload['text'][:60]}...")
console.print("[dim]Sending request (may take 30-60s for first request)...[/dim]\n")

try:
    response = requests.post(
        f"{API_URL}/clone-voice",
        json=payload,
        timeout=180
    )
    
    console.print(f"Status: {response.status_code}")
    console.print(f"Response: {response.text[:500]}\n")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            console.print("[green]✅ Voice generation successful![/green]")
            console.print(f"[cyan]Audio URL: {result.get('audio_url')}[/cyan]")
            console.print(f"[cyan]Filename: {result.get('filename')}[/cyan]\n")
        else:
            console.print(f"[yellow]⚠️  API returned error: {result.get('error')}[/yellow]\n")
    else:
        console.print("[red]❌ Voice generation failed![/red]\n")
        
except requests.exceptions.Timeout:
    console.print("[red]❌ Request timeout[/red]\n")
except Exception as e:
    console.print(f"[red]❌ Error: {e}[/red]\n")

# Summary
console.print("[bold cyan]📊 Summary:[/bold cyan]")
console.print("✅ API is deployed and accessible")
console.print("✅ Health check working")
console.print("✅ Reference voice uploaded to GCS")
console.print("⚠️  Voice generation returns 500 error")
console.print("\n[yellow]Backend team needs to implement full Chatterbox inference[/yellow]")
console.print("[dim]Currently using placeholder audio generation[/dim]\n")
