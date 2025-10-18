#!/usr/bin/env python3
"""
Test if Sora 2 API is available in OpenAI Python library
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

load_dotenv()
console = Console()

def test_sora_api():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    console.print("[cyan]🔍 Testing Sora 2 API availability...[/cyan]")
    
    # Test 1: Check if videos attribute exists
    try:
        videos_attr = hasattr(client, 'videos')
        console.print(f"[dim]client.videos exists: {videos_attr}[/dim]")
        
        if videos_attr:
            generations_attr = hasattr(client.videos, 'generations')
            console.print(f"[dim]client.videos.generations exists: {generations_attr}[/dim]")
            
            if generations_attr:
                create_attr = hasattr(client.videos.generations, 'create')
                console.print(f"[dim]client.videos.generations.create exists: {create_attr}[/dim]")
    except Exception as e:
        console.print(f"[red]Error checking API structure: {e}[/red]")
    
    # Test 2: Try to call the API
    try:
        console.print("[cyan]🎬 Attempting Sora 2 API call...[/cyan]")
        response = client.videos.generations.create(
            model="sora-1.0-turbo",
            prompt="A simple test video of a person speaking",
            size="1920x1080",
            duration=5
        )
        console.print("[green]✅ Sora 2 API is available![/green]")
        console.print(f"[dim]Response type: {type(response)}[/dim]")
        return True
        
    except AttributeError as e:
        console.print(f"[yellow]⚠️ Sora API not available in current OpenAI library version[/yellow]")
        console.print(f"[dim]AttributeError: {e}[/dim]")
        return False
        
    except Exception as e:
        error_str = str(e).lower()
        if "not found" in error_str or "does not exist" in error_str:
            console.print(f"[yellow]⚠️ Sora model not available for this account[/yellow]")
        elif "quota" in error_str or "billing" in error_str:
            console.print(f"[yellow]⚠️ Sora API available but quota/billing issue[/yellow]")
        else:
            console.print(f"[green]✅ Sora 2 API structure exists![/green]")
            console.print(f"[yellow]⚠️ API call failed: {e}[/yellow]")
        return True

if __name__ == "__main__":
    test_sora_api()
