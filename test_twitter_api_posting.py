#!/usr/bin/env python3
"""
Test Twitter API v2 Direct Posting Capabilities
Check if we can post tweets and replies directly via API
"""

import tweepy
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TwitterAPITester:
    def __init__(self):
        self.setup_twitter_apis()
        
    def setup_twitter_apis(self):
        """Setup Twitter API with different credential combinations"""
        
        # Method 1: Try with Bearer Token + OAuth 2.0
        try:
            self.api_v2_bearer = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                wait_on_rate_limit=True
            )
            print("✅ Twitter API v2 (Bearer Token) initialized")
        except Exception as e:
            print(f"❌ Twitter API v2 Bearer setup failed: {e}")
            self.api_v2_bearer = None
            
        # Method 2: Try with Consumer Keys + Access Tokens (OAuth 1.0a)
        try:
            self.api_v2_oauth = tweepy.Client(
                consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            print("✅ Twitter API v2 (OAuth 1.0a) initialized")
        except Exception as e:
            print(f"❌ Twitter API v2 OAuth setup failed: {e}")
            self.api_v2_oauth = None
            
        # Method 3: Try v1.1 API for media upload
        try:
            auth = tweepy.OAuth1UserHandler(
                os.getenv('TWITTER_CONSUMER_KEY'),
                os.getenv('TWITTER_CONSUMER_SECRET'),
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            print("✅ Twitter API v1.1 initialized")
        except Exception as e:
            print(f"❌ Twitter API v1.1 setup failed: {e}")
            self.api_v1 = None
            
    def test_basic_tweet_posting(self):
        """Test basic tweet posting capabilities"""
        print("\n🐦 Testing Basic Tweet Posting")
        print("=" * 40)
        
        test_tweet = f"🧪 Testing Twitter API direct posting - {datetime.now().strftime('%H:%M:%S')}"
        
        # Test with OAuth API
        if self.api_v2_oauth:
            try:
                print("📝 Trying to post with OAuth API...")
                response = self.api_v2_oauth.create_tweet(text=test_tweet)
                
                if response.data:
                    tweet_id = response.data['id']
                    print(f"✅ SUCCESS! Tweet posted via OAuth API")
                    print(f"   Tweet ID: {tweet_id}")
                    print(f"   Content: {test_tweet}")
                    return tweet_id, 'oauth'
                else:
                    print("❌ OAuth API: No response data")
                    
            except Exception as e:
                print(f"❌ OAuth API posting failed: {e}")
                
        # Test with Bearer Token API
        if self.api_v2_bearer:
            try:
                print("📝 Trying to post with Bearer Token API...")
                response = self.api_v2_bearer.create_tweet(text=test_tweet)
                
                if response.data:
                    tweet_id = response.data['id']
                    print(f"✅ SUCCESS! Tweet posted via Bearer Token API")
                    print(f"   Tweet ID: {tweet_id}")
                    return tweet_id, 'bearer'
                else:
                    print("❌ Bearer Token API: No response data")
                    
            except Exception as e:
                print(f"❌ Bearer Token API posting failed: {e}")
                
        print("❌ All API methods failed for basic tweet posting")
        return None, None
        
    def test_reply_posting(self, original_tweet_id, api_method):
        """Test reply posting capabilities"""
        print(f"\n💬 Testing Reply Posting (using {api_method})")
        print("=" * 40)
        
        reply_text = f"🤖 This is a test reply via Twitter API! Time: {datetime.now().strftime('%H:%M:%S')}"
        
        api_client = self.api_v2_oauth if api_method == 'oauth' else self.api_v2_bearer
        
        if api_client:
            try:
                print(f"📝 Posting reply to tweet {original_tweet_id}...")
                
                response = api_client.create_tweet(
                    text=reply_text,
                    in_reply_to_tweet_id=original_tweet_id
                )
                
                if response.data:
                    reply_id = response.data['id']
                    print(f"✅ SUCCESS! Reply posted via {api_method.upper()} API")
                    print(f"   Reply ID: {reply_id}")
                    print(f"   Content: {reply_text}")
                    return reply_id
                else:
                    print(f"❌ {api_method.upper()} API: No response data for reply")
                    
            except Exception as e:
                print(f"❌ {api_method.upper()} API reply failed: {e}")
                
        return None
        
    def test_media_upload(self):
        """Test media (video) upload capabilities"""
        print(f"\n🎬 Testing Media Upload")
        print("=" * 30)
        
        # Look for video files
        video_dir = os.path.expanduser("~/Desktop/AI-video-Generation/")
        
        if not os.path.exists(video_dir):
            print("❌ Video directory not found - skipping media test")
            return None
            
        video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        
        if not video_files:
            print("❌ No video files found - skipping media test")
            return None
            
        video_path = os.path.join(video_dir, video_files[0])
        print(f"📹 Testing with: {video_files[0]}")
        
        # Test media upload with v1.1 API
        if self.api_v1:
            try:
                print("📤 Uploading media via v1.1 API...")
                
                media = self.api_v1.media_upload(video_path)
                
                if media:
                    print(f"✅ Media uploaded successfully!")
                    print(f"   Media ID: {media.media_id}")
                    
                    # Test posting tweet with media
                    if self.api_v2_oauth:
                        try:
                            tweet_text = f"🎬 Testing video upload via API - {datetime.now().strftime('%H:%M:%S')}"
                            
                            response = self.api_v2_oauth.create_tweet(
                                text=tweet_text,
                                media_ids=[media.media_id]
                            )
                            
                            if response.data:
                                tweet_id = response.data['id']
                                print(f"✅ SUCCESS! Video tweet posted!")
                                print(f"   Tweet ID: {tweet_id}")
                                return tweet_id
                                
                        except Exception as e:
                            print(f"❌ Video tweet posting failed: {e}")
                            
            except Exception as e:
                print(f"❌ Media upload failed: {e}")
                
        return None
        
    def test_search_and_reply(self):
        """Test searching for tweets and replying"""
        print(f"\n🔍 Testing Search and Reply")
        print("=" * 30)
        
        # Search for tweets about audio/podcast issues
        search_query = "podcast workflow OR audio organization -is:retweet -is:reply lang:en"
        
        if self.api_v2_oauth or self.api_v2_bearer:
            api_client = self.api_v2_oauth or self.api_v2_bearer
            
            try:
                print(f"🔍 Searching: {search_query}")
                
                tweets = api_client.search_recent_tweets(
                    query=search_query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'public_metrics']
                )
                
                if tweets.data:
                    print(f"✅ Found {len(tweets.data)} tweets")
                    
                    # Try to reply to first tweet
                    first_tweet = tweets.data[0]
                    print(f"📝 Attempting reply to: {first_tweet.text[:50]}...")
                    
                    reply_text = "🎧 I understand this challenge! We've been working on AI solutions for audio workflow optimization at Zenyai. Would love to share some insights!"
                    
                    try:
                        response = api_client.create_tweet(
                            text=reply_text,
                            in_reply_to_tweet_id=first_tweet.id
                        )
                        
                        if response.data:
                            print(f"✅ SUCCESS! Search and reply works!")
                            print(f"   Reply ID: {response.data['id']}")
                            return True
                            
                    except Exception as e:
                        print(f"❌ Reply to searched tweet failed: {e}")
                        
                else:
                    print("❌ No tweets found in search")
                    
            except Exception as e:
                print(f"❌ Search failed: {e}")
                
        return False
        
    def check_api_permissions(self):
        """Check what permissions our API keys have"""
        print(f"\n🔐 Checking API Permissions")
        print("=" * 30)
        
        permissions = {
            'read': False,
            'write': False,
            'direct_messages': False
        }
        
        if self.api_v2_oauth:
            try:
                # Try to get user info (read permission)
                me = self.api_v2_oauth.get_me()
                if me.data:
                    permissions['read'] = True
                    print(f"✅ READ permission: Confirmed")
                    print(f"   User: @{me.data.username}")
                    
            except Exception as e:
                print(f"❌ READ permission check failed: {e}")
                
        # Write permission will be tested by actual posting
        print("📝 WRITE permission: Will be tested by posting")
        
        return permissions
        
    def run_comprehensive_api_test(self):
        """Run comprehensive API testing"""
        print("🧪 Twitter API Direct Posting Test")
        print("=" * 50)
        
        # Check permissions
        permissions = self.check_api_permissions()
        
        # Test basic tweet posting
        tweet_id, api_method = self.test_basic_tweet_posting()
        
        if tweet_id:
            print(f"\n🎉 GREAT NEWS! Direct API posting WORKS!")
            
            # Test reply posting
            reply_id = self.test_reply_posting(tweet_id, api_method)
            
            # Test media upload
            media_tweet_id = self.test_media_upload()
            
            # Test search and reply
            search_reply_success = self.test_search_and_reply()
            
            # Summary
            print(f"\n📊 API Capabilities Summary:")
            print("=" * 35)
            print(f"✅ Basic Tweet Posting: YES ({api_method.upper()} API)")
            print(f"{'✅' if reply_id else '❌'} Reply Posting: {'YES' if reply_id else 'NO'}")
            print(f"{'✅' if media_tweet_id else '❌'} Video Upload: {'YES' if media_tweet_id else 'NO'}")
            print(f"{'✅' if search_reply_success else '❌'} Search & Reply: {'YES' if search_reply_success else 'NO'}")
            
            if reply_id and media_tweet_id and search_reply_success:
                print(f"\n🚀 INCREDIBLE! We can do EVERYTHING via API!")
                print("🔥 No need for browser automation!")
                print("⚡ Direct API posting is:")
                print("   • Faster (no browser overhead)")
                print("   • More reliable (no UI changes)")
                print("   • Easier to scale (no browser limits)")
                print("   • Less detectable (official API)")
                
                return True
            else:
                print(f"\n⚠️ Some features missing - browser automation may be needed")
                return False
                
        else:
            print(f"\n❌ API posting not available")
            print("🌐 Browser automation is required")
            return False

def main():
    """Test Twitter API posting capabilities"""
    tester = TwitterAPITester()
    
    api_works = tester.run_comprehensive_api_test()
    
    if api_works:
        print(f"\n🎯 RECOMMENDATION: Use Direct API Posting!")
        print("✅ Much simpler, faster, and more reliable")
        print("🚀 Can build pure API-based automation")
    else:
        print(f"\n🎯 RECOMMENDATION: Use Browser Automation")
        print("🌐 API limitations require browser approach")

if __name__ == "__main__":
    main()
