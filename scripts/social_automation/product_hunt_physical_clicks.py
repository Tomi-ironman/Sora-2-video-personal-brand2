#!/usr/bin/env python3
"""
Product Hunt Physical Interaction Bot
Actually clicks buttons and interacts with page elements
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

class ProductHuntPhysicalBot:
    def __init__(self):
        self.setup_credentials()
        
    def setup_credentials(self):
        """Setup Product Hunt credentials"""
        self.email = os.getenv('PRODUCTHUNT_EMAIL')
        self.password = os.getenv('PRODUCTHUNT_PASSWORD')
        print(f"🔐 Using Product Hunt account: {self.email}")
        
    async def setup_browser(self):
        """Initialize browser with realistic settings"""
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # Keep visible to see interactions
            slow_mo=1000,    # Slow down to see clicks
            args=['--disable-blink-features=AutomationControlled']
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        self.page = await self.context.new_page()
        
    async def wait_for_manual_login(self):
        """Wait for manual login completion"""
        print("\n🤖 MANUAL LOGIN REQUIRED")
        print("=" * 40)
        print("👀 Please log into Product Hunt in the browser window")
        print("✅ Once logged in and on homepage, press ENTER to continue...")
        
        input("Press ENTER when logged in: ")
        
        # Simple confirmation
        user_confirm = input("Are you logged in and can see the Product Hunt homepage? (yes/no): ").lower().strip()
        
        if user_confirm in ['yes', 'y']:
            print("✅ Login confirmed - starting automation!")
            return True
        else:
            print("❌ Please complete login first")
            return False
            
    async def find_and_click_upvote(self):
        """Find and physically click the upvote button"""
        print("🔍 Looking for upvote button...")
        
        # Wait for page to fully load
        await asyncio.sleep(3)
        
        # Try multiple upvote button selectors
        upvote_selectors = [
            # Common upvote button patterns
            'button[data-test*="vote"]',
            'button[aria-label*="upvote"]',
            'button[aria-label*="vote"]',
            '[data-test="vote-button"]',
            '.vote-button',
            'button:has-text("Upvote")',
            '[class*="vote"][class*="button"]',
            'button[class*="vote"]',
            # More generic patterns
            'button:has([class*="vote"])',
            'div[class*="vote"] button',
            '[role="button"][class*="vote"]'
        ]
        
        for i, selector in enumerate(upvote_selectors):
            try:
                print(f"   Trying selector {i+1}: {selector}")
                
                # Wait for element to be present
                element = await self.page.wait_for_selector(selector, timeout=2000)
                
                if element:
                    # Check if element is visible and clickable
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()
                    
                    print(f"   ✅ Found element - Visible: {is_visible}, Enabled: {is_enabled}")
                    
                    if is_visible and is_enabled:
                        # Get element text/attributes for verification
                        text = await element.inner_text()
                        classes = await element.get_attribute('class') or ''
                        
                        print(f"   📝 Element text: '{text}', Classes: {classes}")
                        
                        # Check if already voted
                        if 'voted' in classes.lower() or 'active' in classes.lower():
                            print("   ℹ️ Already voted on this product")
                            return True
                            
                        # Scroll element into view
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        
                        # Highlight element (visual feedback)
                        await element.evaluate("element => element.style.border = '3px solid red'")
                        await asyncio.sleep(1)
                        
                        # Physical click
                        await element.click()
                        print("   🎯 CLICKED upvote button!")
                        
                        # Remove highlight
                        await element.evaluate("element => element.style.border = ''")
                        
                        # Wait for vote to register
                        await asyncio.sleep(2)
                        
                        return True
                        
            except Exception as e:
                print(f"   ❌ Selector failed: {e}")
                continue
                
        # If no selector worked, try finding by text content
        print("🔍 Trying to find upvote by text content...")
        
        try:
            # Look for any button containing vote-related text
            all_buttons = await self.page.query_selector_all('button')
            
            for button in all_buttons:
                text = await button.inner_text()
                aria_label = await button.get_attribute('aria-label') or ''
                
                if any(keyword in (text + aria_label).lower() for keyword in ['upvote', 'vote', '▲', '↑']):
                    print(f"   🎯 Found vote button by text: '{text}' / '{aria_label}'")
                    
                    # Highlight and click
                    await button.evaluate("element => element.style.border = '3px solid red'")
                    await asyncio.sleep(1)
                    await button.click()
                    print("   ✅ CLICKED vote button!")
                    await button.evaluate("element => element.style.border = ''")
                    
                    return True
                    
        except Exception as e:
            print(f"❌ Text-based search failed: {e}")
            
        print("❌ Could not find upvote button")
        return False
        
    async def find_and_fill_comment(self, comment_text):
        """Find comment input and post comment"""
        print("🔍 Looking for comment input...")
        
        # Scroll down to comments section
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.7)")
        await asyncio.sleep(2)
        
        # Try multiple comment input selectors
        comment_selectors = [
            'textarea[placeholder*="comment" i]',
            'textarea[placeholder*="add" i]',
            'textarea[data-test*="comment"]',
            'textarea[name*="comment"]',
            '.comment-input textarea',
            '.comment-form textarea',
            'textarea',
            'input[placeholder*="comment" i]',
            '[contenteditable="true"]'
        ]
        
        for i, selector in enumerate(comment_selectors):
            try:
                print(f"   Trying selector {i+1}: {selector}")
                
                element = await self.page.wait_for_selector(selector, timeout=2000)
                
                if element:
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()
                    
                    print(f"   ✅ Found element - Visible: {is_visible}, Enabled: {is_enabled}")
                    
                    if is_visible and is_enabled:
                        placeholder = await element.get_attribute('placeholder') or ''
                        print(f"   📝 Placeholder: '{placeholder}'")
                        
                        # Scroll into view and highlight
                        await element.scroll_into_view_if_needed()
                        await element.evaluate("element => element.style.border = '3px solid blue'")
                        await asyncio.sleep(1)
                        
                        # Click and focus
                        await element.click()
                        await asyncio.sleep(1)
                        
                        # Clear any existing text
                        await element.fill('')
                        await asyncio.sleep(0.5)
                        
                        # Type comment with faster, more natural speed
                        print(f"   ⌨️ Typing comment: {comment_text[:50]}...")
                        
                        # Type in chunks for more natural flow
                        words = comment_text.split(' ')
                        for i, word in enumerate(words):
                            await element.type(word)
                            if i < len(words) - 1:  # Add space between words
                                await element.type(' ')
                                await asyncio.sleep(random.randint(10, 30) / 1000)  # Faster typing
                            
                        print("   ✅ Comment typed!")
                        
                        # Remove highlight
                        await element.evaluate("element => element.style.border = ''")
                        
                        # Now find submit button
                        return await self.find_and_click_submit()
                        
            except Exception as e:
                print(f"   ❌ Selector failed: {e}")
                continue
                
        print("❌ Could not find comment input")
        return False
        
    async def find_and_click_submit(self):
        """Find and click comment submit button"""
        print("🔍 Looking for submit button...")
        
        # Try multiple submit button selectors
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Post")',
            'button:has-text("Comment")',
            'button:has-text("Submit")',
            'button:has-text("Send")',
            '.comment-submit',
            '.submit-button',
            'button[data-test*="submit"]',
            'button[data-test*="comment"]'
        ]
        
        for i, selector in enumerate(submit_selectors):
            try:
                print(f"   Trying selector {i+1}: {selector}")
                
                element = await self.page.wait_for_selector(selector, timeout=2000)
                
                if element:
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()
                    text = await element.inner_text()
                    
                    print(f"   ✅ Found button - Text: '{text}', Visible: {is_visible}, Enabled: {is_enabled}")
                    
                    if is_visible and is_enabled:
                        # Highlight and click
                        await element.evaluate("element => element.style.border = '3px solid green'")
                        await asyncio.sleep(1)
                        
                        await element.click()
                        print("   🎯 CLICKED submit button!")
                        
                        await element.evaluate("element => element.style.border = ''")
                        
                        # Wait for comment to post
                        await asyncio.sleep(3)
                        
                        return True
                        
            except Exception as e:
                print(f"   ❌ Selector failed: {e}")
                continue
                
        # Try finding submit button near comment area
        print("🔍 Looking for submit button near comment area...")
        
        try:
            all_buttons = await self.page.query_selector_all('button')
            
            for button in all_buttons:
                text = await button.inner_text()
                
                if any(keyword in text.lower() for keyword in ['post', 'comment', 'submit', 'send']):
                    print(f"   🎯 Found submit by text: '{text}'")
                    
                    await button.evaluate("element => element.style.border = '3px solid green'")
                    await asyncio.sleep(1)
                    await button.click()
                    print("   ✅ CLICKED submit button!")
                    await button.evaluate("element => element.style.border = ''")
                    
                    return True
                    
        except Exception as e:
            print(f"❌ Text-based submit search failed: {e}")
            
        print("❌ Could not find submit button")
        return False
        
    async def engage_with_product(self, product_slug, comment_text):
        """Full engagement with visual feedback"""
        try:
            product_url = f"https://www.producthunt.com/posts/{product_slug}"
            print(f"\n🎯 Engaging with product: {product_slug}")
            print(f"🌐 URL: {product_url}")
            
            # Navigate to product
            await self.page.goto(product_url)
            await asyncio.sleep(3)
            
            # Check for verification (auto-wait instead of manual input)
            page_content = await self.page.content()
            if 'cloudflare' in page_content.lower() or 'verify' in page_content.lower():
                print("🛡️ Cloudflare detected - waiting for it to clear...")
                
                # Auto-wait for verification to complete
                for attempt in range(30):  # Wait up to 30 seconds
                    await asyncio.sleep(1)
                    try:
                        current_content = await self.page.content()
                        if 'cloudflare' not in current_content.lower() and 'verify' not in current_content.lower():
                            print("✅ Verification cleared automatically!")
                            break
                    except:
                        continue
                else:
                    print("⚠️ Verification taking longer than expected, continuing anyway...")
                
            # Upvote product
            print("\n⬆️ ATTEMPTING UPVOTE:")
            upvote_success = await self.find_and_click_upvote()
            
            if upvote_success:
                print("✅ Upvote successful!")
            else:
                print("❌ Upvote failed")
                
            # Wait between actions
            await asyncio.sleep(random.randint(3, 6))
            
            # Post comment
            print("\n💬 ATTEMPTING COMMENT:")
            comment_success = await self.find_and_fill_comment(comment_text)
            
            if comment_success:
                print("✅ Comment posted successfully!")
                return True
            else:
                print("❌ Comment posting failed")
                print(f"🤖 Manual comment needed: {comment_text}")
                input("Please post comment manually and press ENTER: ")
                return True
                
        except Exception as e:
            print(f"❌ Engagement error: {e}")
            return False
            
    async def run_physical_automation(self):
        """Run automation with physical interactions"""
        try:
            print("🤖 Product Hunt Physical Interaction Bot")
            print("=" * 50)
            
            await self.setup_browser()
            
            # Manual login
            await self.page.goto('https://www.producthunt.com/login')
            
            if not await self.wait_for_manual_login():
                return
                
            # Load comments
            comments_file = "producthunt_zenyai_comments.json"
            
            if not os.path.exists(comments_file):
                print("❌ No comments file found")
                return
                
            with open(comments_file, 'r') as f:
                comments = json.load(f)
                
            pending = [c for c in comments if c.get('status') == 'pending']
            
            if not pending:
                print("ℹ️ No pending comments")
                return
                
            print(f"📊 Found {len(pending)} pending comments")
            
            # Process comments with physical interactions
            for i, comment_data in enumerate(pending[:2]):  # Test with 2
                print(f"\n{'='*60}")
                print(f"🎯 PROCESSING {i+1}/{min(2, len(pending))}: {comment_data['product_name']}")
                print(f"{'='*60}")
                
                success = await self.engage_with_product(
                    comment_data['product_slug'],
                    comment_data['comment_text']
                )
                
                if success:
                    comment_data['status'] = 'posted'
                    comment_data['posted_at'] = datetime.now().isoformat()
                    
                # Delay between products
                if i < min(1, len(pending) - 1):
                    delay = random.randint(30, 60)
                    print(f"\n⏳ Waiting {delay} seconds before next product...")
                    await asyncio.sleep(delay)
                    
            # Save results
            with open(comments_file, 'w') as f:
                json.dump(comments, f, indent=2)
                
            print("\n🎉 Physical automation complete!")
            print("👀 Browser will stay open for review...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
        finally:
            if hasattr(self, 'browser'):
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()

async def main():
    """Run physical interaction bot"""
    bot = ProductHuntPhysicalBot()
    await bot.run_physical_automation()

if __name__ == "__main__":
    asyncio.run(main())
