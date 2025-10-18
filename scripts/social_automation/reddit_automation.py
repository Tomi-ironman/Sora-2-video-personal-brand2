#!/usr/bin/env python3
"""
Reddit Multi-Account Automation System
Monitors Reddit for audio/podcast pain points and responds with helpful Zenyai videos
"""

import praw
import os
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedditAutomation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_subreddits()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all Reddit accounts"""
        self.accounts = {}
        
        # Get all available Reddit accounts from environment
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('REDDIT') and key.endswith('_CLIENT_ID'):
                if key == 'REDDIT_CLIENT_ID':
                    account_numbers.append('')
                else:
                    account_numbers.append(key.replace('REDDIT', '').replace('_CLIENT_ID', ''))
        
        print(f"🔍 Found {len(account_numbers)} Reddit accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account
                client_id = os.getenv(f'REDDIT{suffix}_CLIENT_ID')
                client_secret = os.getenv(f'REDDIT{suffix}_CLIENT_SECRET')
                username = os.getenv(f'REDDIT{suffix}_USERNAME')
                password = os.getenv(f'REDDIT{suffix}_PASSWORD')
                user_agent = os.getenv(f'REDDIT{suffix}_USER_AGENT', 'ZenyaiAudioHelper/1.0')
                
                if all([client_id, client_secret, username, password]):
                    # Initialize Reddit client
                    reddit = praw.Reddit(
                        client_id=client_id,
                        client_secret=client_secret,
                        username=username,
                        password=password,
                        user_agent=user_agent
                    )
                    
                    # Test connection
                    reddit.user.me()
                    
                    account_name = f"reddit{suffix}" if suffix else "reddit1"
                    
                    self.accounts[account_name] = {
                        'client': reddit,
                        'username': username,
                        'last_used': 0,
                        'requests_made': 0
                    }
                    
                    print(f"✅ {account_name}: u/{username}")
                    
            except Exception as e:
                print(f"❌ Failed to setup reddit{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization chaos and workflow overwhelm",
                "keywords": ["file", "organize", "chaos", "mess", "folders", "library"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound designer workflow and search problems",
                "keywords": ["sound design", "audio search", "samples", "effects", "library"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Audio professional burnout and workflow issues", 
                "keywords": ["audio professional", "burnout", "deadline", "mixing", "mastering"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast creation and management overwhelm",
                "keywords": ["podcast", "episode", "workflow", "team", "collaboration"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each Reddit account"""
        self.personas = {
            "reddit1": {
                "role": "Experienced Audio Engineer",
                "tone": "Professional and helpful",
                "style": "I've been working in audio for 10+ years and ran into this exact issue. Here's what finally solved it for me:",
                "credibility": "Years of studio experience"
            },
            "reddit2": {
                "role": "Indie Podcaster", 
                "tone": "Friendly and relatable",
                "style": "Fellow podcaster here! I struggled with this for months until I found this approach:",
                "credibility": "Running a successful indie podcast"
            },
            "reddit3": {
                "role": "Sound Designer",
                "tone": "Creative and technical", 
                "style": "Sound designer checking in - this used to be my biggest workflow killer. Game changer:",
                "credibility": "Working on film/game audio"
            },
            "reddit4": {
                "role": "Music Producer",
                "tone": "Industry-focused",
                "style": "Producer perspective: organization is literally everything in this business. This saved my workflow:",
                "credibility": "Producing for indie artists"
            },
            "reddit5": {
                "role": "Audio Student/Enthusiast",
                "tone": "Eager and learning",
                "style": "Audio student here! Just learned about this solution and it's been a lifesaver:",
                "credibility": "Learning audio production"
            }
        }
        
    def setup_subreddits(self):
        """Target subreddits for audio creators"""
        self.target_subreddits = {
            # Podcast Communities
            "podcasting": ["podcast", "episode", "recording", "editing", "workflow"],
            "podcasts": ["show", "production", "audio", "editing"],
            "PodcastGuestExchange": ["guest", "interview", "recording"],
            
            # Music Production
            "WeAreTheMusicMakers": ["production", "mixing", "mastering", "workflow"],
            "edmproduction": ["samples", "organization", "workflow", "files"],
            "trapproduction": ["samples", "beats", "organization"],
            "makinghiphop": ["beats", "samples", "workflow"],
            "FL_Studio": ["project", "files", "organization"],
            "ableton": ["project", "samples", "organization"],
            
            # Audio Engineering
            "audioengineering": ["mixing", "mastering", "workflow", "organization"],
            "audio": ["professional", "workflow", "files"],
            "livesound": ["workflow", "organization"],
            
            # Content Creation
            "NewTubers": ["audio", "editing", "workflow"],
            "youtubers": ["editing", "audio", "workflow"],
            "streaming": ["audio", "setup", "workflow"],
            
            # Sound Design
            "WeAreTheGameMakers": ["audio", "sound", "assets"],
            "gamedev": ["audio", "sound", "assets"]
        }
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (Reddit rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 300:  # Wait at least 5 minutes between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def search_relevant_posts(self):
        """Search for relevant posts across target subreddits"""
        relevant_posts = []
        
        for subreddit_name, keywords in self.target_subreddits.items():
            # Get account for searching
            account_name, account = self.get_next_account()
            
            try:
                print(f"🔍 Searching r/{subreddit_name} with {account_name}...")
                
                subreddit = account['client'].subreddit(subreddit_name)
                
                # Search recent posts (last 24 hours)
                for post in subreddit.new(limit=20):
                    post_age_hours = (time.time() - post.created_utc) / 3600
                    
                    if post_age_hours > 24:  # Skip posts older than 24 hours
                        continue
                        
                    # Check if post contains relevant keywords
                    post_text = (post.title + " " + post.selftext).lower()
                    
                    for keyword in keywords:
                        if keyword in post_text and any([
                            "help" in post_text,
                            "problem" in post_text,
                            "issue" in post_text,
                            "struggle" in post_text,
                            "difficult" in post_text,
                            "how to" in post_text,
                            "?" in post.title
                        ]):
                            relevant_posts.append({
                                'id': post.id,
                                'title': post.title,
                                'text': post.selftext,
                                'subreddit': subreddit_name,
                                'author': str(post.author),
                                'url': post.url,
                                'score': post.score,
                                'num_comments': post.num_comments,
                                'created_utc': post.created_utc,
                                'found_by': account_name,
                                'keyword': keyword
                            })
                            break
                
                account['last_used'] = time.time()
                account['requests_made'] += 1
                
                time.sleep(10)  # Wait between subreddit searches
                
            except Exception as e:
                print(f"❌ Error searching r/{subreddit_name}: {e}")
                time.sleep(30)
                
        return relevant_posts
        
    def analyze_post_context(self, post_title, post_text):
        """Use AI to analyze post and determine best video match"""
        combined_text = f"{post_title} {post_text}"
        
        prompt = f"""
        Analyze this Reddit post about audio/podcast problems and determine which category it best fits:
        
        Post: "{combined_text[:500]}..."
        
        Categories:
        1. file_organization - File management, organization chaos, lost files, project management
        2. sound_design - Sound designer workflow, sample searching, audio effects, sound libraries
        3. audio_professional - Audio professional burnout, mixing/mastering issues, deadlines
        4. podcast_workflow - Podcast creation, episode management, team collaboration, recording
        
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
            
    def generate_helpful_comment(self, post_title, post_text, video_category, account_name):
        """Generate a helpful Reddit comment based on account persona"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['reddit1'])
        
        prompt = f"""
        Create a helpful Reddit comment for this post about audio/podcast problems.
        
        Post Title: "{post_title}"
        Post Content: "{post_text[:300]}..."
        Video solution: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        Credibility: {persona['credibility']}
        
        Requirements:
        - Be genuinely helpful and detailed (Reddit users expect quality)
        - Use the persona's tone and credibility
        - Reference their specific problem
        - Mention sharing a helpful video resource
        - Keep under 500 characters
        - Sound like a real Reddit user, not promotional
        - Add value beyond just the video
        
        Format: "[Persona intro] [Specific advice] [Video mention] [Additional tip]"
        
        Example: "{persona['style']} [specific solution]. I actually created a short video showing the exact workflow - happy to share if it helps! Also, pro tip: [additional advice]"
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"{persona['style']} I created a video that walks through this exact solution - happy to share if it would help! This approach has saved me countless hours."
            
    def respond_to_post(self, post_data):
        """Analyze post and respond with helpful comment + video"""
        post_title = post_data['title']
        post_text = post_data['text']
        post_id = post_data['id']
        
        # Analyze context to determine best video
        video_category = self.analyze_post_context(post_title, post_text)
        
        if not video_category:
            print(f"No relevant video for post: {post_title[:50]}...")
            return False
            
        # Get account for responding
        account_name, account = self.get_next_account()
        
        # Generate helpful comment
        comment_text = self.generate_helpful_comment(post_title, post_text, video_category, account_name)
        
        try:
            print(f"💬 Responding to r/{post_data['subreddit']} with {account_name}...")
            
            # Get the submission object
            submission = account['client'].submission(id=post_id)
            
            # Post comment
            comment = submission.reply(comment_text)
            
            print(f"✅ Comment posted! Comment ID: {comment.id}")
            print(f"💬 Comment: {comment_text[:100]}...")
            
            account['last_used'] = time.time()
            account['requests_made'] += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error responding to post: {e}")
            return False
            
    def run_monitoring_cycle(self):
        """Run one cycle of Reddit monitoring and responding"""
        print(f"\n🔄 Starting Reddit monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        print(f"🎯 Target subreddits: {len(self.target_subreddits)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: u/{account['username']} (requests: {account['requests_made']})")
        
        posts = self.search_relevant_posts()
        print(f"🎯 Found {len(posts)} potentially relevant posts")
        
        responses_sent = 0
        
        for post in posts:
            # Check if we've already responded to this post
            if self.already_responded(post['id']):
                continue
                
            # Add random delay to look natural
            delay = random.randint(120, 300)  # 2-5 minutes
            print(f"⏳ Waiting {delay//60} minutes before responding...")
            time.sleep(delay)
            
            # Respond with helpful comment
            if self.respond_to_post(post):
                responses_sent += 1
                self.log_response(post['id'])
                
                # Limit responses per cycle
                if responses_sent >= 2:
                    print("🛑 Reached response limit for this cycle")
                    break
                    
        print(f"📊 Sent {responses_sent} helpful responses this cycle")
        
    def already_responded(self, post_id):
        """Check if we've already responded to this post"""
        log_file = "reddit_responses.json"
        
        if not os.path.exists(log_file):
            return False
            
        try:
            with open(log_file, 'r') as f:
                responded = json.load(f)
                return str(post_id) in responded
        except:
            return False
            
    def log_response(self, post_id):
        """Log that we've responded to this post"""
        log_file = "reddit_responses.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    responded = json.load(f)
            else:
                responded = {}
                
            responded[str(post_id)] = {
                'timestamp': datetime.now().isoformat(),
                'accounts_used': len(self.accounts)
            }
            
            with open(log_file, 'w') as f:
                json.dump(responded, f, indent=2)
                
        except Exception as e:
            print(f"Error logging response: {e}")
            
    def run_continuous_monitoring(self, check_interval=3600):  # 1 hour
        """Run continuous Reddit monitoring"""
        print("🚀 Starting Reddit Multi-Account Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎯 Subreddits: {len(self.target_subreddits)}")
        print(f"⏰ Check interval: {check_interval/60} minutes")
        print(f"🎬 Max responses per cycle: 2")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/60} minutes...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Reddit monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(600)  # Wait 10 minutes before retrying

def main():
    """Run the Reddit automation"""
    automation = RedditAutomation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
