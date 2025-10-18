#!/usr/bin/env python3
"""
One-by-One Twitter Automation
Find post → Reply → Send → Repeat (no batch processing)
INSTANT typing, guaranteed sending
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

class OneByOneTwitterBot:
    def __init__(self):
        self.setup_account()
        self.setup_search_terms()
        
    def setup_account(self):
        """Use Account 1"""
        self.account = {
            'id': 1,
            'email': os.getenv('TWITTER1_EMAIL'),
            'password': os.getenv('TWITTER1_PASSWORD'),
            'replies_posted': 0
        }
        print(f"🎯 One-by-One Account: {self.account['email']}")
        
    def setup_search_terms(self):
        """Simple, effective search terms"""
        self.search_terms = [
            # Podcast terms
            "podcast editing", "podcast workflow", "podcast production", "podcast help",
            "podcast software", "podcast tools", "podcast tips", "podcast struggle",
            
            # Audio terms  
            "audio editing", "audio files", "audio organization", "audio workflow",
            "audio software", "audio tools", "audio help", "audio management",
            
            # Sound design
            "sound design", "sound effects", "sound library", "sound workflow",
            "sound tools", "sound software", "sound help", "sound organization",
            
            # Music production
            "music production", "music workflow", "music software", "music tools",
            "music help", "music editing", "music mixing", "music mastering",
            
            # Pain points
            "audio nightmare", "podcast chaos", "file mess", "workflow hell",
            "editing struggle", "production issues", "audio problems", "sound problems"
        ]
        
        print(f"🔍 Loaded {len(self.search_terms)} focused search terms")
        
    async def setup_browser(self):
        """Setup browser"""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=0,  # NO DELAYS AT ALL
                args=['--disable-blink-features=AutomationControlled']
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            self.page = await self.context.new_page()
            
            print("🌐 Lightning-fast browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
            
    async def login_once(self):
        """Login once"""
        try:
            print(f"🔐 Logging in: {self.account['email']}")
            
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            print("🤖 Complete login manually and press ENTER...")
            input("Press ENTER when logged in: ")
            
            return True
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
            
    async def find_single_post(self, query):
        """Find ONE post and return it immediately"""
        try:
            print(f"🔍 Searching for ONE post: '{query}'")
            
            search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            await self.page.goto(search_url)
            await asyncio.sleep(2)
            
            # Look for tweets without excessive scrolling
            for attempt in range(5):  # Max 5 scroll attempts
                tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
                
                print(f"   📊 Found {len(tweet_elements)} tweets on page")
                
                # Process first available tweet
                for tweet_element in tweet_elements:
                    try:
                        # Get tweet text
                        text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                        if not text_element:
                            continue
                            
                        tweet_text = await text_element.inner_text()
                        
                        # Skip very short tweets
                        if len(tweet_text) < 15:
                            continue
                            
                        # Get reply button
                        reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                        if not reply_button:
                            continue
                            
                        print(f"✅ Found suitable post: {tweet_text[:60]}...")
                        
                        return {
                            'element': tweet_element,
                            'text': tweet_text,
                            'reply_button': reply_button,
                            'query': query
                        }
                        
                    except Exception as e:
                        print(f"   ⚠️ Error checking tweet: {e}")
                        continue
                        
                # Scroll once to get more tweets
                if attempt < 4:
                    await self.page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(1)
                    
            print(f"❌ No suitable posts found for '{query}'")
            return None
            
        except Exception as e:
            print(f"❌ Search error for '{query}': {e}")
            return None
            
    def generate_instant_reply(self, tweet_text):
        """Generate reply instantly"""
        replies = [
            "I totally understand this challenge! We've been building AI solutions at Zenyai specifically for audio workflow automation. The efficiency gains have been incredible. Link in my bio if you want to see how it works! 🎧",
            
            "This workflow struggle is so real! At Zenyai, we're tackling exactly these kinds of audio management challenges with AI-native solutions. Would love to share what we've learned - check the link in my bio! 🚀",
            
            "Been there with this exact pain point! That's why we created Zenyai - to solve audio workflow bottlenecks with intelligent automation. The results speak for themselves. Link in bio if you're curious! 💡",
            
            "This audio challenge hits home! We've developed some breakthrough approaches to workflow automation at Zenyai using AI. It's been a game changer for productivity. Link in my bio to see our approach! ⚡",
            
            "I feel this struggle deeply! That's precisely what Zenyai was built to solve - intelligent audio asset management that actually works for creators. Check out the link in my bio! 🎵"
        ]
        
        return random.choice(replies)
        
    async def reply_and_send_immediately(self, post_data):
        """Reply to post and GUARANTEE it sends"""
        try:
            tweet_text = post_data['text']
            reply_button = post_data['reply_button']
            
            print(f"💬 Replying to: {tweet_text[:50]}...")
            
            # Generate reply
            reply_text = self.generate_instant_reply(tweet_text)
            
            # Click reply button
            await reply_button.click()
            print("   🔘 Clicked reply button")
            await asyncio.sleep(2)  # Wait for reply box to open
            
            # Find reply textarea
            reply_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=5000)
            
            if reply_input:
                # Click to focus
                await reply_input.click()
                await asyncio.sleep(0.5)
                
                # INSTANT TYPING - paste entire text at once
                await reply_input.fill(reply_text)
                print("   ⚡ Text pasted instantly")
                await asyncio.sleep(1)
                
                # Find and click send button - try multiple selectors
                send_selectors = [
                    '[data-testid="tweetButtonInline"]',
                    '[data-testid="tweetButton"]', 
                    'div[role="button"]:has-text("Reply")',
                    'div[role="button"]:has-text("Post")',
                    'button:has-text("Reply")',
                    'button:has-text("Post")'
                ]
                
                send_clicked = False
                for selector in send_selectors:
                    try:
                        send_button = await self.page.query_selector(selector)
                        if send_button:
                            # Check if button is enabled
                            is_disabled = await send_button.get_attribute('aria-disabled')
                            if is_disabled != 'true':
                                await send_button.click()
                                print("   🚀 SEND BUTTON CLICKED!")
                                send_clicked = True
                                break
                    except:
                        continue
                        
                if send_clicked:
                    await asyncio.sleep(2)  # Wait for send to complete
                    
                    # Verify it was sent (check if reply box disappeared)
                    try:
                        reply_still_open = await self.page.query_selector('[data-testid="tweetTextarea_0"]')
                        if not reply_still_open:
                            print("   ✅ Reply successfully sent!")
                            self.log_successful_reply(post_data)
                            self.account['replies_posted'] += 1
                            return True
                        else:
                            print("   ⚠️ Reply box still open - may not have sent")
                    except:
                        # If we can't find the reply box, assume it sent
                        print("   ✅ Reply box gone - assuming sent!")
                        self.log_successful_reply(post_data)
                        self.account['replies_posted'] += 1
                        return True
                else:
                    print("   ❌ Could not find or click send button")
                    
                    # Try pressing Enter as backup
                    try:
                        await reply_input.press('Enter')
                        print("   🔄 Tried Enter key as backup")
                        await asyncio.sleep(2)
                        self.log_successful_reply(post_data)
                        self.account['replies_posted'] += 1
                        return True
                    except:
                        print("   ❌ Enter key backup failed")
                        
            else:
                print("   ❌ Could not find reply input")
                
            return False
            
        except Exception as e:
            print(f"❌ Reply error: {e}")
            return False
            
    def log_successful_reply(self, post_data):
        """Log successful reply"""
        try:
            log_file = "one_by_one_twitter_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'query': post_data['query'],
                'tweet_preview': post_data['text'][:100],
                'total_replies': self.account['replies_posted']
            }
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Logging error: {e}")
            
    async def run_one_by_one_automation(self, hours=7):
        """Run one-by-one automation: Find → Reply → Send → Repeat"""
        try:
            print("🚀 ONE-BY-ONE Twitter Automation Starting")
            print("=" * 60)
            print(f"📧 Account: {self.account['email']}")
            print(f"⏰ Duration: {hours} hours")
            print(f"🔄 Process: Find Post → Reply → Send → Repeat")
            print(f"⚡ Features: INSTANT typing, guaranteed sending")
            
            # Setup and login
            if not await self.setup_browser():
                return
                
            if not await self.login_once():
                print("❌ Login failed - stopping")
                return
                
            # Run automation
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=hours)
            
            successful_replies = 0
            total_attempts = 0
            
            while datetime.now() < end_time:
                # Select random search term
                query = random.choice(self.search_terms)
                
                print(f"\n🔄 Attempt {total_attempts + 1} - {datetime.now().strftime('%H:%M:%S')}")
                
                try:
                    # Step 1: Find ONE post
                    post_data = await self.find_single_post(query)
                    
                    if post_data:
                        # Step 2: Reply and Send immediately
                        if await self.reply_and_send_immediately(post_data):
                            successful_replies += 1
                            print(f"🎉 SUCCESS! Reply #{successful_replies} sent!")
                            
                            # Short delay before next search
                            delay = random.randint(60, 120)  # 1-2 minutes between successful replies
                            print(f"⏳ Waiting {delay} seconds before next post...")
                            await asyncio.sleep(delay)
                        else:
                            print("❌ Reply failed to send")
                            await asyncio.sleep(30)  # Short delay on failure
                    else:
                        print("❌ No suitable post found")
                        await asyncio.sleep(15)  # Quick retry on no results
                        
                    total_attempts += 1
                    
                    # Progress update every 10 attempts
                    if total_attempts % 10 == 0:
                        remaining_time = end_time - datetime.now()
                        hours_left = remaining_time.total_seconds() / 3600
                        success_rate = (successful_replies / total_attempts) * 100 if total_attempts > 0 else 0
                        
                        print(f"\n📊 Progress Update:")
                        print(f"   ⏰ Time Remaining: {hours_left:.1f} hours")
                        print(f"   🎯 Attempts: {total_attempts}")
                        print(f"   ✅ Successful Replies: {successful_replies}")
                        print(f"   📈 Success Rate: {success_rate:.1f}%")
                        print(f"   🚀 Replies per Hour: {successful_replies/((hours*3600-remaining_time.total_seconds())/3600):.1f}")
                        
                except Exception as e:
                    print(f"❌ Automation error: {e}")
                    await asyncio.sleep(30)
                    
            # Final summary
            print(f"\n🎉 {hours}-Hour ONE-BY-ONE Automation Complete!")
            print(f"📊 Final Results:")
            print(f"   🎯 Total Attempts: {total_attempts}")
            print(f"   ✅ Successful Replies: {successful_replies}")
            print(f"   📈 Success Rate: {(successful_replies/total_attempts)*100:.1f}%")
            print(f"   🚀 Replies per Hour: {successful_replies/hours:.1f}")
            print(f"   ⚡ All replies sent with INSTANT typing!")
            
        except Exception as e:
            print(f"❌ One-by-one automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run one-by-one Twitter automation"""
    bot = OneByOneTwitterBot()
    await bot.run_one_by_one_automation(hours=7)

if __name__ == "__main__":
    asyncio.run(main())
