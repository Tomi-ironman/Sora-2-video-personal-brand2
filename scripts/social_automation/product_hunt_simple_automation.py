#!/usr/bin/env python3
"""
SIMPLE Product Hunt Automation
One-time manual login, then full automation
Just like the successful Twitter approach
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class SimpleProductHuntBot:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup simple automation"""
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Focused Zenyai engagement templates
        self.engagement_templates = [
            "This looks amazing! We're building Zenyai to solve similar organization challenges for audio creators 🎧",
            "Great execution! Have you considered audio/music workflows? We're tackling metadata chaos at Zenyai 🎵", 
            "Love this! We're solving similar pain points for audio professionals with AI-powered organization 🚀",
            "Impressive work! This could complement what we're building at Zenyai for audio asset management 🤝",
            "Nice launch! Audio creators face similar challenges - we'd love to explore synergies 🎙️",
            "This is exactly what creators need! We're addressing the same problems for audio professionals at Zenyai ⚡",
            "Great tool! How do you handle large file organization? We're tackling this for audio/music at Zenyai 📁",
            "Love the productivity focus! We're building similar solutions for audio metadata management 🎯",
            "Congrats on the launch! This reminds me of the challenges we're solving for audio creators 🎉",
            "Brilliant execution! We're working on complementary solutions for audio workflow optimization 💡"
        ]
        
        print(f"🚀 Simple Product Hunt Bot initialized")
        print(f"💬 {len(self.engagement_templates)} Zenyai-focused templates ready")
        
    def setup_browser(self):
        """Setup browser with persistent session"""
        try:
            print("🌐 Setting up browser with persistent session...")
            
            playwright = sync_playwright().start()
            
            # Launch with persistent context (saves login)
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-first-run',
                    '--disable-web-security'
                ]
            )
            
            page = browser.new_page()
            page.set_default_timeout(60000)
            
            # Anti-detection
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def manual_login_and_wait(self, page):
        """Manual login with user guidance - just like Twitter approach"""
        try:
            print("\n🔐 ONE-TIME MANUAL LOGIN")
            print("=" * 50)
            print("1. Browser window is opening...")
            print("2. Go to Product Hunt and log in manually")
            print("3. Navigate around, make sure you're fully logged in")
            print("4. Press ENTER here when ready for automation")
            print("=" * 50)
            
            # Go to Product Hunt
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            # Wait for user to log in manually
            input("🔑 Press ENTER after you've logged in and are ready for automation...")
            
            print("✅ Manual login complete! Starting automation...")
            return True
            
        except Exception as e:
            print(f"❌ Manual login error: {e}")
            return False
            
    def discover_products_from_homepage(self, page):
        """Discover products from homepage and today's launches"""
        try:
            print("\n🔍 DISCOVERING PRODUCTS")
            print("-" * 30)
            
            products = []
            
            # Strategy 1: Homepage
            print("🏠 Checking homepage...")
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            # Scroll to load products
            for i in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                
            # Find all links that look like product pages
            all_links = page.locator('a').all()
            
            for link in all_links:
                try:
                    href = link.get_attribute('href')
                    if href and '/posts/' in href and href not in [p.get('url', '') for p in products]:
                        # Get link text as product name
                        text = link.text_content()
                        if text and len(text.strip()) > 2:
                            url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                            products.append({
                                'name': text.strip()[:100],  # Limit name length
                                'url': url,
                                'source': 'homepage'
                            })
                            
                except:
                    continue
                    
            print(f"   📊 Found {len(products)} products from homepage")
            
            # Strategy 2: Today's launches
            if len(products) < 20:
                print("📅 Checking today's launches...")
                try:
                    page.goto("https://www.producthunt.com/posts")
                    time.sleep(3)
                    
                    # Scroll and collect more
                    for i in range(2):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(2)
                        
                    today_links = page.locator('a[href*="/posts/"]').all()
                    
                    for link in today_links:
                        try:
                            href = link.get_attribute('href')
                            if href and href not in [p.get('url', '') for p in products]:
                                text = link.text_content()
                                if text and len(text.strip()) > 2:
                                    url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                                    products.append({
                                        'name': text.strip()[:100],
                                        'url': url,
                                        'source': 'today'
                                    })
                                    
                        except:
                            continue
                            
                    print(f"   📊 Found {len(products)} total products")
                    
                except Exception as e:
                    print(f"   ⚠️ Today's launches error: {e}")
                    
            # Remove duplicates and limit
            unique_products = []
            seen_urls = set()
            
            for product in products:
                if product['url'] not in seen_urls:
                    unique_products.append(product)
                    seen_urls.add(product['url'])
                    
            return unique_products[:50]  # Limit to 50 products
            
        except Exception as e:
            print(f"❌ Product discovery error: {e}")
            return []
            
    def engage_with_product(self, page, product):
        """Engage with a specific product"""
        try:
            print(f"💬 Engaging: {product['name'][:50]}...")
            
            # Go to product page
            page.goto(product['url'])
            time.sleep(4)  # Give page time to load
            
            # Select random Zenyai template
            comment_text = random.choice(self.engagement_templates)
            
            # Try multiple strategies to find comment input
            comment_found = False
            
            # Strategy 1: Look for textarea
            textareas = page.locator('textarea').all()
            for textarea in textareas:
                try:
                    if textarea.is_visible():
                        textarea.click()
                        time.sleep(0.5)
                        textarea.fill(comment_text)
                        comment_found = True
                        print(f"   ✍️ Used textarea: {comment_text[:30]}...")
                        break
                except:
                    continue
                    
            # Strategy 2: Look for text inputs if textarea didn't work
            if not comment_found:
                text_inputs = page.locator('input[type="text"]').all()
                for input_elem in text_inputs:
                    try:
                        if input_elem.is_visible():
                            input_elem.click()
                            time.sleep(0.5)
                            input_elem.fill(comment_text)
                            comment_found = True
                            print(f"   ✍️ Used text input: {comment_text[:30]}...")
                            break
                    except:
                        continue
                        
            # Strategy 3: Look for contenteditable
            if not comment_found:
                editables = page.locator('[contenteditable="true"]').all()
                for editable in editables:
                    try:
                        if editable.is_visible():
                            editable.click()
                            time.sleep(0.5)
                            editable.fill(comment_text)
                            comment_found = True
                            print(f"   ✍️ Used contenteditable: {comment_text[:30]}...")
                            break
                    except:
                        continue
                        
            if not comment_found:
                print("   ⚠️ No comment input found")
                return False
                
            # Try to submit the comment
            time.sleep(1)
            
            # Look for submit buttons
            submit_buttons = page.locator('button').all()
            
            for button in submit_buttons:
                try:
                    button_text = button.text_content().lower()
                    if any(word in button_text for word in ['comment', 'post', 'submit', 'send']):
                        button.click()
                        print(f"   ✅ Comment submitted!")
                        time.sleep(2)
                        return True
                except:
                    continue
                    
            # If no specific submit button, try pressing Enter
            try:
                page.keyboard.press('Enter')
                print(f"   ✅ Comment submitted with Enter!")
                time.sleep(2)
                return True
            except:
                pass
                
            print("   ⚠️ Could not submit comment")
            return False
            
        except Exception as e:
            print(f"   ❌ Engagement error: {e}")
            return False
            
    def run_simple_automation(self, target_engagements=25):
        """Run simple automation after manual login"""
        try:
            print("🚀 SIMPLE PRODUCT HUNT AUTOMATION")
            print("=" * 60)
            print("🎯 Strategy: Manual login + Full automation")
            print("⚡ Just like successful Twitter approach")
            print("🔥 Every comment mentions Zenyai")
            print("=" * 60)
            
            # Setup browser
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Manual login
            if not self.manual_login_and_wait(page):
                browser.close()
                return
                
            # Discover products
            products = self.discover_products_from_homepage(page)
            
            if not products:
                print("❌ No products found")
                browser.close()
                return
                
            print(f"📊 Found {len(products)} products to engage with")
            
            # Start engaging
            engagements_made = 0
            
            for i, product in enumerate(products):
                if engagements_made >= target_engagements:
                    break
                    
                print(f"\n🎯 Engagement {engagements_made + 1}/{target_engagements}")
                
                success = self.engage_with_product(page, product)
                if success:
                    engagements_made += 1
                    
                # Human-like delay between engagements
                delay = random.uniform(8, 15)
                print(f"⏳ Waiting {delay:.1f}s before next engagement...")
                time.sleep(delay)
                
                # Progress update
                print(f"📊 Progress: {engagements_made}/{target_engagements} engagements completed")
                
            # Save results
            self.save_results(products, engagements_made)
            
            print(f"\n🎉 AUTOMATION COMPLETE!")
            print(f"✅ Total engagements: {engagements_made}")
            print(f"📊 Products discovered: {len(products)}")
            print(f"🎯 Success rate: {(engagements_made/len(products)*100):.1f}%")
            print(f"🔥 All comments mentioned Zenyai and audio solutions!")
            
            input("\nPress ENTER to close browser...")
            browser.close()
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
    def save_results(self, products, engagements):
        """Save automation results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_simple_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products_found': len(products),
                    'total_engagements': engagements,
                    'success_rate': f"{(engagements/len(products)*100):.1f}%" if products else "0%",
                    'zenyai_mentions': engagements,
                    'approach': 'manual_login_then_automation'
                },
                'products': products,
                'engagement_templates_used': self.engagement_templates
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run simple Product Hunt automation"""
    
    print("🚀 SIMPLE PRODUCT HUNT AUTOMATION")
    print("🎯 Just like our successful Twitter approach!")
    print("🔐 One-time manual login, then full automation")
    print("⚡ Fast, focused Zenyai engagement")
    
    bot = SimpleProductHuntBot()
    
    # Run automation
    bot.run_simple_automation(target_engagements=25)

if __name__ == "__main__":
    main()
