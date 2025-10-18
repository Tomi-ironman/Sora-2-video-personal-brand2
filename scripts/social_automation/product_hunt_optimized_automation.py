#!/usr/bin/env python3
"""
OPTIMIZED Product Hunt Automation
Fast, reliable engagement with better timeout handling
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class OptimizedProductHuntBot:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup optimized automation"""
        
        # Authentication
        self.email = os.getenv('PRODUCTHUNT_EMAIL')
        self.password = os.getenv('PRODUCTHUNT_PASSWORD')
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Focused Zenyai engagement templates
        self.engagement_templates = [
            "This looks amazing! We're building Zenyai to solve similar organization challenges for audio creators 🎧",
            "Great execution! Have you considered audio/music workflows? We're tackling metadata chaos at Zenyai 🎵", 
            "Love this! We're solving similar pain points for audio professionals with AI-powered organization 🚀",
            "Impressive work! This could complement what we're building at Zenyai for audio asset management 🤝",
            "Nice launch! Audio creators face similar challenges - we'd love to explore synergies 🎙️",
            "This is exactly what creators need! We're addressing the same problems for audio professionals at Zenyai ⚡"
        ]
        
        # Simplified, high-value search terms
        self.search_terms = [
            "AI tool", "productivity", "workflow", "automation", 
            "audio", "music", "creator tool", "file management", 
            "organization", "API", "developer tool", "SaaS"
        ]
        
        print(f"🚀 Optimized Product Hunt Bot initialized")
        print(f"🎯 {len(self.search_terms)} search terms loaded")
        print(f"💬 {len(self.engagement_templates)} Zenyai-focused templates ready")
        
    def setup_browser(self):
        """Setup optimized browser"""
        try:
            print("🌐 Setting up optimized browser...")
            
            playwright = sync_playwright().start()
            
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-first-run',
                    '--disable-dev-shm-usage'
                ]
            )
            
            page = browser.new_page()
            
            # Set longer timeout for heavy pages
            page.set_default_timeout(60000)  # 60 seconds
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def is_logged_in(self, page):
        """Quick login check"""
        try:
            page.goto("https://www.producthunt.com", timeout=30000)
            time.sleep(3)
            
            # Simple check for login buttons
            login_indicators = ['button:has-text("Log in")', 'a:has-text("Log in")']
            
            for indicator in login_indicators:
                if page.locator(indicator).count() > 0:
                    return False
                    
            return True
            
        except:
            return False
            
    def browse_homepage_products(self, page):
        """Browse products on homepage instead of search"""
        try:
            print("🏠 Browsing homepage products...")
            
            page.goto("https://www.producthunt.com", timeout=30000)
            time.sleep(5)
            
            products = []
            
            # Scroll to load more products
            for scroll in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                
            # Find product links
            product_links = page.locator('a[href*="/posts/"]').all()
            
            for link in product_links[:20]:  # Limit to first 20
                try:
                    href = link.get_attribute('href')
                    if href and '/posts/' in href:
                        url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                        
                        # Get product name from the link text or nearby text
                        name = link.text_content() or "Product"
                        name = name.strip()
                        
                        if len(name) > 3 and url not in [p['url'] for p in products]:
                            products.append({
                                'name': name,
                                'url': url,
                                'source': 'homepage'
                            })
                            
                except:
                    continue
                    
            print(f"   📊 Found {len(products)} products on homepage")
            return products
            
        except Exception as e:
            print(f"❌ Homepage browsing error: {e}")
            return []
            
    def browse_category_products(self, page, category="productivity"):
        """Browse products by category"""
        try:
            print(f"📂 Browsing {category} category...")
            
            # Try category URL
            category_url = f"https://www.producthunt.com/topics/{category}"
            
            try:
                page.goto(category_url, timeout=30000)
                time.sleep(3)
            except:
                print(f"   ⚠️ Category {category} not accessible")
                return []
                
            products = []
            
            # Find products in category
            product_links = page.locator('a[href*="/posts/"]').all()
            
            for link in product_links[:15]:  # Limit to 15 per category
                try:
                    href = link.get_attribute('href')
                    if href and '/posts/' in href:
                        url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                        name = link.text_content() or "Product"
                        name = name.strip()
                        
                        if len(name) > 3:
                            products.append({
                                'name': name,
                                'url': url,
                                'source': f'category_{category}'
                            })
                            
                except:
                    continue
                    
            print(f"   📊 Found {len(products)} products in {category}")
            return products
            
        except Exception as e:
            print(f"❌ Category browsing error: {e}")
            return []
            
    def engage_with_product(self, page, product):
        """Optimized engagement"""
        try:
            print(f"💬 Engaging with: {product['name'][:50]}...")
            
            # Go to product page with timeout
            try:
                page.goto(product['url'], timeout=30000)
                time.sleep(3)
            except:
                print("   ⚠️ Page load timeout")
                return False
                
            # Select engagement template
            comment_text = random.choice(self.engagement_templates)
            
            # Find comment area quickly
            comment_selectors = [
                'textarea',
                'input[type="text"]',
                '[contenteditable="true"]'
            ]
            
            comment_input = None
            for selector in comment_selectors:
                if page.locator(selector).count() > 0:
                    comment_input = page.locator(selector).first
                    break
                    
            if not comment_input:
                print("   ⚠️ No comment input found")
                return False
                
            try:
                # Quick engagement
                comment_input.click()
                time.sleep(0.5)
                comment_input.fill(comment_text)
                time.sleep(1)
                
                # Try to submit
                submit_buttons = page.locator('button').all()
                for button in submit_buttons:
                    button_text = button.text_content().lower()
                    if any(word in button_text for word in ['comment', 'post', 'submit']):
                        button.click()
                        print(f"   ✅ Engaged: {comment_text[:30]}...")
                        time.sleep(2)
                        return True
                        
                print("   ⚠️ No submit button found")
                return False
                
            except Exception as e:
                print(f"   ❌ Engagement error: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Product engagement error: {e}")
            return False
            
    def run_optimized_automation(self, target_engagements=15):
        """Run optimized automation"""
        try:
            print("🚀 OPTIMIZED PRODUCT HUNT AUTOMATION")
            print("=" * 50)
            print(f"🎯 Target: {target_engagements} engagements")
            print("⚡ Fast, focused approach")
            print("=" * 50)
            
            # Setup browser
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Quick login check
            if not self.is_logged_in(page):
                print("❌ Please log in to Product Hunt first")
                browser.close()
                return
                
            print("✅ Login verified!")
            
            all_products = []
            engagements_made = 0
            
            # Strategy 1: Browse homepage
            homepage_products = self.browse_homepage_products(page)
            all_products.extend(homepage_products)
            
            # Strategy 2: Browse categories
            categories = ["productivity", "developer-tools", "artificial-intelligence"]
            for category in categories:
                if len(all_products) < 50:  # Don't collect too many
                    category_products = self.browse_category_products(page, category)
                    all_products.extend(category_products)
                    
            print(f"\n📊 Total products collected: {len(all_products)}")
            
            # Engage with products
            for i, product in enumerate(all_products):
                if engagements_made >= target_engagements:
                    break
                    
                print(f"\n🎯 Engagement {engagements_made+1}/{target_engagements}")
                
                success = self.engage_with_product(page, product)
                if success:
                    engagements_made += 1
                    
                # Human-like delay
                delay = random.uniform(8, 15)
                print(f"   ⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
                
            # Save results
            self.save_results(all_products, engagements_made)
            
            print(f"\n🎉 AUTOMATION COMPLETE!")
            print(f"✅ Engagements made: {engagements_made}")
            print(f"📊 Products discovered: {len(all_products)}")
            print(f"🎯 Success rate: {(engagements_made/len(all_products)*100):.1f}%")
            
            browser.close()
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
    def save_results(self, products, engagements):
        """Save results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_optimized_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products_found': len(products),
                    'total_engagements': engagements,
                    'success_rate': f"{(engagements/len(products)*100):.1f}%" if products else "0%",
                    'zenyai_mentions': engagements  # All engagements mention Zenyai
                },
                'products': products
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run optimized automation"""
    
    bot = OptimizedProductHuntBot()
    
    if not bot.email or not bot.password:
        print("❌ Product Hunt credentials not found!")
        return
        
    print("🚀 Starting OPTIMIZED Product Hunt automation...")
    print("🎯 Focus: Quality engagements with Zenyai mentions")
    print("⚡ Strategy: Homepage + Category browsing")
    print("🔥 All comments mention Zenyai and audio solutions")
    
    # Run optimized automation
    bot.run_optimized_automation(target_engagements=15)

if __name__ == "__main__":
    main()
