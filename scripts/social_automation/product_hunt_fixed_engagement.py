#!/usr/bin/env python3
"""
FIXED Product Hunt Engagement
Browse homepage + today's launches instead of search
Search → Find → Engage → Post → Repeat
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class FixedProductHuntEngagement:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup fixed automation"""
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Track commented products to avoid duplicates
        self.commented_products_file = "product_hunt_commented_history.json"
        self.commented_products = self.load_commented_history()
        
        # ZENYAI ENGAGEMENT TEMPLATES - Strategic plugs
        self.zenyai_templates = [
            "This looks great for audio workflow! Speaking of audio organization, we're building Zenyai to solve the metadata chaos that podcasters and producers face daily 🎧 Check us out if you're dealing with sample/audio file organization!",
            
            "Love seeing tools for audio professionals! We're tackling a similar pain point at Zenyai - helping music producers and podcasters organize their audio assets with AI-powered metadata management 🎵",
            
            "Great tool! For anyone in audio production struggling with file organization, we're building Zenyai specifically to solve the metadata nightmare that every producer knows too well 🚀",
            
            "This is exactly what the audio community needs! We're solving the complementary problem at Zenyai - audio file organization and metadata management for producers who have thousands of samples 🎙️",
            
            "Impressive work! If you're in audio/music production and this tool helps your workflow, you might also want to check out Zenyai - we're solving the audio asset organization problem that every producer faces 💡",
            
            "Nice launch! The audio production community needs more tools like this. We're building Zenyai to tackle the specific problem of audio metadata and sample library organization 🔥"
        ]
        
        print(f"🚀 FIXED Product Hunt Engagement initialized")
        print(f"💬 {len(self.zenyai_templates)} strategic Zenyai plug templates")
        print(f"📝 Avoiding {len(self.commented_products)} previously commented products")
        
    def load_commented_history(self):
        """Load history of products we've already commented on"""
        try:
            if os.path.exists(self.commented_products_file):
                with open(self.commented_products_file, 'r') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
            
    def save_commented_history(self):
        """Save updated history of commented products"""
        try:
            with open(self.commented_products_file, 'w') as f:
                json.dump(list(self.commented_products), f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save comment history: {e}")
            
    def setup_browser(self):
        """Setup browser with persistent session"""
        try:
            print("🌐 Setting up browser...")
            
            playwright = sync_playwright().start()
            
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-first-run'
                ]
            )
            
            page = browser.new_page()
            page.set_default_timeout(60000)
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def manual_login_and_wait(self, page):
        """Manual login - one time setup"""
        try:
            print("\n🔐 ONE-TIME MANUAL LOGIN")
            print("=" * 50)
            print("1. Log into Product Hunt in the browser")
            print("2. Make sure you're fully logged in")
            print("3. Press ENTER when ready for automation")
            print("=" * 50)
            
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            input("🔑 Press ENTER after logging in...")
            
            print("✅ Ready for engagement!")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def find_one_product_from_homepage(self, page):
        """Find ONE product from homepage or today's launches"""
        try:
            print(f"🏠 Looking for products on homepage...")
            
            # Go to homepage
            page.goto("https://www.producthunt.com")
            time.sleep(4)
            
            # Scroll to load more products
            for i in range(2):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                
            # Find ALL links on the page
            all_links = page.locator('a').all()
            print(f"   📊 Found {len(all_links)} total links on page")
            
            # Look for product links
            for link in all_links:
                try:
                    href = link.get_attribute('href')
                    if href and '/posts/' in href:
                        url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                        
                        # Skip if we've already commented
                        if url in self.commented_products:
                            continue
                            
                        # Get product name
                        name = link.text_content()
                        if name:
                            name = name.strip()
                            
                            # Skip if name is too short or generic
                            if len(name) > 5 and name not in ['Learn more', 'View', 'See more', 'Read more']:
                                product = {
                                    'name': name[:100],
                                    'url': url,
                                    'source': 'homepage',
                                    'found_at': datetime.now().isoformat()
                                }
                                
                                print(f"   ✅ Found product: {name[:50]}")
                                return product
                                
                except:
                    continue
                    
            # If no products on homepage, try today's launches
            print(f"   🔄 Trying today's launches...")
            
            try:
                page.goto("https://www.producthunt.com/posts")
                time.sleep(4)
                
                # Scroll and look for products
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                
                today_links = page.locator('a').all()
                print(f"   📊 Found {len(today_links)} links on today's page")
                
                for link in today_links:
                    try:
                        href = link.get_attribute('href')
                        if href and '/posts/' in href:
                            url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                            
                            # Skip if we've already commented
                            if url in self.commented_products:
                                continue
                                
                            # Get product name
                            name = link.text_content()
                            if name:
                                name = name.strip()
                                
                                if len(name) > 5 and name not in ['Learn more', 'View', 'See more', 'Read more']:
                                    product = {
                                        'name': name[:100],
                                        'url': url,
                                        'source': 'today',
                                        'found_at': datetime.now().isoformat()
                                    }
                                    
                                    print(f"   ✅ Found product: {name[:50]}")
                                    return product
                                    
                    except:
                        continue
                        
            except Exception as e:
                print(f"   ⚠️ Today's launches error: {e}")
                
            print(f"   ❌ No new products found")
            return None
            
        except Exception as e:
            print(f"❌ Product finding error: {e}")
            return None
            
    def engage_and_post_comment(self, page, product):
        """Engage with product and POST comment"""
        try:
            print(f"💬 Engaging with: {product['name'][:50]}...")
            
            # Go to product page
            page.goto(product['url'])
            time.sleep(5)  # Give more time for page to load
            
            # Select strategic Zenyai template
            comment_text = random.choice(self.zenyai_templates)
            
            # Find comment input - try multiple strategies
            comment_input = None
            
            # Strategy 1: Look for textarea
            print(f"   🔍 Looking for comment input...")
            textareas = page.locator('textarea').all()
            print(f"   📊 Found {len(textareas)} textareas")
            
            for textarea in textareas:
                try:
                    if textarea.is_visible():
                        comment_input = textarea
                        print(f"   ✅ Using visible textarea")
                        break
                except:
                    continue
                    
            # Strategy 2: Text input
            if not comment_input:
                text_inputs = page.locator('input[type="text"]').all()
                print(f"   📊 Found {len(text_inputs)} text inputs")
                
                for input_elem in text_inputs:
                    try:
                        if input_elem.is_visible():
                            comment_input = input_elem
                            print(f"   ✅ Using visible text input")
                            break
                    except:
                        continue
                        
            # Strategy 3: Any input
            if not comment_input:
                all_inputs = page.locator('input').all()
                print(f"   📊 Found {len(all_inputs)} total inputs")
                
                for input_elem in all_inputs:
                    try:
                        if input_elem.is_visible():
                            input_type = input_elem.get_attribute('type') or 'text'
                            if input_type in ['text', 'search', '']:
                                comment_input = input_elem
                                print(f"   ✅ Using input type: {input_type}")
                                break
                    except:
                        continue
                        
            if not comment_input:
                print("   ❌ No comment input found")
                return False
                
            # TYPE COMMENT
            try:
                print(f"   ⌨️ Typing Zenyai comment...")
                comment_input.click()
                time.sleep(1)
                comment_input.fill(comment_text)
                time.sleep(2)
                
                print(f"   ✍️ Typed: {comment_text[:60]}...")
                
                # FIND AND PRESS SEND/POST BUTTON
                print(f"   🔍 Looking for submit button...")
                
                buttons = page.locator('button').all()
                print(f"   📊 Found {len(buttons)} buttons")
                
                submit_success = False
                
                for button in buttons:
                    try:
                        button_text = button.text_content()
                        if button_text:
                            button_text_lower = button_text.lower()
                            if any(word in button_text_lower for word in ['comment', 'post', 'submit', 'send', 'reply']):
                                print(f"   🎯 Trying button: '{button_text}'")
                                button.click()
                                submit_success = True
                                print(f"   ✅ POSTED comment using button!")
                                break
                    except Exception as e:
                        continue
                        
                # Try Enter key if no button worked
                if not submit_success:
                    print(f"   ⌨️ Trying Enter key...")
                    comment_input.press('Enter')
                    submit_success = True
                    print(f"   ✅ POSTED comment using Enter!")
                    
                if submit_success:
                    # Mark as commented to avoid duplicates
                    self.commented_products.add(product['url'])
                    self.save_commented_history()
                    
                    time.sleep(3)
                    return True
                else:
                    print("   ❌ Could not post comment")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Comment posting error: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Engagement error: {e}")
            return False
            
    def run_fixed_automation(self, target_engagements=25):
        """Run FIXED automation"""
        try:
            print("🚀 FIXED PRODUCT HUNT AUTOMATION")
            print("=" * 60)
            print("🏠 Strategy: Browse homepage + today's launches")
            print("🔄 Process: Find → Engage → Post → Repeat")
            print("💬 Goal: Strategic Zenyai plugs")
            print("=" * 60)
            
            # Setup
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Manual login
            if not self.manual_login_and_wait(page):
                browser.close()
                return
                
            # START AUTOMATION
            engagements_made = 0
            attempts = 0
            max_attempts = 100  # Prevent infinite loop
            
            print(f"\n🎯 STARTING ENGAGEMENT LOOP")
            print(f"Target: {target_engagements} engagements")
            
            while engagements_made < target_engagements and attempts < max_attempts:
                attempts += 1
                
                print(f"\n🔄 ATTEMPT {engagements_made + 1}/{target_engagements}")
                print(f"🔍 Overall attempt #{attempts}")
                
                # STEP 1: Find ONE product
                product = self.find_one_product_from_homepage(page)
                
                if not product:
                    print(f"   ⚠️ No product found, trying again...")
                    time.sleep(5)
                    continue
                    
                # STEP 2: Engage and post comment
                success = self.engage_and_post_comment(page, product)
                
                if success:
                    engagements_made += 1
                    print(f"   🎉 SUCCESS! Engagement {engagements_made}/{target_engagements}")
                    
                    # Human-like delay between successful engagements
                    delay = random.uniform(15, 25)
                    print(f"   ⏳ Waiting {delay:.1f}s before next attempt...")
                    time.sleep(delay)
                else:
                    print(f"   ❌ Engagement failed, trying again...")
                    # Shorter delay on failure
                    time.sleep(random.uniform(5, 8))
                    
                # Progress update
                print(f"📊 PROGRESS: {engagements_made}/{target_engagements} successful engagements")
                
            # Save results
            self.save_results(engagements_made, attempts)
            
            print(f"\n🎉 FIXED AUTOMATION COMPLETE!")
            print(f"✅ Successful engagements: {engagements_made}")
            print(f"🔍 Total attempts: {attempts}")
            print(f"🎯 Success rate: {(engagements_made/attempts*100):.1f}%")
            print(f"🔥 All comments strategically plug Zenyai!")
            
            input("\nPress ENTER to close...")
            browser.close()
            
        except Exception as e:
            print(f"❌ Fixed automation error: {e}")
            
    def save_results(self, engagements, attempts):
        """Save automation results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_fixed_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'successful_engagements': engagements,
                    'total_attempts': attempts,
                    'success_rate': f"{(engagements/attempts*100):.1f}%" if attempts > 0 else "0%",
                    'total_commented_history': len(self.commented_products),
                    'strategy': 'homepage_and_today_browsing'
                },
                'zenyai_templates': self.zenyai_templates
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run FIXED Product Hunt engagement"""
    
    print("🚀 FIXED PRODUCT HUNT AUTOMATION")
    print("🏠 Browse homepage + today's launches")
    print("🔄 Find → Engage → Post → Repeat")
    print("💬 Strategic Zenyai plugs")
    
    bot = FixedProductHuntEngagement()
    
    # Run fixed automation
    bot.run_fixed_automation(target_engagements=25)

if __name__ == "__main__":
    main()
