#!/usr/bin/env python3
"""
Test Product Hunt login and inspect the page structure
"""

import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def test_login():
    """Test Product Hunt login and inspect page"""
    
    async with async_playwright() as p:
        # Launch browser in non-headless mode to see what's happening
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=1000
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        try:
            print("🌐 Navigating to Product Hunt...")
            await page.goto('https://www.producthunt.com/login')
            
            # Wait for page to load
            await asyncio.sleep(3)
            
            print("📋 Page title:", await page.title())
            print("🔍 Current URL:", page.url)
            
            # Try to find login elements with different selectors
            selectors_to_try = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email" i]',
                '#email',
                '.email-input',
                'input[data-test*="email"]'
            ]
            
            print("\n🔍 Looking for email input...")
            email_input = None
            
            for selector in selectors_to_try:
                try:
                    email_input = await page.query_selector(selector)
                    if email_input:
                        print(f"✅ Found email input with selector: {selector}")
                        break
                except:
                    continue
                    
            if not email_input:
                print("❌ No email input found")
                
                # Get all input elements to see what's available
                inputs = await page.query_selector_all('input')
                print(f"\n📋 Found {len(inputs)} input elements:")
                
                for i, input_elem in enumerate(inputs):
                    input_type = await input_elem.get_attribute('type')
                    input_name = await input_elem.get_attribute('name')
                    input_placeholder = await input_elem.get_attribute('placeholder')
                    input_id = await input_elem.get_attribute('id')
                    
                    print(f"  {i+1}. Type: {input_type}, Name: {input_name}, Placeholder: {input_placeholder}, ID: {input_id}")
                    
            # Look for password input
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[placeholder*="password" i]',
                '#password'
            ]
            
            print("\n🔍 Looking for password input...")
            password_input = None
            
            for selector in password_selectors:
                try:
                    password_input = await page.query_selector(selector)
                    if password_input:
                        print(f"✅ Found password input with selector: {selector}")
                        break
                except:
                    continue
                    
            if not password_input:
                print("❌ No password input found")
                
            # Look for login/submit buttons
            button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Log in")',
                'button:has-text("Sign in")',
                'button:has-text("Login")',
                '.login-button',
                '[data-test*="login"]'
            ]
            
            print("\n🔍 Looking for login button...")
            login_button = None
            
            for selector in button_selectors:
                try:
                    login_button = await page.query_selector(selector)
                    if login_button:
                        button_text = await login_button.inner_text()
                        print(f"✅ Found login button with selector: {selector}, text: '{button_text}'")
                        break
                except:
                    continue
                    
            if not login_button:
                print("❌ No login button found")
                
                # Get all buttons to see what's available
                buttons = await page.query_selector_all('button')
                print(f"\n📋 Found {len(buttons)} button elements:")
                
                for i, button in enumerate(buttons):
                    button_text = await button.inner_text()
                    button_type = await button.get_attribute('type')
                    button_class = await button.get_attribute('class')
                    
                    print(f"  {i+1}. Text: '{button_text}', Type: {button_type}, Class: {button_class}")
            
            # If we found the elements, try to login
            if email_input and password_input and login_button:
                print("\n🔐 Attempting login...")
                
                email = os.getenv('PRODUCTHUNT_EMAIL')
                password = os.getenv('PRODUCTHUNT_PASSWORD')
                
                await email_input.fill(email)
                await asyncio.sleep(1)
                
                await password_input.fill(password)
                await asyncio.sleep(1)
                
                await login_button.click()
                
                # Wait for navigation
                try:
                    await page.wait_for_url('https://www.producthunt.com/', timeout=10000)
                    print("✅ Login successful!")
                except:
                    print("❌ Login may have failed - didn't redirect to homepage")
                    print(f"Current URL: {page.url}")
                    
            # Keep browser open for inspection
            print("\n👀 Browser will stay open for 30 seconds for inspection...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_login())
