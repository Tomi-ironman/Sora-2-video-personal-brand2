#!/usr/bin/env python3
"""
Styled Personal Brand Videos - Batch Creator
Creates multiple videos automatically (supports 20 unique styles) and saves to Desktop
"""

from create_video_master import create_video_from_script
from pathlib import Path
import shutil
import os
import json
from datetime import datetime
import argparse
import random
from rich.console import Console

console = Console()


# 10 VIDEO TOPICS WITH SCRIPTS
VIDEO_BATCH = [
    {
        "id": 1,
        "title": "Music Composition - Where Creativity Meets Discipline",
        "topic": "music composition production",
        "script": """Music composition. Where creativity meets discipline!

The blank page. Every composer's greatest fear!

But here's the truth. You don't need perfect inspiration!

Start with a simple melody. Just four notes!

Build it. Layer it. Transform it!

This is how masterpieces are born. One note at a time!""",
        "filename": "01_music_composition.mp4"
    },
    
    {
        "id": 2,
        "title": "Greek Culture - Ancient Wisdom for Modern Life",
        "topic": "greek culture philosophy ancient",
        "script": """Greece. Where philosophy changed the world!

Ancient wisdom. Modern problems!

The Greeks knew something we forgot. Balance!

Art. Science. Body. Mind!

This is timeless knowledge. This is power!

Ancient Greece. Still teaching us today!""",
        "filename": "02_greek_culture.mp4"
    },
    
    {
        "id": 3,
        "title": "AI and Humanity - What Cannot Be Replaced",
        "topic": "artificial intelligence human creativity",
        "script": """AI is everywhere. But here's what it can't replace!

Your story. Your experience. Your soul!

Machines create. Humans inspire!

AI generates content. Humans create meaning!

The future isn't human versus machine. It's human WITH machine!

Your humanity. That's your superpower!""",
        "filename": "03_ai_and_humanity.mp4"
    },
    
    {
        "id": 4,
        "title": "Creative Process - Embracing the Chaos",
        "topic": "creative process art inspiration",
        "script": """Creativity isn't clean. It's messy!

The struggle. The doubt. The breakthrough!

Every artist faces the same demon. Perfectionism!

But here's the secret. Done beats perfect!

Create. Ship. Repeat!

This is the only way. This is the path!""",
        "filename": "04_creative_process.mp4"
    },
    
    {
        "id": 5,
        "title": "Time Management - The Creator's Dilemma",
        "topic": "time management productivity creative",
        "script": """Twenty four hours. That's all we get!

The creator's curse. Never enough time!

But time isn't the problem. Focus is!

One hour of deep work beats ten hours of distraction!

Protect your time. Guard your energy!

Your art depends on it!""",
        "filename": "05_time_management.mp4"
    },
    
    {
        "id": 6,
        "title": "Building in Public - The New Way",
        "topic": "social media content creation building public",
        "script": """Hide your process? That's old thinking!

The new way. Build in public!

Share your journey. Show the struggle!

People don't want perfect. They want real!

Your mess. Your progress. Your story!

This is how you build a real audience!""",
        "filename": "06_building_public.mp4"
    },
    
    {
        "id": 7,
        "title": "Mediterranean Mindset - Living with Purpose",
        "topic": "mediterranean lifestyle philosophy culture",
        "script": """The Mediterranean way. Slow down to speed up!

Family. Food. Philosophy!

They don't rush life. They savor it!

Work to live. Don't live to work!

This ancient wisdom. Still true today!

Life isn't a race. It's a journey!""",
        "filename": "07_mediterranean_mindset.mp4"
    },
    
    {
        "id": 8,
        "title": "Artistic Vision - Staying True to Yourself",
        "topic": "artistic vision authentic creativity",
        "script": """Everyone has an opinion. About your art!

The trends. The algorithms. The pressure!

But here's what matters. Your vision!

Stay true. Stay authentic. Stay you!

The world doesn't need another copy. It needs the original you!

Your voice. That's what the world needs!""",
        "filename": "08_artistic_vision.mp4"
    },
    
    {
        "id": 9,
        "title": "Learning Music - It's Never Too Late",
        "topic": "music learning instruments education",
        "script": """Too old to learn music? Wrong!

Your brain at any age. It can learn!

The piano. The guitar. The voice!

Every master was once a beginner!

Start today. Start now!

Music isn't just for the young. It's for the brave!""",
        "filename": "09_learning_music.mp4"
    },
    
    {
        "id": 10,
        "title": "Content Creation - Quality Over Quantity",
        "topic": "content creation strategy quality",
        "script": """Post every day? That's not the answer!

One great video beats ten mediocre ones!

Quality. That's what builds a brand!

Take your time. Do it right!

The algorithm rewards consistency. But your audience rewards excellence!

Create less. Create better!""",
        "filename": "10_content_creation.mp4"
    }
]


def create_desktop_folder():
    """Create dated folder on Desktop for video batch"""
    desktop = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    folder_name = f"Personal_Brand_Videos_{timestamp}"
    output_folder = desktop / folder_name
    output_folder.mkdir(exist_ok=True)
    
    console.print(f"\n[bold green]📁 Created output folder:[/bold green]")
    console.print(f"[cyan]{output_folder}[/cyan]\n")
    
    return output_folder


def load_styles(limit=20):
    """Load first N style names from styles/index.json"""
    styles_dir = Path(__file__).resolve().parents[2] / "styles"
    index_path = styles_dir / "index.json"
    if not index_path.exists():
        return []
    try:
        with open(index_path, 'r') as f:
            names = json.load(f)
        return names[:limit]
    except Exception:
        return []


def create_batch_videos(total_videos=20, seed=None):
    """Create videos and organize them on Desktop (default 20 with styles)"""
    
    console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]🎬 BATCH VIDEO PRODUCTION - 10 PERSONAL BRAND VIDEOS[/bold cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
    
    # Create Desktop folder
    output_folder = create_desktop_folder()
    
    # Create manifest file
    manifest = output_folder / "VIDEO_MANIFEST.txt"
    
    with open(manifest, 'w') as f:
        f.write("PERSONAL BRAND VIDEO BATCH\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write("Styles used will be listed per video.\n\n")
    
    # Prepare styles
    style_names = load_styles(limit=total_videos)
    if len(style_names) < total_videos:
        console.print(f"[yellow]⚠️ Only {len(style_names)} styles available; proceeding with what we have.[/yellow]")
    # Shuffle style assignment for randomness
    rng = random.Random(seed)
    rng.shuffle(style_names)
    
    # Create each video
    for i in range(1, total_videos + 1):
        base = VIDEO_BATCH[(i - 1) % len(VIDEO_BATCH)]
        style_name = style_names[i - 1] if i - 1 < len(style_names) else None
        styled_filename = base['filename'].replace('.mp4', f"__{style_name}.mp4") if style_name else base['filename']
        title = f"{base['title']} [{style_name}]" if style_name else base['title']
        
        console.print(f"\n[bold yellow]{'='*60}[/bold yellow]")
        console.print(f"[bold yellow]VIDEO {i}/{total_videos}: {title}[/bold yellow]")
        console.print(f"[bold yellow]{'='*60}[/bold yellow]\n")
        
        # Update manifest
        with open(manifest, 'a') as f:
            f.write(f"VIDEO {i}: {title}\n")
            f.write(f"Topic: {base['topic']}\n")
            f.write(f"Style: {style_name}\n")
            f.write(f"Filename: {styled_filename}\n")
            f.write(f"Script:\n{base['script']}\n")
            f.write("-"*60 + "\n\n")
        
        try:
            # Create video
            console.print(f"[cyan]🎬 Creating video for: {title}[/cyan]\n")
            
            video_file = create_video_from_script(
                script_text=base['script'],
                topic=base['topic'],
                output_name=styled_filename,
                style_name=style_name,
                seed=seed,
                randomize=True
            )
            
            # Copy to Desktop folder
            source = Path("professional_videos") / styled_filename
            destination = output_folder / styled_filename
            
            if source.exists():
                shutil.copy(source, destination)
                console.print(f"\n[bold green]✅ VIDEO {i} COMPLETE![/bold green]")
                console.print(f"[green]📁 Saved to: {destination.name}[/green]\n")
            else:
                console.print(f"\n[red]⚠️  Video file not found: {source}[/red]\n")
            
        except Exception as e:
            console.print(f"\n[red]❌ Error creating video {i}: {str(e)}[/red]\n")
            with open(manifest, 'a') as f:
                f.write(f"ERROR: {str(e)}\n\n")
    
    # Final summary
    console.print("\n[bold green]" + "="*60 + "[/bold green]")
    console.print("[bold green]🎉 BATCH PRODUCTION COMPLETE![/bold green]")
    console.print("[bold green]" + "="*60 + "[/bold green]\n")
    
    console.print(f"[bold]📊 Summary:[/bold]")
    console.print(f"[green]  • Videos created: {total_videos}[/green]")
    console.print(f"[green]  • Location: {output_folder}[/green]")
    console.print(f"[green]  • Manifest: VIDEO_MANIFEST.txt[/green]\n")
    
    console.print(f"[cyan]📁 Opening folder...[/cyan]\n")
    os.system(f'open "{output_folder}"')
    
    return output_folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a batch of styled personal brand videos")
    parser.add_argument("--total", type=int, default=20, help="Number of videos to create")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    args = parser.parse_args()

    create_batch_videos(total_videos=args.total, seed=args.seed)
