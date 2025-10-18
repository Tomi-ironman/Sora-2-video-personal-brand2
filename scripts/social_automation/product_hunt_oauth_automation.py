#!/usr/bin/env python3
"""
Product Hunt OAuth Browser Automation
Handles LinkedIn OAuth login for Product Hunt
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

class ProductHuntOAuthBot:
    def __init__(self):
        self.setup_credentials()
        self.setup_browser_config()
        
    def setup_credentials(self):
        """Setup LinkedIn credentials for OAuth"""
        # Use LinkedIn credentials since Product Hunt uses LinkedIn OAuth
        self.linkedin_email = os.getenv('LINKEDIN_EMAIL', 'your_linkedin_email@example.com')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD', 'your_linkedin_password')
        
        print(f"🔐 Using LinkedIn account for Product Hunt OAuth: {self.linkedin_email}")
        
    def setup_browser_config(self):
        """Configure browser for stealth operation"""
        self.browser_config = {
            'headless': False,  # Keep visible for OAuth
            'slow_mo': 1000,
            'viewport': {'width': 1920, 'height': 1080}
        }
        
    async def setup_browser(self):
        """Initialize browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(**self.browser_config)
        self.context = await self.browser.new_context(viewport=self.browser_config['viewport'])
        self.page = await self.context.new_page()
        
    async def login_via_linkedin_oauth(self):
        """Login to Product Hunt via LinkedIn OAuth"""
        try:
            print("🔐 Starting LinkedIn OAuth login...")
            
            # Go to Product Hunt login
            await self.page.goto('https://www.producthunt.com/login')
            await asyncio.sleep(3)
            
            # Click LinkedIn login button
            linkedin_button = await self.page.query_selector('button:has-text("Sign in with Linkedin")')
            if not linkedin_button:
                print("❌ LinkedIn login button not found")
                return False
                
            await linkedin_button.click()
            print("🔗 Clicked LinkedIn OAuth button")
            
            # Wait for LinkedIn login page
            await asyncio.sleep(3)
            
            # Fill LinkedIn credentials
            email_input = await self.page.wait_for_selector('input[name="session_key"], input[id="username"]', timeout=10000)
            await email_input.fill(self.linkedin_email)
            
            password_input = await self.page.query_selector('input[name="session_password"], input[id="password"]')
            await password_input.fill(self.linkedin_password)
            
            # Click LinkedIn login
            login_button = await self.page.query_selector('button[type="submit"], .sign-in-form__submit-button')
            await login_button.click()
            
            print("🔐 Submitted LinkedIn credentials")
            
            # Wait for OAuth redirect back to Product Hunt
            try:
                await self.page.wait_for_url('https://www.producthunt.com/', timeout=15000)
                print("✅ Successfully logged into Product Hunt via LinkedIn")
                return True
            except:
                # Check if we're still on LinkedIn (might need 2FA or approval)
                current_url = self.page.url
                if 'linkedin.com' in current_url:
                    print("⚠️ Still on LinkedIn - may need manual 2FA or approval")
                    print("👀 Please complete any required steps in the browser...")
                    
                    # Wait for user to complete OAuth manually
                    for i in range(30):  # Wait up to 30 seconds
                        await asyncio.sleep(1)
                        if 'producthunt.com' in self.page.url:
                            print("✅ OAuth completed - now on Product Hunt")
                            return True
                            
                print("❌ OAuth login may have failed")
                return False
                
        except Exception as e:
            print(f"❌ OAuth login failed: {e}")
            return False
            
    async def navigate_to_product(self, product_slug):
        """Navigate to product page"""
        try:
            product_url = f"https://www.producthunt.com/posts/{product_slug}"
            await self.page.goto(product_url)
            await asyncio.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Failed to navigate to product: {e}")
            return False
            
    async def upvote_product(self):
        """Upvote the product"""
        try:
            # Look for upvote button with various selectors
            upvote_selectors = [
                '[data-test*="vote"]',
                'button[aria-label*="upvote"]',
                '.vote-button',
                'button:has-text("Upvote")'
            ]
            
            for selector in upvote_selectors:
                upvote_button = await self.page.query_selector(selector)
                if upvote_button:
                    await upvote_button.click()
                    print("✅ Product upvoted")
                    return True
                    
            print("⚠️ Upvote button not found")
            return False
            
        except Exception as e:
            print(f"❌ Failed to upvote: {e}")
            return False
            
    async def post_comment(self, comment_text):
        """Post comment on product"""
        try:
            # Scroll down to find comment section
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
                    
            if not comment_input:
                print("❌ Comment input not found")
                return False
                
            # Type comment
            await comment_input.click()
            await comment_input.fill(comment_text)
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
                print("✅ Comment posted")
                return True
            else:
                print("❌ Submit button not found")
                return False
                
        except Exception as e:
            print(f"❌ Failed to post comment: {e}")
            return False
            
    async def run_manual_oauth_demo(self):
        """Run a demo that shows the OAuth process"""
        try:
            print("🚀 Product Hunt OAuth Demo")
            print("=" * 40)
            
            await self.setup_browser()
            
            # Check credentials
            if self.linkedin_email == 'your_linkedin_email@example.com':
                print("❌ LinkedIn credentials not configured")
                print("Please add to .env file:")
                print("LINKEDIN_EMAIL=your_linkedin_email@example.com")
                print("LINKEDIN_PASSWORD=your_linkedin_password")
                return
                
            # Attempt OAuth login
            if await self.login_via_linkedin_oauth():
                print("\n🎉 OAuth login successful!")
                
                # Load a sample product to test engagement
                print("\n🔍 Testing product engagement...")
                
                # Get pending comments
                comments_file = "producthunt_zenyai_comments.json"
                if os.path.exists(comments_file):
                    with open(comments_file, 'r') as f:
                        comments = json.load(f)
                        
                    pending = [c for c in comments if c.get('status') == 'pending']
                    
                    if pending:
                        # Test with first pending comment
                        test_comment = pending[0]
                        
                        print(f"🎯 Testing with: {test_comment['product_name']}")
                        
                        if await self.navigate_to_product(test_comment['product_slug']):
                            await self.upvote_product()
                            await asyncio.sleep(2)
                            await self.post_comment(test_comment['comment_text'])
                            
                            print("✅ Test engagement complete!")
                        else:
                            print("❌ Failed to navigate to test product")
                    else:
                        print("ℹ️ No pending comments to test with")
                else:
                    print("ℹ️ No comments file found")
                    
            else:
                print("❌ OAuth login failed")
                
            print("\n👀 Browser will stay open for inspection...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run OAuth demo"""
    bot = ProductHuntOAuthBot()
    await bot.run_manual_oauth_demo()

if __name__ == "__main__":
    asyncio.run(main())
