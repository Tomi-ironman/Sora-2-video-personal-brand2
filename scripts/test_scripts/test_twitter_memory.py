#!/usr/bin/env python3
"""
Test Twitter Memory System
Verify that engagement tracking works correctly
"""

import json
import os
from datetime import datetime

def test_memory_system():
    """Test the engagement memory system"""
    print("🧪 Testing Twitter Engagement Memory System")
    print("=" * 50)
    
    memory_file = "twitter_engagement_memory.json"
    
    # Test 1: Create new memory
    print("\n1️⃣ Creating new memory...")
    engaged_posts = {}
    
    # Simulate engaging with posts
    test_posts = [
        {
            'url': 'https://twitter.com/user1/status/123456',
            'text': 'I hate organizing my audio files!'
        },
        {
            'url': 'https://twitter.com/user2/status/789012',
            'text': 'My podcast workflow is a nightmare'
        },
        {
            'url': 'https://twitter.com/user3/status/345678',
            'text': 'Sound design is killing me'
        }
    ]
    
    for post in test_posts:
        engaged_posts[post['url']] = {
            'engaged_at': datetime.now().isoformat(),
            'post_preview': post['text'][:100]
        }
        print(f"   ✅ Added: {post['url']}")
    
    # Save to file
    with open(memory_file, 'w') as f:
        json.dump(engaged_posts, f, indent=2)
    
    print(f"   💾 Saved {len(engaged_posts)} posts to memory")
    
    # Test 2: Load memory
    print("\n2️⃣ Loading memory from file...")
    with open(memory_file, 'r') as f:
        loaded_posts = json.load(f)
    
    print(f"   ✅ Loaded {len(loaded_posts)} posts from memory")
    
    # Test 3: Check if post already engaged
    print("\n3️⃣ Testing duplicate detection...")
    
    test_url_1 = 'https://twitter.com/user1/status/123456'
    test_url_2 = 'https://twitter.com/user4/status/999999'
    
    if test_url_1 in loaded_posts:
        print(f"   ✅ Correctly detected already engaged: {test_url_1}")
    else:
        print(f"   ❌ Failed to detect engaged post")
    
    if test_url_2 not in loaded_posts:
        print(f"   ✅ Correctly identified new post: {test_url_2}")
    else:
        print(f"   ❌ False positive on new post")
    
    # Test 4: Display memory contents
    print("\n4️⃣ Memory contents:")
    for url, data in loaded_posts.items():
        print(f"   📝 {url}")
        print(f"      Engaged: {data['engaged_at']}")
        print(f"      Preview: {data['post_preview']}")
    
    print("\n" + "=" * 50)
    print("✅ Memory system test complete!")
    print(f"📊 Total engaged posts: {len(loaded_posts)}")
    print(f"💾 Memory file: {memory_file}")
    
    return True

if __name__ == "__main__":
    test_memory_system()
