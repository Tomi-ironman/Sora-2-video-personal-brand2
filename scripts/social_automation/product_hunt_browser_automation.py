#!/usr/bin/env python3
"""
Product Hunt Browser Automation
Uses Playwright to actually post comments and engage with products
"""

import os
import time
import json
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()

class ProductHuntBrowserBot:
    def __init__(self):
        self.setup_credentials()
        self.setup_browser_config()
        self.setup_anti_detection()
        
    def setup_credentials(self):
        """Setup Product Hunt login credentials"""
        self.email = os.getenv('PRODUCTHUNT_EMAIL', 'your_email@example.com')
        self.password = os.getenv('PRODUCTHUNT_PASSWORD', 'your_password')
        
        print(f"🔐 Using Product Hunt account: {self.email}")
        
    def setup_browser_config(self):
        """Configure browser for stealth operation"""
        self.browser_config = {
            'headless': False,  # Set to True for production
            'slow_mo': 1000,    # Slow down actions to appear human
            'viewport': {'width': 1920, 'height': 1080},
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def setup_anti_detection(self):
        """Setup anti-detection measures"""
        self.human_delays = {
            'typing_delay': (50, 150),      # ms between keystrokes
            'click_delay': (500, 2000),     # ms before clicking
            'scroll_delay': (1000, 3000),   # ms between scrolls
            'page_load_delay': (2000, 5000) # ms after page loads
        }
        
    async def human_delay(self, delay_type='click_delay'):
        """Add human-like delays"""
        min_delay, max_delay = self.human_delays[delay_type]
        delay = random.randint(min_delay, max_delay)
        await asyncio.sleep(delay / 1000)
        
    async def human_type(self, element, text):
        """Type text with human-like delays"""
        await element.click()
        await self.human_delay('click_delay')
        
        for char in text:
            await element.type(char)
            await asyncio.sleep(random.randint(50, 150) / 1000)
            
    async def setup_browser(self):
        """Initialize browser with stealth settings"""
        self.playwright = await async_playwright().start()
        
        # Launch browser with stealth settings
        self.browser = await self.playwright.chromium.launch(
            headless=self.browser_config['headless'],
            slow_mo=self.browser_config['slow_mo'],
            args=[
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport=self.browser_config['viewport'],
            user_agent=self.browser_config['user_agent'],
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        # Add stealth scripts
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            window.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        self.page = await self.context.new_page()
        
        print("🌐 Browser initialized with stealth settings")
        
    async def login_to_product_hunt(self):
        """Login to Product Hunt"""
        try:
            print("🔐 Logging into Product Hunt...")
            
            # Navigate to login page
            await self.page.goto('https://www.producthunt.com/login')
            await self.human_delay('page_load_delay')
            
            # Wait for login form
            await self.page.wait_for_selector('input[type="email"]', timeout=10000)
            
            # Fill email
            email_input = await self.page.query_selector('input[type="email"]')
            await self.human_type(email_input, self.email)
            
            await self.human_delay()
            
            # Fill password
            password_input = await self.page.query_selector('input[type="password"]')
            await self.human_type(password_input, self.password)
            
            await self.human_delay()
            
            # Click login button
            login_button = await self.page.query_selector('button[type="submit"]')
            await login_button.click()
            
            # Wait for login to complete
            await self.page.wait_for_url('https://www.producthunt.com/', timeout=15000)
            
            print("✅ Successfully logged into Product Hunt")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
            
    async def navigate_to_product(self, product_slug):
        """Navigate to a specific product page"""
        try:
            product_url = f"https://www.producthunt.com/posts/{product_slug}"
            print(f"🔍 Navigating to: {product_url}")
            
            await self.page.goto(product_url)
            await self.human_delay('page_load_delay')
            
            # Wait for page to load
            await self.page.wait_for_selector('[data-test="product-name"]', timeout=10000)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to navigate to product: {e}")
            return False
            
    async def upvote_product(self):
        """Upvote the product"""
        try:
            # Look for upvote button
            upvote_selectors = [
                '[data-test="vote-button"]',
                'button[aria-label*="upvote"]',
                'button[aria-label*="vote"]',
                '.vote-button'
            ]
            
            for selector in upvote_selectors:
                upvote_button = await self.page.query_selector(selector)
                if upvote_button:
                    # Check if already voted
                    classes = await upvote_button.get_attribute('class')
                    if 'voted' not in classes.lower():
                        await self.human_delay()
                        await upvote_button.click()
                        print("✅ Product upvoted")
                        return True
                    else:
                        print("ℹ️ Already voted on this product")
                        return True
                        
            print("⚠️ Upvote button not found")
            return False
            
        except Exception as e:
            print(f"❌ Failed to upvote: {e}")
            return False
            
    async def post_comment(self, comment_text):
        """Post a comment on the product"""
        try:
            print(f"💬 Posting comment: {comment_text[:50]}...")
            
            # Scroll to comments section
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await self.human_delay('scroll_delay')
            
            # Look for comment input
            comment_selectors = [
                'textarea[placeholder*="comment"]',
                'textarea[placeholder*="Add"]',
                'textarea[data-test="comment-input"]',
                '.comment-input textarea'
            ]
            
            comment_input = None
            for selector in comment_selectors:
                comment_input = await self.page.query_selector(selector)
                if comment_input:
                    break
                    
            if not comment_input:
                print("❌ Comment input not found")
                return False
                
            # Click and type comment
            await self.human_type(comment_input, comment_text)
            await self.human_delay()
            
            # Look for submit button
            submit_selectors = [
                'button[type="submit"]',
                'button[data-test="comment-submit"]',
                'button:has-text("Post")',
                'button:has-text("Comment")'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                submit_button = await self.page.query_selector(selector)
                if submit_button:
                    break
                    
            if submit_button:
                await submit_button.click()
                await self.human_delay('page_load_delay')
                print("✅ Comment posted successfully")
                return True
            else:
                print("❌ Submit button not found")
                return False
                
        except Exception as e:
            print(f"❌ Failed to post comment: {e}")
            return False
            
    async def engage_with_product(self, product_data, comment_text):
        """Full engagement with a product (navigate, upvote, comment)"""
        try:
            # Navigate to product
            if not await self.navigate_to_product(product_data['slug']):
                return False
                
            # Random delay to appear human
            await self.human_delay('page_load_delay')
            
            # Upvote product
            await self.upvote_product()
            
            # Random delay between actions
            await asyncio.sleep(random.randint(3, 8))
            
            # Post comment
            success = await self.post_comment(comment_text)
            
            if success:
                # Update engagement log
                self.log_successful_engagement(product_data, comment_text)
                
            return success
            
        except Exception as e:
            print(f"❌ Engagement failed: {e}")
            return False
            
    def log_successful_engagement(self, product_data, comment_text):
        """Log successful engagements"""
        log_file = "producthunt_successful_engagements.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    engagements = json.load(f)
            else:
                engagements = []
                
            engagements.append({
                'product_name': product_data['name'],
                'product_slug': product_data['slug'],
                'comment_text': comment_text,
                'timestamp': datetime.now().isoformat(),
                'status': 'posted'
            })
            
            with open(log_file, 'w') as f:
                json.dump(engagements, f, indent=2)
                
            print(f"📝 Logged successful engagement")
                
        except Exception as e:
            print(f"Error logging engagement: {e}")
            
    async def run_daily_automation(self):
        """Run daily Product Hunt automation"""
        try:
            print("🚀 Starting Product Hunt Browser Automation")
            print("=" * 50)
            
            # Setup browser
            await self.setup_browser()
            
            # Login
            if not await self.login_to_product_hunt():
                print("❌ Login failed - stopping automation")
                return
                
            # Load pending comments from engagement system
            comments_file = "producthunt_zenyai_comments.json"
            
            if not os.path.exists(comments_file):
                print("❌ No pending comments found")
                return
                
            with open(comments_file, 'r') as f:
                pending_comments = json.load(f)
                
            # Filter pending comments
            pending = [c for c in pending_comments if c.get('status') == 'pending']
            
            if not pending:
                print("ℹ️ No pending comments to post")
                return
                
            print(f"📊 Found {len(pending)} pending comments")
            
            successful_posts = 0
            
            # Process each pending comment
            for comment_data in pending[:5]:  # Limit to 5 per run
                product_data = {
                    'name': comment_data['product_name'],
                    'slug': comment_data['product_slug']
                }
                
                print(f"\n🎯 Engaging with: {product_data['name']}")
                
                success = await self.engage_with_product(
                    product_data, 
                    comment_data['comment_text']
                )
                
                if success:
                    successful_posts += 1
                    # Mark as posted
                    comment_data['status'] = 'posted'
                    comment_data['posted_at'] = datetime.now().isoformat()
                    
                # Human-like delay between products
                await asyncio.sleep(random.randint(30, 90))
                
            # Update comments file
            with open(comments_file, 'w') as f:
                json.dump(pending_comments, f, indent=2)
                
            print(f"\n🎉 Automation complete!")
            print(f"✅ Successfully posted: {successful_posts} comments")
            print(f"📊 Remaining pending: {len([c for c in pending_comments if c.get('status') == 'pending'])}")
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
        finally:
            # Cleanup
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run the browser automation"""
    bot = ProductHuntBrowserBot()
    await bot.run_daily_automation()

if __name__ == "__main__":
    asyncio.run(main())
