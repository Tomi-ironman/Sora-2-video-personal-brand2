#!/usr/bin/env python3
"""
Setup script for Reddit Multi-Account Automation
Helps configure Reddit API keys and test the system
"""

import os
import json

def setup_reddit_environment():
    """Guide user through setting up Reddit API credentials"""
    print("🔧 Reddit API Setup Guide")
    print("=" * 40)
    
    print("\n1. Create Reddit Apps:")
    print("   • Go to https://www.reddit.com/prefs/apps")
    print("   • Click 'Create App' or 'Create Another App'")
    print("   • Fill out:")
    print("     - Name: 'Zenyai Audio Helper'")
    print("     - App type: 'script'") 
    print("     - Description: 'MIT research project studying audio creator workflows'")
    print("     - Redirect URI: http://localhost:8080")
    print("   • Click 'Create app'")
    print("   • Repeat for each Reddit account (5 total)")
    
    print("\n2. Add these to your .env file:")
    
    env_template = """
# Reddit Account 1
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=ZenyaiAudioHelper/1.0

# Reddit Account 2
REDDIT2_CLIENT_ID=your_client_id_here
REDDIT2_CLIENT_SECRET=your_client_secret_here
REDDIT2_USERNAME=your_reddit_username
REDDIT2_PASSWORD=your_reddit_password
REDDIT2_USER_AGENT=ZenyaiAudioHelper/1.0

# Reddit Account 3
REDDIT3_CLIENT_ID=your_client_id_here
REDDIT3_CLIENT_SECRET=your_client_secret_here
REDDIT3_USERNAME=your_reddit_username
REDDIT3_PASSWORD=your_reddit_password
REDDIT3_USER_AGENT=ZenyaiAudioHelper/1.0

# Reddit Account 4
REDDIT4_CLIENT_ID=your_client_id_here
REDDIT4_CLIENT_SECRET=your_client_secret_here
REDDIT4_USERNAME=your_reddit_username
REDDIT4_PASSWORD=your_reddit_password
REDDIT4_USER_AGENT=ZenyaiAudioHelper/1.0

# Reddit Account 5
REDDIT5_CLIENT_ID=your_client_id_here
REDDIT5_CLIENT_SECRET=your_client_secret_here
REDDIT5_USERNAME=your_reddit_username
REDDIT5_PASSWORD=your_reddit_password
REDDIT5_USER_AGENT=ZenyaiAudioHelper/1.0
"""
    
    print(env_template)
    
def show_target_subreddits():
    """Show which subreddits we'll target"""
    print("\n🎯 Target Subreddits:")
    
    subreddits = {
        "Podcast Communities": [
            "r/podcasting", "r/podcasts", "r/PodcastGuestExchange"
        ],
        "Music Production": [
            "r/WeAreTheMusicMakers", "r/edmproduction", "r/trapproduction", 
            "r/makinghiphop", "r/FL_Studio", "r/ableton"
        ],
        "Audio Engineering": [
            "r/audioengineering", "r/audio", "r/livesound"
        ],
        "Content Creation": [
            "r/NewTubers", "r/youtubers", "r/streaming"
        ],
        "Sound Design": [
            "r/WeAreTheGameMakers", "r/gamedev"
        ]
    }
    
    for category, subs in subreddits.items():
        print(f"\n**{category}:**")
        for sub in subs:
            print(f"   • {sub}")

def create_reddit_config():
    """Create configuration file for Reddit monitoring"""
    config = {
        "monitoring": {
            "check_interval": 3600,  # 1 hour
            "max_responses_per_cycle": 2,
            "delay_between_responses": 300  # 5 minutes
        },
        "personas": {
            "reddit1": "Experienced Audio Engineer",
            "reddit2": "Indie Podcaster", 
            "reddit3": "Sound Designer",
            "reddit4": "Music Producer",
            "reddit5": "Audio Student/Enthusiast"
        },
        "response_strategy": {
            "min_post_age_hours": 1,
            "max_post_age_hours": 24,
            "min_upvotes": 1,
            "avoid_controversial": True
        }
    }
    
    with open("reddit_config.json", "w") as f:
        json.dump(config, f, indent=2)
        
    print("✅ Created reddit_config.json")

def install_reddit_requirements():
    """Show required packages for Reddit automation"""
    print("\n📦 Required Packages:")
    
    requirements = [
        "praw>=7.7.0",  # Python Reddit API Wrapper
        "openai>=0.28.0", 
        "python-dotenv>=1.0.0"
    ]
    
    print("Run: pip install " + " ".join(requirements))
    
    # Update requirements.txt
    with open("requirements.txt", "a") as f:
        f.write("\n# Reddit Automation\n")
        for req in requirements:
            f.write(f"{req}\n")
            
    print("✅ Added to requirements.txt")

def show_reddit_strategy():
    """Explain the Reddit automation strategy"""
    print("\n🚀 Reddit Automation Strategy:")
    print("=" * 40)
    
    print("\n🎯 **How It Works:**")
    print("1. **Monitor 15+ audio creator subreddits** for pain point posts")
    print("2. **5 different account personas** respond naturally")
    print("3. **AI analyzes posts** to match appropriate videos")
    print("4. **Helpful comments** that provide real value + video resources")
    print("5. **1-hour cycles** with max 2 responses per cycle")
    
    print("\n🔥 **Why Reddit is PERFECT:**")
    print("• **Active help-seeking** - people literally asking for solutions")
    print("• **High-quality discussions** - detailed problems and solutions")
    print("• **Massive reach** - millions of creators across subreddits")
    print("• **Long-term visibility** - comments stay visible for months")
    print("• **Community trust** - helpful responses build credibility")
    
    print("\n📊 **Expected Impact:**")
    print("• **50+ relevant posts per day** across all subreddits")
    print("• **10-20 helpful responses per day** from different personas")
    print("• **Thousands of creators** seeing Zenyai solutions")
    print("• **Organic community building** around your content")

def main():
    """Run Reddit setup process"""
    print("🚀 Reddit Multi-Account Automation Setup")
    print("=" * 50)
    
    setup_reddit_environment()
    show_target_subreddits()
    create_reddit_config()
    install_reddit_requirements()
    show_reddit_strategy()
    
    print("\n🎯 Next Steps:")
    print("1. Create 5 Reddit accounts with different usernames")
    print("2. Get API credentials for each account")
    print("3. Fill in your .env file with Reddit credentials")
    print("4. Run: pip install praw")
    print("5. Test with: python reddit_automation.py")
    
    print("\n🔥 Reddit + Twitter = TOTAL MARKET DOMINATION!")
    print("You'll be helping creators across EVERY major platform!")

if __name__ == "__main__":
    main()
