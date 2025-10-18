#!/usr/bin/env python3
"""
Autonomous Twitter Login System
Handles Google OAuth, detects human verification, falls back to manual when needed
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

class AutonomousTwitterLogin:
    def __init__(self):
        self.setup_accounts()
        
    def setup_accounts(self):
        """Setup all Twitter accounts"""
        self.accounts = []
        
        for i in range(1, 5):
            email = os.getenv(f'TWITTER{i}_EMAIL')
            password = os.getenv(f'TWITTER{i}_PASSWORD')
            
            if email and email != f'your_twitter{i}_email@example.com':
                self.accounts.append({
                    'id': i,
                    'email': email,
                    'password': password,
                    'login_method': 'unknown',  # Will detect: google_oauth, email_password, manual
                    'last_login': None,
                    'login_success_rate': 0,
                    'status': 'ready'
                })
                
        print(f"✅ Loaded {len(self.accounts)} accounts for autonomous login")
        
    async def setup_stealth_browser(self, account):
        """Setup stealth browser for autonomous operation"""
        try:
            self.playwright = await async_playwright().start()
            
            # Enhanced stealth settings
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Keep visible for manual fallback
                slow_mo=400,     # Faster than manual but still human-like
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--no-first-run',
                    '--disable-extensions',
                    '--disable-default-apps'
                ]
            )
            
            # Unique context per account
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Account{account["id"]}',
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            self.page = await self.context.new_page()
            
            # Advanced anti-detection
            await self.page.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Mock languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            """)
            
            print(f"🌐 Stealth browser ready for Account {account['id']}")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed for Account {account['id']}: {e}")
            return False
            
    async def detect_login_method(self, account):
        """Detect available login methods on Twitter"""
        try:
            print(f"🔍 Detecting login methods for Account {account['id']}")
            
            await self.page.goto('https://twitter.com/login')
            await asyncio.sleep(3)
            
            # Check for Google OAuth button
            google_selectors = [
                'div:has-text("Continue with Google")',
                'button:has-text("Continue with Google")',
                'a:has-text("Continue with Google")',
                '[data-testid="google-auth"]'
            ]
            
            google_available = False
            for selector in google_selectors:
                try:
                    google_button = await self.page.query_selector(selector)
                    if google_button:
                        google_available = True
                        print(f"✅ Google OAuth available for Account {account['id']}")
                        break
                except:
                    continue
                    
            # Check for email/password login
            email_selectors = [
                'input[name="text"]',
                'input[autocomplete="username"]',
                'input[data-testid="ocfEnterTextTextInput"]'
            ]
            
            email_available = False
            for selector in email_selectors:
                try:
                    email_input = await self.page.query_selector(selector)
                    if email_input:
                        email_available = True
                        print(f"✅ Email/password login available for Account {account['id']}")
                        break
                except:
                    continue
                    
            # Determine best method
            if google_available and '@gmail.com' in account['email']:
                account['login_method'] = 'google_oauth'
                print(f"🎯 Account {account['id']} will use Google OAuth")
            elif email_available:
                account['login_method'] = 'email_password'
                print(f"🎯 Account {account['id']} will use email/password")
            else:
                account['login_method'] = 'manual'
                print(f"⚠️ Account {account['id']} requires manual login")
                
            return account['login_method']
            
        except Exception as e:
            print(f"❌ Login method detection failed for Account {account['id']}: {e}")
            account['login_method'] = 'manual'
            return 'manual'
            
    async def attempt_google_oauth_login(self, account):
        """Attempt Google OAuth login"""
        try:
            print(f"🔐 Attempting Google OAuth for Account {account['id']}")
            
            # Find and click Google OAuth button
            google_selectors = [
                'div:has-text("Continue with Google")',
                'button:has-text("Continue with Google")',
                'a:has-text("Continue with Google")'
            ]
            
            google_button = None
            for selector in google_selectors:
                try:
                    google_button = await self.page.query_selector(selector)
                    if google_button:
                        break
                except:
                    continue
                    
            if google_button:
                await google_button.click()
                print(f"🔗 Clicked Google OAuth for Account {account['id']}")
                await asyncio.sleep(3)
                
                # Handle Google login page
                current_url = self.page.url
                if 'accounts.google.com' in current_url:
                    print(f"🌐 Redirected to Google OAuth for Account {account['id']}")
                    
                    # Check for email input
                    email_input = await self.page.query_selector('input[type="email"]')
                    if email_input:
                        await email_input.fill(account['email'])
                        await asyncio.sleep(1)
                        
                        # Click Next
                        next_button = await self.page.query_selector('#identifierNext')
                        if next_button:
                            await next_button.click()
                            await asyncio.sleep(3)
                            
                            # Check for password input
                            password_input = await self.page.query_selector('input[type="password"]')
                            if password_input:
                                await password_input.fill(account['password'])
                                await asyncio.sleep(1)
                                
                                # Click Next
                                password_next = await self.page.query_selector('#passwordNext')
                                if password_next:
                                    await password_next.click()
                                    await asyncio.sleep(5)
                                    
                                    # Check if back on Twitter
                                    current_url = self.page.url
                                    if 'twitter.com' in current_url and 'login' not in current_url:
                                        print(f"✅ Google OAuth successful for Account {account['id']}")
                                        return True
                                        
                # Check for verification challenges
                page_content = await self.page.content()
                if any(keyword in page_content.lower() for keyword in ['verify', 'captcha', '2fa', 'challenge']):
                    print(f"🛡️ Verification challenge detected for Account {account['id']}")
                    return await self.handle_verification_challenge(account)
                    
            return False
            
        except Exception as e:
            print(f"❌ Google OAuth failed for Account {account['id']}: {e}")
            return False
            
    async def attempt_email_password_login(self, account):
        """Attempt email/password login"""
        try:
            print(f"🔐 Attempting email/password login for Account {account['id']}")
            
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
                            current_url = self.page.url
                            if 'twitter.com' in current_url and 'login' not in current_url:
                                print(f"✅ Email/password login successful for Account {account['id']}")
                                return True
                                
                            # Check for verification
                            page_content = await self.page.content()
                            if any(keyword in page_content.lower() for keyword in ['verify', 'captcha', 'challenge']):
                                print(f"🛡️ Verification challenge detected for Account {account['id']}")
                                return await self.handle_verification_challenge(account)
                                
            return False
            
        except Exception as e:
            print(f"❌ Email/password login failed for Account {account['id']}: {e}")
            return False
            
    async def handle_verification_challenge(self, account):
        """Handle verification challenges autonomously or fall back to manual"""
        try:
            print(f"🛡️ Handling verification for Account {account['id']}")
            
            page_content = await self.page.content()
            
            # Check for different types of verification
            if 'cloudflare' in page_content.lower():
                print(f"☁️ Cloudflare detected for Account {account['id']} - waiting for auto-resolution...")
                
                # Wait for Cloudflare to resolve automatically
                for attempt in range(30):  # Wait up to 30 seconds
                    await asyncio.sleep(1)
                    try:
                        current_content = await self.page.content()
                        if 'cloudflare' not in current_content.lower():
                            print(f"✅ Cloudflare resolved for Account {account['id']}")
                            
                            # Check if now logged in
                            current_url = self.page.url
                            if 'twitter.com' in current_url and 'login' not in current_url:
                                return True
                            break
                    except:
                        continue
                        
            elif 'captcha' in page_content.lower():
                print(f"🤖 CAPTCHA detected for Account {account['id']} - requires manual intervention")
                return await self.fallback_to_manual_login(account)
                
            elif '2fa' in page_content.lower() or 'two-factor' in page_content.lower():
                print(f"📱 2FA detected for Account {account['id']} - requires manual intervention")
                return await self.fallback_to_manual_login(account)
                
            else:
                print(f"❓ Unknown verification for Account {account['id']} - trying manual fallback")
                return await self.fallback_to_manual_login(account)
                
            return False
            
        except Exception as e:
            print(f"❌ Verification handling failed for Account {account['id']}: {e}")
            return await self.fallback_to_manual_login(account)
            
    async def fallback_to_manual_login(self, account):
        """Fallback to manual login with user assistance"""
        try:
            print(f"\n🤖 MANUAL LOGIN REQUIRED - Account {account['id']}")
            print("=" * 50)
            print(f"📧 Account: {account['email']}")
            print("👀 Please complete login manually in the browser window")
            print("✅ Once logged in and on Twitter homepage, press ENTER to continue...")
            
            # Wait for user input
            input(f"Press ENTER when Account {account['id']} is logged in: ")
            
            # Verify login
            await asyncio.sleep(2)
            current_url = self.page.url
            
            if 'twitter.com' in current_url and 'login' not in current_url:
                print(f"✅ Manual login confirmed for Account {account['id']}")
                account['login_method'] = 'manual_verified'
                return True
            else:
                # Give user another chance
                print(f"⚠️ Login verification unclear for Account {account['id']}")
                user_confirm = input(f"Is Account {account['id']} logged in and on Twitter homepage? (yes/no): ").lower().strip()
                
                if user_confirm in ['yes', 'y']:
                    print(f"✅ User confirmed login for Account {account['id']}")
                    return True
                else:
                    print(f"❌ Login failed for Account {account['id']}")
                    return False
                    
        except Exception as e:
            print(f"❌ Manual login fallback failed for Account {account['id']}: {e}")
            return False
            
    async def autonomous_login(self, account):
        """Main autonomous login function"""
        try:
            print(f"\n🚀 Starting autonomous login for Account {account['id']}")
            print(f"📧 Email: {account['email']}")
            
            # Setup browser
            if not await self.setup_stealth_browser(account):
                return False
                
            # Detect login method
            login_method = await self.detect_login_method(account)
            
            # Attempt login based on detected method
            success = False
            
            if login_method == 'google_oauth':
                success = await self.attempt_google_oauth_login(account)
                
            elif login_method == 'email_password':
                success = await self.attempt_email_password_login(account)
                
            # If autonomous methods fail, fall back to manual
            if not success:
                print(f"🔄 Autonomous login failed for Account {account['id']} - falling back to manual")
                success = await self.fallback_to_manual_login(account)
                
            # Update account status
            if success:
                account['last_login'] = datetime.now().isoformat()
                account['status'] = 'logged_in'
                account['login_success_rate'] += 1
                print(f"🎉 Account {account['id']} successfully logged in!")
            else:
                account['status'] = 'login_failed'
                print(f"❌ Account {account['id']} login failed")
                
            return success
            
        except Exception as e:
            print(f"❌ Autonomous login error for Account {account['id']}: {e}")
            return False
            
    async def test_autonomous_login_system(self):
        """Test the autonomous login system with all accounts"""
        try:
            print("🧪 Testing Autonomous Twitter Login System")
            print("=" * 60)
            
            successful_logins = 0
            
            for account in self.accounts:
                print(f"\n{'='*60}")
                print(f"🎯 TESTING ACCOUNT {account['id']}/{len(self.accounts)}")
                print(f"{'='*60}")
                
                if await self.autonomous_login(account):
                    successful_logins += 1
                    
                    # Close browser for this account
                    if hasattr(self, 'browser'):
                        await self.browser.close()
                    if hasattr(self, 'playwright'):
                        await self.playwright.stop()
                        
                    # Small delay between accounts
                    if account != self.accounts[-1]:  # Not the last account
                        print(f"⏳ Waiting 30 seconds before next account...")
                        await asyncio.sleep(30)
                        
            # Final summary
            print(f"\n🎉 Autonomous Login Test Complete!")
            print(f"📊 Results: {successful_logins}/{len(self.accounts)} accounts logged in successfully")
            
            if successful_logins >= len(self.accounts) * 0.75:  # 75% success rate
                print("✅ Autonomous login system is working well!")
                print("🚀 Ready for full automation!")
            else:
                print("⚠️ Some accounts need manual attention")
                print("🔧 Consider adjusting login strategies")
                
            return successful_logins
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            return 0

async def main():
    """Test autonomous login system"""
    login_system = AutonomousTwitterLogin()
    
    if len(login_system.accounts) == 0:
        print("❌ No Twitter accounts configured!")
        return
        
    await login_system.test_autonomous_login_system()

if __name__ == "__main__":
    asyncio.run(main())
