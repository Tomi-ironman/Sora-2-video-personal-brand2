#!/usr/bin/env python3
"""
Final cleanup - move remaining files to appropriate folders
"""

import shutil
from pathlib import Path
from rich.console import Console

console = Console()

# Remaining files to organize
REMAINING_FILES = {
    # Documentation
    "docs/summaries": [
        "ANGEL_INVESTORS_README.md",
        "COMPLETE_INVESTOR_DATABASE_180.md",
        "COST_OPTIMIZATION_UPDATE.md",
        "INTEGRATION_COMPLETE.md",
        "INVESTOR_DATABASE_120.md",
        "YOUR_VOICE_READY.md",
        "ZENYAI_CREATIVE_BRIEF.md",
        "TWITTER_MEMORY_ENHANCEMENT.md",
        "twitter_permissions_upgrade.md",
    ],
    "docs/setup_guides": [
        "QUICK_REFERENCE.md",
        "PROJECT_ORGANIZATION.md",
    ],
    
    # Scripts that were missed
    "scripts/video_creation": [
        "make_video_quick.py",
        "generate_culture_voice.py",
        "create_zenyai_intro.py",
        "create_japanese_v2_faster.py",
        "create_japanese_video_now.py",
        "create_japanese_video_simple.py",
        "fantasy_cutaways.py",
        "podcast_avalanche_commercial.py",
        "podcast_drowning_commercial.py",
        "podcast_file_wave_commercial.py",
        "sound_designer_commercial.py",
    ],
    
    "scripts/social_automation": [
        "generate_authentic_comments.py",
        "add_outreach_messages.py",
        "find_email_login.py",
        "setup_multi_account_twitter.py",
    ],
    
    "scripts/market_intelligence": [
        "free_sources_research.py",
        "advanced_data_sources.py",
        "creative_metadata_research.py",
        "comprehensive_market_analyzer.py",
        "multi_source_research.py",
        "rate_limit_friendly_research.py",
        "real_market_research.py",
        "real_time_competitor_monitor.py",
        "smart_market_research.py",
        "affiliate_partnerships_batch1.py",
    ],
    
    "scripts/video_providers": [
        "sora2_direct_api.py",
        "sora2_multi_key_api.py",
        "sora_generator.py",
        "veo3_generator.py",
        "veo_generator.py",
    ],
    
    "scripts/media_downloads": [
        "download_background_music.py",
        "download_illustration_gifs.py",
        "download_pinterest_images.py",
        "pinterest_gif_downloader.py",
        "mixed_media_downloader.py",
    ],
    
    # Config files
    "config": [
        "requirements.txt",
        "requirements_social.txt",
        "research_cache.pkl",
        "setup_python311.sh",
        "setup_sadtalker.sh",
        "setup_voice_complete.sh",
        "voice_generation.log",
        "video1_id.txt",
        "video2_id.txt",
        "video3_id.txt",
        "video_15sec_id.txt",
    ],
    
    # Archive
    "archive/prompts": [
        "BLACK_HOLE_VIDEO_PROMPT.txt",
    ],
}

def cleanup_remaining_files():
    base_path = Path(__file__).parent
    
    console.print("\n[bold cyan]🧹 Final Cleanup - Moving Remaining Files[/bold cyan]\n")
    
    moved = 0
    
    for target_dir, files in REMAINING_FILES.items():
        target_path = base_path / target_dir
        target_path.mkdir(parents=True, exist_ok=True)
        
        for file_name in files:
            source = base_path / file_name
            if source.exists() and source.is_file():
                try:
                    dest = target_path / file_name
                    shutil.move(str(source), str(dest))
                    console.print(f"[green]✓ {file_name} → {target_dir}/[/green]")
                    moved += 1
                except Exception as e:
                    console.print(f"[yellow]⚠ {file_name}: {e}[/yellow]")
    
    console.print(f"\n[bold green]✅ Moved {moved} files[/bold green]\n")
    
    # Show final root structure
    console.print("[bold cyan]📁 Final Root Directory:[/bold cyan]\n")
    items = sorted([x.name for x in base_path.iterdir() if not x.name.startswith('.')])
    for item in items[:20]:  # Show first 20
        console.print(f"[dim]  • {item}[/dim]")
    if len(items) > 20:
        console.print(f"[dim]  ... and {len(items)-20} more[/dim]")

if __name__ == "__main__":
    cleanup_remaining_files()
