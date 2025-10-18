#!/usr/bin/env python3
"""
Test the Twitter automation system
"""

from twitter_video_responder import TwitterVideoResponder
import os

def test_api_connection():
    """Test if we can connect to Twitter API"""
    print("🔍 Testing Twitter API connection...")
    
    try:
        responder = TwitterVideoResponder()
        
        # Test basic API connection
        me = responder.twitter_api.get_me()
        print(f"✅ Connected to Twitter as: @{me.data.username}")
        
        return True
        
    except Exception as e:
        print(f"❌ Twitter API connection failed: {e}")
        return False

def test_video_files():
    """Test if video files exist"""
    print("\n🎬 Testing video file access...")
    
    responder = TwitterVideoResponder()
    all_found = True
    
    for category, info in responder.video_library.items():
        video_file = info['file']
        video_path = os.path.expanduser(f"~/Desktop/AI-video-Generation/{video_file}")
        
        if os.path.exists(video_path):
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            print(f"✅ {category}: {video_file} ({size_mb:.1f}MB)")
        else:
            print(f"❌ {category}: {video_file} - NOT FOUND")
            all_found = False
            
    return all_found

def test_keyword_search():
    """Test searching for relevant tweets"""
    print("\n🔍 Testing keyword search...")
    
    try:
        responder = TwitterVideoResponder()
        
        # Test with one keyword
        test_keyword = "podcast file organization"
        tweets = responder.twitter_api.search_recent_tweets(
            query=f'"{test_keyword}" -is:retweet -is:reply',
            max_results=10,
            tweet_fields=['created_at', 'author_id', 'public_metrics']
        )
        
        if tweets.data:
            print(f"✅ Found {len(tweets.data)} tweets for '{test_keyword}'")
            for tweet in tweets.data[:2]:  # Show first 2
                print(f"   📝 {tweet.text[:80]}...")
        else:
            print(f"⚠️  No tweets found for '{test_keyword}' (this is normal)")
            
        return True
        
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def test_ai_analysis():
    """Test AI context analysis"""
    print("\n🤖 Testing AI context analysis...")
    
    try:
        responder = TwitterVideoResponder()
        
        # Test tweets
        test_tweets = [
            "My podcast file organization is a complete disaster",
            "Spent hours looking for the right sound effect today",
            "Audio professional burnout is real",
            "Episode management is overwhelming our team"
        ]
        
        for tweet in test_tweets:
            category = responder.analyze_tweet_context(tweet)
            print(f"✅ '{tweet[:40]}...' → {category}")
            
        return True
        
    except Exception as e:
        print(f"❌ AI analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Zenyai Twitter Automation System")
    print("=" * 50)
    
    tests = [
        ("API Connection", test_api_connection),
        ("Video Files", test_video_files),
        ("Keyword Search", test_keyword_search),
        ("AI Analysis", test_ai_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results:")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All systems ready! You can start the automation with:")
        print("   python3 twitter_video_responder.py")
    else:
        print("⚠️  Fix the failing tests before running the automation")

if __name__ == "__main__":
    main()
