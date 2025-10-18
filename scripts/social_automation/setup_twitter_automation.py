#!/usr/bin/env python3
"""
Setup script for Twitter Video Response Automation
Helps configure API keys and test the system
"""

import os
import json

def setup_environment():
    """Guide user through setting up environment variables"""
    print("🔧 Twitter API Setup Guide")
    print("=" * 40)
    
    print("\n1. Get Twitter API Credentials:")
    print("   • Go to https://developer.twitter.com/")
    print("   • Create a new app")
    print("   • Generate API keys")
    
    print("\n2. Add these to your .env file:")
    
    env_template = """
# Twitter API Credentials
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_CONSUMER_KEY=your_consumer_key_here
TWITTER_CONSUMER_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here

# OpenAI API (for context analysis)
OPENAI_API_KEY=your_openai_key_here
"""
    
    print(env_template)
    
    # Check if .env exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found existing {env_file} file")
    else:
        print(f"❌ No {env_file} file found - please create one with the above template")
        
def test_video_library():
    """Check if our video files exist"""
    print("\n🎬 Checking Video Library...")
    
    video_files = [
        "podcast_file_wave_commercial.mp4",
        "sound_designer_commercial.mp4", 
        "audio_professional_commercial.mp4",
        "podcast_avalanche_commercial.mp4"
    ]
    
    video_dir = os.path.expanduser("~/Desktop/AI-video-Generation/")
    
    for video in video_files:
        video_path = os.path.join(video_dir, video)
        if os.path.exists(video_path):
            print(f"✅ Found: {video}")
        else:
            print(f"❌ Missing: {video}")
            
def create_monitoring_config():
    """Create configuration file for monitoring"""
    config = {
        "monitoring": {
            "check_interval": 300,  # 5 minutes
            "max_responses_per_cycle": 5,
            "rate_limit_delay": 30
        },
        "keywords": [
            "podcast file organization",
            "audio library mess", 
            "sound design workflow",
            "too many audio files",
            "can't find samples",
            "audio asset management",
            "podcast workflow chaos",
            "drowning in files",
            "audio professional burnout",
            "sound designer struggle",
            "episode organization",
            "audio collaboration nightmare"
        ],
        "response_templates": {
            "empathetic": "I totally feel this pain! ",
            "helpful": "Created a video that might help with this exact problem. ",
            "closing": "Hope this helps! 🎧"
        }
    }
    
    with open("twitter_config.json", "w") as f:
        json.dump(config, f, indent=2)
        
    print("✅ Created twitter_config.json")

def install_requirements():
    """Show required packages"""
    print("\n📦 Required Packages:")
    
    requirements = [
        "tweepy>=4.14.0",
        "openai>=0.28.0", 
        "python-dotenv>=1.0.0"
    ]
    
    print("Run: pip install " + " ".join(requirements))
    
    # Update requirements.txt
    with open("requirements.txt", "a") as f:
        f.write("\n# Twitter Automation\n")
        for req in requirements:
            f.write(f"{req}\n")
            
    print("✅ Added to requirements.txt")

def main():
    """Run setup process"""
    print("🚀 Zenyai Twitter Automation Setup")
    print("=" * 50)
    
    setup_environment()
    test_video_library()
    create_monitoring_config()
    install_requirements()
    
    print("\n🎯 Next Steps:")
    print("1. Fill in your .env file with API credentials")
    print("2. Run: pip install -r requirements.txt")
    print("3. Test with: python twitter_video_responder.py")
    print("4. Monitor logs for successful responses")
    
    print("\n🔥 Your Twitter automation is ready!")
    print("The system will:")
    print("• Monitor Twitter for audio/podcast pain points")
    print("• Analyze context with AI")
    print("• Respond with relevant Zenyai videos")
    print("• Track responses to avoid duplicates")

if __name__ == "__main__":
    main()
