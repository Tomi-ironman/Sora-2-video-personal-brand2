#!/usr/bin/env python3
"""
ROBUST Product Hunt Engagement - EXACTLY like Twitter automation
Search → Find → Engage → Post → Repeat
Target where YOUR CUSTOMERS are looking!
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class RobustProductHuntEngagement:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup robust automation exactly like Twitter"""
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Track commented products to avoid duplicates
        self.commented_products_file = "product_hunt_commented_history.json"
        self.commented_products = self.load_commented_history()
        
        # TARGET WHERE YOUR CUSTOMERS ARE LOOKING!
        # These are tools YOUR ICP (audio professionals) would be searching for
        self.customer_search_terms = [
            # PODCAST TOOLS (where podcasters look)
            "podcast editing", "podcast software", "podcast tool", "podcast production",
            "podcast workflow", "podcast automation", "podcast management", "podcast platform",
            
            # AUDIO PRODUCTION (where audio professionals look)
            "audio editing", "audio software", "audio production", "audio tool",
            "sound editing", "sound design", "audio workflow", "music production",
            
            # MUSIC TOOLS (where music producers look)
            "music software", "music production", "music tool", "beat making",
            "music workflow", "music management", "sample library", "music organization",
            
            # BROADCASTING (where broadcasters look)
            "broadcasting software", "radio software", "streaming tool", "live audio",
            "broadcast automation", "radio automation", "streaming platform",
            
            # SOUND DESIGN (where sound designers look)
            "sound design", "audio effects", "sound library", "foley tool",
            "sound management", "audio assets", "sound organization",
            
            # FILM/VIDEO AUDIO (where filmmakers look)
            "video editing", "film audio", "post production", "audio sync",
            "video production", "film software", "editing workflow",
            
            # CONTENT CREATION (where content creators look)
            "content creation", "creator tool", "video tool", "social media tool",
            "content workflow", "creator platform", "content management"
        ]
        
        # ZENYAI ENGAGEMENT TEMPLATES - Strategic plugs
        self.zenyai_templates = [
            "This looks great for audio workflow! Speaking of audio organization, we're building Zenyai to solve the metadata chaos that podcasters and producers face daily 🎧 Check us out if you're dealing with sample/audio file organization!",
            
            "Love seeing tools for audio professionals! We're tackling a similar pain point at Zenyai - helping music producers and podcasters organize their audio assets with AI-powered metadata management 🎵",
            
            "Great tool! For anyone in audio production struggling with file organization, we're building Zenyai specifically to solve the metadata nightmare that every producer knows too well 🚀",
            
            "This is exactly what the audio community needs! We're solving the complementary problem at Zenyai - audio file organization and metadata management for producers who have thousands of samples 🎙️",
            
            "Impressive work! If you're in audio/music production and this tool helps your workflow, you might also want to check out Zenyai - we're solving the audio asset organization problem that every producer faces 💡",
            
            "Nice launch! The audio production community needs more tools like this. We're building Zenyai to tackle the specific problem of audio metadata and sample library organization 🔥",
            
            "Great to see innovation in audio tools! For producers and podcasters reading this - if you struggle with organizing your audio files/samples, that's exactly what we're solving at Zenyai 🎯",
            
            "Love the focus on audio workflow! We're addressing the flip side at Zenyai - helping audio professionals organize and find their files faster with smart metadata management 📁"
        ]
        
        print(f"🚀 ROBUST Product Hunt Engagement initialized")
        print(f"🎯 {len(self.customer_search_terms)} customer-focused search terms")
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
            print("🌐 Setting up robust browser...")
            
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
        """Manual login - one time setup"""
        try:
            print("\n🔐 ONE-TIME MANUAL LOGIN")
            print("=" * 50)
            print("1. Log into Product Hunt in the browser")
            print("2. Make sure you're fully logged in")
            print("3. Press ENTER when ready for ROBUST automation")
            print("=" * 50)
            
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            input("🔑 Press ENTER after logging in...")
            
            print("✅ Ready for ROBUST engagement!")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def search_and_find_one_product(self, page, search_term):
        """Search for ONE product and return it - just like Twitter"""
        try:
            print(f"🔍 Searching: '{search_term}'")
            
            # Search on Product Hunt
            search_url = f"https://www.producthunt.com/search?q={search_term.replace(' ', '%20')}"
            
            try:
                page.goto(search_url, timeout=30000)
                time.sleep(4)
            except:
                print(f"   ⚠️ Search timeout for '{search_term}'")
                return None
                
            # DEBUG: Check what's on the page
            print(f"   🔍 Analyzing page content...")
            
            # Try multiple selectors based on current Product Hunt interface
            product_selectors = [
                'a[href*="/posts/"]',  # Original
                'a[href*="/products/"]',  # Alternative
                '[data-test="product-item"] a',  # Data test
                '.product-item a',  # Class based
                'h3 a',  # Heading links
                'h2 a',  # Heading links
                'div[role="link"]',  # Role based
                'a'  # All links as fallback
            ]
            
            found_any_links = False
            
            for selector in product_selectors:
                try:
                    links = page.locator(selector).all()
                    print(f"   📊 Selector '{selector}': {len(links)} links found")
                    
                    if len(links) > 0:
                        found_any_links = True
                        
                        # Try to find a product link
                        for link in links:
                            try:
                                href = link.get_attribute('href')
                                if href and ('/posts/' in href or '/products/' in href):
                                    url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                                    
                                    # Skip if we've already commented
                                    if url in self.commented_products:
                                        continue
                                        
                                    # Get product name from link text or nearby text
                                    name = link.text_content() or "Product"
                                    name = name.strip()
                                    
                                    # If name is too short, try to get it from parent element
                                    if len(name) <= 3:
                                        try:
                                            parent = link.locator('xpath=..')
                                            parent_text = parent.text_content()
                                            if parent_text and len(parent_text.strip()) > 3:
                                                name = parent_text.strip()
                                        except:
                                            pass
                                    
                                    if len(name) > 3:
                                        product = {
                                            'name': name[:100],  # Limit name length
                                            'url': url,
                                            'search_term': search_term,
                                            'found_at': datetime.now().isoformat(),
                                            'selector_used': selector
                                        }
                                        
                                        print(f"   ✅ Found product: {name[:50]} (using {selector})")
                                        return product
                                        
                            except Exception as e:
                                continue
                                
                except Exception as e:
                    continue
                    
            if not found_any_links:
                print(f"   ❌ No links found with any selector")
                
                # DEBUG: Print page title and URL to see what we're actually on
                try:
                    page_title = page.title()
                    current_url = page.url
                    print(f"   📄 Page title: {page_title}")
                    print(f"   🌐 Current URL: {current_url}")
                except:
                    pass
                            
                except:
                    continue
                    
            print(f"   ❌ No new products found for '{search_term}'")
            return None
            
        except Exception as e:
            print(f"❌ Search error for '{search_term}': {e}")
            return None
            
    def engage_and_post_comment(self, page, product):
        """Engage with product and POST comment - just like Twitter"""
        try:
            print(f"💬 Engaging with: {product['name'][:50]}...")
            
            # Go to product page
            page.goto(product['url'], timeout=30000)
            time.sleep(4)
            
            # Select strategic Zenyai template
            comment_text = random.choice(self.zenyai_templates)
            
            # Find comment input - try multiple strategies
            comment_input = None
            
            # Strategy 1: Textarea
            textareas = page.locator('textarea').all()
            for textarea in textareas:
                try:
                    if textarea.is_visible():
                        comment_input = textarea
                        print(f"   📝 Found textarea input")
                        break
                except:
                    continue
                    
            # Strategy 2: Text input
            if not comment_input:
                text_inputs = page.locator('input[type="text"]').all()
                for input_elem in text_inputs:
                    try:
                        if input_elem.is_visible():
                            comment_input = input_elem
                            print(f"   📝 Found text input")
                            break
                    except:
                        continue
                        
            # Strategy 3: Contenteditable
            if not comment_input:
                editables = page.locator('[contenteditable="true"]').all()
                for editable in editables:
                    try:
                        if editable.is_visible():
                            comment_input = editable
                            print(f"   📝 Found contenteditable")
                            break
                    except:
                        continue
                        
            if not comment_input:
                print("   ❌ No comment input found")
                return False
                
            # TYPE COMMENT (instant like Twitter)
            try:
                comment_input.click()
                time.sleep(0.5)
                comment_input.fill(comment_text)
                time.sleep(1)
                
                print(f"   ✍️ Typed Zenyai plug: {comment_text[:60]}...")
                
                # FIND AND PRESS SEND/POST BUTTON
                submit_success = False
                
                # Look for submit buttons
                buttons = page.locator('button').all()
                for button in buttons:
                    try:
                        button_text = button.text_content().lower()
                        if any(word in button_text for word in ['comment', 'post', 'submit', 'send']):
                            button.click()
                            submit_success = True
                            print(f"   ✅ POSTED comment using button: {button_text}")
                            break
                    except:
                        continue
                        
                # Try Enter key if no button worked
                if not submit_success:
                    page.keyboard.press('Enter')
                    submit_success = True
                    print(f"   ✅ POSTED comment using Enter key")
                    
                if submit_success:
                    # Mark as commented to avoid duplicates
                    self.commented_products.add(product['url'])
                    self.save_commented_history()
                    
                    time.sleep(2)
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
            
    def run_robust_automation(self, target_engagements=30):
        """Run ROBUST automation - EXACTLY like Twitter approach"""
        try:
            print("🚀 ROBUST PRODUCT HUNT AUTOMATION")
            print("=" * 70)
            print("🎯 Strategy: Search → Find → Engage → Post → Repeat")
            print("🔍 Target: Where YOUR CUSTOMERS are looking")
            print("💬 Goal: Strategic Zenyai plugs for visibility")
            print("🔄 Process: One search, one engagement, one post, repeat")
            print("=" * 70)
            
            # Setup
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Manual login
            if not self.manual_login_and_wait(page):
                browser.close()
                return
                
            # START ROBUST AUTOMATION
            engagements_made = 0
            search_attempts = 0
            max_search_attempts = len(self.customer_search_terms) * 3  # Try each term multiple times
            
            # Shuffle search terms for variety
            search_terms = self.customer_search_terms.copy()
            random.shuffle(search_terms)
            
            print(f"\n🎯 STARTING ROBUST ENGAGEMENT LOOP")
            print(f"Target: {target_engagements} engagements")
            
            while engagements_made < target_engagements and search_attempts < max_search_attempts:
                # Pick search term (cycle through them)
                search_term = search_terms[search_attempts % len(search_terms)]
                search_attempts += 1
                
                print(f"\n🔄 ATTEMPT {engagements_made + 1}/{target_engagements}")
                print(f"🔍 Search attempt {search_attempts}")
                
                # STEP 1: Search and find ONE product
                product = self.search_and_find_one_product(page, search_term)
                
                if not product:
                    print(f"   ⚠️ No product found, trying next search term...")
                    time.sleep(2)
                    continue
                    
                # STEP 2: Engage and post comment
                success = self.engage_and_post_comment(page, product)
                
                if success:
                    engagements_made += 1
                    print(f"   🎉 SUCCESS! Engagement {engagements_made}/{target_engagements}")
                    
                    # Human-like delay between successful engagements
                    delay = random.uniform(15, 25)
                    print(f"   ⏳ Waiting {delay:.1f}s before next search...")
                    time.sleep(delay)
                else:
                    print(f"   ❌ Engagement failed, trying next search term...")
                    # Shorter delay on failure
                    time.sleep(random.uniform(3, 6))
                    
                # Progress update
                print(f"📊 PROGRESS: {engagements_made}/{target_engagements} successful engagements")
                
            # Save results
            self.save_results(engagements_made, search_attempts)
            
            print(f"\n🎉 ROBUST AUTOMATION COMPLETE!")
            print(f"✅ Successful engagements: {engagements_made}")
            print(f"🔍 Search attempts: {search_attempts}")
            print(f"🎯 Success rate: {(engagements_made/search_attempts*100):.1f}%")
            print(f"🔥 All comments strategically plug Zenyai!")
            print(f"👀 Your comments are now visible to YOUR target customers!")
            
            input("\nPress ENTER to close...")
            browser.close()
            
        except Exception as e:
            print(f"❌ Robust automation error: {e}")
            
    def save_results(self, engagements, search_attempts):
        """Save robust automation results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_robust_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'successful_engagements': engagements,
                    'search_attempts': search_attempts,
                    'success_rate': f"{(engagements/search_attempts*100):.1f}%" if search_attempts > 0 else "0%",
                    'total_commented_history': len(self.commented_products),
                    'strategy': 'search_find_engage_post_repeat',
                    'target_audience': 'audio_professionals_looking_for_tools'
                },
                'search_terms_used': self.customer_search_terms,
                'zenyai_templates': self.zenyai_templates
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run ROBUST Product Hunt engagement"""
    
    print("🚀 ROBUST PRODUCT HUNT AUTOMATION")
    print("🎯 Target: Where YOUR CUSTOMERS are looking")
    print("🔄 Process: Search → Find → Engage → Post → Repeat")
    print("💬 Strategy: Strategic Zenyai plugs for maximum visibility")
    
    bot = RobustProductHuntEngagement()
    
    # Run robust automation
    bot.run_robust_automation(target_engagements=30)

if __name__ == "__main__":
    main()
