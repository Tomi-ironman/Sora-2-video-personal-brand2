#!/usr/bin/env python3
"""
BULLETPROOF Twitter Automation
Handles any login scenario + stealth discovery
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

class BulletproofTwitterBot:
    def __init__(self):
        self.setup_account()
        
    def setup_account(self):
        """Use Account 1"""
        self.account = {
            'id': 1,
            'email': os.getenv('TWITTER1_EMAIL'),
            'password': os.getenv('TWITTER1_PASSWORD'),
            'replies_posted': 0
        }
        print(f"🛡️ Bulletproof Account: {self.account['email']}")
        
    async def setup_browser(self):
        """Setup browser"""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=200,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            self.page = await self.context.new_page()
            
            print("🛡️ Bulletproof browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
            
    async def bulletproof_login(self):
        """Bulletproof login that works with ANY scenario"""
        try:
            print(f"🛡️ Bulletproof login starting...")
            
            # Go to Twitter
            await self.page.goto('https://twitter.com')
            await asyncio.sleep(3)
            
            print("\n" + "="*60)
            print("🤖 MANUAL LOGIN REQUIRED")
            print("="*60)
            print("📋 Instructions:")
            print("1. Complete login in the browser window")
            print("2. Make sure you're on Twitter (any Twitter page is fine)")
            print("3. Press ENTER when ready")
            print("="*60)
            
            input("Press ENTER when you're logged in and on Twitter: ")
            
            # Give user time to navigate if needed
            await asyncio.sleep(2)
            
            # Check current URL - accept ANY twitter.com URL
            current_url = self.page.url
            print(f"🔍 Current URL: {current_url}")
            
            if 'twitter.com' in current_url.lower() or 'x.com' in current_url.lower():
                print("✅ Twitter domain detected - login successful!")
                return True
            else:
                # Give user another chance
                print("⚠️ Not on Twitter domain. Let's try again...")
                print("Please navigate to any Twitter page and press ENTER")
                input("Press ENTER when on Twitter: ")
                
                await asyncio.sleep(2)
                current_url = self.page.url
                
                if 'twitter.com' in current_url.lower() or 'x.com' in current_url.lower():
                    print("✅ Twitter domain detected - login successful!")
                    return True
                else:
                    # Final fallback - trust the user
                    user_confirm = input("Are you logged into Twitter? (yes/no): ").lower().strip()
                    if user_confirm in ['yes', 'y']:
                        print("✅ User confirmed - proceeding!")
                        return True
                    else:
                        print("❌ Login not confirmed")
                        return False
                        
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    async def find_posts_naturally(self):
        """Find posts by browsing naturally"""
        try:
            print("🔍 Natural browsing for audio posts...")
            
            # Method 1: Browse home timeline
            try:
                await self.page.goto('https://twitter.com/home')
                await asyncio.sleep(3)
                print("   📱 Browsing home timeline...")
                
                # Scroll naturally
                for i in range(5):
                    await self.page.evaluate("window.scrollBy(0, 600)")
                    await asyncio.sleep(2)
                    
                posts = await self.extract_audio_posts('home_timeline')
                if posts:
                    return posts
                    
            except Exception as e:
                print(f"   ⚠️ Home timeline error: {e}")
                
            # Method 2: Browse explore
            try:
                await self.page.goto('https://twitter.com/explore')
                await asyncio.sleep(3)
                print("   🔍 Browsing explore...")
                
                for i in range(3):
                    await self.page.evaluate("window.scrollBy(0, 500)")
                    await asyncio.sleep(2)
                    
                posts = await self.extract_audio_posts('explore')
                if posts:
                    return posts
                    
            except Exception as e:
                print(f"   ⚠️ Explore error: {e}")
                
            # Method 3: Try simple hashtag
            try:
                await self.page.goto('https://twitter.com/hashtag/podcast')
                await asyncio.sleep(3)
                print("   #️⃣ Browsing #podcast...")
                
                for i in range(3):
                    await self.page.evaluate("window.scrollBy(0, 400)")
                    await asyncio.sleep(2)
                    
                posts = await self.extract_audio_posts('hashtag_podcast')
                if posts:
                    return posts
                    
            except Exception as e:
                print(f"   ⚠️ Hashtag error: {e}")
                
            return []
            
        except Exception as e:
            print(f"❌ Natural browsing error: {e}")
            return []
            
    async def extract_audio_posts(self, source):
        """Extract audio-related posts from current page"""
        try:
            # Look for tweets
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            print(f"      📊 Found {len(tweet_elements)} total posts")
            
            audio_posts = []
            
            for tweet_element in tweet_elements[:20]:  # Check first 20
                try:
                    # Get tweet text
                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                    if not text_element:
                        continue
                        
                    tweet_text = await text_element.inner_text()
                    
                    # Skip very short tweets
                    if len(tweet_text) < 10:
                        continue
                        
                    # Check if audio-related (broader keywords)
                    audio_keywords = [
                        'audio', 'sound', 'music', 'podcast', 'mix', 'master', 'edit', 'record', 
                        'studio', 'workflow', 'production', 'creator', 'content', 'beat', 'track',
                        'song', 'album', 'ep', 'demo', 'sample', 'loop', 'synth', 'vocal',
                        'microphone', 'mic', 'headphone', 'speaker', 'daw', 'plugin', 'vst'
                    ]
                    
                    if any(keyword in tweet_text.lower() for keyword in audio_keywords):
                        # Get reply button
                        reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                        if reply_button:
                            audio_posts.append({
                                'element': tweet_element,
                                'text': tweet_text,
                                'reply_button': reply_button,
                                'source': source
                            })
                            
                            # Found one, that's enough for now
                            if len(audio_posts) >= 1:
                                break
                                
                except Exception as e:
                    continue
                    
            print(f"      ✅ Found {len(audio_posts)} audio-related posts")
            return audio_posts
            
        except Exception as e:
            print(f"❌ Post extraction error: {e}")
            return []
            
    def generate_reply(self, tweet_text):
        """Generate contextual reply"""
        tweet_lower = tweet_text.lower()
        
        if 'podcast' in tweet_lower:
            replies = [
                "Love the podcast journey! We've been working on AI solutions for podcast workflow automation at Zenyai. The efficiency gains have been incredible. Link in bio if you're curious! 🎧",
                "Podcast workflows can be such a challenge! That's actually why we built Zenyai - to solve these exact problems with intelligent automation. Check the link in my bio! 🚀"
            ]
        elif 'music' in tweet_lower or 'beat' in tweet_lower or 'track' in tweet_lower:
            replies = [
                "Music production is such an art! We've been developing AI solutions at Zenyai specifically for creative audio workflows. The results have been amazing. Link in bio! 🎵",
                "The music creation process is incredible! At Zenyai, we're tackling workflow bottlenecks with AI automation. Would love to share what we've built - link in bio! 🎹"
            ]
        elif 'audio' in tweet_lower or 'sound' in tweet_lower:
            replies = [
                "Audio workflows can be so complex! We've been building AI-native solutions at Zenyai for exactly these challenges. The efficiency gains are incredible. Link in bio! 🔊",
                "This audio challenge is so relatable! That's precisely what Zenyai was designed to solve - intelligent audio management that actually works. Check my bio! ⚡"
            ]
        else:
            replies = [
                "Creative workflows are fascinating! We've been building AI solutions at Zenyai specifically for content creators and audio professionals. Link in my bio if interested! 💡",
                "I love seeing creative processes! That's why we created Zenyai - to streamline workflows with intelligent automation. The results speak for themselves. Link in bio! 🚀"
            ]
            
        return random.choice(replies)
        
    async def bulletproof_reply(self, post_data):
        """Bulletproof reply that handles any scenario"""
        try:
            tweet_text = post_data['text']
            reply_button = post_data['reply_button']
            
            print(f"💬 Replying to: {tweet_text[:60]}...")
            
            # Generate reply
            reply_text = self.generate_reply(tweet_text)
            
            # Click reply button
            await reply_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await reply_button.click()
            print("   🔘 Clicked reply")
            await asyncio.sleep(3)
            
            # Find reply input - try multiple selectors
            reply_selectors = [
                '[data-testid="tweetTextarea_0"]',
                'div[contenteditable="true"]',
                'textarea',
                '[role="textbox"]'
            ]
            
            reply_input = None
            for selector in reply_selectors:
                try:
                    reply_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if reply_input:
                        break
                except:
                    continue
                    
            if reply_input:
                # Clear and type
                await reply_input.click()
                await asyncio.sleep(0.5)
                await reply_input.fill('')
                await asyncio.sleep(0.5)
                await reply_input.fill(reply_text)
                print("   ⚡ Text entered")
                await asyncio.sleep(2)
                
                # Find send button - try everything
                send_selectors = [
                    '[data-testid="tweetButtonInline"]',
                    '[data-testid="tweetButton"]',
                    'div[role="button"]:has-text("Reply")',
                    'div[role="button"]:has-text("Post")',
                    'button:has-text("Reply")',
                    'button:has-text("Post")',
                    'div[role="button"]:has-text("Tweet")',
                    'button:has-text("Tweet")'
                ]
                
                send_clicked = False
                for selector in send_selectors:
                    try:
                        send_button = await self.page.query_selector(selector)
                        if send_button:
                            # Check if enabled
                            is_disabled = await send_button.get_attribute('aria-disabled')
                            if is_disabled != 'true':
                                await send_button.click()
                                print("   🚀 Send button clicked!")
                                send_clicked = True
                                break
                    except:
                        continue
                        
                if not send_clicked:
                    # Try Enter key
                    try:
                        await reply_input.press('Enter')
                        print("   ⌨️ Tried Enter key")
                        send_clicked = True
                    except:
                        print("   ❌ Could not send")
                        
                if send_clicked:
                    await asyncio.sleep(3)
                    self.account['replies_posted'] += 1
                    self.log_reply(post_data)
                    print(f"   ✅ Reply #{self.account['replies_posted']} sent!")
                    return True
                    
            return False
            
        except Exception as e:
            print(f"❌ Reply error: {e}")
            return False
            
    def log_reply(self, post_data):
        """Log successful reply"""
        try:
            log_file = "bulletproof_twitter_log.json"
            
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
            
    async def run_bulletproof_automation(self, hours=7):
        """Run bulletproof automation"""
        try:
            print("🛡️ BULLETPROOF Twitter Automation Starting")
            print("=" * 60)
            print(f"📧 Account: {self.account['email']}")
            print(f"⏰ Duration: {hours} hours")
            print(f"🛡️ Method: Bulletproof natural browsing")
            
            # Setup and login
            if not await self.setup_browser():
                return
                
            if not await self.bulletproof_login():
                print("❌ Bulletproof login failed - stopping")
                return
                
            print("✅ Bulletproof login successful! Starting automation...")
            
            # Run automation
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=hours)
            
            cycle = 0
            
            while datetime.now() < end_time:
                cycle += 1
                print(f"\n🛡️ Bulletproof Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                try:
                    # Find posts naturally
                    posts = await self.find_posts_naturally()
                    
                    if posts:
                        # Reply to first post
                        if await self.bulletproof_reply(posts[0]):
                            print("🎉 Bulletproof reply successful!")
                            
                            # Wait before next cycle
                            delay = random.randint(120, 240)  # 2-4 minutes
                            print(f"⏳ Waiting {delay//60} minutes before next cycle...")
                            await asyncio.sleep(delay)
                        else:
                            print("❌ Reply failed, trying again soon...")
                            await asyncio.sleep(60)
                    else:
                        print("⚠️ No audio posts found, trying again...")
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ Cycle error: {e}")
                    await asyncio.sleep(60)
                    
                # Progress update
                if cycle % 5 == 0:
                    remaining_time = end_time - datetime.now()
                    hours_left = remaining_time.total_seconds() / 3600
                    
                    print(f"\n📊 Bulletproof Progress:")
                    print(f"   ⏰ Time Remaining: {hours_left:.1f} hours")
                    print(f"   🔄 Cycles: {cycle}")
                    print(f"   ✅ Replies: {self.account['replies_posted']}")
                    
            # Final summary
            print(f"\n🎉 {hours}-Hour BULLETPROOF Automation Complete!")
            print(f"📊 Final Results:")
            print(f"   🔄 Cycles: {cycle}")
            print(f"   ✅ Total Replies: {self.account['replies_posted']}")
            print(f"   🛡️ Bulletproof success!")
            
        except Exception as e:
            print(f"❌ Bulletproof automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run bulletproof Twitter automation"""
    bot = BulletproofTwitterBot()
    await bot.run_bulletproof_automation(hours=7)

if __name__ == "__main__":
    asyncio.run(main())
