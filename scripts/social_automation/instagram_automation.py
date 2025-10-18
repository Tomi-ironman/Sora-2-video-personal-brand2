#!/usr/bin/env python3
"""
Instagram Multi-Account Automation System
Monitors Instagram for audio/podcast creator content and engages with helpful responses
"""

import os
import time
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class InstagramAutomation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_hashtags()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all Instagram accounts"""
        self.accounts = {}
        
        # Get all available Instagram accounts from environment
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('INSTAGRAM') and key.endswith('_ACCESS_TOKEN'):
                if key == 'INSTAGRAM_ACCESS_TOKEN':
                    account_numbers.append('')
                else:
                    account_numbers.append(key.replace('INSTAGRAM', '').replace('_ACCESS_TOKEN', ''))
        
        print(f"🔍 Found {len(account_numbers)} Instagram accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account
                access_token = os.getenv(f'INSTAGRAM{suffix}_ACCESS_TOKEN')
                
                if access_token:
                    account_name = f"instagram{suffix}" if suffix else "instagram1"
                    
                    self.accounts[account_name] = {
                        'access_token': access_token,
                        'last_used': 0,
                        'requests_made': 0
                    }
                    
                    print(f"✅ {account_name}: Access token configured")
                    
            except Exception as e:
                print(f"❌ Failed to setup instagram{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization chaos and workflow overwhelm",
                "keywords": ["organize", "workflow", "files", "chaos", "productivity"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound designer workflow and search problems",
                "keywords": ["sounddesign", "audio", "samples", "creative", "workflow"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Audio professional burnout and workflow issues", 
                "keywords": ["audio", "professional", "studio", "mixing", "mastering"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast creation and management overwhelm",
                "keywords": ["podcast", "podcasting", "recording", "content", "creator"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each Instagram account"""
        self.personas = {
            "instagram1": {
                "role": "Audio Engineer",
                "tone": "Professional and inspiring",
                "style": "Love this! As an audio engineer, I've found that workflow optimization is everything. 🎧",
                "hashtags": ["#AudioEngineering", "#ProAudio", "#StudioLife"]
            },
            "instagram2": {
                "role": "Podcaster", 
                "tone": "Friendly and relatable",
                "style": "This hits home! Fellow podcaster here - organization has been a game-changer for my workflow ✨",
                "hashtags": ["#PodcastLife", "#ContentCreator", "#PodcastTips"]
            },
            "instagram3": {
                "role": "Sound Designer",
                "tone": "Creative and artistic", 
                "style": "So relatable! Sound designer life means constant organization challenges. Found some great solutions 🎵",
                "hashtags": ["#SoundDesign", "#AudioPost", "#CreativeWorkflow"]
            }
        }
        
    def setup_hashtags(self):
        """Hashtags to monitor for relevant content"""
        self.target_hashtags = [
            # Podcast hashtags
            "podcast", "podcasting", "podcastlife", "podcasttips", "podcastworkflow",
            "podcastproduction", "podcastrecording", "podcastedit",
            
            # Audio production hashtags  
            "audioproduction", "audioengineering", "proaudio", "studiolife",
            "mixing", "mastering", "audioworkflow", "studiotips",
            
            # Sound design hashtags
            "sounddesign", "audiopost", "sounddesigner", "sfx", "foley",
            "gameaudio", "filmaudio", "soundeffects",
            
            # Music production hashtags
            "musicproduction", "musicproducer", "beatmaker", "producer",
            "musicstudio", "dawlife", "samplepack", "beats",
            
            # Content creation hashtags
            "contentcreator", "creator", "creatorlife", "workflow",
            "productivity", "organization", "creative"
        ]
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (Instagram rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 600:  # Wait at least 10 minutes between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def search_hashtag_posts(self, hashtag):
        """Search for recent posts with specific hashtag"""
        # Note: Instagram Basic Display API has limited search capabilities
        # This is a framework - actual implementation would need Instagram Graph API
        # or third-party services for hashtag monitoring
        
        print(f"🔍 Monitoring #{hashtag} for relevant posts...")
        
        # Placeholder for actual Instagram API calls
        # In practice, you'd use Instagram Graph API or tools like:
        # - Instagram Basic Display API (limited)
        # - Third-party services (Hootsuite, Buffer APIs)
        # - Web scraping tools (with proper rate limiting)
        
        return []
        
    def analyze_post_context(self, caption, hashtags):
        """Use AI to analyze Instagram post and determine relevance"""
        combined_text = f"{caption} {' '.join(hashtags)}"
        
        prompt = f"""
        Analyze this Instagram post about audio/content creation and determine which category it best fits:
        
        Post Caption: "{caption[:200]}..."
        Hashtags: {hashtags[:10]}
        
        Categories:
        1. file_organization - Workflow, organization, productivity challenges
        2. sound_design - Sound design, audio effects, creative audio work
        3. audio_professional - Professional audio, mixing, mastering, studio work
        4. podcast_workflow - Podcast creation, recording, editing, content creation
        
        Return only the category name that best matches, or "none" if not relevant.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            return category if category in self.video_library else None
            
        except Exception as e:
            print(f"Error analyzing post: {e}")
            return None
            
    def generate_engaging_comment(self, caption, video_category, account_name):
        """Generate an engaging Instagram comment based on account persona"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['instagram1'])
        
        prompt = f"""
        Create an engaging Instagram comment for this post about audio/content creation.
        
        Post Caption: "{caption[:200]}..."
        Solution category: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        
        Requirements:
        - Be genuinely engaging and supportive (Instagram community style)
        - Use the persona's tone and expertise
        - Reference the specific post content
        - Mention having a helpful resource/video
        - Keep under 150 characters (Instagram optimal)
        - Include relevant emojis
        - Sound authentic and community-focused
        
        Format: "[Supportive comment] [Personal connection] [Resource offer] [Emoji]"
        
        Example: "{persona['style']} I have a video that covers this exact challenge - DM me if you'd like to see it! 💪"
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.7
            )
            
            comment = response.choices[0].message.content.strip()
            
            # Add hashtags if space allows
            hashtags = " ".join(persona['hashtags'][:2])
            if len(comment + " " + hashtags) <= 150:
                return f"{comment} {hashtags}"
            else:
                return comment
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"{persona['style']} I have a resource that might help with this! DM me 🎧"
            
    def log_intended_engagement(self, post_data, comment_text, account_name):
        """Log intended engagements for manual posting or API setup"""
        log_file = "instagram_intended_engagements.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    engagements = json.load(f)
            else:
                engagements = []
                
            engagements.append({
                'post_id': post_data.get('id', 'unknown'),
                'post_url': post_data.get('url', 'unknown'),
                'caption': post_data.get('caption', '')[:100] + '...',
                'comment_text': comment_text,
                'account_name': account_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            })
            
            with open(log_file, 'w') as f:
                json.dump(engagements, f, indent=2)
                
            print(f"📝 Logged intended engagement to {log_file}")
                
        except Exception as e:
            print(f"Error logging engagement: {e}")
            
    def run_monitoring_cycle(self):
        """Run one cycle of Instagram monitoring"""
        print(f"\n🔄 Starting Instagram monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        print(f"🎯 Target hashtags: {len(self.target_hashtags)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: {account['requests_made']} requests made")
        
        # Monitor a subset of hashtags each cycle
        hashtags_to_check = random.sample(self.target_hashtags, min(5, len(self.target_hashtags)))
        
        total_posts_found = 0
        engagements_planned = 0
        
        for hashtag in hashtags_to_check:
            posts = self.search_hashtag_posts(hashtag)
            total_posts_found += len(posts)
            
            for post in posts[:2]:  # Limit to 2 posts per hashtag
                # Analyze and potentially engage with post
                # (Implementation would depend on actual Instagram API integration)
                pass
                
        print(f"🎯 Found {total_posts_found} potentially relevant posts")
        print(f"📊 Planned {engagements_planned} engagements this cycle")
        
    def run_continuous_monitoring(self, check_interval=3600):  # 1 hour
        """Run continuous Instagram monitoring"""
        print("🚀 Starting Instagram Multi-Account Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎯 Target hashtags: {len(self.target_hashtags)}")
        print(f"⏰ Check interval: {check_interval/3600} hours")
        print("")
        print("📝 Note: This is a framework - requires Instagram API integration")
        print("🔧 Consider using Instagram Graph API or third-party tools")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/3600} hours...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Instagram monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(600)  # Wait 10 minutes before retrying

def main():
    """Run the Instagram automation"""
    print("📸 Instagram Automation Framework")
    print("Note: Requires Instagram API integration for full functionality")
    
    automation = InstagramAutomation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
