#!/usr/bin/env python3
"""
YouTube Multi-Account Comment Automation System
Monitors YouTube for audio/podcast creator videos and responds with helpful Zenyai content
"""

import os
import time
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

class YouTubeAutomation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_search_terms()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all YouTube accounts"""
        self.accounts = {}
        
        # Get all available YouTube accounts from environment
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('YOUTUBE') and key.endswith('_API_KEY'):
                if key == 'YOUTUBE_API_KEY':
                    account_numbers.append('')
                else:
                    account_numbers.append(key.replace('YOUTUBE', '').replace('_API_KEY', ''))
        
        print(f"🔍 Found {len(account_numbers)} YouTube accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account
                api_key = os.getenv(f'YOUTUBE{suffix}_API_KEY')
                
                if api_key:
                    # Initialize YouTube client
                    youtube = build('youtube', 'v3', developerKey=api_key)
                    
                    account_name = f"youtube{suffix}" if suffix else "youtube1"
                    
                    self.accounts[account_name] = {
                        'client': youtube,
                        'api_key': api_key,
                        'last_used': 0,
                        'requests_made': 0
                    }
                    
                    print(f"✅ {account_name}: API key configured")
                    
            except Exception as e:
                print(f"❌ Failed to setup youtube{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization chaos and workflow overwhelm",
                "keywords": ["file", "organize", "chaos", "mess", "folders", "library", "workflow"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound designer workflow and search problems",
                "keywords": ["sound design", "audio search", "samples", "effects", "library", "sfx"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Audio professional burnout and workflow issues", 
                "keywords": ["audio professional", "burnout", "deadline", "mixing", "mastering", "studio"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast creation and management overwhelm",
                "keywords": ["podcast", "episode", "workflow", "team", "collaboration", "recording"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each YouTube account"""
        self.personas = {
            "youtube1": {
                "role": "Audio Engineer",
                "tone": "Professional and technical",
                "style": "Great tutorial! As an audio engineer, I've found this workflow approach really helpful:",
                "expertise": "10+ years in professional audio"
            },
            "youtube2": {
                "role": "Podcaster", 
                "tone": "Friendly and supportive",
                "style": "Fellow podcaster here! This resonates so much - I struggled with this exact issue until I found:",
                "expertise": "Running successful indie podcast"
            },
            "youtube3": {
                "role": "Sound Designer",
                "tone": "Creative and collaborative", 
                "style": "Sound designer checking in! This workflow challenge used to kill my creativity until I discovered:",
                "expertise": "Film/game audio professional"
            }
        }
        
    def setup_search_terms(self):
        """Search terms to find relevant YouTube videos"""
        self.search_terms = [
            # Podcast Creation
            "podcast workflow tutorial",
            "podcast file organization",
            "podcast editing workflow",
            "podcast production tips",
            "how to organize podcast files",
            
            # Audio Production
            "audio production workflow",
            "mixing and mastering tutorial", 
            "audio file management",
            "studio workflow organization",
            "audio professional tips",
            
            # Sound Design
            "sound design workflow",
            "sound effects organization",
            "audio library management",
            "sound designer tips",
            "audio asset management",
            
            # Music Production
            "music production workflow",
            "sample library organization",
            "DAW project management",
            "music producer tips",
            "beat making workflow"
        ]
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (YouTube rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 300:  # Wait at least 5 minutes between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def search_relevant_videos(self):
        """Search for relevant YouTube videos"""
        relevant_videos = []
        
        for search_term in self.search_terms[:5]:  # Limit to 5 searches per cycle
            # Get account for searching
            account_name, account = self.get_next_account()
            
            try:
                print(f"🔍 Searching YouTube with {account_name}: '{search_term}'...")
                
                # Search for videos
                search_response = account['client'].search().list(
                    q=search_term,
                    part='id,snippet',
                    type='video',
                    maxResults=10,
                    publishedAfter=(datetime.now() - timedelta(days=7)).isoformat() + 'Z',  # Last 7 days
                    order='relevance'
                ).execute()
                
                for item in search_response['items']:
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    channel_title = item['snippet']['channelTitle']
                    published_at = item['snippet']['publishedAt']
                    
                    # Check if video is relevant (has pain point indicators)
                    combined_text = f"{title} {description}".lower()
                    
                    if any(indicator in combined_text for indicator in [
                        'help', 'problem', 'issue', 'struggle', 'difficult', 
                        'how to', 'tutorial', 'tips', 'workflow', 'organize'
                    ]):
                        relevant_videos.append({
                            'video_id': video_id,
                            'title': title,
                            'description': description,
                            'channel_title': channel_title,
                            'published_at': published_at,
                            'search_term': search_term,
                            'found_by': account_name
                        })
                
                account['last_used'] = time.time()
                account['requests_made'] += 1
                
                time.sleep(10)  # Wait between searches
                
            except HttpError as e:
                print(f"❌ YouTube API error: {e}")
                time.sleep(30)
            except Exception as e:
                print(f"❌ Error searching YouTube: {e}")
                time.sleep(30)
                
        return relevant_videos
        
    def analyze_video_context(self, title, description):
        """Use AI to analyze video and determine best response category"""
        combined_text = f"{title} {description}"
        
        prompt = f"""
        Analyze this YouTube video about audio/podcast creation and determine which category it best fits:
        
        Video Title: "{title}"
        Description: "{description[:300]}..."
        
        Categories:
        1. file_organization - File management, organization, workflow optimization
        2. sound_design - Sound design, audio effects, sample management
        3. audio_professional - Professional audio, mixing, mastering, studio work
        4. podcast_workflow - Podcast creation, recording, editing, production
        
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
            print(f"Error analyzing video: {e}")
            return None
            
    def generate_helpful_comment(self, title, description, video_category, account_name):
        """Generate a helpful YouTube comment based on account persona"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['youtube1'])
        
        prompt = f"""
        Create a helpful YouTube comment for this video about audio/podcast creation.
        
        Video Title: "{title}"
        Video Description: "{description[:200]}..."
        Solution category: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        Expertise: {persona['expertise']}
        
        Requirements:
        - Be genuinely helpful and supportive (YouTube community style)
        - Use the persona's expertise and tone
        - Reference the specific video content
        - Mention having a helpful resource/video to share
        - Keep under 300 characters
        - Sound encouraging and collaborative
        - Use YouTube-appropriate language
        
        Format: "[Supportive comment about video] [Personal experience] [Offer to share helpful resource] [Encouraging closing]"
        
        Example: "{persona['style']} [specific solution]. I actually have a short video that walks through this exact workflow - happy to share if it would help! Keep up the great content! 🎧"
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"{persona['style']} I have a video resource that covers this exact workflow challenge - happy to share if it would help! Great content! 🎧"
            
    def comment_on_video(self, video_data):
        """Comment on a YouTube video (Note: Requires OAuth for actual commenting)"""
        title = video_data['title']
        description = video_data['description']
        video_id = video_data['video_id']
        
        # Analyze context to determine best response
        video_category = self.analyze_video_context(title, description)
        
        if not video_category:
            print(f"No relevant category for video: {title[:50]}...")
            return False
            
        # Get account for commenting
        account_name, account = self.get_next_account()
        
        # Generate helpful comment
        comment_text = self.generate_helpful_comment(title, description, video_category, account_name)
        
        print(f"💬 Would comment on '{title[:50]}...' with {account_name}:")
        print(f"   Comment: {comment_text}")
        print(f"   Video: https://youtube.com/watch?v={video_id}")
        
        # Note: Actual commenting requires OAuth authentication
        # For now, we'll log the intended comments
        self.log_intended_comment(video_id, comment_text, account_name)
        
        return True
        
    def log_intended_comment(self, video_id, comment_text, account_name):
        """Log intended comments for manual posting or OAuth setup"""
        log_file = "youtube_intended_comments.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    comments = json.load(f)
            else:
                comments = []
                
            comments.append({
                'video_id': video_id,
                'video_url': f'https://youtube.com/watch?v={video_id}',
                'comment_text': comment_text,
                'account_name': account_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            })
            
            with open(log_file, 'w') as f:
                json.dump(comments, f, indent=2)
                
            print(f"📝 Logged intended comment to {log_file}")
                
        except Exception as e:
            print(f"Error logging comment: {e}")
            
    def run_monitoring_cycle(self):
        """Run one cycle of YouTube monitoring"""
        print(f"\n🔄 Starting YouTube monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        print(f"🎯 Search terms: {len(self.search_terms)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: {account['requests_made']} requests made")
        
        videos = self.search_relevant_videos()
        print(f"🎯 Found {len(videos)} potentially relevant videos")
        
        comments_planned = 0
        
        for video in videos[:3]:  # Limit to 3 comments per cycle
            # Add random delay to look natural
            delay = random.randint(60, 180)  # 1-3 minutes
            print(f"⏳ Waiting {delay//60} minutes before commenting...")
            time.sleep(delay)
            
            # Plan comment on video
            if self.comment_on_video(video):
                comments_planned += 1
                
        print(f"📊 Planned {comments_planned} helpful comments this cycle")
        
    def run_continuous_monitoring(self, check_interval=7200):  # 2 hours
        """Run continuous YouTube monitoring"""
        print("🚀 Starting YouTube Multi-Account Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎯 Search terms: {len(self.search_terms)}")
        print(f"⏰ Check interval: {check_interval/3600} hours")
        print(f"🎬 Max comments per cycle: 3")
        print("")
        print("📝 Note: Comments are logged for manual posting until OAuth is set up")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/3600} hours...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 YouTube monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(600)  # Wait 10 minutes before retrying

def main():
    """Run the YouTube automation"""
    automation = YouTubeAutomation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
