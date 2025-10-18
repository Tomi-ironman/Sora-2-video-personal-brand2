#!/usr/bin/env python3
"""
Test Reddit API connection
"""

import praw
import os
from dotenv import load_dotenv

load_dotenv()

def test_reddit_connection():
    """Test basic Reddit API connection"""
    print("🔍 Testing Reddit API Connection...")
    
    # Get credentials
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'ZenyaiAudioHelper/1.0')
    
    print(f"Client ID: {client_id}")
    print(f"Username: {username}")
    print(f"User Agent: {user_agent}")
    
    try:
        # Initialize Reddit client
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )
        
        # Test connection
        print("🔗 Attempting to authenticate...")
        me = reddit.user.me()
        print(f"✅ Successfully connected as: u/{me}")
        
        # Test basic functionality
        print("🔍 Testing subreddit access...")
        subreddit = reddit.subreddit('test')
        print(f"✅ Can access r/test: {subreddit.display_name}")
        
        # Test search
        print("🔍 Testing search functionality...")
        posts = list(subreddit.new(limit=1))
        if posts:
            print(f"✅ Can read posts: Found post '{posts[0].title[:50]}...'")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        # Common error solutions
        if "401" in str(e):
            print("\n🔧 401 Error Solutions:")
            print("1. Check if Reddit username/password are correct")
            print("2. Make sure the Reddit account is verified (check email)")
            print("3. Try logging into Reddit manually first")
            print("4. Check if 2FA is enabled (disable for API access)")
            
        elif "403" in str(e):
            print("\n🔧 403 Error Solutions:")
            print("1. Check if the app is properly configured")
            print("2. Make sure app type is 'script'")
            print("3. Verify client ID and secret are correct")
            
        return False

if __name__ == "__main__":
    test_reddit_connection()
