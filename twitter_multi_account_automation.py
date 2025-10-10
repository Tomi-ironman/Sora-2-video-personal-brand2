#!/usr/bin/env python3
"""
Multi-Account Twitter Browser Automation
Rotates between 4 Twitter accounts for maximum reach and engagement
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

class MultiAccountTwitterBot:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_search_targets()
        self.current_account = 0
        
    def setup_accounts(self):
        """Setup all 4 Twitter accounts"""
        self.accounts = []
        
        for i in range(1, 5):
            email = os.getenv(f'TWITTER{i}_EMAIL')
            password = os.getenv(f'TWITTER{i}_PASSWORD')
            
            if email and email != f'your_twitter{i}_email@example.com':
                self.accounts.append({
                    'id': i,
                    'email': email,
                    'password': password,
                    'replies_posted': 0,
                    'last_used': None,
                    'status': 'ready'
                })
                
        print(f"✅ Loaded {len(self.accounts)} Twitter accounts")
        
    def setup_video_library(self):
        """Setup video library with different videos per account"""
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
        """Setup different search strategies per account"""
        self.search_strategies = {
            1: {  # Account 1: Audio Professionals
                "queries": [
                    "audio engineer workflow nightmare",
                    "mixing deadline stress help",
                    "mastering workflow chaos",
                    "studio file organization mess"
                ],
                "focus": "audio_professionals"
            },
            2: {  # Account 2: Podcast Creators
                "queries": [
                    "podcast editing workflow hell",
                    "episode organization disaster",
                    "podcast team collaboration nightmare",
                    "podcast file management chaos"
                ],
                "focus": "podcast_creators"
            },
            3: {  # Account 3: Sound Designers
                "queries": [
                    "sound design sample library mess",
                    "audio effects organization chaos",
                    "sound designer workflow pain",
                    "can't find my sound effects"
                ],
                "focus": "sound_designers"
            },
            4: {  # Account 4: Content Creators
                "queries": [
                    "content creator audio workflow",
                    "video audio editing nightmare",
                    "creator audio quality issues",
                    "audio workflow for creators"
                ],
                "focus": "content_creators"
            }
        }
        
    def get_next_account(self):
        """Get next account for rotation"""
        if not self.accounts:
            return None
            
        # Find account that hasn't been used recently
        available_accounts = []
        
        for account in self.accounts:
            if account['status'] == 'ready':
                if account['last_used'] is None:
                    available_accounts.append(account)
                else:
                    # Check if enough time has passed (2+ hours)
                    last_used = datetime.fromisoformat(account['last_used'])
                    if datetime.now() - last_used > timedelta(hours=2):
                        available_accounts.append(account)
                        
        if available_accounts:
            # Select account with least replies posted
            next_account = min(available_accounts, key=lambda x: x['replies_posted'])
            return next_account
        else:
            # If all accounts used recently, wait or use least recently used
            least_recent = min(self.accounts, key=lambda x: x['last_used'] or '2000-01-01')
            return least_recent
            
    async def setup_browser_for_account(self, account):
        """Setup browser session for specific account"""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                slow_mo=600,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-first-run'
                ]
            )
            
            # Create unique context for each account
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Account{account["id"]}'
            )
            
            self.page = await self.context.new_page()
            
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            print(f"🌐 Browser setup for Account {account['id']}: {account['email']}")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed for Account {account['id']}: {e}")
            return False
            
    async def autonomous_login_to_twitter(self, account):
        """Autonomous login with Google OAuth detection and fallback"""
        try:
            print(f"🔐 Autonomous login for Account {account['id']}: {account['email']}")
            
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            # Try Google OAuth first if Gmail account
            if '@gmail.com' in account['email']:
                if await self.try_google_oauth_login(account):
                    return True
                    
            # Fall back to email/password login
            if await self.try_email_password_login(account):
                return True
                
            # Final fallback to manual
            return await self.manual_login_fallback(account)
            
        except Exception as e:
            print(f"❌ Login error for Account {account['id']}: {e}")
            return await self.manual_login_fallback(account)
            
    async def try_google_oauth_login(self, account):
        """Try Google OAuth login"""
        try:
            print(f"🔗 Trying Google OAuth for Account {account['id']}")
            
            # Look for Google OAuth button
            google_selectors = [
                'div:has-text("Continue with Google")',
                'button:has-text("Continue with Google")',
                'a:has-text("Continue with Google")'
            ]
            
            for selector in google_selectors:
                try:
                    google_button = await self.page.query_selector(selector)
                    if google_button:
                        await google_button.click()
                        await asyncio.sleep(3)
                        
                        # Handle Google login
                        if 'accounts.google.com' in self.page.url:
                            # Fill email
                            email_input = await self.page.query_selector('input[type="email"]')
                            if email_input:
                                await email_input.fill(account['email'])
                                await asyncio.sleep(1)
                                
                                # Click Next
                                next_btn = await self.page.query_selector('#identifierNext')
                                if next_btn:
                                    await next_btn.click()
                                    await asyncio.sleep(3)
                                    
                                    # Fill password
                                    pwd_input = await self.page.query_selector('input[type="password"]')
                                    if pwd_input:
                                        await pwd_input.fill(account['password'])
                                        await asyncio.sleep(1)
                                        
                                        # Click Next
                                        pwd_next = await self.page.query_selector('#passwordNext')
                                        if pwd_next:
                                            await pwd_next.click()
                                            await asyncio.sleep(5)
                                            
                                            # Check if back on Twitter
                                            if 'twitter.com' in self.page.url and 'login' not in self.page.url:
                                                print(f"✅ Google OAuth successful for Account {account['id']}")
                                                return True
                        break
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"❌ Google OAuth failed for Account {account['id']}: {e}")
            return False
            
    async def try_email_password_login(self, account):
        """Try email/password login"""
        try:
            print(f"📧 Trying email/password for Account {account['id']}")
            
            # Find email input
            email_selectors = [
                'input[name="text"]',
                'input[autocomplete="username"]',
                'input[data-testid="ocfEnterTextTextInput"]'
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = await self.page.query_selector(selector)
                    if email_input:
                        break
                except:
                    continue
                    
            if email_input:
                await email_input.fill(account['email'])
                await asyncio.sleep(1)
                
                # Click Next
                next_button = await self.page.query_selector('div[role="button"]:has-text("Next")')
                if next_button:
                    await next_button.click()
                    await asyncio.sleep(3)
                    
                    # Find password input
                    password_input = await self.page.query_selector('input[type="password"]')
                    if password_input:
                        await password_input.fill(account['password'])
                        await asyncio.sleep(1)
                        
                        # Click Login
                        login_button = await self.page.query_selector('div[role="button"]:has-text("Log in")')
                        if login_button:
                            await login_button.click()
                            await asyncio.sleep(5)
                            
                            # Check success
                            if 'twitter.com' in self.page.url and 'login' not in self.page.url:
                                print(f"✅ Email/password successful for Account {account['id']}")
                                return True
                                
            return False
            
        except Exception as e:
            print(f"❌ Email/password failed for Account {account['id']}: {e}")
            return False
            
    async def manual_login_fallback(self, account):
        """Manual login fallback with user assistance"""
        try:
            print(f"\n🤖 MANUAL LOGIN REQUIRED - Account {account['id']}")
            print("=" * 50)
            print(f"📧 Account: {account['email']}")
            print("👀 Browser window is open - please complete login manually")
            print("✅ Once logged in and on Twitter homepage, press ENTER...")
            
            # Wait for user
            input(f"Press ENTER when Account {account['id']} is logged in: ")
            
            # Verify
            await asyncio.sleep(2)
            if 'twitter.com' in self.page.url and 'login' not in self.page.url:
                print(f"✅ Manual login confirmed for Account {account['id']}")
                return True
            else:
                # Double check with user
                confirm = input(f"Is Account {account['id']} logged in? (yes/no): ").lower().strip()
                return confirm in ['yes', 'y']
                
        except Exception as e:
            print(f"❌ Manual fallback failed for Account {account['id']}: {e}")
            return False
            
    async def run_account_session(self, account, session_duration_minutes=90):
        """Run engagement session for specific account"""
        try:
            print(f"\n🚀 Starting session for Account {account['id']}")
            print(f"📧 Email: {account['email']}")
            print(f"🎯 Focus: {self.search_strategies[account['id']]['focus']}")
            print(f"⏰ Duration: {session_duration_minutes} minutes")
            
            session_start = datetime.now()
            session_end = session_start + timedelta(minutes=session_duration_minutes)
            
            replies_this_session = 0
            queries = self.search_strategies[account['id']]['queries']
            
            while datetime.now() < session_end and replies_this_session < 8:  # Max 8 replies per session
                for query in queries[:2]:  # Limit queries per cycle
                    try:
                        print(f"\n🔍 Account {account['id']} searching: {query}")
                        
                        # Search for tweets
                        search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
                        await self.page.goto(search_url)
                        await asyncio.sleep(3)
                        
                        # Scroll to load tweets
                        for i in range(2):
                            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            await asyncio.sleep(2)
                            
                        # Find and reply to tweets
                        tweet_elements = await self.page.query_selector_all('[data-testid="tweet"]')
                        
                        if tweet_elements:
                            for tweet_element in tweet_elements[:2]:  # Max 2 replies per query
                                try:
                                    # Get tweet text
                                    text_element = await tweet_element.query_selector('[data-testid="tweetText"]')
                                    if text_element:
                                        tweet_text = await text_element.inner_text()
                                        
                                        # Get reply button
                                        reply_button = await tweet_element.query_selector('[data-testid="reply"]')
                                        
                                        if reply_button and len(tweet_text) > 20:  # Avoid very short tweets
                                            if await self.reply_to_tweet_with_video(tweet_text, reply_button, account):
                                                replies_this_session += 1
                                                account['replies_posted'] += 1
                                                
                                                # Log successful reply
                                                self.log_account_activity(account, query, tweet_text[:50])
                                                
                                                # Delay between replies
                                                delay = random.randint(180, 360)  # 3-6 minutes
                                                print(f"⏳ Account {account['id']} waiting {delay//60} minutes...")
                                                await asyncio.sleep(delay)
                                                
                                                break  # One reply per query
                                                
                                except Exception as e:
                                    print(f"❌ Tweet processing error: {e}")
                                    continue
                                    
                        # Delay between queries
                        await asyncio.sleep(random.randint(60, 120))
                        
                        # Check if session time is up
                        if datetime.now() >= session_end:
                            break
                            
                    except Exception as e:
                        print(f"❌ Query error for Account {account['id']}: {e}")
                        await asyncio.sleep(60)
                        
                # Break if session time is up
                if datetime.now() >= session_end:
                    break
                    
            # Update account status
            account['last_used'] = datetime.now().isoformat()
            account['status'] = 'cooldown'
            
            print(f"\n📊 Account {account['id']} session complete:")
            print(f"   💬 Replies posted: {replies_this_session}")
            print(f"   📈 Total replies: {account['replies_posted']}")
            print(f"   ⏰ Next available: {(datetime.now() + timedelta(hours=2)).strftime('%H:%M')}")
            
            return replies_this_session
            
        except Exception as e:
            print(f"❌ Session error for Account {account['id']}: {e}")
            return 0
            
    async def reply_to_tweet_with_video(self, tweet_text, reply_button, account):
        """Reply to tweet with appropriate video"""
        try:
            # Determine best video
            video_type = self.match_video_to_tweet(tweet_text)
            video_info = self.video_library[video_type]
            
            # Generate reply text
            reply_text = self.generate_authentic_reply(tweet_text, video_type, account)
            
            print(f"💬 Account {account['id']} replying with {video_type} video")
            
            # Click reply button
            await reply_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await reply_button.click()
            await asyncio.sleep(2)
            
            # Find reply input
            reply_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=5000)
            
            if reply_input:
                # Type reply
                await reply_input.click()
                await asyncio.sleep(1)
                
                # Type with human-like speed
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
                    try:
                        # Find file input
                        file_input = await self.page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(video_path)
                            print(f"📹 Account {account['id']} uploaded video")
                            await asyncio.sleep(4)  # Wait for upload
                    except Exception as e:
                        print(f"❌ Video upload failed: {e}")
                        
                # Post tweet
                tweet_button = await self.page.query_selector('[data-testid="tweetButtonInline"]')
                if tweet_button:
                    await tweet_button.click()
                    print(f"🚀 Account {account['id']} posted reply!")
                    await asyncio.sleep(3)
                    return True
                    
            return False
            
        except Exception as e:
            print(f"❌ Reply error for Account {account['id']}: {e}")
            return False
            
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
                
        return best_match if max_matches > 0 else "file_organization"
        
    def generate_authentic_reply(self, tweet_text, video_type, account):
        """Generate authentic reply text"""
        templates = [
            "I completely understand this struggle! Just created a video showing how AI can streamline {problem}. Hope this helps! 🎧",
            "This hits home! We've been tackling exactly this with Zenyai's AI-native approach. Check out this quick demo! 🚀",
            "Been there! Created a short video about solving {problem} efficiently. Might save you some headaches! 💡",
            "This is such a common pain point! Here's how we approach {problem} with AI automation. Take a look! ⚡"
        ]
        
        problem_map = {
            "file_organization": "audio file chaos",
            "sound_design": "sound design workflow",
            "audio_professional": "audio workflow burnout", 
            "podcast_workflow": "podcast management"
        }
        
        template = random.choice(templates)
        problem = problem_map.get(video_type, "workflow optimization")
        
        return template.format(problem=problem)
        
    def log_account_activity(self, account, query, tweet_preview):
        """Log account activity"""
        try:
            log_file = "multi_account_twitter_log.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'account_id': account['id'],
                'account_email': account['email'],
                'query': query,
                'tweet_preview': tweet_preview,
                'total_replies': account['replies_posted']
            }
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Logging error: {e}")
            
    async def run_multi_account_automation(self, total_hours=7):
        """Run multi-account automation for specified hours"""
        try:
            print("🚀 Multi-Account Twitter Automation")
            print("=" * 50)
            print(f"📊 Accounts loaded: {len(self.accounts)}")
            print(f"⏰ Total duration: {total_hours} hours")
            print(f"🎯 Expected replies: {len(self.accounts) * 8 * (total_hours // 2)} (approx)")
            
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=total_hours)
            
            total_replies = 0
            cycle_count = 0
            
            while datetime.now() < end_time:
                cycle_count += 1
                print(f"\n🔄 CYCLE {cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Get next available account
                account = self.get_next_account()
                
                if account:
                    try:
                        # Setup browser for this account
                        if await self.setup_browser_for_account(account):
                            
                            # Autonomous login to Twitter
                            if await self.autonomous_login_to_twitter(account):
                                
                                # Run engagement session (90 minutes)
                                session_replies = await self.run_account_session(account, 90)
                                total_replies += session_replies
                                
                            # Close browser
                            await self.browser.close()
                            await self.playwright.stop()
                            
                    except Exception as e:
                        print(f"❌ Account {account['id']} error: {e}")
                        
                    # Progress update
                    remaining_time = end_time - datetime.now()
                    hours_left = remaining_time.total_seconds() / 3600
                    
                    print(f"\n📊 Progress Update:")
                    print(f"   ⏰ Time Remaining: {hours_left:.1f} hours")
                    print(f"   🔄 Cycles Completed: {cycle_count}")
                    print(f"   💬 Total Replies: {total_replies}")
                    print(f"   📈 Replies/Hour: {total_replies/(total_hours-hours_left):.1f}")
                    
                else:
                    print("⏳ All accounts in cooldown - waiting 30 minutes...")
                    await asyncio.sleep(1800)  # 30 minutes
                    
            # Final summary
            print(f"\n🎉 {total_hours}-Hour Multi-Account Automation Complete!")
            print(f"📊 Final Results:")
            print(f"   🔄 Cycles: {cycle_count}")
            print(f"   💬 Total Replies: {total_replies}")
            print(f"   📈 Average per Account: {total_replies/len(self.accounts):.1f}")
            
            # Account summary
            print(f"\n👥 Account Performance:")
            for account in self.accounts:
                print(f"   Account {account['id']}: {account['replies_posted']} replies")
                
        except Exception as e:
            print(f"❌ Multi-account automation error: {e}")

async def main():
    """Run multi-account Twitter automation"""
    bot = MultiAccountTwitterBot()
    
    if len(bot.accounts) == 0:
        print("❌ No Twitter accounts configured!")
        print("Please add your Twitter credentials to .env file")
        return
        
    await bot.run_multi_account_automation(total_hours=7)

if __name__ == "__main__":
    asyncio.run(main())
