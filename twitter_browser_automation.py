#!/usr/bin/env python3
"""
Twitter Browser Automation System
Physically navigates Twitter, finds relevant tweets, and posts video replies
Just like Product Hunt automation but for Twitter!
"""

import os
import time
import json
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

class TwitterBrowserBot:
    def __init__(self):
        self.setup_credentials()
        self.setup_video_library()
        self.setup_search_targets()
        
    def setup_credentials(self):
        """Setup Twitter login credentials"""
        self.twitter_email = os.getenv('TWITTER_EMAIL', 'your_twitter_email@example.com')
        self.twitter_password = os.getenv('TWITTER_PASSWORD', 'your_twitter_password')
        print(f"🔐 Using Twitter account: {self.twitter_email}")
        
    def setup_video_library(self):
        """Setup our video library for responses"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization chaos solution",
                "keywords": ["file", "organize", "chaos", "mess", "folders", "library", "lost files"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound designer workflow optimization",
                "keywords": ["sound design", "audio search", "samples", "effects", "library", "workflow"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Audio professional burnout solution",
                "keywords": ["audio professional", "burnout", "deadline", "mixing", "mastering", "studio"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast workflow automation",
                "keywords": ["podcast", "episode", "workflow", "team", "collaboration", "editing"]
            }
        }
        
    def setup_search_targets(self):
        """Setup search queries for finding relevant tweets"""
        self.search_queries = [
            "podcast file organization nightmare",
            "audio library mess help",
            "sound design workflow chaos", 
            "too many audio files drowning",
            "can't find my samples",
            "audio asset management pain",
            "podcast editing workflow hell",
            "audio professional burnout",
            "sound designer struggle",
            "episode organization disaster",
            "audio collaboration nightmare",
            "mixing deadline stress"
        ]
        
    async def setup_browser(self):
        """Initialize browser with realistic settings"""
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # Keep visible to see interactions
            slow_mo=800,     # Slow down to appear human
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--disable-web-security'
            ]
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # Remove automation indicators
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
    async def login_to_twitter(self):
        """Login to Twitter with manual verification support"""
        try:
            print("🌐 Navigating to Twitter...")
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            # Check for verification/captcha
            page_content = await self.page.content()
            if 'verification' in page_content.lower() or 'captcha' in page_content.lower():
                print("🛡️ Verification detected - please complete manually")
                input("Complete verification and press ENTER: ")
                
            # Try to find email/username input
            email_selectors = [
                'input[name="text"]',
                'input[autocomplete="username"]',
                'input[data-testid="ocfEnterTextTextInput"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="username" i]'
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if email_input:
                        print(f"✅ Found email input: {selector}")
                        break
                except:
                    continue
                    
            if email_input:
                # Fill email
                await email_input.fill(self.twitter_email)
                await asyncio.sleep(1)
                
                # Click Next button
                next_selectors = [
                    'div[role="button"]:has-text("Next")',
                    'button:has-text("Next")',
                    '[data-testid="LoginForm_Login_Button"]'
                ]
                
                for selector in next_selectors:
                    try:
                        next_button = await self.page.query_selector(selector)
                        if next_button:
                            await next_button.click()
                            print("🔘 Clicked Next")
                            break
                    except:
                        continue
                        
                await asyncio.sleep(3)
                
                # Find password input
                password_selectors = [
                    'input[name="password"]',
                    'input[type="password"]',
                    'input[autocomplete="current-password"]'
                ]
                
                password_input = None
                for selector in password_selectors:
                    try:
                        password_input = await self.page.wait_for_selector(selector, timeout=3000)
                        if password_input:
                            print(f"✅ Found password input: {selector}")
                            break
                    except:
                        continue
                        
                if password_input:
                    await password_input.fill(self.twitter_password)
                    await asyncio.sleep(1)
                    
                    # Click Login button
                    login_selectors = [
                        'div[role="button"]:has-text("Log in")',
                        'button:has-text("Log in")',
                        '[data-testid="LoginForm_Login_Button"]'
                    ]
                    
                    for selector in login_selectors:
                        try:
                            login_button = await self.page.query_selector(selector)
                            if login_button:
                                await login_button.click()
                                print("🔐 Clicked Login")
                                break
                        except:
                            continue
                            
                    await asyncio.sleep(5)
                    
                    # Check if login successful
                    current_url = self.page.url
                    if 'home' in current_url or 'twitter.com' in current_url and 'login' not in current_url:
                        print("✅ Login successful!")
                        return True
                        
            # If automated login fails, ask for manual completion
            print("🤖 Please complete login manually in the browser")
            input("Press ENTER when logged in and on Twitter homepage: ")
            
            # Verify login
            current_url = self.page.url
            if 'twitter.com' in current_url and 'login' not in current_url:
                print("✅ Manual login confirmed!")
                return True
            else:
                print("❌ Login verification failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            print("🤖 Please complete login manually")
            input("Press ENTER when logged in: ")
            return True
            
    async def search_for_tweets(self, query):
        """Search for tweets using Twitter's search"""
        try:
            print(f"🔍 Searching for: {query}")
            
            # Navigate to search
            search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            await self.page.goto(search_url)
            await asyncio.sleep(3)
            
            # Scroll to load more tweets
            for i in range(3):
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
                
            # Find tweet elements
            tweet_selectors = [
                '[data-testid="tweet"]',
                'article[role="article"]',
                '[data-testid="tweetText"]'
            ]
            
            tweets_found = []
            
            for selector in tweet_selectors:
                try:
                    tweet_elements = await self.page.query_selector_all(selector)
                    if tweet_elements:
                        print(f"✅ Found {len(tweet_elements)} tweets with selector: {selector}")
                        
                        # Process first few tweets
                        for i, tweet_element in enumerate(tweet_elements[:5]):
                            try:
                                # Get tweet text
                                text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                                if text_element:
                                    tweet_text = await text_element.inner_text()
                                    
                                    # Get reply button
                                    reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                                    
                                    if reply_button and tweet_text:
                                        tweets_found.append({
                                            'element': tweet_element,
                                            'text': tweet_text,
                                            'reply_button': reply_button,
                                            'query': query
                                        })
                                        
                            except Exception as e:
                                print(f"❌ Error processing tweet {i}: {e}")
                                continue
                                
                        break
                        
                except Exception as e:
                    print(f"❌ Error with selector {selector}: {e}")
                    continue
                    
            print(f"📊 Found {len(tweets_found)} actionable tweets")
            return tweets_found
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
            
    def match_video_to_tweet(self, tweet_text):
        """Match best video to tweet content"""
        tweet_lower = tweet_text.lower()
        
        best_match = None
        max_matches = 0
        
        for video_type, video_info in self.video_library.items():
            matches = sum(1 for keyword in video_info['keywords'] if keyword in tweet_lower)
            
            if matches > max_matches:
                max_matches = matches
                best_match = video_type
                
        return best_match if max_matches > 0 else "file_organization"  # Default
        
    def generate_reply_text(self, tweet_text, video_type):
        """Generate authentic reply text"""
        video_info = self.video_library[video_type]
        
        # Authentic reply templates
        templates = [
            "I totally feel this pain! Just created a video showing how AI can help with {problem}. Hope this helps! 🎧",
            "Been there! This is exactly why we built Zenyai - AI-native solution for {problem}. Check out this quick demo! 🚀",
            "This resonates so much! Created a short video about solving {problem} with AI automation. Might be helpful! 💡",
            "I understand this struggle completely! Here's a quick video showing how to tackle {problem} efficiently. Hope it helps! ⚡",
            "This is such a common pain point! Made a video demonstrating AI solutions for {problem}. Take a look! 🎯"
        ]
        
        problem_map = {
            "file_organization": "audio file organization",
            "sound_design": "sound design workflow",
            "audio_professional": "audio professional burnout",
            "podcast_workflow": "podcast workflow chaos"
        }
        
        template = random.choice(templates)
        problem = problem_map.get(video_type, "workflow optimization")
        
        return template.format(problem=problem)
        
    async def reply_to_tweet(self, tweet_data):
        """Reply to a tweet with video"""
        try:
            tweet_text = tweet_data['text']
            reply_button = tweet_data['reply_button']
            
            print(f"💬 Replying to: {tweet_text[:50]}...")
            
            # Determine best video
            video_type = self.match_video_to_tweet(tweet_text)
            video_info = self.video_library[video_type]
            
            # Generate reply text
            reply_text = self.generate_reply_text(tweet_text, video_type)
            
            # Click reply button
            await reply_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await reply_button.click()
            await asyncio.sleep(2)
            
            # Find reply text area
            reply_selectors = [
                '[data-testid="tweetTextarea_0"]',
                'div[role="textbox"]',
                '[contenteditable="true"]'
            ]
            
            reply_input = None
            for selector in reply_selectors:
                try:
                    reply_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if reply_input:
                        print(f"✅ Found reply input: {selector}")
                        break
                except:
                    continue
                    
            if reply_input:
                # Type reply
                await reply_input.click()
                await asyncio.sleep(1)
                
                # Type slowly like human
                words = reply_text.split(' ')
                for i, word in enumerate(words):
                    await reply_input.type(word)
                    if i < len(words) - 1:
                        await reply_input.type(' ')
                        await asyncio.sleep(random.randint(50, 150) / 1000)
                        
                await asyncio.sleep(2)
                
                # Upload video
                video_path = os.path.expanduser(f"~/Desktop/AI-video-Generation/{video_info['file']}")
                
                if os.path.exists(video_path):
                    # Find media upload button
                    media_selectors = [
                        '[data-testid="fileInput"]',
                        'input[type="file"]',
                        '[aria-label*="media" i]'
                    ]
                    
                    for selector in media_selectors:
                        try:
                            media_input = await self.page.query_selector(selector)
                            if media_input:
                                await media_input.set_input_files(video_path)
                                print(f"📹 Uploaded video: {video_info['file']}")
                                await asyncio.sleep(3)  # Wait for upload
                                break
                        except Exception as e:
                            print(f"❌ Media upload error with {selector}: {e}")
                            continue
                            
                # Find and click Tweet button
                tweet_selectors = [
                    '[data-testid="tweetButtonInline"]',
                    'div[role="button"]:has-text("Tweet")',
                    'button:has-text("Tweet")'
                ]
                
                for selector in tweet_selectors:
                    try:
                        tweet_button = await self.page.query_selector(selector)
                        if tweet_button:
                            await tweet_button.click()
                            print("🚀 Posted reply!")
                            await asyncio.sleep(3)
                            return True
                    except:
                        continue
                        
            print("❌ Failed to post reply")
            return False
            
        except Exception as e:
            print(f"❌ Reply error: {e}")
            return False
            
    async def run_twitter_engagement_cycle(self):
        """Run one cycle of Twitter engagement"""
        try:
            print("🚀 Starting Twitter Engagement Cycle")
            print("=" * 50)
            
            successful_replies = 0
            
            # Process each search query
            for i, query in enumerate(self.search_queries[:3]):  # Limit to 3 queries per cycle
                print(f"\n🎯 Query {i+1}/3: {query}")
                
                # Search for tweets
                tweets = await self.search_for_tweets(query)
                
                if tweets:
                    # Reply to first relevant tweet
                    for tweet_data in tweets[:1]:  # One reply per query
                        if await self.reply_to_tweet(tweet_data):
                            successful_replies += 1
                            
                            # Log successful reply
                            self.log_reply(tweet_data)
                            
                            # Human-like delay between replies
                            delay = random.randint(120, 300)  # 2-5 minutes
                            print(f"⏳ Waiting {delay} seconds before next reply...")
                            await asyncio.sleep(delay)
                            break
                            
                # Delay between searches
                await asyncio.sleep(random.randint(30, 60))
                
            print(f"\n📊 Cycle Complete: {successful_replies} replies posted")
            return successful_replies
            
        except Exception as e:
            print(f"❌ Engagement cycle error: {e}")
            return 0
            
    def log_reply(self, tweet_data):
        """Log successful reply"""
        try:
            log_file = "twitter_replies_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'tweet_text': tweet_data['text'][:100],
                'query': tweet_data['query'],
                'status': 'posted'
            }
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Logging error: {e}")
            
    async def run_continuous_engagement(self, hours=7):
        """Run continuous Twitter engagement"""
        try:
            print(f"🔄 Starting {hours}-Hour Twitter Engagement")
            print("=" * 50)
            
            await self.setup_browser()
            
            if not await self.login_to_twitter():
                print("❌ Login failed - stopping automation")
                return
                
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=hours)
            
            cycle_count = 0
            total_replies = 0
            
            while datetime.now() < end_time:
                cycle_count += 1
                
                replies_this_cycle = await self.run_twitter_engagement_cycle()
                total_replies += replies_this_cycle
                
                # Progress update
                remaining_time = end_time - datetime.now()
                hours_left = remaining_time.total_seconds() / 3600
                
                print(f"\n⏰ Progress Update:")
                print(f"   🕐 Time Remaining: {hours_left:.1f} hours")
                print(f"   🔄 Cycles Completed: {cycle_count}")
                print(f"   💬 Total Replies Posted: {total_replies}")
                
                if hours_left > 0.5:  # If more than 30 minutes left
                    cycle_delay = random.randint(1800, 3600)  # 30-60 minutes between cycles
                    print(f"   😴 Sleeping for {cycle_delay/60:.0f} minutes...")
                    await asyncio.sleep(cycle_delay)
                else:
                    break
                    
            print(f"\n🎉 {hours}-Hour Twitter Engagement Complete!")
            print(f"📊 Final Results:")
            print(f"   🔄 Cycles: {cycle_count}")
            print(f"   💬 Total Replies: {total_replies}")
            print(f"   🎯 Average per Cycle: {total_replies/cycle_count:.1f}")
            
        except Exception as e:
            print(f"❌ Continuous engagement error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run Twitter browser automation"""
    bot = TwitterBrowserBot()
    await bot.run_continuous_engagement(hours=7)

if __name__ == "__main__":
    asyncio.run(main())
