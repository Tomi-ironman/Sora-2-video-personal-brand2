#!/usr/bin/env python3
"""
Product Hunt Automation with Manual Verification Support
Pauses for human verification, then continues automation
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

class ProductHuntManualBot:
    def __init__(self):
        self.setup_credentials()
        self.setup_browser_config()
        
    def setup_credentials(self):
        """Setup Product Hunt credentials"""
        self.email = os.getenv('PRODUCTHUNT_EMAIL')
        self.password = os.getenv('PRODUCTHUNT_PASSWORD')
        print(f"🔐 Using Product Hunt account: {self.email}")
        
    def setup_browser_config(self):
        """Configure browser for manual interaction"""
        self.browser_config = {
            'headless': False,  # Must be visible for manual verification
            'slow_mo': 500,
            'viewport': {'width': 1920, 'height': 1080}
        }
        
    async def setup_browser(self):
        """Initialize browser with realistic settings"""
        self.playwright = await async_playwright().start()
        
        # Launch with realistic browser settings
        self.browser = await self.playwright.chromium.launch(
            headless=self.browser_config['headless'],
            slow_mo=self.browser_config['slow_mo'],
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--disable-web-security'
            ]
        )
        
        # Create context with realistic fingerprint
        self.context = await self.browser.new_context(
            viewport=self.browser_config['viewport'],
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        self.page = await self.context.new_page()
        
        # Remove automation indicators
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
    async def wait_for_manual_verification(self):
        """Wait for user to complete manual verification"""
        print("\n🤖 MANUAL VERIFICATION REQUIRED")
        print("=" * 50)
        print("👀 Please complete the human verification in the browser window")
        print("✅ Once you're logged into Product Hunt, press ENTER here to continue...")
        
        # Wait for user input
        input("Press ENTER when verification is complete and you're logged in: ")
        
        # Better login verification - check multiple indicators
        await asyncio.sleep(2)  # Give page time to load
        current_url = self.page.url
        print(f"🔍 Current URL: {current_url}")
        
        # Check multiple ways to verify login
        login_indicators = []
        
        # 1. URL check (more flexible)
        if 'producthunt.com' in current_url:
            if '/login' not in current_url and '/auth' not in current_url:
                login_indicators.append("URL indicates logged in")
            
        # 2. Check for user profile elements
        try:
            profile_selectors = [
                '[data-test*="user"]',
                '.user-avatar',
                '[aria-label*="profile"]',
                'button[aria-label*="user"]',
                '.avatar'
            ]
            
            for selector in profile_selectors:
                element = await self.page.query_selector(selector)
                if element:
                    login_indicators.append(f"Found user element: {selector}")
                    break
        except:
            pass
            
        # 3. Check page title
        try:
            title = await self.page.title()
            if 'login' not in title.lower() and 'sign in' not in title.lower():
                login_indicators.append(f"Page title: {title}")
        except:
            pass
            
        # 4. Check for logout button or user menu
        try:
            logout_elements = await self.page.query_selector_all('a:has-text("Logout"), a:has-text("Sign out"), button:has-text("Logout")')
            if logout_elements:
                login_indicators.append("Found logout element")
        except:
            pass
            
        print(f"📊 Login indicators found: {len(login_indicators)}")
        for indicator in login_indicators:
            print(f"   ✅ {indicator}")
            
        if len(login_indicators) >= 1:
            print("✅ Login verification successful - continuing automation!")
            return True
        else:
            print("⚠️ Login verification unclear - let's double check...")
            
            # Show what we can see on the page
            try:
                page_text = await self.page.evaluate("document.body.innerText")
                if 'welcome' in page_text.lower() or 'dashboard' in page_text.lower():
                    print("✅ Found welcome/dashboard text - assuming logged in")
                    return True
            except:
                pass
            
            # Ask user to confirm
            print("🤖 I'm having trouble detecting if you're logged in.")
            print("👀 Are you currently logged into Product Hunt and can see the homepage?")
            
            user_confirm = input("Type 'yes' if logged in, or 'no' to try again: ").lower().strip()
            
            if user_confirm in ['yes', 'y', '1']:
                print("✅ User confirmed login - continuing!")
                return True
            else:
                print("❌ Login not confirmed")
                return False
                
    async def login_with_manual_verification(self):
        """Login process with manual verification support"""
        try:
            print("🌐 Navigating to Product Hunt...")
            await self.page.goto('https://www.producthunt.com/login')
            await asyncio.sleep(3)
            
            # Check if we hit Cloudflare verification
            page_content = await self.page.content()
            
            if 'cloudflare' in page_content.lower() or 'verify you are human' in page_content.lower():
                print("🛡️ Cloudflare verification detected!")
                return await self.wait_for_manual_verification()
            
            # Try to find email login (might be hidden behind OAuth)
            print("🔍 Looking for email login...")
            
            # Look for email input or email login trigger
            email_input = await self.page.query_selector('input[type="email"], input[name="email"]')
            
            if not email_input:
                # Look for email login trigger
                email_triggers = [
                    'button:has-text("email")',
                    'a:has-text("email")',
                    'button:has-text("Continue with email")',
                    '.email-login'
                ]
                
                for selector in email_triggers:
                    trigger = await self.page.query_selector(selector)
                    if trigger:
                        print("🔗 Found email login trigger")
                        await trigger.click()
                        await asyncio.sleep(2)
                        break
                        
                # Check again for email input
                email_input = await self.page.query_selector('input[type="email"], input[name="email"]')
            
            if email_input:
                print("📧 Found email input - attempting login...")
                
                # Fill credentials
                await email_input.fill(self.email)
                await asyncio.sleep(1)
                
                password_input = await self.page.query_selector('input[type="password"]')
                if password_input:
                    await password_input.fill(self.password)
                    await asyncio.sleep(1)
                    
                    # Submit form
                    submit_button = await self.page.query_selector('button[type="submit"], button:has-text("Sign in")')
                    if submit_button:
                        await submit_button.click()
                        await asyncio.sleep(5)
                        
                        # Check if verification is needed
                        page_content = await self.page.content()
                        if 'cloudflare' in page_content.lower() or 'verify' in page_content.lower():
                            print("🛡️ Verification required after login attempt")
                            return await self.wait_for_manual_verification()
                        
                        # Check if login successful
                        current_url = self.page.url
                        if '/login' not in current_url:
                            print("✅ Login successful!")
                            return True
                            
            # If we get here, manual intervention needed
            print("🤖 Manual login required")
            print("👀 Please log in manually in the browser window")
            return await self.wait_for_manual_verification()
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            print("🤖 Please complete login manually")
            return await self.wait_for_manual_verification()
            
    async def navigate_to_product(self, product_slug):
        """Navigate to product page"""
        try:
            product_url = f"https://www.producthunt.com/posts/{product_slug}"
            print(f"🎯 Navigating to: {product_slug}")
            
            await self.page.goto(product_url)
            await asyncio.sleep(3)
            
            # Check for verification again
            page_content = await self.page.content()
            if 'cloudflare' in page_content.lower() or 'verify' in page_content.lower():
                print("🛡️ Verification required for product page")
                input("Please complete verification and press ENTER: ")
                
            return True
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
            
    async def upvote_product(self):
        """Upvote the product"""
        try:
            # Look for upvote button
            upvote_selectors = [
                '[data-test*="vote"]',
                'button[aria-label*="upvote"]',
                '.vote-button',
                'button:has-text("Upvote")',
                '[class*="vote"]'
            ]
            
            for selector in upvote_selectors:
                upvote_button = await self.page.query_selector(selector)
                if upvote_button:
                    # Check if already voted
                    classes = await upvote_button.get_attribute('class') or ''
                    if 'voted' not in classes.lower():
                        await upvote_button.click()
                        print("✅ Product upvoted")
                        await asyncio.sleep(2)
                        return True
                    else:
                        print("ℹ️ Already voted on this product")
                        return True
                        
            print("⚠️ Upvote button not found")
            return False
            
        except Exception as e:
            print(f"❌ Upvote error: {e}")
            return False
            
    async def post_comment(self, comment_text):
        """Post comment with manual fallback"""
        try:
            print(f"💬 Posting comment: {comment_text[:50]}...")
            
            # Scroll to comments section
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await asyncio.sleep(2)
            
            # Look for comment input
            comment_selectors = [
                'textarea[placeholder*="comment"]',
                'textarea[data-test*="comment"]',
                '.comment-input textarea',
                'textarea'
            ]
            
            comment_input = None
            for selector in comment_selectors:
                comment_input = await self.page.query_selector(selector)
                if comment_input:
                    break
                    
            if comment_input:
                # Click and type comment
                await comment_input.click()
                await asyncio.sleep(1)
                
                # Type slowly to appear human
                for char in comment_text:
                    await comment_input.type(char)
                    await asyncio.sleep(random.randint(50, 150) / 1000)
                    
                await asyncio.sleep(1)
                
                # Look for submit button
                submit_selectors = [
                    'button[type="submit"]',
                    'button:has-text("Post")',
                    'button:has-text("Comment")',
                    '.comment-submit'
                ]
                
                submit_button = None
                for selector in submit_selectors:
                    submit_button = await self.page.query_selector(selector)
                    if submit_button:
                        break
                        
                if submit_button:
                    await submit_button.click()
                    await asyncio.sleep(3)
                    print("✅ Comment posted successfully")
                    return True
                else:
                    print("❌ Submit button not found")
                    print("🤖 Please post the comment manually:")
                    print(f"Comment: {comment_text}")
                    input("Press ENTER when comment is posted: ")
                    return True
            else:
                print("❌ Comment input not found")
                print("🤖 Please post the comment manually:")
                print(f"Comment: {comment_text}")
                input("Press ENTER when comment is posted: ")
                return True
                
        except Exception as e:
            print(f"❌ Comment error: {e}")
            print("🤖 Please post the comment manually:")
            print(f"Comment: {comment_text}")
            input("Press ENTER when comment is posted: ")
            return True
            
    async def run_manual_assisted_automation(self):
        """Run automation with manual assistance"""
        try:
            print("🚀 Product Hunt Manual-Assisted Automation")
            print("=" * 50)
            print("This system will pause for manual verification when needed")
            
            await self.setup_browser()
            
            # Login with manual verification support
            if not await self.login_with_manual_verification():
                print("❌ Login failed - stopping automation")
                return
                
            # Load pending comments
            comments_file = "producthunt_zenyai_comments.json"
            
            if not os.path.exists(comments_file):
                print("❌ No pending comments found")
                print("Run: python3 product_hunt_engagement.py first")
                return
                
            with open(comments_file, 'r') as f:
                comments = json.load(f)
                
            pending = [c for c in comments if c.get('status') == 'pending']
            
            if not pending:
                print("ℹ️ No pending comments to post")
                return
                
            print(f"📊 Found {len(pending)} pending comments")
            
            successful_posts = 0
            
            # Process each comment
            for i, comment_data in enumerate(pending[:3]):  # Limit to 3 for testing
                print(f"\n🎯 Processing {i+1}/{min(3, len(pending))}: {comment_data['product_name']}")
                
                # Navigate to product
                if await self.navigate_to_product(comment_data['product_slug']):
                    
                    # Upvote
                    await self.upvote_product()
                    await asyncio.sleep(random.randint(2, 5))
                    
                    # Post comment
                    if await self.post_comment(comment_data['comment_text']):
                        successful_posts += 1
                        comment_data['status'] = 'posted'
                        comment_data['posted_at'] = datetime.now().isoformat()
                        
                    # Human-like delay between products
                    if i < min(2, len(pending) - 1):  # Don't delay after last item
                        delay = random.randint(30, 90)
                        print(f"⏳ Waiting {delay} seconds before next product...")
                        await asyncio.sleep(delay)
                        
            # Update comments file
            with open(comments_file, 'w') as f:
                json.dump(comments, f, indent=2)
                
            print(f"\n🎉 Automation complete!")
            print(f"✅ Successfully posted: {successful_posts} comments")
            
            # Keep browser open for review
            print("\n👀 Browser will stay open for 60 seconds for review...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run manual-assisted automation"""
    bot = ProductHuntManualBot()
    await bot.run_manual_assisted_automation()

if __name__ == "__main__":
    asyncio.run(main())
