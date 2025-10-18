#!/usr/bin/env python3
"""
Twitter Video Comment Automation System
Monitors Twitter for audio/podcast pain points and responds with relevant Zenyai videos
"""

import tweepy
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwitterVideoResponder:
    def __init__(self):
        self.setup_apis()
        self.setup_video_library()
        self.setup_keywords()
        
    def setup_apis(self):
        """Initialize Twitter API and OpenAI"""
        # Twitter API credentials (add to .env file)
        self.twitter_api = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
            consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # OpenAI for context analysis
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
        
    def setup_keywords(self):
        """Keywords to monitor for relevant conversations"""
        self.monitor_keywords = [
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
        ]
        
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
            
    def generate_contextual_comment(self, tweet_text, video_category):
        """Generate a helpful, contextual comment for the tweet"""
        video_info = self.video_library[video_category]
        
        prompt = f"""
        Create a helpful, empathetic comment for this tweet about audio/podcast problems.
        
        Tweet: "{tweet_text}"
        Video solution: {video_info['description']}
        
        Requirements:
        - Be genuinely helpful and empathetic
        - Reference their specific problem
        - Mention that you've created something that might help
        - Keep it under 280 characters
        - Don't be overly salesy
        - Include relevant emojis
        - End with "Hope this helps! 🎧"
        
        Example tone: "I totally feel this pain! I actually created a short video showing how AI can help organize audio files automatically. Hope this helps! 🎧"
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
            return "I feel this pain! Created a video that might help with audio organization. Hope this helps! 🎧"
            
    def search_relevant_tweets(self):
        """Search for tweets mentioning our target keywords - EFFICIENT VERSION"""
        relevant_tweets = []
        
        # Combine keywords into fewer, broader searches to reduce API calls
        combined_queries = [
            "podcast file organization OR audio library mess OR episode organization",
            "sound design workflow OR audio search OR can't find samples", 
            "audio professional burnout OR mixing deadline OR mastering workflow",
            "podcast workflow chaos OR audio collaboration nightmare"
        ]
        
        for query in combined_queries:
            try:
                tweets = self.twitter_api.search_recent_tweets(
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
                            'query': query
                        })
                        
                time.sleep(5)  # Longer delay between searches
                
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                time.sleep(10)  # Wait longer on error
                
        return relevant_tweets
        
    def respond_to_tweet(self, tweet_data):
        """Analyze tweet and respond with appropriate video"""
        tweet_text = tweet_data['text']
        tweet_id = tweet_data['id']
        
        # Analyze context to determine best video
        video_category = self.analyze_tweet_context(tweet_text)
        
        if not video_category:
            print(f"No relevant video for tweet: {tweet_text[:50]}...")
            return False
            
        # Generate contextual comment
        comment = self.generate_contextual_comment(tweet_text, video_category)
        
        # Get video file path
        video_file = self.video_library[video_category]['file']
        video_path = os.path.expanduser(f"~/Desktop/AI-video-Generation/{video_file}")
        
        try:
            # Upload video and post comment
            media = self.twitter_api.media_upload(video_path)
            
            response = self.twitter_api.create_tweet(
                text=comment,
                in_reply_to_tweet_id=tweet_id,
                media_ids=[media.media_id]
            )
            
            print(f"✅ Responded to tweet {tweet_id} with {video_category} video")
            print(f"Comment: {comment}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error responding to tweet {tweet_id}: {e}")
            return False
            
    def run_monitoring_cycle(self):
        """Run one cycle of monitoring and responding"""
        print("🔍 Searching for relevant tweets...")
        
        tweets = self.search_relevant_tweets()
        print(f"Found {len(tweets)} potentially relevant tweets")
        
        responses_sent = 0
        
        for tweet in tweets:
            # Check if we've already responded to this tweet
            if self.already_responded(tweet['id']):
                continue
                
            # Respond with appropriate video
            if self.respond_to_tweet(tweet):
                responses_sent += 1
                self.log_response(tweet['id'])
                
                # Rate limiting - wait between responses
                time.sleep(60)  # Wait 1 minute between responses
                
        print(f"📊 Sent {responses_sent} video responses this cycle")
        
    def already_responded(self, tweet_id):
        """Check if we've already responded to this tweet"""
        # Simple file-based tracking (could use database)
        log_file = "responded_tweets.json"
        
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
        log_file = "responded_tweets.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    responded = json.load(f)
            else:
                responded = {}
                
            responded[str(tweet_id)] = datetime.now().isoformat()
            
            with open(log_file, 'w') as f:
                json.dump(responded, f)
                
        except Exception as e:
            print(f"Error logging response: {e}")
            
    def run_continuous_monitoring(self, check_interval=900):  # 15 minutes instead of 5
        """Run continuous monitoring (check every 5 minutes by default)"""
        print("🚀 Starting continuous Twitter monitoring...")
        print(f"📊 Monitoring {len(self.monitor_keywords)} keywords")
        print(f"🎬 {len(self.video_library)} videos ready to deploy")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"😴 Sleeping for {check_interval} seconds...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Run the Twitter video responder"""
    print("🐦 Zenyai Twitter Video Response System")
    print("=" * 50)
    
    # Initialize responder
    responder = TwitterVideoResponder()
    
    # Run continuous monitoring
    responder.run_continuous_monitoring()

if __name__ == "__main__":
    main()
