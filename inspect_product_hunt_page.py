#!/usr/bin/env python3
"""
Inspect Product Hunt page structure more thoroughly
"""

import asyncio
from playwright.async_api import async_playwright

async def inspect_page():
    """Inspect Product Hunt login page thoroughly"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("🌐 Navigating to Product Hunt login...")
            await page.goto('https://www.producthunt.com/login')
            await asyncio.sleep(3)
            
            # Get page HTML to analyze
            content = await page.content()
            
            # Look for different login methods
            print("\n🔍 Looking for login options...")
            
            # Check for OAuth buttons
            oauth_buttons = await page.query_selector_all('button, a')
            login_options = []
            
            for button in oauth_buttons:
                text = await button.inner_text()
                href = await button.get_attribute('href')
                
                if any(keyword in text.lower() for keyword in ['sign', 'login', 'google', 'linkedin', 'twitter', 'facebook']):
                    login_options.append({
                        'text': text.strip(),
                        'href': href,
                        'tag': button
                    })
            
            print(f"\n📋 Found {len(login_options)} login options:")
            for i, option in enumerate(login_options):
                print(f"  {i+1}. Text: '{option['text']}', Href: {option['href']}")
            
            # Look for email/password toggle
            print("\n🔍 Looking for email login toggle...")
            
            # Common patterns for email login toggles
            toggle_selectors = [
                'button:has-text("Email")',
                'a:has-text("Email")',
                'button:has-text("email")',
                'a:has-text("email")',
                '[data-test*="email"]',
                '.email-toggle',
                'button:has-text("Continue with email")',
                'a:has-text("Continue with email")'
            ]
            
            email_toggle = None
            for selector in toggle_selectors:
                try:
                    email_toggle = await page.query_selector(selector)
                    if email_toggle:
                        toggle_text = await email_toggle.inner_text()
                        print(f"✅ Found email toggle: '{toggle_text}'")
                        
                        # Click the toggle to reveal email form
                        await email_toggle.click()
                        await asyncio.sleep(2)
                        
                        # Now look for email/password inputs again
                        email_input = await page.query_selector('input[type="email"], input[name="email"]')
                        password_input = await page.query_selector('input[type="password"], input[name="password"]')
                        
                        if email_input and password_input:
                            print("✅ Email/password form revealed!")
                        else:
                            print("❌ Email/password form not found after toggle")
                        
                        break
                except:
                    continue
            
            if not email_toggle:
                print("❌ No email login toggle found")
                
                # Check if there's a different login page
                print("\n🔍 Checking for alternative login URLs...")
                
                alternative_urls = [
                    'https://www.producthunt.com/users/sign_in',
                    'https://www.producthunt.com/signin',
                    'https://www.producthunt.com/auth/login'
                ]
                
                for url in alternative_urls:
                    try:
                        await page.goto(url)
                        await asyncio.sleep(2)
                        
                        email_input = await page.query_selector('input[type="email"], input[name="email"]')
                        if email_input:
                            print(f"✅ Found email form at: {url}")
                            break
                    except:
                        continue
            
            # Keep browser open for manual inspection
            print(f"\n👀 Current URL: {page.url}")
            print("Browser will stay open for 60 seconds for manual inspection...")
            print("You can manually navigate and inspect the login process")
            
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_page())
