#!/usr/bin/env python3
"""
Find email login option on Product Hunt
"""

import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def find_email_login():
    """Find email login form on Product Hunt"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("🔍 Searching for email login on Product Hunt...")
            
            # Try different login URLs
            login_urls = [
                'https://www.producthunt.com/login',
                'https://www.producthunt.com/users/sign_in',
                'https://www.producthunt.com/signin',
                'https://www.producthunt.com/auth/login'
            ]
            
            for url in login_urls:
                print(f"\n🌐 Trying: {url}")
                await page.goto(url)
                await asyncio.sleep(3)
                
                # Look for "Continue with email" or similar buttons
                email_triggers = [
                    'button:has-text("email")',
                    'a:has-text("email")', 
                    'button:has-text("Email")',
                    'a:has-text("Email")',
                    'button:has-text("Continue with email")',
                    'a:has-text("Continue with email")',
                    'button:has-text("Sign in with email")',
                    'a:has-text("Sign in with email")',
                    '.email-login',
                    '[data-test*="email"]'
                ]
                
                # Check if email form is already visible
                email_input = await page.query_selector('input[type="email"], input[name="email"]')
                if email_input:
                    print(f"✅ Found email input directly at {url}")
                    break
                    
                # Look for email login trigger
                for selector in email_triggers:
                    try:
                        trigger = await page.query_selector(selector)
                        if trigger:
                            trigger_text = await trigger.inner_text()
                            print(f"🔗 Found email trigger: '{trigger_text}'")
                            
                            # Click the trigger
                            await trigger.click()
                            await asyncio.sleep(2)
                            
                            # Check if email form appeared
                            email_input = await page.query_selector('input[type="email"], input[name="email"]')
                            if email_input:
                                print("✅ Email form revealed after clicking trigger!")
                                break
                    except:
                        continue
                        
                # If we found email input, test the login
                email_input = await page.query_selector('input[type="email"], input[name="email"]')
                password_input = await page.query_selector('input[type="password"], input[name="password"]')
                
                if email_input and password_input:
                    print("🎯 Found complete email/password form!")
                    
                    # Test with your credentials
                    email = os.getenv('PRODUCTHUNT_EMAIL')
                    password = os.getenv('PRODUCTHUNT_PASSWORD')
                    
                    print(f"🔐 Testing login with: {email}")
                    
                    await email_input.fill(email)
                    await asyncio.sleep(1)
                    
                    await password_input.fill(password)
                    await asyncio.sleep(1)
                    
                    # Look for submit button
                    submit_selectors = [
                        'button[type="submit"]',
                        'input[type="submit"]',
                        'button:has-text("Sign in")',
                        'button:has-text("Log in")',
                        'button:has-text("Login")'
                    ]
                    
                    submit_button = None
                    for selector in submit_selectors:
                        submit_button = await page.query_selector(selector)
                        if submit_button:
                            button_text = await submit_button.inner_text()
                            print(f"🔘 Found submit button: '{button_text}'")
                            break
                            
                    if submit_button:
                        await submit_button.click()
                        print("🚀 Submitted login form")
                        
                        # Wait for result
                        await asyncio.sleep(5)
                        
                        current_url = page.url
                        if 'producthunt.com' in current_url and '/login' not in current_url:
                            print("✅ Login successful!")
                            print(f"Redirected to: {current_url}")
                            
                            # Keep browser open to verify
                            print("\n👀 Login successful! Browser will stay open for verification...")
                            await asyncio.sleep(30)
                            return True
                        else:
                            print(f"❌ Login may have failed. Current URL: {current_url}")
                    else:
                        print("❌ No submit button found")
                        
                    break
                    
            if not email_input:
                print("❌ No email login form found on any URL")
                
                # Show all available buttons for manual inspection
                print("\n📋 All available buttons/links:")
                buttons = await page.query_selector_all('button, a')
                
                for i, button in enumerate(buttons[:20]):  # Limit to first 20
                    try:
                        text = await button.inner_text()
                        href = await button.get_attribute('href')
                        if text.strip():
                            print(f"  {i+1}. '{text.strip()}' (href: {href})")
                    except:
                        continue
                        
            print("\n👀 Browser will stay open for manual inspection...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(find_email_login())
