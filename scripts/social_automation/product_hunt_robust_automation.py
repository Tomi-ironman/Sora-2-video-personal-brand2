#!/usr/bin/env python3
"""
ROBUST Product Hunt Automation
Enhanced login detection and engagement system
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class RobustProductHuntBot:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup robust automation"""
        
        # Authentication
        self.email = os.getenv('PRODUCTHUNT_EMAIL')
        self.password = os.getenv('PRODUCTHUNT_PASSWORD')
        
        # Session persistence
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Engagement templates focused on Zenyai's audio metadata solution
        self.engagement_templates = [
            "This looks amazing! We're building Zenyai to solve similar organization challenges for audio creators 🎧",
            "Great execution! Have you considered applications for audio/music workflows? We're tackling metadata chaos at Zenyai 🎵",
            "Love the approach! We're solving similar pain points for audio professionals with AI-powered organization 🚀",
            "Impressive work! This could complement what we're building at Zenyai for audio asset management 🤝",
            "Nice launch! Audio creators face similar challenges - we'd love to explore synergies 🎙️",
            "This is exactly what creators need! We're addressing the same problems for audio professionals at Zenyai ⚡",
            "Great tool! How do you handle large file organization? We're tackling this for audio/music at Zenyai 📁",
            "Love the productivity focus! We're building similar solutions for audio metadata management 🎯",
            "Congrats on the launch! This reminds me of the challenges we're solving for audio creators 🎉",
            "Brilliant execution! We're working on complementary solutions for audio workflow optimization 💡"
        ]
        
        # Search terms focused on relevant companies
        self.search_terms = [
            "AI tool", "productivity", "workflow", "automation", "audio", "music", 
            "creator tool", "file management", "organization", "metadata", "API",
            "developer tool", "SaaS", "business tool", "content creation", "media"
        ]
        
        print(f"🚀 Robust Product Hunt Bot initialized")
        print(f"🎯 {len(self.search_terms)} search terms loaded")
        print(f"💬 {len(self.engagement_templates)} Zenyai-focused templates ready")
        
    def setup_browser(self):
        """Setup browser with better detection avoidance"""
        try:
            print("🌐 Setting up robust browser...")
            
            playwright = sync_playwright().start()
            
            # Launch with persistent context and better stealth
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-sandbox'
                ]
            )
            
            page = browser.new_page()
            
            # Enhanced anti-detection
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            """)
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def manual_login_guide(self, page):
        """Guide user through manual login if needed"""
        try:
            print("\n🔐 MANUAL LOGIN REQUIRED")
            print("=" * 40)
            print("1. The browser window should be open")
            print("2. Navigate to Product Hunt and log in manually")
            print("3. Once logged in, press ENTER here to continue")
            print("4. The automation will take over from there")
            print("=" * 40)
            
            # Go to Product Hunt
            page.goto("https://www.producthunt.com", wait_until='networkidle')
            time.sleep(3)
            
            # Wait for manual login
            input("Press ENTER after you've logged in manually...")
            
            # Verify login
            if self.is_logged_in(page):
                print("✅ Login verified! Starting automation...")
                return True
            else:
                print("❌ Login not detected. Please try again.")
                return False
                
        except Exception as e:
            print(f"❌ Manual login error: {e}")
            return False
            
    def is_logged_in(self, page):
        """Check if user is logged in with multiple methods"""
        try:
            # Wait a moment for page to load
            time.sleep(2)
            
            # Look for various logged-in indicators
            logged_in_indicators = [
                # User avatar/profile
                '[data-test="user-avatar"]',
                '.user-avatar',
                '[data-test="profile-dropdown"]',
                
                # Post/Submit buttons
                'button:has-text("Submit")',
                'a:has-text("Submit")',
                '[href="/posts/new"]',
                
                # User menu elements
                '[data-test="user-menu"]',
                '.user-menu',
                
                # Profile links
                'a[href*="/users/"]',
                
                # General user indicators
                '.logged-in',
                '[data-logged-in="true"]'
            ]
            
            for indicator in logged_in_indicators:
                try:
                    if page.locator(indicator).count() > 0:
                        print(f"✅ Login detected via: {indicator}")
                        return True
                except:
                    continue
                    
            # Check for absence of login/signup buttons
            login_buttons = [
                'button:has-text("Log in")',
                'a:has-text("Log in")',
                'button:has-text("Sign up")',
                'a:has-text("Sign up")'
            ]
            
            has_login_buttons = False
            for button in login_buttons:
                try:
                    if page.locator(button).count() > 0:
                        has_login_buttons = True
                        break
                except:
                    continue
                    
            if not has_login_buttons:
                print("✅ Login detected (no login buttons found)")
                return True
                
            return False
            
        except Exception as e:
            print(f"⚠️ Login check error: {e}")
            return False
            
    def find_products_on_page(self, page):
        """Find products on current page"""
        try:
            products = []
            
            # Multiple selectors for product cards
            product_selectors = [
                '[data-test="post-item"]',
                '[data-test="product-item"]', 
                'article[data-test*="post"]',
                '.post-item',
                '.product-card',
                'article',
                '[href*="/posts/"]'
            ]
            
            for selector in product_selectors:
                try:
                    elements = page.locator(selector).all()
                    if len(elements) > 0:
                        print(f"   📊 Found {len(elements)} products using selector: {selector}")
                        
                        for element in elements:
                            try:
                                # Get product name
                                name_selectors = ['h3', 'h2', 'h1', '.product-name', 'a']
                                name = "Unknown Product"
                                
                                for name_sel in name_selectors:
                                    try:
                                        name_elem = element.locator(name_sel).first
                                        if name_elem.count() > 0:
                                            text = name_elem.text_content()
                                            if text and len(text.strip()) > 0:
                                                name = text.strip()
                                                break
                                    except:
                                        continue
                                        
                                # Get product URL
                                url = None
                                try:
                                    # Try to find link within the element
                                    link_elem = element.locator('a[href*="/posts/"]').first
                                    if link_elem.count() > 0:
                                        href = link_elem.get_attribute('href')
                                        if href:
                                            url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                                except:
                                    pass
                                    
                                if name != "Unknown Product" and url:
                                    products.append({
                                        'name': name,
                                        'url': url,
                                        'found_at': datetime.now().isoformat()
                                    })
                                    
                            except Exception as e:
                                continue
                                
                        if len(products) > 0:
                            break  # Found products, no need to try other selectors
                            
                except Exception as e:
                    continue
                    
            return products
            
        except Exception as e:
            print(f"❌ Product finding error: {e}")
            return []
            
    def engage_with_product(self, page, product):
        """Engage with a product"""
        try:
            print(f"💬 Engaging with: {product['name']}")
            
            # Go to product page
            page.goto(product['url'], wait_until='networkidle')
            time.sleep(3)
            
            # Select random engagement template
            comment_text = random.choice(self.engagement_templates)
            
            # Find comment input with multiple selectors
            comment_selectors = [
                'textarea[placeholder*="comment"]',
                'textarea[placeholder*="Add"]',
                'textarea[data-test*="comment"]',
                'textarea',
                'input[placeholder*="comment"]',
                '[data-test="comment-input"]',
                '.comment-input'
            ]
            
            comment_input = None
            for selector in comment_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        comment_input = page.locator(selector).first
                        print(f"   📝 Found comment input: {selector}")
                        break
                except:
                    continue
                    
            if not comment_input:
                print("   ⚠️ Could not find comment input")
                return False
                
            # Click and type comment
            try:
                comment_input.click()
                time.sleep(0.5)
                comment_input.fill(comment_text)
                time.sleep(1)
                
                print(f"   ✍️ Typed: {comment_text[:50]}...")
                
                # Find submit button
                submit_selectors = [
                    'button:has-text("Comment")',
                    'button:has-text("Post")',
                    'button:has-text("Submit")',
                    'button[type="submit"]',
                    '[data-test*="submit"]',
                    '[data-test*="comment-submit"]'
                ]
                
                for selector in submit_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.click(selector)
                            print(f"   ✅ Comment submitted!")
                            time.sleep(2)
                            return True
                    except:
                        continue
                        
                print("   ⚠️ Could not find submit button")
                return False
                
            except Exception as e:
                print(f"   ❌ Comment submission error: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Engagement error: {e}")
            return False
            
    def run_automation(self, target_engagements=50):
        """Run robust automation with smaller target for testing"""
        try:
            print("🚀 ROBUST PRODUCT HUNT AUTOMATION")
            print("=" * 50)
            print(f"🎯 Target: {target_engagements} engagements")
            print("=" * 50)
            
            # Setup browser
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Check login or guide manual login
            if not self.is_logged_in(page):
                if not self.manual_login_guide(page):
                    browser.close()
                    return
                    
            print("🎯 Starting product discovery and engagement...")
            
            engagements_made = 0
            all_products = []
            
            # Go through search terms
            for i, search_term in enumerate(self.search_terms):
                if engagements_made >= target_engagements:
                    break
                    
                print(f"\n🔍 Search {i+1}/{len(self.search_terms)}: '{search_term}'")
                
                # Search for products
                search_url = f"https://www.producthunt.com/search?q={search_term.replace(' ', '%20')}"
                page.goto(search_url, wait_until='networkidle')
                time.sleep(3)
                
                # Find products on this page
                products = self.find_products_on_page(page)
                all_products.extend(products)
                
                print(f"   📊 Found {len(products)} products")
                
                # Engage with products
                for product in products[:5]:  # Limit to 5 per search
                    if engagements_made >= target_engagements:
                        break
                        
                    success = self.engage_with_product(page, product)
                    if success:
                        engagements_made += 1
                        
                    # Delay between engagements
                    delay = random.uniform(5, 10)
                    print(f"   ⏳ Waiting {delay:.1f}s...")
                    time.sleep(delay)
                    
                print(f"📊 Progress: {engagements_made}/{target_engagements} engagements")
                
                # Delay between searches
                if i < len(self.search_terms) - 1:
                    delay = random.uniform(10, 15)
                    time.sleep(delay)
                    
            # Save results
            self.save_results(all_products, engagements_made)
            
            print(f"\n🎉 AUTOMATION COMPLETE!")
            print(f"✅ Total engagements: {engagements_made}")
            print(f"📊 Products discovered: {len(all_products)}")
            
            browser.close()
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
    def save_results(self, products, engagements):
        """Save automation results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_robust_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products_found': len(products),
                    'total_engagements': engagements,
                    'success_rate': f"{(engagements/len(products)*100):.1f}%" if products else "0%"
                },
                'products': products
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run robust Product Hunt automation"""
    
    bot = RobustProductHuntBot()
    
    if not bot.email or not bot.password:
        print("❌ Product Hunt credentials not found!")
        print("📝 Please check PRODUCTHUNT_EMAIL and PRODUCTHUNT_PASSWORD in .env")
        return
        
    print("🚀 Starting robust Product Hunt automation...")
    print("🎯 Goal: Engage with relevant companies about Zenyai")
    print("🔐 Manual login assistance if needed")
    print("⚡ Focused engagement templates")
    
    # Start with smaller target for testing
    bot.run_automation(target_engagements=20)

if __name__ == "__main__":
    main()
