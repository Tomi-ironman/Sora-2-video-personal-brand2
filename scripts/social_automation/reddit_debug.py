#!/usr/bin/env python3
"""
Advanced Reddit API debugging
"""

import praw
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_reddit_credentials():
    """Test Reddit credentials step by step"""
    print("🔍 Advanced Reddit API Debugging...")
    
    # Get credentials
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret[:10]}...")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    
    # Test 1: Basic OAuth token request
    print("\n🔧 Test 1: OAuth Token Request...")
    try:
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        headers = {'User-Agent': 'ZenyaiAudioHelper/1.0'}
        
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                               auth=auth, data=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ OAuth token request successful!")
        else:
            print("❌ OAuth token request failed")
            
    except Exception as e:
        print(f"❌ OAuth test failed: {e}")
    
    # Test 2: Try different user agent
    print("\n🔧 Test 2: Different User Agent...")
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent='python:ZenyaiHelper:v1.0 (by /u/Plastic-Vanilla-4273)'
        )
        
        me = reddit.user.me()
        print(f"✅ Success with different user agent: u/{me}")
        return True
        
    except Exception as e:
        print(f"❌ Different user agent failed: {e}")
    
    # Test 3: Try read-only mode
    print("\n🔧 Test 3: Read-only Mode...")
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='ZenyaiAudioHelper/1.0'
        )
        
        # Test read-only access
        subreddit = reddit.subreddit('test')
        posts = list(subreddit.hot(limit=1))
        print(f"✅ Read-only access works: Found post '{posts[0].title[:50]}...'")
        
    except Exception as e:
        print(f"❌ Read-only test failed: {e}")
    
    # Test 4: Check if account exists
    print("\n🔧 Test 4: Check if username exists...")
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='ZenyaiAudioHelper/1.0'
        )
        
        user = reddit.redditor(username)
        print(f"User created: {user.created_utc}")
        print(f"Comment karma: {user.comment_karma}")
        print(f"✅ Username exists and is accessible")
        
    except Exception as e:
        print(f"❌ Username check failed: {e}")
    
    return False

def suggest_solutions():
    """Suggest potential solutions"""
    print("\n🔧 Potential Solutions:")
    print("1. **New Account Issue**: Reddit sometimes restricts API access for very new accounts")
    print("   - Wait 24-48 hours after account creation")
    print("   - Make a few manual posts/comments first")
    print("")
    print("2. **Password Issue**: Try resetting your Reddit password")
    print("   - Go to: https://www.reddit.com/password")
    print("   - Reset password and update .env file")
    print("")
    print("3. **App Configuration**: Double-check Reddit app settings")
    print("   - Go to: https://www.reddit.com/prefs/apps")
    print("   - Make sure app type is 'script'")
    print("   - Verify client ID/secret are correct")
    print("")
    print("4. **Create Fresh Account**: Sometimes easiest solution")
    print("   - Create new Reddit account")
    print("   - Wait 24 hours before API access")
    print("   - Get fresh credentials")

if __name__ == "__main__":
    success = test_reddit_credentials()
    if not success:
        suggest_solutions()
