#!/usr/bin/env python3
"""
Simplified Single-Account Twitter Automation
Uses broader search terms and runs one account for full duration
"""

import os
import time
import json
import random
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

class SimpleTwitterBot:
    def __init__(self):
        self.setup_account()
        self.setup_video_library()
        self.setup_simple_searches()
        
    def setup_account(self):
        """Use Account 1 for simplicity"""
        self.account = {
            'id': 1,
            'email': os.getenv('TWITTER1_EMAIL'),
            'password': os.getenv('TWITTER1_PASSWORD'),
            'replies_posted': 0
        }
        print(f"🎯 Using Account 1: {self.account['email']}")
        
    def setup_video_library(self):
        """Setup video library"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "keywords": ["file", "organize", "chaos", "mess", "folders", "library", "lost", "find"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "keywords": ["sound", "audio", "sample", "effect", "design", "music", "beat"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "keywords": ["mixing", "mastering", "studio", "engineer", "producer", "deadline"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "keywords": ["podcast", "episode", "editing", "show", "host", "interview"]
            }
        }
        
    def setup_simple_searches(self):
        """Setup SIMPLE, broad search terms that actually get results"""
        self.search_queries = [
            # Simple, common terms people actually use
            "podcast editing",
            "audio files",
            "sound design", 
            "music production",
            "audio editing",
            "podcast workflow",
            "mixing music",
            "audio organization",
            "sound effects",
            "podcast setup",
            "audio software",
            "music studio",
            
            # Pain point keywords (broader)
            "audio nightmare",
            "podcast chaos",
            "file mess",
            "audio help",
            "mixing help",
            "podcast problems",
            "audio issues",
            "sound problems"
        ]
        
        print(f"🔍 Loaded {len(self.search_queries)} simple search terms")
        
    async def setup_browser(self):
        """Setup browser for automation"""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=500,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            self.page = await self.context.new_page()
            
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            print("🌐 Browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
            
    async def login_once(self):
        """Login once at the beginning"""
        try:
            print(f"🔐 Logging in: {self.account['email']}")
            
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            print("🤖 Please complete login manually in the browser")
            print("✅ Once logged in and on Twitter homepage, press ENTER...")
            
            input("Press ENTER when logged in: ")
            
            # Verify login
            await asyncio.sleep(2)
            if 'twitter.com' in self.page.url and 'login' not in self.page.url:
                print("✅ Login confirmed!")
                return True
            else:
                confirm = input("Are you logged in and on Twitter homepage? (yes/no): ").lower().strip()
                return confirm in ['yes', 'y']
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
            
    async def search_with_simple_terms(self, query):
        """Search using simple, broad terms"""
        try:
            print(f"🔍 Searching: '{query}'")
            
            # Use simple search URL
            search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            await self.page.goto(search_url)
            await asyncio.sleep(4)
            
            # Scroll to load tweets
            for i in range(3):
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
                
            # Find tweets
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            
            if not tweet_elements:
                # Try alternative selector
                tweet_elements = await self.page.query_selector_all('[data-testid="tweet"]')
                
            print(f"📊 Found {len(tweet_elements)} tweets for '{query}'")
            
            tweets_data = []
            
            for i, tweet_element in enumerate(tweet_elements[:5]):  # Process first 5
                try:
                    # Get tweet text
                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                    if text_element:
                        tweet_text = await text_element.inner_text()
                        
                        # Get reply button
                        reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                        
                        if reply_button and len(tweet_text) > 15:  # Avoid very short tweets
                            tweets_data.append({
                                'element': tweet_element,
                                'text': tweet_text,
                                'reply_button': reply_button,
                                'query': query
                            })
                            
                except Exception as e:
                    print(f"❌ Error processing tweet {i}: {e}")
                    continue
                    
            return tweets_data
            
        except Exception as e:
            print(f"❌ Search error for '{query}': {e}")
            return []
            
    def match_video_to_tweet(self, tweet_text):
        """Match best video to tweet"""
        tweet_lower = tweet_text.lower()
        
        best_match = "file_organization"  # Default
        max_score = 0
        
        for video_type, video_info in self.video_library.items():
            score = sum(1 for keyword in video_info['keywords'] if keyword in tweet_lower)
            
            if score > max_score:
                max_score = score
                best_match = video_type
                
        return best_match
        
    def generate_helpful_reply(self, tweet_text, video_type):
        """Generate helpful, authentic reply"""
        templates = [
            "I totally understand this! Just created a video showing how AI can help with {topic}. Hope this helps! 🎧",
            "This hits home! We've been working on solutions for {topic} at Zenyai. Check out this quick demo! 🚀", 
            "Been there! Made a short video about tackling {topic} efficiently. Might save you some headaches! 💡",
            "This is such a common challenge! Here's how we approach {topic} with AI automation. Take a look! ⚡"
        ]
        
        topics = {
            "file_organization": "audio file organization",
            "sound_design": "sound design workflow", 
            "audio_professional": "audio production workflow",
            "podcast_workflow": "podcast editing workflow"
        }
        
        template = random.choice(templates)
        topic = topics.get(video_type, "audio workflow")
        
        return template.format(topic=topic)
        
    async def reply_to_tweet(self, tweet_data):
        """Reply to tweet with video"""
        try:
            tweet_text = tweet_data['text']
            reply_button = tweet_data['reply_button']
            
            print(f"💬 Replying to: {tweet_text[:60]}...")
            
            # Match video
            video_type = self.match_video_to_tweet(tweet_text)
            video_info = self.video_library[video_type]
            
            # Generate reply
            reply_text = self.generate_helpful_reply(tweet_text, video_type)
            
            # Click reply
            await reply_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await reply_button.click()
            await asyncio.sleep(3)
            
            # Find reply input
            reply_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=5000)
            
            if reply_input:
                # Type reply naturally
                await reply_input.click()
                await asyncio.sleep(1)
                
                for char in reply_text:
                    await reply_input.type(char)
                    await asyncio.sleep(random.randint(30, 80) / 1000)  # Human-like typing
                    
                await asyncio.sleep(2)
                
                # Upload video
                video_path = os.path.expanduser(f"~/Desktop/AI-video-Generation/{video_info['file']}")
                
                if os.path.exists(video_path):
                    try:
                        file_input = await self.page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(video_path)
                            print(f"📹 Uploaded {video_type} video")
                            await asyncio.sleep(4)
                    except Exception as e:
                        print(f"⚠️ Video upload failed: {e}")
                        
                # Post reply
                tweet_button = await self.page.query_selector('[data-testid="tweetButtonInline"]')
                if tweet_button:
                    await tweet_button.click()
                    print("🚀 Reply posted!")
                    await asyncio.sleep(3)
                    
                    # Log success
                    self.log_reply(tweet_data)
                    self.account['replies_posted'] += 1
                    
                    return True
                    
            return False
            
        except Exception as e:
            print(f"❌ Reply error: {e}")
            return False
            
    def log_reply(self, tweet_data):
        """Log successful reply"""
        try:
            log_file = "simple_twitter_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'query': tweet_data['query'],
                'tweet_preview': tweet_data['text'][:100],
                'total_replies': self.account['replies_posted']
            }
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Logging error: {e}")
            
    async def run_simple_automation(self, hours=7):
        """Run simple automation for specified hours"""
        try:
            print("🚀 Simple Twitter Automation Starting")
            print("=" * 50)
            print(f"📧 Account: {self.account['email']}")
            print(f"⏰ Duration: {hours} hours")
            print(f"🔍 Search terms: {len(self.search_queries)}")
            
            # Setup and login once
            if not await self.setup_browser():
                return
                
            if not await self.login_once():
                print("❌ Login failed - stopping")
                return
                
            # Run automation
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=hours)
            
            cycle_count = 0
            
            while datetime.now() < end_time:
                cycle_count += 1
                
                print(f"\n🔄 CYCLE {cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Rotate through search queries
                query_batch = random.sample(self.search_queries, 3)  # 3 random queries per cycle
                
                for query in query_batch:
                    try:
                        # Search for tweets
                        tweets = await self.search_with_simple_terms(query)
                        
                        if tweets:
                            # Reply to first good tweet
                            for tweet_data in tweets[:1]:  # One reply per query
                                if await self.reply_to_tweet(tweet_data):
                                    # Success! Wait before next reply
                                    delay = random.randint(300, 600)  # 5-10 minutes
                                    print(f"⏳ Waiting {delay//60} minutes before next search...")
                                    await asyncio.sleep(delay)
                                    break
                        else:
                            print(f"⚠️ No tweets found for '{query}' - trying next query")
                            
                        # Small delay between queries
                        await asyncio.sleep(random.randint(30, 60))
                        
                    except Exception as e:
                        print(f"❌ Query error: {e}")
                        await asyncio.sleep(60)
                        
                # Progress update
                remaining_time = end_time - datetime.now()
                hours_left = remaining_time.total_seconds() / 3600
                
                print(f"\n📊 Progress Update:")
                print(f"   ⏰ Time Remaining: {hours_left:.1f} hours")
                print(f"   🔄 Cycles Completed: {cycle_count}")
                print(f"   💬 Replies Posted: {self.account['replies_posted']}")
                
                if hours_left <= 0:
                    break
                    
            # Final summary
            print(f"\n🎉 {hours}-Hour Simple Automation Complete!")
            print(f"📊 Final Results:")
            print(f"   🔄 Cycles: {cycle_count}")
            print(f"   💬 Total Replies: {self.account['replies_posted']}")
            print(f"   📈 Replies per Hour: {self.account['replies_posted']/hours:.1f}")
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run simple Twitter automation"""
    bot = SimpleTwitterBot()
    await bot.run_simple_automation(hours=7)

if __name__ == "__main__":
    asyncio.run(main())
