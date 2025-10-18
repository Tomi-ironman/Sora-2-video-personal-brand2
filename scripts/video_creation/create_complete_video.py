#!/usr/bin/env python3
"""
Complete Video Generator - Idea to Professional Video
Just give an idea → Get complete professional video with your voice!
"""

from pathlib import Path
import subprocess
from rich.console import Console
from rich.prompt import Prompt
import sys

console = Console()

def generate_script(topic, style="educational", duration=20):
    """
    Generate a professional script based on topic
    
    Args:
        topic: Main topic/idea
        style: "educational", "commercial", "storytelling", "motivational"
        duration: Target duration in seconds
    """
    
    console.print(f"\n[bold cyan]📝 Generating script for: {topic}[/bold cyan]\n")
    
    # Calculate approximate word count (2.5 words per second is natural speaking pace)
    target_words = int(duration * 2.5)
    
    # Script templates based on style
    if style == "educational":
        script = f"""
        {topic} is changing the world. Here's what you need to know.
        
        This isn't just another trend. It's a fundamental shift in how we approach the future.
        The technology behind this is revolutionary, and the implications are massive.
        
        Whether you're a creator, entrepreneur, or just curious, understanding {topic} 
        gives you a competitive edge. The future belongs to those who adapt first.
        """
    
    elif style == "commercial":
        script = f"""
        Struggling with {topic}? You're not alone.
        
        Thousands of creators face this challenge every day. The old solutions are slow, 
        expensive, and frustrating. But there's a better way.
        
        Imagine cutting your workflow time in half while producing better results.
        That's the power of modern {topic} solutions. The future is here.
        """
    
    elif style == "storytelling":
        script = f"""
        There's a revolution happening in {topic}, and most people don't even know it yet.
        
        What started as a small innovation has grown into something extraordinary.
        The pioneers who saw this coming early are already reaping the benefits.
        
        This is your moment to be part of something bigger. To transform how you work,
        create, and succeed. The story of {topic} is just beginning.
        """
    
    elif style == "motivational":
        script = f"""
        You have everything you need to master {topic}. Let me show you how.
        
        Success isn't about having more resources. It's about using what you have better.
        The same tools that professionals use are available to you right now.
        
        Your journey starts with one decision. To learn, to grow, to push forward.
        {topic} is your path to the next level. Take the first step today.
        """
    
    else:
        script = f"""
        Let's talk about {topic}. This is important.
        
        Understanding this concept can completely change your perspective.
        The principles are simple, but the impact is profound.
        
        Whether you're just starting or you're experienced, there's always more to learn.
        {topic} is evolving rapidly, and staying informed gives you an edge.
        """
    
    # Clean up script
    script = " ".join(script.split())  # Remove extra whitespace
    script = script.strip()
    
    return script

def generate_search_queries(topic, script_text):
    """
    Generate smart B-roll search queries based on topic and script
    """
    
    console.print("[cyan]Generating visual search queries...[/cyan]")
    
    # Extract key concepts from topic
    topic_lower = topic.lower()
    
    queries = []
    
    # Add topic-specific queries
    if "ai" in topic_lower or "artificial" in topic_lower:
        queries.extend([
            "artificial intelligence technology",
            "futuristic tech innovation",
            "digital transformation",
            "robot ai future",
            "machine learning data"
        ])
    
    elif "business" in topic_lower or "entrepreneur" in topic_lower:
        queries.extend([
            "business people working",
            "entrepreneur startup office",
            "success achievement team",
            "professional workspace",
            "growth strategy planning"
        ])
    
    elif "creative" in topic_lower or "content" in topic_lower:
        queries.extend([
            "creative person working",
            "content creator filming",
            "artistic creation process",
            "digital content production",
            "creative workspace studio"
        ])
    
    elif "technology" in topic_lower or "tech" in topic_lower:
        queries.extend([
            "modern technology devices",
            "innovation digital future",
            "tech workspace coding",
            "digital transformation",
            "future technology abstract"
        ])
    
    else:
        # Generic professional queries
        queries.extend([
            f"{topic} innovation",
            f"{topic} professional",
            "people working together",
            "success achievement",
            "modern workspace",
            "future innovation",
            "professional environment"
        ])
    
    # Ensure we have at least 7 queries
    while len(queries) < 7:
        queries.append(f"{topic} concept")
    
    return queries[:7]

def create_professional_video(
    topic,
    style="educational",
    duration=20,
    voice_name="Tomi_Zenyai",
    output_name=None
):
    """
    Complete pipeline: Idea → Professional Video
    
    Args:
        topic: Main topic/idea for the video
        style: Script style
        duration: Target duration
        voice_name: Voice to use for cloning
        output_name: Output filename (auto-generated if None)
    """
    
    console.print("\n[bold cyan]🎬 Complete Video Generator[/bold cyan]")
    console.print(f"[dim]From idea to professional video in minutes![/dim]\n")
    
    # Step 1: Generate script
    console.print("[bold]Step 1/5: Generating script[/bold]")
    script = generate_script(topic, style=style, duration=duration)
    console.print(f"\n[green]✅ Script created ({len(script.split())} words)[/green]")
    console.print(f"\n[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    console.print(f"[yellow]{script}[/yellow]")
    console.print(f"[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")
    
    # Step 2: Generate voice with Chatterbox - SIMPLE METHOD
    console.print("\n[bold]Step 2/5: Generating voice with your cloned voice[/bold]")
    
    narrations_dir = Path("narrations")
    narrations_dir.mkdir(exist_ok=True)
    
    # Create unique filename for this script
    import hashlib
    script_hash = hashlib.md5(script.encode()).hexdigest()[:8]
    audio_path = narrations_dir / f"voice_{script_hash}.wav"
    
    # Use the SAME method that was working before
    console.print("[cyan]Using Chatterbox voice provider...[/cyan]")
    
    try:
        from voice_providers.chatterbox_provider import ChatterboxProvider
        
        provider = ChatterboxProvider()
        
        provider.generate_with_voice(
            text=script,
            voice_name=voice_name,
            exaggeration=0.5,
            output_path=audio_path
        )
        
        console.print(f"[green]✅ Voice generated with {voice_name}![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Voice generation failed: {e}[/red]")
        console.print("[bold yellow]Cannot generate new voice for this script![/bold yellow]")
        return None
    
    # Step 3: Generate search queries
    console.print("\n[bold]Step 3/5: Planning visual content[/bold]")
    search_queries = generate_search_queries(topic, script)
    
    for i, query in enumerate(search_queries, 1):
        console.print(f"  {i}. {query}")
    
    # Step 4: Create synced video
    console.print("\n[bold]Step 4/5: Creating video with smart-synced B-roll[/bold]")
    
    # Determine output path
    if not output_name:
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_').lower()[:30]
        output_name = f"{safe_topic}_video.mp4"
    
    video_output = Path("professional_videos") / output_name
    
    # Import and use the synced video creator
    from create_synced_video import create_synced_video
    
    result = create_synced_video(
        audio_path=str(audio_path),
        script_text=script,
        output_path=str(video_output),
        aspect_ratio="9:16",
        add_music=True
    )
    
    if not result:
        console.print("[red]❌ Video creation failed[/red]")
        return None
    
    # Step 5: Add captions
    console.print("\n[bold]Step 5/5: Adding auto-captions[/bold]")
    
    captioned_output = video_output.parent / f"{video_output.stem}_WITH_CAPTIONS.mp4"
    
    from add_captions import add_captions_to_video
    
    final_video = add_captions_to_video(
        video_path=str(video_output),
        output_path=str(captioned_output),
        audio_path=str(audio_path),
        script_text=script,
        style="modern"
    )
    
    # Cleanup
    console.print("\n[dim]Cleaning up temp files...[/dim]")
    import shutil
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    # Final summary
    console.print("\n" + "="*60)
    console.print("[bold green]🎉 COMPLETE PROFESSIONAL VIDEO READY![/bold green]")
    console.print("="*60 + "\n")
    
    console.print("[bold cyan]📊 Video Details:[/bold cyan]")
    console.print(f"  • Topic: {topic}")
    console.print(f"  • Style: {style}")
    console.print(f"  • Duration: ~{duration}s")
    console.print(f"  • Format: 9:16 (social media)")
    
    if final_video:
        file_size = Path(final_video).stat().st_size / (1024 * 1024)
        console.print(f"  • Size: {file_size:.1f} MB")
        console.print(f"  • File: {final_video}\n")
    
    console.print("[bold cyan]✨ Features:[/bold cyan]")
    console.print("  ✅ Your cloned voice")
    console.print("  ✅ AI-generated script")
    console.print("  ✅ Smart-synced B-roll (7 clips)")
    console.print("  ✅ Cinematic color grading")
    console.print("  ✅ Background music")
    console.print("  ✅ Word-by-word captions")
    console.print("  ✅ Visual-based sound effects (ready)")
    console.print("  ✅ Professional transitions")
    
    console.print("\n[bold green]Ready to post on TikTok, Instagram Reels, YouTube Shorts![/bold green]\n")
    
    # Open video
    if final_video:
        subprocess.run(["open", str(final_video)])
    
    return final_video


if __name__ == "__main__":
    console.print("\n[bold cyan]🎬 COMPLETE VIDEO GENERATOR[/bold cyan]")
    console.print("[dim]Idea → Professional Video in Minutes[/dim]\n")
    
    # Check if topic was provided as argument
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        console.print("[bold]What video do you want to create?[/bold]\n")
        console.print("[dim]Examples:[/dim]")
        console.print("  • AI for Content Creators")
        console.print("  • Building a Personal Brand")
        console.print("  • The Future of Work")
        console.print("  • Productivity Hacks\n")
        
        topic = Prompt.ask("[cyan]Enter your video topic/idea")
    
    if not topic:
        console.print("[red]Please provide a topic![/red]")
        sys.exit(1)
    
    # Ask for style
    console.print("\n[bold]Choose video style:[/bold]")
    console.print("  1. Educational (informative, clear)")
    console.print("  2. Commercial (problem-solution)")
    console.print("  3. Storytelling (narrative-driven)")
    console.print("  4. Motivational (inspiring)")
    
    style_choice = Prompt.ask("[cyan]Style", choices=["1", "2", "3", "4"], default="1")
    
    style_map = {
        "1": "educational",
        "2": "commercial",
        "3": "storytelling",
        "4": "motivational"
    }
    
    style = style_map[style_choice]
    
    # Create video!
    result = create_professional_video(
        topic=topic,
        style=style,
        duration=20,
        voice_name="Tomi_Zenyai"
    )
    
    if result:
        console.print("\n[bold green]✅ SUCCESS! Your video is ready![/bold green]")
    else:
        console.print("\n[bold red]❌ Something went wrong. Check the logs above.[/bold red]")
