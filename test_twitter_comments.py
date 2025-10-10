#!/usr/bin/env python3
"""
Test Twitter Comment/Reply Functionality
Verify we can post comments and replies on Twitter
"""

import tweepy
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TwitterCommentTester:
    def __init__(self):
        self.setup_twitter_api()
        
    def setup_twitter_api(self):
        """Initialize Twitter API with all credentials"""
        try:
            # Use v1.1 API for media upload and v2 for tweets
            self.twitter_api_v2 = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # v1.1 API for media upload
            auth = tweepy.OAuth1UserHandler(
                os.getenv('TWITTER_CONSUMER_KEY'),
                os.getenv('TWITTER_CONSUMER_SECRET'),
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            
            print("✅ Twitter API initialized successfully")
            
        except Exception as e:
            print(f"❌ Twitter API setup failed: {e}")
            
    def test_basic_tweet(self):
        """Test posting a basic tweet"""
        try:
            test_tweet = f"🧪 Testing Twitter API functionality - {datetime.now().strftime('%H:%M:%S')}"
            
            response = self.twitter_api_v2.create_tweet(text=test_tweet)
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✅ Basic tweet posted successfully!")
                print(f"   Tweet ID: {tweet_id}")
                print(f"   Content: {test_tweet}")
                return tweet_id
            else:
                print("❌ Failed to post basic tweet")
                return None
                
        except Exception as e:
            print(f"❌ Error posting basic tweet: {e}")
            return None
            
    def test_reply_to_tweet(self, tweet_id):
        """Test replying to a specific tweet"""
        try:
            reply_text = f"🤖 This is a test reply from Zenyai automation system! Time: {datetime.now().strftime('%H:%M:%S')}"
            
            response = self.twitter_api_v2.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            
            if response.data:
                reply_id = response.data['id']
                print(f"✅ Reply posted successfully!")
                print(f"   Reply ID: {reply_id}")
                print(f"   Content: {reply_text}")
                return reply_id
            else:
                print("❌ Failed to post reply")
                return None
                
        except Exception as e:
            print(f"❌ Error posting reply: {e}")
            return None
            
    def test_tweet_with_media(self):
        """Test posting tweet with media (if video exists)"""
        try:
            # Look for any video file in the expected directory
            video_dir = os.path.expanduser("~/Desktop/AI-video-Generation/")
            
            if not os.path.exists(video_dir):
                print("⚠️ Video directory not found - skipping media test")
                return None
                
            # Find first .mp4 file
            video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
            
            if not video_files:
                print("⚠️ No video files found - skipping media test")
                return None
                
            video_path = os.path.join(video_dir, video_files[0])
            print(f"📹 Testing with video: {video_files[0]}")
            
            # Upload media using v1.1 API
            media = self.twitter_api_v1.media_upload(video_path)
            
            # Post tweet with media using v2 API
            tweet_text = f"🎬 Testing video upload functionality - {datetime.now().strftime('%H:%M:%S')}"
            
            response = self.twitter_api_v2.create_tweet(
                text=tweet_text,
                media_ids=[media.media_id]
            )
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✅ Video tweet posted successfully!")
                print(f"   Tweet ID: {tweet_id}")
                print(f"   Video: {video_files[0]}")
                return tweet_id
            else:
                print("❌ Failed to post video tweet")
                return None
                
        except Exception as e:
            print(f"❌ Error posting video tweet: {e}")
            return None
            
    def test_search_and_reply(self):
        """Test searching for tweets and replying to them"""
        try:
            print("🔍 Testing search and reply functionality...")
            
            # Search for tweets about audio/podcast issues
            search_query = "podcast organization OR audio files mess -is:retweet -is:reply"
            
            tweets = self.twitter_api_v2.search_recent_tweets(
                query=search_query,
                max_results=5,
                tweet_fields=['created_at', 'author_id', 'public_metrics']
            )
            
            if not tweets.data:
                print("⚠️ No tweets found for search query")
                return False
                
            print(f"✅ Found {len(tweets.data)} tweets")
            
            # Test replying to first tweet
            first_tweet = tweets.data[0]
            print(f"📝 Testing reply to: {first_tweet.text[:50]}...")
            
            reply_text = "🎧 I totally understand this pain point! We've been working on solutions for audio workflow optimization. Would love to share some insights that might help!"
            
            response = self.twitter_api_v2.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=first_tweet.id
            )
            
            if response.data:
                print(f"✅ Search and reply test successful!")
                print(f"   Replied to tweet: {first_tweet.id}")
                return True
            else:
                print("❌ Failed to reply to searched tweet")
                return False
                
        except Exception as e:
            print(f"❌ Error in search and reply test: {e}")
            return False
            
    def test_rate_limits(self):
        """Test current rate limit status"""
        try:
            print("📊 Checking Twitter API rate limits...")
            
            # Get rate limit status
            rate_limits = self.twitter_api_v1.get_rate_limit_status()
            
            # Check key endpoints
            endpoints_to_check = [
                '/statuses/update',  # Tweet posting
                '/search/tweets',    # Tweet searching
                '/statuses/show/:id' # Tweet details
            ]
            
            print("📈 Rate Limit Status:")
            for endpoint in endpoints_to_check:
                if endpoint in rate_limits['resources'].get('statuses', {}):
                    limit_info = rate_limits['resources']['statuses'][endpoint]
                    remaining = limit_info['remaining']
                    limit = limit_info['limit']
                    reset_time = datetime.fromtimestamp(limit_info['reset'])
                    
                    print(f"   {endpoint}: {remaining}/{limit} remaining (resets at {reset_time.strftime('%H:%M:%S')})")
                    
            return True
            
        except Exception as e:
            print(f"❌ Error checking rate limits: {e}")
            return False
            
    def run_comprehensive_test(self):
        """Run all Twitter functionality tests"""
        print("🧪 Twitter Comment/Reply Functionality Test")
        print("=" * 50)
        
        test_results = {
            'basic_tweet': False,
            'reply_functionality': False,
            'media_upload': False,
            'search_and_reply': False,
            'rate_limits': False
        }
        
        # Test 1: Basic tweet
        print("\n📝 Test 1: Basic Tweet Posting")
        tweet_id = self.test_basic_tweet()
        test_results['basic_tweet'] = tweet_id is not None
        
        # Test 2: Reply functionality
        if tweet_id:
            print("\n💬 Test 2: Reply Functionality")
            time.sleep(2)  # Brief delay
            reply_id = self.test_reply_to_tweet(tweet_id)
            test_results['reply_functionality'] = reply_id is not None
            
        # Test 3: Media upload
        print("\n🎬 Test 3: Media Upload")
        time.sleep(2)
        media_tweet_id = self.test_tweet_with_media()
        test_results['media_upload'] = media_tweet_id is not None
        
        # Test 4: Search and reply
        print("\n🔍 Test 4: Search and Reply")
        time.sleep(5)  # Longer delay for search
        search_success = self.test_search_and_reply()
        test_results['search_and_reply'] = search_success
        
        # Test 5: Rate limits
        print("\n📊 Test 5: Rate Limit Check")
        rate_limit_success = self.test_rate_limits()
        test_results['rate_limits'] = rate_limit_success
        
        # Summary
        print(f"\n🎯 Test Results Summary:")
        print("=" * 30)
        
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
            
        print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests >= 3:
            print("🎉 Twitter functionality is working well!")
            print("✅ Ready for optimized automation")
        else:
            print("⚠️ Some issues detected - may need troubleshooting")
            
        return test_results

def main():
    """Run Twitter comment testing"""
    tester = TwitterCommentTester()
    results = tester.run_comprehensive_test()
    
    if results['basic_tweet'] and results['reply_functionality']:
        print(f"\n🚀 Next Steps:")
        print("1. ✅ Twitter commenting works - ready for optimization")
        print("2. 🔧 Run optimized Twitter automation for 7 hours")
        print("3. 📊 Monitor engagement and results")
        print("4. 🎯 Then expand to 50+ company processing")

if __name__ == "__main__":
    main()
