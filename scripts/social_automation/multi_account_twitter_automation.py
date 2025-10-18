#!/usr/bin/env python3
"""
Multi-Account Twitter Video Response Automation System
Coordinates multiple Twitter accounts for maximum market reach and impact
"""

import tweepy
import os
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MultiAccountTwitterAutomation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_keywords()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all Twitter accounts"""
        self.accounts = {}
        
        # Get all available accounts from environment
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('TWITTER') and key.endswith('_CONSUMER_KEY'):
                if key == 'TWITTER_CONSUMER_KEY':
                    account_numbers.append('')
                else:
                    account_numbers.append(key.replace('TWITTER', '').replace('_CONSUMER_KEY', ''))
        
        print(f"🔍 Found {len(account_numbers)} Twitter accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account
                bearer_token = os.getenv(f'TWITTER{suffix}_BEARER_TOKEN')
                consumer_key = os.getenv(f'TWITTER{suffix}_CONSUMER_KEY')
                consumer_secret = os.getenv(f'TWITTER{suffix}_CONSUMER_SECRET')
                access_token = os.getenv(f'TWITTER{suffix}_ACCESS_TOKEN')
                access_token_secret = os.getenv(f'TWITTER{suffix}_ACCESS_TOKEN_SECRET')
                
                if all([bearer_token, consumer_key, consumer_secret, access_token, access_token_secret]):
                    # Initialize Twitter client
                    client = tweepy.Client(
                        bearer_token=bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True
                    )
                    
                    # Get account info
                    me = client.get_me()
                    account_name = f"account{suffix}" if suffix else "account1"
                    
                    self.accounts[account_name] = {
                        'client': client,
                        'username': me.data.username,
                        'user_id': me.data.id,
                        'last_used': 0,
                        'requests_made': 0
                    }
                    
                    print(f"✅ {account_name}: @{me.data.username}")
                    
            except Exception as e:
                print(f"❌ Failed to setup account{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",  # File Wave commercial
                "description": "File organization chaos and workflow overwhelm",
                "keywords": ["file", "organize", "chaos", "mess", "folders", "library"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",  # Sound Designer commercial
                "description": "Sound designer workflow and search problems",
                "keywords": ["sound design", "audio search", "samples", "effects", "library"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",  # Audio Professional commercial
                "description": "Audio professional burnout and workflow issues", 
                "keywords": ["audio professional", "burnout", "deadline", "mixing", "mastering"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",  # Avalanche commercial
                "description": "Podcast creation and management overwhelm",
                "keywords": ["podcast", "episode", "workflow", "team", "collaboration"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each account"""
        self.personas = {
            "account1": {
                "role": "Audio Engineer",
                "tone": "Professional and technical",
                "style": "I've been working in audio for years and found this approach really helpful:",
                "hashtags": ["#AudioEngineering", "#ProAudio", "#WorkflowTips"]
            },
            "account2": {
                "role": "Podcaster", 
                "tone": "Friendly and relatable",
                "style": "As a fellow podcaster, I totally get this struggle! Here's what saved me:",
                "hashtags": ["#PodcastLife", "#CreatorTips", "#PodcastWorkflow"]
            },
            "account3": {
                "role": "Sound Designer",
                "tone": "Creative and artistic", 
                "style": "Sound designer here! This exact problem used to drive me crazy until I found:",
                "hashtags": ["#SoundDesign", "#AudioPost", "#CreativeWorkflow"]
            },
            "account4": {
                "role": "Music Producer",
                "tone": "Industry-focused",
                "style": "Producer perspective: organization is everything in this business. This helped me:",
                "hashtags": ["#MusicProduction", "#StudioLife", "#ProducerTips"]
            }
        }
        
    def setup_keywords(self):
        """Keywords to monitor for relevant conversations"""
        self.combined_queries = [
            "podcast file organization OR audio library mess OR episode organization",
            "sound design workflow OR audio search OR can't find samples", 
            "audio professional burnout OR mixing deadline OR mastering workflow",
            "podcast workflow chaos OR audio collaboration nightmare"
        ]
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (basic rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 60:  # Wait at least 1 minute between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def search_relevant_tweets(self):
        """Search for tweets using different accounts"""
        relevant_tweets = []
        
        for query in self.combined_queries:
            # Get account for searching
            account_name, account = self.get_next_account()
            
            try:
                print(f"🔍 Searching with {account_name} (@{account['username']}): {query[:50]}...")
                
                tweets = account['client'].search_recent_tweets(
                    query=f'({query}) -is:retweet -is:reply',
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'public_metrics']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        relevant_tweets.append({
                            'id': tweet.id,
                            'text': tweet.text,
                            'author_id': tweet.author_id,
                            'created_at': tweet.created_at,
                            'query': query,
                            'found_by': account_name
                        })
                        
                account['last_used'] = time.time()
                account['requests_made'] += 1
                
                time.sleep(10)  # Wait between searches
                
            except Exception as e:
                print(f"❌ Error searching with {account_name}: {e}")
                time.sleep(30)  # Wait longer on error
                
        return relevant_tweets
        
    def analyze_tweet_context(self, tweet_text):
        """Use AI to analyze tweet and determine best video match"""
        prompt = f"""
        Analyze this tweet about audio/podcast problems and determine which category it best fits:
        
        Tweet: "{tweet_text}"
        
        Categories:
        1. file_organization - File management, organization chaos, lost files
        2. sound_design - Sound designer workflow, sample searching, audio effects
        3. audio_professional - Audio professional burnout, mixing/mastering issues
        4. podcast_workflow - Podcast creation, episode management, team collaboration
        
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
            print(f"Error analyzing tweet: {e}")
            return None
            
    def generate_contextual_comment(self, tweet_text, video_category, account_name):
        """Generate a contextual comment based on account persona"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['account1'])
        
        prompt = f"""
        Create a helpful comment for this tweet about audio/podcast problems.
        
        Tweet: "{tweet_text}"
        Video solution: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        
        Requirements:
        - Be genuinely helpful and empathetic
        - Use the persona's tone and style
        - Reference their specific problem
        - Mention sharing a helpful video
        - Keep under 250 characters (leave room for hashtags)
        - Don't be overly salesy
        
        Example: "{persona['style']} [solution]. Sharing a quick video that shows exactly how to fix this! 🎧"
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            comment = response.choices[0].message.content.strip()
            
            # Add relevant hashtags
            hashtags = " ".join(persona['hashtags'][:2])  # Use first 2 hashtags
            
            # Ensure total length is under 280 characters
            if len(comment + " " + hashtags) <= 280:
                return f"{comment} {hashtags}"
            else:
                return comment
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"I feel this pain! Created a video that might help with this exact problem. Hope this helps! 🎧 {persona['hashtags'][0]}"
            
    def respond_to_tweet(self, tweet_data):
        """Analyze tweet and respond with appropriate video using best account"""
        tweet_text = tweet_data['text']
        tweet_id = tweet_data['id']
        
        # Analyze context to determine best video
        video_category = self.analyze_tweet_context(tweet_text)
        
        if not video_category:
            print(f"No relevant video for tweet: {tweet_text[:50]}...")
            return False
            
        # Get account for responding (different from search account if possible)
        account_name, account = self.get_next_account()
        
        # Generate contextual comment based on account persona
        comment = self.generate_contextual_comment(tweet_text, video_category, account_name)
        
        # Get video file path
        video_file = self.video_library[video_category]['file']
        video_path = os.path.expanduser(f"~/Desktop/AI-video-Generation/{video_file}")
        
        try:
            print(f"📤 Responding with {account_name} (@{account['username']})...")
            
            # Get the suffix for this account
            suffix = account_name.replace('account', '')
            if suffix == '1':
                suffix = ''
            
            # Create API v1.1 client for media upload
            import tweepy
            auth = tweepy.OAuth1UserHandler(
                os.getenv(f'TWITTER{suffix}_CONSUMER_KEY'),
                os.getenv(f'TWITTER{suffix}_CONSUMER_SECRET'),
                os.getenv(f'TWITTER{suffix}_ACCESS_TOKEN'),
                os.getenv(f'TWITTER{suffix}_ACCESS_TOKEN_SECRET')
            )
            api_v1 = tweepy.API(auth)
            
            # Upload video using v1.1 API
            media = api_v1.media_upload(video_path)
            
            # Post tweet with video using v2 API
            response = account['client'].create_tweet(
                text=comment,
                in_reply_to_tweet_id=tweet_id,
                media_ids=[media.media_id]
            )
            
            print(f"✅ Response sent! Tweet ID: {response.data['id']}")
            print(f"💬 Comment: {comment}")
            
            account['last_used'] = time.time()
            account['requests_made'] += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error responding with {account_name}: {e}")
            return False
            
    def run_monitoring_cycle(self):
        """Run one cycle of monitoring and responding"""
        print(f"\n🔄 Starting monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: @{account['username']} (requests: {account['requests_made']})")
        
        tweets = self.search_relevant_tweets()
        print(f"🎯 Found {len(tweets)} potentially relevant tweets")
        
        responses_sent = 0
        
        for tweet in tweets:
            # Check if we've already responded to this tweet
            if self.already_responded(tweet['id']):
                continue
                
            # Add random delay to look more natural
            delay = random.randint(30, 120)  # 30 seconds to 2 minutes
            print(f"⏳ Waiting {delay} seconds before responding...")
            time.sleep(delay)
            
            # Respond with appropriate video
            if self.respond_to_tweet(tweet):
                responses_sent += 1
                self.log_response(tweet['id'])
                
                # Limit responses per cycle to avoid looking spammy
                if responses_sent >= 3:
                    print("🛑 Reached response limit for this cycle")
                    break
                    
        print(f"📊 Sent {responses_sent} video responses this cycle")
        
    def already_responded(self, tweet_id):
        """Check if we've already responded to this tweet"""
        log_file = "multi_account_responses.json"
        
        if not os.path.exists(log_file):
            return False
            
        try:
            with open(log_file, 'r') as f:
                responded = json.load(f)
                return str(tweet_id) in responded
        except:
            return False
            
    def log_response(self, tweet_id):
        """Log that we've responded to this tweet"""
        log_file = "multi_account_responses.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    responded = json.load(f)
            else:
                responded = {}
                
            responded[str(tweet_id)] = {
                'timestamp': datetime.now().isoformat(),
                'accounts_used': len(self.accounts)
            }
            
            with open(log_file, 'w') as f:
                json.dump(responded, f, indent=2)
                
        except Exception as e:
            print(f"Error logging response: {e}")
            
    def run_continuous_monitoring(self, check_interval=1800):  # 30 minutes
        """Run continuous monitoring with multiple accounts"""
        print("🚀 Starting Multi-Account Twitter Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎬 Videos: {len(self.video_library)}")
        print(f"⏰ Check interval: {check_interval/60} minutes")
        print(f"🎯 Max responses per cycle: 3")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/60} minutes...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Multi-account monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

def main():
    """Run the multi-account Twitter automation"""
    automation = MultiAccountTwitterAutomation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
