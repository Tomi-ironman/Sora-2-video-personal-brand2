#!/usr/bin/env python3
"""
Setup script for YouTube Multi-Account Automation
Helps configure YouTube API keys and explains the system
"""

import os
import json

def setup_youtube_environment():
    """Guide user through setting up YouTube API credentials"""
    print("🔧 YouTube API Setup Guide")
    print("=" * 40)
    
    print("\n1. Get YouTube API Keys:")
    print("   • Go to: https://console.developers.google.com/")
    print("   • Create a new project or select existing")
    print("   • Enable 'YouTube Data API v3'")
    print("   • Go to 'Credentials' → 'Create Credentials' → 'API Key'")
    print("   • Copy the API key")
    print("   • Repeat for multiple Google accounts (3 recommended)")
    
    print("\n2. Add these to your .env file:")
    
    env_template = """
# YouTube Account 1
YOUTUBE_API_KEY=your_youtube_api_key_here

# YouTube Account 2  
YOUTUBE2_API_KEY=your_youtube_api_key_here

# YouTube Account 3
YOUTUBE3_API_KEY=your_youtube_api_key_here
"""
    
    print(env_template)
    
def show_youtube_strategy():
    """Explain the YouTube automation strategy"""
    print("\n🚀 YouTube Automation Strategy:")
    print("=" * 40)
    
    print("\n🎯 **How It Works:**")
    print("1. **Search for relevant videos** about audio/podcast creation")
    print("2. **Target recent uploads** (last 7 days) for maximum visibility")
    print("3. **AI analyzes video content** to match appropriate responses")
    print("4. **Generate helpful comments** with persona-based expertise")
    print("5. **Log intended comments** for manual posting (initially)")
    
    print("\n🔍 **Target Video Types:**")
    print("• **Podcast workflow tutorials**")
    print("• **Audio production guides**") 
    print("• **Sound design workflows**")
    print("• **Music production tips**")
    print("• **Studio organization videos**")
    
    print("\n💬 **Comment Strategy:**")
    print("• **Genuinely helpful** - add real value to the conversation")
    print("• **Persona-based** - different expertise for each account")
    print("• **Offer resources** - mention having helpful videos to share")
    print("• **Community-focused** - supportive YouTube creator tone")
    
    print("\n📊 **Expected Impact:**")
    print("• **50+ relevant videos per day** across all search terms")
    print("• **10-15 helpful comments per day** from different personas")
    print("• **Thousands of creators** seeing Zenyai mentioned helpfully")
    print("• **Long-term visibility** - comments stay visible for months")

def show_target_searches():
    """Show which search terms we'll use"""
    print("\n🎯 Target Search Terms:")
    
    search_categories = {
        "Podcast Creation": [
            "podcast workflow tutorial",
            "podcast file organization", 
            "podcast editing workflow",
            "podcast production tips"
        ],
        "Audio Production": [
            "audio production workflow",
            "mixing and mastering tutorial",
            "audio file management",
            "studio workflow organization"
        ],
        "Sound Design": [
            "sound design workflow",
            "sound effects organization",
            "audio library management",
            "sound designer tips"
        ],
        "Music Production": [
            "music production workflow",
            "sample library organization",
            "DAW project management",
            "beat making workflow"
        ]
    }
    
    for category, terms in search_categories.items():
        print(f"\n**{category}:**")
        for term in terms:
            print(f"   • \"{term}\"")

def create_youtube_config():
    """Create configuration file for YouTube monitoring"""
    config = {
        "monitoring": {
            "check_interval": 7200,  # 2 hours
            "max_comments_per_cycle": 3,
            "delay_between_comments": 120,  # 2 minutes
            "video_age_limit_days": 7
        },
        "personas": {
            "youtube1": "Audio Engineer - Professional & Technical",
            "youtube2": "Podcaster - Friendly & Supportive", 
            "youtube3": "Sound Designer - Creative & Collaborative"
        },
        "comment_strategy": {
            "max_comment_length": 300,
            "include_expertise": True,
            "offer_resources": True,
            "supportive_tone": True
        }
    }
    
    with open("youtube_config.json", "w") as f:
        json.dump(config, f, indent=2)
        
    print("✅ Created youtube_config.json")

def install_youtube_requirements():
    """Show required packages for YouTube automation"""
    print("\n📦 Required Packages:")
    
    requirements = [
        "google-api-python-client>=2.0.0",
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=0.5.0",
        "openai>=0.28.0", 
        "python-dotenv>=1.0.0"
    ]
    
    print("Run: pip install " + " ".join(requirements))
    
    # Update requirements.txt
    with open("requirements.txt", "a") as f:
        f.write("\n# YouTube Automation\n")
        for req in requirements:
            f.write(f"{req}\n")
            
    print("✅ Added to requirements.txt")

def explain_oauth_setup():
    """Explain OAuth setup for actual commenting"""
    print("\n🔐 OAuth Setup (For Actual Commenting):")
    print("=" * 40)
    
    print("\n**Phase 1: Search & Analysis (API Key Only)**")
    print("• ✅ Search for relevant videos")
    print("• ✅ Analyze video content with AI") 
    print("• ✅ Generate helpful comments")
    print("• ✅ Log intended comments for manual posting")
    
    print("\n**Phase 2: Automated Commenting (OAuth Required)**")
    print("• 🔐 Requires OAuth 2.0 setup for each account")
    print("• 🔐 Need to create OAuth credentials in Google Console")
    print("• 🔐 Users must authorize the application")
    print("• 🔐 More complex but enables full automation")
    
    print("\n**Recommendation: Start with Phase 1**")
    print("• Get the system finding and analyzing videos")
    print("• Review the quality of generated comments")
    print("• Manually post the best comments initially")
    print("• Set up OAuth later for full automation")

def main():
    """Run YouTube setup process"""
    print("🚀 YouTube Multi-Account Automation Setup")
    print("=" * 50)
    
    setup_youtube_environment()
    show_youtube_strategy()
    show_target_searches()
    create_youtube_config()
    install_youtube_requirements()
    explain_oauth_setup()
    
    print("\n🎯 Next Steps:")
    print("1. Create 3 Google accounts for YouTube API access")
    print("2. Get API keys for each account")
    print("3. Fill in your .env file with YouTube API keys")
    print("4. Run: pip install google-api-python-client")
    print("5. Test with: python youtube_automation.py")
    
    print("\n🔥 Multi-Platform Domination Strategy:")
    print("✅ **Twitter:** 4 accounts actively responding (LIVE)")
    print("🎬 **YouTube:** 3 accounts finding videos to comment on")
    print("📸 **Instagram:** Next platform to build")
    print("🎵 **TikTok:** Future expansion")
    
    print("\n🎯 **Total Market Coverage:**")
    print("With Twitter + YouTube, you'll reach creators across:")
    print("• Real-time conversations (Twitter)")
    print("• Educational content (YouTube)")
    print("• = Complete audio creator ecosystem domination!")

if __name__ == "__main__":
    main()
