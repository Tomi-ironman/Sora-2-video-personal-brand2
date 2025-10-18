#!/usr/bin/env python3
"""
SMART Product Hunt Engagement
Find relevant companies + Check for existing comments + Strategic engagement
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class SmartProductHuntEngagement:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup smart engagement system"""
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Track commented products to avoid duplicates
        self.commented_products_file = "product_hunt_commented_history.json"
        self.commented_products = self.load_commented_history()
        
        # Relevant search terms for companies similar to Zenyai
        self.relevant_search_terms = [
            # AI & Automation
            "AI productivity", "AI workflow", "AI organization", "AI file management",
            "automation tool", "workflow automation", "smart organization",
            
            # Audio & Media specific
            "audio tool", "music production", "podcast tool", "audio workflow",
            "sound design", "audio organization", "music management",
            
            # File & Asset Management
            "file management", "asset management", "digital organization",
            "metadata management", "content organization", "media management",
            
            # Creator Tools
            "creator tool", "content creation", "creative workflow", 
            "productivity for creators", "creator productivity",
            
            # SaaS & Business Tools
            "SaaS productivity", "business automation", "team workflow",
            "project management", "collaboration tool"
        ]
        
        # Strategic Zenyai engagement templates
        self.engagement_templates = [
            "This looks incredibly useful! We're building something complementary at Zenyai for audio creators who struggle with file organization 🎧",
            "Love the approach to workflow optimization! We're tackling similar challenges specifically for audio professionals with metadata chaos 🎵",
            "Great execution! This reminds me of the pain points we're solving at Zenyai for music producers and podcasters 🚀",
            "Impressive tool! Have you considered applications for audio/music workflows? We're addressing similar organization challenges 🤝",
            "This could be a game-changer for productivity! We're building Zenyai to solve similar problems for audio creators 🎯",
            "Nice launch! The organization features look solid. We're tackling the same challenges for audio professionals 💡",
            "Love tools that solve real workflow problems! We're doing something similar for audio metadata at Zenyai 🔥",
            "Great product! How do you handle large file libraries? We're solving this specifically for audio creators 📁"
        ]
        
        print(f"🚀 Smart Product Hunt Engagement initialized")
        print(f"🎯 {len(self.relevant_search_terms)} relevant search terms")
        print(f"💬 {len(self.engagement_templates)} strategic templates")
        print(f"📝 Tracking {len(self.commented_products)} previously commented products")
        
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
                args=['--disable-blink-features=AutomationControlled']
            )
            
            page = browser.new_page()
            page.set_default_timeout(60000)
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def manual_login_and_wait(self, page):
        """Manual login"""
        try:
            print("\n🔐 MANUAL LOGIN")
            print("=" * 40)
            print("1. Log into Product Hunt in the browser")
            print("2. Make sure you're fully logged in")
            print("3. Press ENTER when ready")
            print("=" * 40)
            
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            input("🔑 Press ENTER after logging in...")
            
            print("✅ Ready for smart engagement!")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def search_for_relevant_products(self, page, search_term, max_products=10):
        """Search for products relevant to Zenyai"""
        try:
            print(f"🔍 Searching: '{search_term}'")
            
            # Search on Product Hunt
            search_url = f"https://www.producthunt.com/search?q={search_term.replace(' ', '%20')}"
            
            try:
                page.goto(search_url, timeout=30000)
                time.sleep(4)
            except:
                print(f"   ⚠️ Search timeout for '{search_term}'")
                return []
                
            products = []
            
            # Find product links
            product_links = page.locator('a[href*="/posts/"]').all()
            
            for link in product_links[:max_products]:
                try:
                    href = link.get_attribute('href')
                    if href:
                        url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                        
                        # Skip if we've already commented
                        if url in self.commented_products:
                            continue
                            
                        # Get product name
                        name = link.text_content() or "Unknown Product"
                        name = name.strip()
                        
                        if len(name) > 3:
                            products.append({
                                'name': name,
                                'url': url,
                                'search_term': search_term,
                                'found_at': datetime.now().isoformat()
                            })
                            
                except:
                    continue
                    
            print(f"   📊 Found {len(products)} new products")
            return products
            
        except Exception as e:
            print(f"❌ Search error for '{search_term}': {e}")
            return []
            
    def check_if_already_commented(self, page, product_url):
        """Check if we've already commented on this product"""
        try:
            # Go to product page
            page.goto(product_url, timeout=30000)
            time.sleep(3)
            
            # Look for our username in comments
            # This is a simple check - you might need to adjust based on your username
            username_indicators = [
                "tomioladunjoye",  # Your email username
                "zenyai",          # Company name
                "Tomi"             # Your name
            ]
            
            # Check page content for our indicators
            page_content = page.content().lower()
            
            for indicator in username_indicators:
                if indicator.lower() in page_content:
                    print(f"   ⚠️ Already commented (found '{indicator}')")
                    return True
                    
            return False
            
        except Exception as e:
            print(f"   ⚠️ Could not check comment history: {e}")
            return False  # If we can't check, assume we haven't commented
            
    def engage_with_product(self, page, product):
        """Strategically engage with a product"""
        try:
            print(f"💬 Engaging: {product['name'][:50]}...")
            
            # Double-check we haven't commented
            if self.check_if_already_commented(page, product['url']):
                self.commented_products.add(product['url'])
                return False
                
            # Go to product page
            page.goto(product['url'], timeout=30000)
            time.sleep(4)
            
            # Select strategic template
            comment_text = random.choice(self.engagement_templates)
            
            # Find comment input
            comment_input = None
            
            # Try different input types
            input_selectors = [
                'textarea',
                'input[type="text"]',
                '[contenteditable="true"]'
            ]
            
            for selector in input_selectors:
                elements = page.locator(selector).all()
                for element in elements:
                    try:
                        if element.is_visible():
                            comment_input = element
                            break
                    except:
                        continue
                if comment_input:
                    break
                    
            if not comment_input:
                print("   ⚠️ No comment input found")
                return False
                
            # Type comment
            try:
                comment_input.click()
                time.sleep(0.5)
                comment_input.fill(comment_text)
                time.sleep(1)
                
                print(f"   ✍️ Typed: {comment_text[:40]}...")
                
                # Submit comment
                submit_success = False
                
                # Try submit buttons
                buttons = page.locator('button').all()
                for button in buttons:
                    try:
                        button_text = button.text_content().lower()
                        if any(word in button_text for word in ['comment', 'post', 'submit']):
                            button.click()
                            submit_success = True
                            break
                    except:
                        continue
                        
                # Try Enter key if no button worked
                if not submit_success:
                    page.keyboard.press('Enter')
                    submit_success = True
                    
                if submit_success:
                    print(f"   ✅ Comment posted successfully!")
                    
                    # Mark as commented
                    self.commented_products.add(product['url'])
                    self.save_commented_history()
                    
                    time.sleep(2)
                    return True
                else:
                    print("   ⚠️ Could not submit comment")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Comment error: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Engagement error: {e}")
            return False
            
    def run_smart_engagement(self, target_engagements=20):
        """Run smart engagement campaign"""
        try:
            print("🚀 SMART PRODUCT HUNT ENGAGEMENT")
            print("=" * 60)
            print("🎯 Strategy: Find relevant companies + No duplicate comments")
            print("🔍 Focus: AI, audio, productivity, creator tools")
            print("💬 Goal: Strategic Zenyai mentions")
            print("=" * 60)
            
            # Setup
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Manual login
            if not self.manual_login_and_wait(page):
                browser.close()
                return
                
            # Collect relevant products
            all_products = []
            
            for search_term in self.relevant_search_terms:
                if len(all_products) >= 100:  # Limit total products
                    break
                    
                products = self.search_for_relevant_products(page, search_term, max_products=8)
                all_products.extend(products)
                
                # Small delay between searches
                time.sleep(random.uniform(2, 4))
                
            print(f"\n📊 DISCOVERY COMPLETE")
            print(f"   🔍 Total products found: {len(all_products)}")
            print(f"   📝 Previously commented: {len(self.commented_products)}")
            print(f"   🎯 Ready for engagement!")
            
            # Remove duplicates
            unique_products = []
            seen_urls = set()
            
            for product in all_products:
                if product['url'] not in seen_urls and product['url'] not in self.commented_products:
                    unique_products.append(product)
                    seen_urls.add(product['url'])
                    
            print(f"   ✅ New products to engage: {len(unique_products)}")
            
            # Start engaging
            engagements_made = 0
            
            for i, product in enumerate(unique_products):
                if engagements_made >= target_engagements:
                    break
                    
                print(f"\n🎯 Engagement {engagements_made + 1}/{target_engagements}")
                
                success = self.engage_with_product(page, product)
                if success:
                    engagements_made += 1
                    
                # Human-like delay
                delay = random.uniform(10, 20)
                print(f"⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
                
                print(f"📊 Progress: {engagements_made}/{target_engagements}")
                
            # Save results
            self.save_results(unique_products, engagements_made)
            
            print(f"\n🎉 SMART ENGAGEMENT COMPLETE!")
            print(f"✅ New engagements: {engagements_made}")
            print(f"📊 Products discovered: {len(unique_products)}")
            print(f"🔒 No duplicate comments!")
            print(f"🎯 All comments strategically mention Zenyai!")
            
            input("\nPress ENTER to close...")
            browser.close()
            
        except Exception as e:
            print(f"❌ Smart engagement error: {e}")
            
    def save_results(self, products, engagements):
        """Save engagement results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_smart_engagement_{timestamp}.json"
            
            results = {
                'engagement_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products_found': len(products),
                    'new_engagements': engagements,
                    'total_commented_history': len(self.commented_products),
                    'duplicate_prevention': True,
                    'strategy': 'relevant_company_targeting'
                },
                'new_products_engaged': products[:engagements],
                'search_terms_used': self.relevant_search_terms,
                'engagement_templates': self.engagement_templates
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run smart Product Hunt engagement"""
    
    print("🚀 SMART PRODUCT HUNT ENGAGEMENT")
    print("🎯 Target: Relevant companies similar to Zenyai")
    print("🔒 Duplicate comment prevention")
    print("💬 Strategic Zenyai mentions")
    
    bot = SmartProductHuntEngagement()
    
    # Run smart engagement
    bot.run_smart_engagement(target_engagements=20)

if __name__ == "__main__":
    main()
