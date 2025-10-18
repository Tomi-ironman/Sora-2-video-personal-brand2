#!/usr/bin/env python3
"""
Project Organization Script
Reorganizes all files into a clean, logical folder structure
"""

import os
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

# Define the new folder structure
FOLDER_STRUCTURE = {
    "docs": {
        "setup_guides": [],
        "summaries": [],
        "research": [],
        "api_docs": [],
    },
    "data": {
        "audio_industry": [],
        "market_research": [],
        "investor_data": [],
        "social_intelligence": [],
    },
    "scripts": {
        "video_creation": [],
        "voice_cloning": [],
        "social_automation": [],
        "market_intelligence": [],
        "test_scripts": [],
    },
    "outputs": {
        "videos": [],
        "voices": [],
        "images": [],
    },
    "config": [],
    "archive": {
        "old_scripts": [],
        "deprecated": [],
    }
}

# File categorization rules
FILE_CATEGORIES = {
    # Documentation
    "docs/setup_guides": [
        "*_SETUP*.md", "*_GUIDE*.md", "START_HERE.md", "QUICK_START*.md",
        "GET_API_KEYS.md", "EMAIL_SETUP_GUIDE.md", "api_setup_guide.md"
    ],
    "docs/summaries": [
        "*_SUMMARY.md", "*_STATUS.md", "SYSTEM_STATUS.md", "CULTURE_VIDEO_STATUS.md",
        "DEVELOPMENT_SUMMARY.md", "FINAL_PLATFORM_SUMMARY.md"
    ],
    "docs/research": [
        "*_RESEARCH.md", "MIRAGE_LIPSYNC_RESEARCH.md", "AUDIO_INTELLIGENCE*.md",
        "SOCIAL_INTELLIGENCE*.md", "COMPETITOR_TRACKER*.md", "*_INTELLIGENCE*.md"
    ],
    "docs/api_docs": [
        "CHATTERBOX*.md", "COLAB_LIPSYNC.md", "FREE_LIPSYNC_GUIDE.md",
        "FREE_MEDIA*.md", "ILLUSTRATION_GIF_SEARCH_GUIDE.md"
    ],
    
    # Data files
    "data/audio_industry": [
        "audio_industry_intelligence*.json", "audio_professional*.py"
    ],
    "data/market_research": [
        "*market_research*.json", "comprehensive_market_analysis.json",
        "creative_metadata_research*.json", "latest_comprehensive_analysis.json"
    ],
    "data/investor_data": [
        "*investor*.json", "*investor*.py", "angel_investors_data.py",
        "affiliate_partners_database.py", "complete_60_investors.json"
    ],
    "data/social_intelligence": [
        "financial_intelligence*.json", "market_intelligence_videos*.json",
        "producthunt_zenyai_comments.json", "twitter_*.json", "youtube_*.json",
        "product_hunt_*.json", "bulletproof_twitter_log.json", "one_by_one_twitter_log.json"
    ],
    
    # Video creation scripts
    "scripts/video_creation": [
        "create_*_video.py", "generate_*_video.py", "auto_video_generator.py",
        "hybrid_video_generator.py", "video_topics_batch.py", "create_video_*.py",
        "step1_generate_voice.py", "step2_create_video.py", "add_captions*.py",
        "add_visual_sound_effects.py", "add_smart_sound_effects.py", "add_word_by_word_captions.py",
        "market_intelligence_video_generator.py", "viral_marketing_generator.py"
    ],
    
    # Voice cloning
    "scripts/voice_cloning": [
        "voice_*.py", "clone_my_voice.py", "cultural_voices*.py",
        "step1_generate_voice.py"
    ],
    
    # Social automation
    "scripts/social_automation": [
        "twitter_*.py", "instagram_*.py", "youtube_*.py", "reddit_*.py",
        "product_hunt_*.py", "multi_platform_automation.py", "multi_account_twitter_automation.py",
        "setup_*_automation.py"
    ],
    
    # Market intelligence
    "scripts/market_intelligence": [
        "*_intelligence*.py", "competitor_intelligence.py", "market_monitor_alerts.py",
        "social_intelligence_*.py", "zenyai_market_intelligence.py", "market_intelligence_web*.py",
        "*_scraper.py", "bulk_company_processor.py", "g2_automation.py"
    ],
    
    # Test scripts
    "scripts/test_scripts": [
        "test_*.py", "platform_test.py", "inspect_*.py"
    ],
    
    # Config files
    "config": [
        ".env*", "requirements*.txt", "*.json", "api_key_manager.py",
        "email_config.py", "error_handler.py", "performance_optimizer.py",
        "setup_*.sh"
    ],
    
    # Output directories
    "outputs/videos": [
        "professional_videos", "generated_videos", "simple_videos", "wav2lip_videos",
        "talking_videos", "test_output"
    ],
    "outputs/voices": [
        "narrations", "voice_samples"
    ],
    "outputs/images": [
        "pinterest_downloads", "pinterest_images", "pinterest_gifs", "B-roll"
    ],
    
    # Archive old/deprecated
    "archive/old_scripts": [
        "simple_apartment_video.py", "text_to_video_apartment.py",
        "download_12sec_video.py", "fix_indentation.py", "resize_and_generate.py"
    ],
    "archive/deprecated": [
        "*_broken.py", "*_old.py", "market_intelligence_web_broken.py"
    ]
}


def create_folder_structure(base_path):
    """Create the new folder structure"""
    console.print("\n[bold cyan]📁 Creating folder structure...[/bold cyan]\n")
    
    def create_nested_folders(path, structure):
        for folder, subfolders in structure.items():
            folder_path = path / folder
            folder_path.mkdir(exist_ok=True)
            console.print(f"[green]  ✓ {folder}/[/green]")
            
            if isinstance(subfolders, dict):
                create_nested_folders(folder_path, subfolders)
    
    create_nested_folders(base_path, FOLDER_STRUCTURE)


def move_files(base_path):
    """Move files according to categorization rules"""
    console.print("\n[bold cyan]📦 Organizing files...[/bold cyan]\n")
    
    moved_count = 0
    
    for category, patterns in FILE_CATEGORIES.items():
        target_dir = base_path / category
        
        for pattern in patterns:
            # Handle directory patterns
            if not pattern.endswith('.py') and not pattern.endswith('.json') and not pattern.endswith('.md'):
                matching = list(base_path.glob(pattern))
                for item in matching:
                    if item.is_dir() and item.name not in ['docs', 'data', 'scripts', 'outputs', 'config', 'archive']:
                        try:
                            dest = target_dir / item.name
                            if not dest.exists():
                                shutil.move(str(item), str(dest))
                                console.print(f"[dim]  → {item.name}/ → {category}/[/dim]")
                                moved_count += 1
                        except Exception as e:
                            console.print(f"[yellow]  ⚠ Could not move {item.name}: {e}[/yellow]")
            else:
                # Handle file patterns
                matching = list(base_path.glob(pattern))
                for file in matching:
                    if file.is_file():
                        try:
                            dest = target_dir / file.name
                            if not dest.exists() and file.parent == base_path:
                                shutil.copy(str(file), str(dest))
                                file.unlink()  # Remove original
                                console.print(f"[dim]  → {file.name} → {category}/[/dim]")
                                moved_count += 1
                        except Exception as e:
                            console.print(f"[yellow]  ⚠ Could not move {file.name}: {e}[/yellow]")
    
    console.print(f"\n[green]✅ Moved {moved_count} files[/green]")


def create_index_files(base_path):
    """Create README files for each major directory"""
    console.print("\n[bold cyan]📝 Creating index files...[/bold cyan]\n")
    
    indexes = {
        "docs/README.md": """# Documentation

## Setup Guides
All setup and installation guides for the project.

## Summaries
Project status updates and summaries.

## Research
Market research, competitor analysis, and technical research.

## API Docs
Third-party API integration documentation.
""",
        "data/README.md": """# Data Storage

## Audio Industry
Audio industry intelligence and research data.

## Market Research
Market analysis and research results.

## Investor Data
Angel investors and affiliate partner databases.

## Social Intelligence
Social media analytics and engagement data.
""",
        "scripts/README.md": """# Scripts

## Video Creation
All video generation and editing scripts.

## Voice Cloning
Voice generation and cloning utilities.

## Social Automation
Social media automation tools (Twitter, Instagram, YouTube, etc.).

## Market Intelligence
Market research and competitor tracking automation.

## Test Scripts
Testing and debugging scripts.
""",
        "outputs/README.md": """# Outputs

## Videos
All generated video files.

## Voices
Generated voice files and narrations.

## Images
Downloaded images, Pinterest content, and B-roll.
""",
    }
    
    for path, content in indexes.items():
        readme_path = base_path / path
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        with open(readme_path, 'w') as f:
            f.write(content)
        console.print(f"[green]  ✓ {path}[/green]")


def generate_organization_report(base_path):
    """Generate a report of the new organization"""
    console.print("\n[bold cyan]📊 Generating organization report...[/bold cyan]\n")
    
    from datetime import datetime
    
    report_path = base_path / "PROJECT_ORGANIZATION.md"
    
    report = """# Project Organization

**Date:** {date}
**Status:** ✅ Organized

## Folder Structure

```
Sora-2-video-personal-brand2/
├── docs/                    # All documentation
│   ├── setup_guides/        # Setup and installation guides
│   ├── summaries/           # Status updates and summaries
│   ├── research/            # Research and analysis
│   └── api_docs/            # API documentation
│
├── data/                    # All data files
│   ├── audio_industry/      # Audio industry data
│   ├── market_research/     # Market research results
│   ├── investor_data/       # Investor databases
│   └── social_intelligence/ # Social media data
│
├── scripts/                 # All executable scripts
│   ├── video_creation/      # Video generation scripts
│   ├── voice_cloning/       # Voice cloning utilities
│   ├── social_automation/   # Social media automation
│   ├── market_intelligence/ # Market research automation
│   └── test_scripts/        # Testing scripts
│
├── outputs/                 # Generated outputs
│   ├── videos/              # Video files
│   ├── voices/              # Voice files
│   └── images/              # Image files
│
├── config/                  # Configuration files
│   ├── .env files
│   ├── requirements.txt
│   └── setup scripts
│
├── archive/                 # Deprecated files
│   ├── old_scripts/
│   └── deprecated/
│
├── frontend/                # Web interface (unchanged)
├── chatterbox/             # Chatterbox integration (unchanged)
├── Tomi/                   # Personal videos (unchanged)
└── Reference Character/    # Character references (unchanged)
```

## Quick Access

### Most Used Scripts
- **Create Video:** `scripts/video_creation/create_video_master.py`
- **Batch Videos:** `scripts/video_creation/video_topics_batch.py`
- **Clone Voice:** `scripts/voice_cloning/clone_my_voice.py`

### Documentation
- **Start Here:** `docs/setup_guides/START_HERE.md`
- **Quick Start:** `docs/setup_guides/QUICK_START.md`
- **API Keys:** `docs/setup_guides/GET_API_KEYS.md`

### Data
- **Market Research:** `data/market_research/`
- **Audio Industry:** `data/audio_industry/`

## Notes
- Personal videos remain in `Tomi/` folder
- Frontend and chatterbox folders unchanged
- All test scripts moved to `scripts/test_scripts/`
- Configuration files in `config/`
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    console.print(f"[green]✅ Report saved: PROJECT_ORGANIZATION.md[/green]")


def main():
    base_path = Path(__file__).parent
    
    console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]🗂️  PROJECT ORGANIZATION SYSTEM[/bold cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]")
    
    console.print("\n[yellow]⚠️  Note: Video generation will continue uninterrupted[/yellow]")
    
    # Create structure
    create_folder_structure(base_path)
    
    # Move files
    move_files(base_path)
    
    # Create index files
    create_index_files(base_path)
    
    # Generate report
    generate_organization_report(base_path)
    
    console.print("\n[bold green]" + "="*60 + "[/bold green]")
    console.print("[bold green]✅ PROJECT ORGANIZATION COMPLETE![/bold green]")
    console.print("[bold green]" + "="*60 + "[/bold green]\n")
    
    console.print("[cyan]📁 New structure created with:[/cyan]")
    console.print("[cyan]   • docs/ - All documentation organized[/cyan]")
    console.print("[cyan]   • data/ - All data files categorized[/cyan]")
    console.print("[cyan]   • scripts/ - All scripts by function[/cyan]")
    console.print("[cyan]   • outputs/ - All generated content[/cyan]")
    console.print("[cyan]   • config/ - All configuration files[/cyan]")
    console.print("[cyan]   • archive/ - Old/deprecated files[/cyan]\n")


if __name__ == "__main__":
    main()
