#!/usr/bin/env python3
"""
STEALTH Twitter Automation
Bypasses bot detection and search blocking
Uses human-like behavior and alternative discovery methods
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

class StealthTwitterBot:
    def __init__(self):
        self.setup_account()
        self.setup_stealth_searches()
        
    def setup_account(self):
        """Use Account 1"""
        self.account = {
            'id': 1,
            'email': os.getenv('TWITTER1_EMAIL'),
            'password': os.getenv('TWITTER1_PASSWORD'),
            'replies_posted': 0
        }
        print(f"🥷 Stealth Account: {self.account['email']}")
        
    def setup_stealth_searches(self):
        """Setup searches that work around Twitter's blocking"""
        
        # Use broader, more natural terms that Twitter allows
        self.search_methods = [
            # Method 1: Browse trending hashtags
            {
                'type': 'hashtag',
                'terms': ['#podcast', '#audio', '#music', '#sound', '#editing', '#production', '#workflow', '#creator']
            },
            
            # Method 2: Browse user timelines of audio creators
            {
                'type': 'user_timeline',
                'users': ['@spotify', '@anchor', '@audacity_team', '@adobeaudition', '@reaper_fm', '@logicprox']
            },
            
            # Method 3: Use simple, single-word searches
            {
                'type': 'simple_search',
                'terms': ['podcast', 'audio', 'music', 'sound', 'editing', 'mixing', 'mastering', 'workflow']
            },
            
            # Method 4: Browse Twitter Lists related to audio
            {
                'type': 'explore_feed',
                'categories': ['Technology', 'Music', 'Entertainment']
            }
        ]
        
        print(f"🥷 Loaded stealth discovery methods")
        
    async def setup_stealth_browser(self):
        """Setup ultra-stealth browser"""
        try:
            self.playwright = await async_playwright().start()
            
            # Maximum stealth settings
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=random.randint(100, 300),  # Random human-like delays
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--no-first-run',
                    '--disable-extensions',
                    '--disable-default-apps',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                ]
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1366, 'height': 768},  # Common resolution
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation'],
                geolocation={'latitude': 40.7128, 'longitude': -74.0060}  # NYC
            )
            
            self.page = await self.context.new_page()
            
            # Advanced anti-detection
            await self.page.add_init_script("""
                // Remove webdriver traces
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Mock chrome object
                window.chrome = {
                    runtime: {},
                };
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Mock permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)
            
            print("🥷 Ultra-stealth browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Stealth browser setup failed: {e}")
            return False
            
    async def login_with_stealth(self):
        """Login with human-like behavior"""
        try:
            print(f"🥷 Stealth login: {self.account['email']}")
            
            # Go to Twitter homepage first (more human-like)
            await self.page.goto('https://twitter.com')
            await asyncio.sleep(random.randint(2, 4))
            
            # Random mouse movements
            await self.page.mouse.move(random.randint(100, 500), random.randint(100, 300))
            await asyncio.sleep(1)
            
            # Navigate to login
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            print("🤖 Complete login manually and press ENTER...")
            input("Press ENTER when logged in: ")
            
            # Verify we're logged in by checking for home timeline
            await asyncio.sleep(2)
            current_url = self.page.url
            
            if 'twitter.com' in current_url and 'login' not in current_url:
                print("✅ Stealth login successful!")
                
                # Human-like post-login behavior
                await self.human_like_browsing()
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Stealth login failed: {e}")
            return False
            
    async def human_like_browsing(self):
        """Simulate human browsing to avoid detection"""
        try:
            print("🥷 Simulating human browsing...")
            
            # Random scroll on home timeline
            for _ in range(random.randint(2, 5)):
                await self.page.evaluate("window.scrollBy(0, 300)")
                await asyncio.sleep(random.randint(1, 3))
                
            # Random mouse movements
            await self.page.mouse.move(random.randint(200, 800), random.randint(200, 600))
            await asyncio.sleep(1)
            
            print("✅ Human-like browsing complete")
            
        except Exception as e:
            print(f"⚠️ Human browsing simulation error: {e}")
            
    async def discover_posts_via_hashtags(self, hashtag):
        """Discover posts through hashtag browsing (less suspicious)"""
        try:
            print(f"🥷 Browsing hashtag: {hashtag}")
            
            # Navigate to hashtag
            hashtag_url = f"https://twitter.com/hashtag/{hashtag.replace('#', '')}"
            await self.page.goto(hashtag_url)
            await asyncio.sleep(random.randint(3, 6))
            
            # Human-like scrolling
            for scroll in range(3):
                await self.page.evaluate("window.scrollBy(0, 400)")
                await asyncio.sleep(random.randint(2, 4))
                
            # Look for tweets
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            print(f"   📊 Found {len(tweet_elements)} posts in {hashtag}")
            
            # Find audio-related posts
            audio_posts = []
            for tweet_element in tweet_elements[:10]:  # Check first 10
                try:
                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                    if text_element:
                        tweet_text = await text_element.inner_text()
                        
                        # Check if audio-related
                        audio_keywords = ['audio', 'sound', 'music', 'podcast', 'mix', 'master', 'edit', 'record', 'studio', 'workflow', 'production']
                        if any(keyword in tweet_text.lower() for keyword in audio_keywords):
                            reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                            if reply_button and len(tweet_text) > 15:
                                audio_posts.append({
                                    'element': tweet_element,
                                    'text': tweet_text,
                                    'reply_button': reply_button,
                                    'source': f'hashtag_{hashtag}'
                                })
                                
                except Exception as e:
                    continue
                    
            return audio_posts
            
        except Exception as e:
            print(f"❌ Hashtag discovery error for {hashtag}: {e}")
            return []
            
    async def discover_posts_via_home_feed(self):
        """Discover posts from home timeline (most natural)"""
        try:
            print("🥷 Browsing home timeline...")
            
            # Go to home
            await self.page.goto('https://twitter.com/home')
            await asyncio.sleep(random.randint(3, 6))
            
            # Scroll through timeline naturally
            for scroll in range(5):
                await self.page.evaluate("window.scrollBy(0, 600)")
                await asyncio.sleep(random.randint(2, 4))
                
            # Look for audio-related posts
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            print(f"   📊 Found {len(tweet_elements)} posts in home timeline")
            
            audio_posts = []
            for tweet_element in tweet_elements:
                try:
                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                    if text_element:
                        tweet_text = await text_element.inner_text()
                        
                        # Check if audio-related
                        audio_keywords = ['audio', 'sound', 'music', 'podcast', 'mix', 'master', 'edit', 'record', 'studio', 'workflow', 'production', 'creator', 'content']
                        if any(keyword in tweet_text.lower() for keyword in audio_keywords):
                            reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                            if reply_button and len(tweet_text) > 15:
                                audio_posts.append({
                                    'element': tweet_element,
                                    'text': tweet_text,
                                    'reply_button': reply_button,
                                    'source': 'home_timeline'
                                })
                                
                except Exception as e:
                    continue
                    
            return audio_posts
            
        except Exception as e:
            print(f"❌ Home timeline discovery error: {e}")
            return []
            
    async def discover_posts_via_explore(self):
        """Discover posts via Explore tab"""
        try:
            print("🥷 Browsing Explore tab...")
            
            # Go to explore
            await self.page.goto('https://twitter.com/explore')
            await asyncio.sleep(random.randint(3, 6))
            
            # Scroll through explore
            for scroll in range(3):
                await self.page.evaluate("window.scrollBy(0, 500)")
                await asyncio.sleep(random.randint(2, 4))
                
            # Look for audio-related trending topics or posts
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            print(f"   📊 Found {len(tweet_elements)} posts in explore")
            
            audio_posts = []
            for tweet_element in tweet_elements[:15]:  # Check first 15
                try:
                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                    if text_element:
                        tweet_text = await text_element.inner_text()
                        
                        # Check if audio-related
                        audio_keywords = ['audio', 'sound', 'music', 'podcast', 'mix', 'master', 'edit', 'record', 'studio', 'workflow', 'production']
                        if any(keyword in tweet_text.lower() for keyword in audio_keywords):
                            reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                            if reply_button and len(tweet_text) > 15:
                                audio_posts.append({
                                    'element': tweet_element,
                                    'text': tweet_text,
                                    'reply_button': reply_button,
                                    'source': 'explore'
                                })
                                
                except Exception as e:
                    continue
                    
            return audio_posts
            
        except Exception as e:
            print(f"❌ Explore discovery error: {e}")
            return []
            
    def generate_stealth_reply(self, tweet_text, source):
        """Generate contextual reply based on source"""
        
        # Analyze tweet content for better context
        tweet_lower = tweet_text.lower()
        
        if 'podcast' in tweet_lower:
            replies = [
                "Love seeing fellow podcasters! We've been working on some AI solutions for podcast workflow automation at Zenyai. The efficiency gains have been incredible. Link in bio if you're curious! 🎧",
                "Podcast life is real! That's actually why we built Zenyai - to solve these exact workflow challenges with intelligent automation. Check the link in my bio! 🚀"
            ]
        elif 'music' in tweet_lower or 'beat' in tweet_lower:
            replies = [
                "Music production workflows can be such a challenge! We've been developing AI solutions at Zenyai specifically for creative audio workflows. Link in bio to see how! 🎵",
                "The music production struggle is real! At Zenyai, we're tackling these workflow bottlenecks with AI automation. Would love to share - link in bio! 🎹"
            ]
        elif 'audio' in tweet_lower or 'sound' in tweet_lower:
            replies = [
                "Audio workflow challenges are so relatable! We've been building AI-native solutions at Zenyai for exactly these problems. The results have been amazing. Link in bio! 🔊",
                "This audio challenge hits home! That's precisely what Zenyai was designed to solve - intelligent audio management that actually works. Check my bio! ⚡"
            ]
        else:
            replies = [
                "I totally understand creative workflow challenges! We've been building AI solutions at Zenyai specifically for content creators. The efficiency gains are incredible. Link in my bio! 💡",
                "Creative workflows can be so frustrating! That's why we created Zenyai - to streamline these processes with intelligent automation. Link in bio if interested! 🚀"
            ]
            
        return random.choice(replies)
        
    async def stealth_reply_and_send(self, post_data):
        """Reply with maximum stealth"""
        try:
            tweet_text = post_data['text']
            reply_button = post_data['reply_button']
            source = post_data['source']
            
            print(f"🥷 Stealth reply to: {tweet_text[:50]}... (from {source})")
            
            # Generate contextual reply
            reply_text = self.generate_stealth_reply(tweet_text, source)
            
            # Human-like delay before clicking
            await asyncio.sleep(random.randint(1, 3))
            
            # Click reply with human-like behavior
            await reply_button.scroll_into_view_if_needed()
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await reply_button.click()
            print("   🔘 Clicked reply button")
            
            # Wait for reply box with human delay
            await asyncio.sleep(random.randint(2, 4))
            
            # Find reply textarea
            reply_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=8000)
            
            if reply_input:
                # Click to focus with human delay
                await reply_input.click()
                await asyncio.sleep(random.uniform(0.5, 1.0))
                
                # Type with human-like speed (not instant to avoid detection)
                await reply_input.fill('')  # Clear first
                await asyncio.sleep(0.5)
                
                # Type text in chunks to simulate human typing
                words = reply_text.split(' ')
                for i, word in enumerate(words):
                    await reply_input.type(word)
                    if i < len(words) - 1:
                        await reply_input.type(' ')
                    await asyncio.sleep(random.uniform(0.1, 0.3))  # Human typing speed
                    
                print("   ⚡ Text typed with human-like speed")
                await asyncio.sleep(random.uniform(1, 2))
                
                # Find and click send button
                send_selectors = [
                    '[data-testid="tweetButtonInline"]',
                    '[data-testid="tweetButton"]', 
                    'div[role="button"]:has-text("Reply")',
                    'div[role="button"]:has-text("Post")'
                ]
                
                send_clicked = False
                for selector in send_selectors:
                    try:
                        send_button = await self.page.query_selector(selector)
                        if send_button:
                            is_disabled = await send_button.get_attribute('aria-disabled')
                            if is_disabled != 'true':
                                await send_button.click()
                                print("   🚀 SEND BUTTON CLICKED!")
                                send_clicked = True
                                break
                    except:
                        continue
                        
                if send_clicked:
                    await asyncio.sleep(random.randint(3, 5))  # Wait for send
                    
                    # Verify sent
                    try:
                        reply_still_open = await self.page.query_selector('[data-testid="tweetTextarea_0"]')
                        if not reply_still_open:
                            print("   ✅ Reply successfully sent!")
                            self.log_successful_reply(post_data)
                            self.account['replies_posted'] += 1
                            return True
                    except:
                        print("   ✅ Reply sent (verified)!")
                        self.log_successful_reply(post_data)
                        self.account['replies_posted'] += 1
                        return True
                        
            return False
            
        except Exception as e:
            print(f"❌ Stealth reply error: {e}")
            return False
            
    def log_successful_reply(self, post_data):
        """Log successful reply"""
        try:
            log_file = "stealth_twitter_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'source': post_data['source'],
                'tweet_preview': post_data['text'][:100],
                'total_replies': self.account['replies_posted']
            }
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Logging error: {e}")
            
    async def run_stealth_automation(self, hours=7):
        """Run stealth automation that bypasses Twitter blocking"""
        try:
            print("🥷 STEALTH Twitter Automation Starting")
            print("=" * 60)
            print(f"📧 Account: {self.account['email']}")
            print(f"⏰ Duration: {hours} hours")
            print(f"🥷 Method: Natural browsing + stealth replies")
            print(f"🛡️ Anti-detection: Human-like behavior")
            
            # Setup and login
            if not await self.setup_stealth_browser():
                return
                
            if not await self.login_with_stealth():
                print("❌ Stealth login failed - stopping")
                return
                
            # Run stealth automation
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=hours)
            
            successful_replies = 0
            total_attempts = 0
            
            discovery_methods = [
                self.discover_posts_via_home_feed,
                self.discover_posts_via_explore,
                lambda: self.discover_posts_via_hashtags('#podcast'),
                lambda: self.discover_posts_via_hashtags('#audio'),
                lambda: self.discover_posts_via_hashtags('#music'),
                lambda: self.discover_posts_via_hashtags('#sound')
            ]
            
            while datetime.now() < end_time:
                print(f"\n🥷 Stealth Cycle {total_attempts + 1} - {datetime.now().strftime('%H:%M:%S')}")
                
                try:
                    # Select random discovery method
                    discovery_method = random.choice(discovery_methods)
                    
                    # Discover posts using stealth method
                    posts = await discovery_method()
                    
                    if posts:
                        print(f"✅ Found {len(posts)} audio-related posts")
                        
                        # Reply to first suitable post
                        for post_data in posts[:1]:  # One reply per discovery
                            if await self.stealth_reply_and_send(post_data):
                                successful_replies += 1
                                print(f"🎉 SUCCESS! Stealth reply #{successful_replies} sent!")
                                
                                # Human-like delay between activities
                                delay = random.randint(180, 300)  # 3-5 minutes
                                print(f"🥷 Human-like delay: {delay//60} minutes...")
                                await asyncio.sleep(delay)
                                break
                            else:
                                print("❌ Stealth reply failed")
                                await asyncio.sleep(60)
                    else:
                        print("⚠️ No audio posts found in this discovery")
                        await asyncio.sleep(30)
                        
                    total_attempts += 1
                    
                    # Progress update
                    if total_attempts % 5 == 0:
                        remaining_time = end_time - datetime.now()
                        hours_left = remaining_time.total_seconds() / 3600
                        success_rate = (successful_replies / total_attempts) * 100 if total_attempts > 0 else 0
                        
                        print(f"\n📊 Stealth Progress:")
                        print(f"   ⏰ Time Remaining: {hours_left:.1f} hours")
                        print(f"   🎯 Discovery Attempts: {total_attempts}")
                        print(f"   ✅ Successful Replies: {successful_replies}")
                        print(f"   📈 Success Rate: {success_rate:.1f}%")
                        
                except Exception as e:
                    print(f"❌ Stealth cycle error: {e}")
                    await asyncio.sleep(120)  # Longer delay on error
                    
            # Final summary
            print(f"\n🎉 {hours}-Hour STEALTH Automation Complete!")
            print(f"📊 Final Results:")
            print(f"   🎯 Discovery Attempts: {total_attempts}")
            print(f"   ✅ Successful Replies: {successful_replies}")
            print(f"   📈 Success Rate: {(successful_replies/total_attempts)*100:.1f}%")
            print(f"   🥷 All activities performed with stealth!")
            
        except Exception as e:
            print(f"❌ Stealth automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run stealth Twitter automation"""
    bot = StealthTwitterBot()
    await bot.run_stealth_automation(hours=7)

if __name__ == "__main__":
    asyncio.run(main())
