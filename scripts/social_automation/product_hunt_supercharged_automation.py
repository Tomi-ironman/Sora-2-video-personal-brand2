#!/usr/bin/env python3
"""
SUPERCHARGED Product Hunt Automation
Find 1000+ companies and engage authentically
One-time login, persistent session, massive scale
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class SuperchargedProductHuntBot:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup supercharged automation"""
        
        # Authentication - use your existing variable names
        self.email = (
            os.getenv('PRODUCTHUNT_EMAIL') or 
            os.getenv('PRODUCT_HUNT_EMAIL') or 
            os.getenv('PH_EMAIL')
        )
        self.password = (
            os.getenv('PRODUCTHUNT_PASSWORD') or 
            os.getenv('PRODUCT_HUNT_PASSWORD') or 
            os.getenv('PH_PASSWORD')
        )
        
        # API credentials (for potential future API usage)
        self.api_key = os.getenv('PRODUCTHUNT_API_KEY')
        self.api_secret = os.getenv('PRODUCTHUNT_API_SECRET')
        self.access_token = os.getenv('PRODUCTHUNT_ACCESS_TOKEN')
        self.developer_token = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
        
        # Session persistence
        self.session_file = "product_hunt_session.json"
        self.browser_data_dir = "product_hunt_browser_data"
        
        # Engagement targets
        self.target_categories = [
            "AI", "SaaS", "Productivity", "Developer Tools", "Design Tools",
            "Marketing", "Analytics", "Automation", "API", "No-Code",
            "Audio", "Video", "Content Creation", "Social Media", "Workflow",
            "Data", "Machine Learning", "Startup Tools", "Business Intelligence",
            "Project Management", "Communication", "Finance", "E-commerce"
        ]
        
        # Engagement templates for different scenarios
        self.engagement_templates = {
            "ai_tools": [
                "This looks incredibly powerful! How does the AI training process work? 🤖",
                "Love the AI integration! Have you considered audio/metadata applications? 🎵",
                "Impressive AI capabilities! We're building something similar at Zenyai for audio creators 🚀",
                "The AI workflow looks smooth! How do you handle large datasets? 📊",
                "Amazing AI tool! We'd love to explore integration opportunities 🤝"
            ],
            
            "productivity": [
                "This could be a game-changer for creative workflows! 🎯",
                "Love the productivity focus! We're solving similar pain points for audio professionals 🎧",
                "Great execution! How do you handle file organization at scale? 📁",
                "This workflow optimization is brilliant! We're tackling similar challenges at Zenyai 🚀",
                "Impressive productivity gains! Have you considered audio/media use cases? 🎵"
            ],
            
            "developer_tools": [
                "Clean implementation! What's your tech stack? 💻",
                "Love the developer experience! We're building APIs for audio metadata at Zenyai 🔧",
                "Great tool! How do you handle API rate limiting? ⚡",
                "Impressive dev tools! We'd love to explore integration possibilities 🤝",
                "Nice work! Have you considered audio processing applications? 🎵"
            ],
            
            "content_creation": [
                "This is exactly what creators need! 🎬",
                "Love the creator focus! We're solving metadata chaos for audio creators at Zenyai 🎧",
                "Great for content workflows! How do you handle large media files? 📁",
                "Perfect for creators! We're tackling similar organization challenges 🚀",
                "Impressive creator tools! Have you considered audio/podcast applications? 🎙️"
            ],
            
            "general": [
                "Congrats on the launch! This looks really promising 🎉",
                "Great execution! We're building something complementary at Zenyai for audio creators 🎵",
                "Love the approach! How do you plan to scale this? 📈",
                "Impressive work! We'd love to connect and explore synergies 🤝",
                "Nice launch! Have you considered applications in audio/media workflows? 🎧"
            ]
        }
        
        # Massive search terms for finding companies
        self.search_terms = [
            # AI & ML
            "AI tool", "machine learning", "artificial intelligence", "neural network",
            "deep learning", "computer vision", "natural language", "AI assistant",
            "AI automation", "AI analytics", "AI platform", "AI API",
            
            # Audio & Media
            "audio tool", "music production", "podcast tool", "audio editor",
            "sound design", "audio API", "music app", "audio processing",
            "voice tool", "audio analytics", "music platform", "audio workflow",
            
            # Productivity
            "productivity tool", "workflow automation", "task management", "project tool",
            "team collaboration", "productivity app", "efficiency tool", "automation platform",
            "workflow tool", "productivity suite", "organization tool", "planning app",
            
            # Developer Tools
            "developer tool", "API platform", "coding tool", "dev environment",
            "development platform", "programming tool", "code editor", "dev tool",
            "API management", "developer API", "coding platform", "dev suite",
            
            # SaaS & Business
            "SaaS platform", "business tool", "enterprise software", "B2B tool",
            "business automation", "company software", "business platform", "SaaS app",
            "business solution", "enterprise platform", "business API", "SaaS solution",
            
            # Design & Creative
            "design tool", "creative software", "design platform", "creative tool",
            "design app", "creative suite", "design automation", "creative platform",
            "design API", "creative workflow", "design solution", "creative app",
            
            # Data & Analytics
            "analytics tool", "data platform", "business intelligence", "data analytics",
            "analytics platform", "data tool", "metrics tool", "analytics app",
            "data visualization", "analytics API", "data science", "analytics suite",
            
            # Marketing & Social
            "marketing tool", "social media", "marketing automation", "growth tool",
            "marketing platform", "social tool", "marketing app", "growth platform",
            "marketing API", "social automation", "marketing suite", "growth app"
        ]
        
        print(f"🚀 Supercharged Product Hunt Bot initialized")
        print(f"🎯 {len(self.search_terms)} search terms loaded")
        print(f"💬 {sum(len(templates) for templates in self.engagement_templates.values())} engagement templates ready")
        
    def setup_persistent_browser(self):
        """Setup browser with persistent session"""
        try:
            print("🌐 Setting up persistent browser...")
            
            playwright = sync_playwright().start()
            
            # Launch with persistent context
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                headless=False,  # Visible for initial setup
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions-except=',
                    '--disable-extensions',
                    '--no-first-run',
                    '--no-default-browser-check'
                ]
            )
            
            # Anti-detection
            page = browser.new_page()
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
            """)
            
            return browser, page
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return None, None
            
    def login_once(self, page):
        """One-time login with session persistence"""
        try:
            print("🔐 Checking login status...")
            
            # Go to Product Hunt
            page.goto("https://www.producthunt.com", wait_until='networkidle')
            time.sleep(3)
            
            # Check if already logged in
            if self.is_logged_in(page):
                print("✅ Already logged in!")
                return True
                
            print("🔑 Logging in...")
            
            # Find and click login button
            login_selectors = [
                'a[href="/login"]',
                'button:has-text("Log in")',
                '[data-test="login-button"]',
                '.login-button'
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.click(selector)
                        login_clicked = True
                        break
                except:
                    continue
                    
            if not login_clicked:
                print("❌ Could not find login button")
                return False
                
            time.sleep(3)
            
            # Fill email
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                '#email',
                '[data-test="email-input"]'
            ]
            
            email_filled = False
            for selector in email_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, self.email)
                        email_filled = True
                        break
                except:
                    continue
                    
            if not email_filled:
                print("❌ Could not find email field")
                return False
                
            # Fill password
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password',
                '[data-test="password-input"]'
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, self.password)
                        password_filled = True
                        break
                except:
                    continue
                    
            if not password_filled:
                print("❌ Could not find password field")
                return False
                
            # Submit login
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Log in")',
                'button:has-text("Sign in")',
                '[data-test="login-submit"]'
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.click(selector)
                        submit_clicked = True
                        break
                except:
                    continue
                    
            if not submit_clicked:
                print("❌ Could not find submit button")
                return False
                
            # Wait for login to complete
            time.sleep(5)
            
            # Verify login
            if self.is_logged_in(page):
                print("✅ Login successful!")
                return True
            else:
                print("❌ Login failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def is_logged_in(self, page):
        """Check if user is logged in"""
        try:
            # Look for logged-in indicators
            logged_in_indicators = [
                '[data-test="user-menu"]',
                '.user-avatar',
                'button:has-text("Post")',
                'a[href="/posts/new"]',
                '.profile-dropdown'
            ]
            
            for indicator in logged_in_indicators:
                if page.locator(indicator).count() > 0:
                    return True
                    
            return False
            
        except:
            return False
            
    def search_and_collect_products(self, page, search_term, target_count=50):
        """Search for products and collect them"""
        try:
            print(f"🔍 Searching for: '{search_term}'")
            
            # Go to search
            search_url = f"https://www.producthunt.com/search?q={search_term.replace(' ', '%20')}"
            page.goto(search_url, wait_until='networkidle')
            time.sleep(3)
            
            products = []
            scroll_count = 0
            max_scrolls = 10
            
            while len(products) < target_count and scroll_count < max_scrolls:
                # Find product cards
                product_selectors = [
                    '[data-test="product-item"]',
                    '.product-card',
                    'article',
                    '[data-test="post-item"]'
                ]
                
                current_products = []
                for selector in product_selectors:
                    elements = page.locator(selector).all()
                    if elements:
                        current_products = elements
                        break
                        
                # Extract product info
                for element in current_products:
                    try:
                        # Get product name
                        name_selectors = [
                            'h3', 'h2', '.product-name', 
                            '[data-test="product-name"]', 'a[href*="/posts/"]'
                        ]
                        
                        name = "Unknown Product"
                        for name_sel in name_selectors:
                            name_elem = element.locator(name_sel).first
                            if name_elem.count() > 0:
                                name = name_elem.text_content().strip()
                                break
                                
                        # Get product URL
                        url_selectors = [
                            'a[href*="/posts/"]',
                            'a[href*="/products/"]',
                            'a'
                        ]
                        
                        url = None
                        for url_sel in url_selectors:
                            url_elem = element.locator(url_sel).first
                            if url_elem.count() > 0:
                                href = url_elem.get_attribute('href')
                                if href and ('/posts/' in href or '/products/' in href):
                                    url = href if href.startswith('http') else f"https://www.producthunt.com{href}"
                                    break
                                    
                        if name and url and url not in [p['url'] for p in products]:
                            products.append({
                                'name': name,
                                'url': url,
                                'search_term': search_term,
                                'found_at': datetime.now().isoformat()
                            })
                            
                    except Exception as e:
                        continue
                        
                # Scroll for more products
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                scroll_count += 1
                
                print(f"   📊 Found {len(products)} products (scroll {scroll_count}/{max_scrolls})")
                
            print(f"✅ Collected {len(products)} products for '{search_term}'")
            return products
            
        except Exception as e:
            print(f"❌ Search error for '{search_term}': {e}")
            return []
            
    def engage_with_product(self, page, product):
        """Engage with a specific product"""
        try:
            print(f"💬 Engaging with: {product['name']}")
            
            # Go to product page
            page.goto(product['url'], wait_until='networkidle')
            time.sleep(3)
            
            # Determine engagement template based on product
            template_category = self.categorize_product(product)
            templates = self.engagement_templates.get(template_category, self.engagement_templates['general'])
            
            # Select random template
            comment_text = random.choice(templates)
            
            # Find comment input
            comment_selectors = [
                'textarea[placeholder*="comment"]',
                'textarea[placeholder*="Add"]',
                'textarea[data-test="comment-input"]',
                'textarea',
                'input[placeholder*="comment"]'
            ]
            
            comment_input = None
            for selector in comment_selectors:
                if page.locator(selector).count() > 0:
                    comment_input = page.locator(selector).first
                    break
                    
            if not comment_input:
                print("   ⚠️ Could not find comment input")
                return False
                
            # Type comment with human-like speed
            comment_input.click()
            time.sleep(0.5)
            
            # Type instantly (like Twitter automation)
            comment_input.fill(comment_text)
            time.sleep(1)
            
            # Find and click submit
            submit_selectors = [
                'button:has-text("Comment")',
                'button:has-text("Post")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                '[data-test="comment-submit"]'
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.click(selector)
                        submit_clicked = True
                        break
                except:
                    continue
                    
            if submit_clicked:
                print(f"   ✅ Comment posted: {comment_text[:50]}...")
                time.sleep(2)
                return True
            else:
                print("   ⚠️ Could not find submit button")
                return False
                
        except Exception as e:
            print(f"   ❌ Engagement error: {e}")
            return False
            
    def categorize_product(self, product):
        """Categorize product for appropriate engagement template"""
        try:
            name_lower = product['name'].lower()
            search_term_lower = product['search_term'].lower()
            
            # AI/ML keywords
            if any(keyword in name_lower or keyword in search_term_lower for keyword in 
                   ['ai', 'artificial', 'machine learning', 'neural', 'deep learning']):
                return 'ai_tools'
                
            # Productivity keywords
            elif any(keyword in name_lower or keyword in search_term_lower for keyword in 
                     ['productivity', 'workflow', 'automation', 'task', 'project']):
                return 'productivity'
                
            # Developer tools
            elif any(keyword in name_lower or keyword in search_term_lower for keyword in 
                     ['developer', 'api', 'code', 'programming', 'dev']):
                return 'developer_tools'
                
            # Content creation
            elif any(keyword in name_lower or keyword in search_term_lower for keyword in 
                     ['content', 'creative', 'design', 'video', 'audio', 'media']):
                return 'content_creation'
                
            else:
                return 'general'
                
        except:
            return 'general'
            
    def run_supercharged_automation(self, target_engagements=1000):
        """Run supercharged Product Hunt automation"""
        try:
            print("🚀 SUPERCHARGED PRODUCT HUNT AUTOMATION")
            print("=" * 60)
            print(f"🎯 Target: {target_engagements} engagements")
            print(f"🔍 Search terms: {len(self.search_terms)}")
            print("=" * 60)
            
            # Setup browser
            browser, page = self.setup_persistent_browser()
            if not browser or not page:
                return
                
            # One-time login
            if not self.login_once(page):
                print("❌ Login failed - stopping automation")
                browser.close()
                return
                
            # Start automation
            all_products = []
            engagements_made = 0
            
            # Shuffle search terms for variety
            search_terms = self.search_terms.copy()
            random.shuffle(search_terms)
            
            for i, search_term in enumerate(search_terms):
                if engagements_made >= target_engagements:
                    break
                    
                print(f"\n🔍 Search {i+1}/{len(search_terms)}: '{search_term}'")
                
                # Collect products for this search term
                products = self.search_and_collect_products(page, search_term, target_count=20)
                all_products.extend(products)
                
                # Engage with products
                for product in products:
                    if engagements_made >= target_engagements:
                        break
                        
                    success = self.engage_with_product(page, product)
                    if success:
                        engagements_made += 1
                        
                    # Human-like delay between engagements
                    delay = random.uniform(3, 8)
                    time.sleep(delay)
                    
                print(f"📊 Progress: {engagements_made}/{target_engagements} engagements")
                
                # Longer delay between search terms
                if i < len(search_terms) - 1:
                    delay = random.uniform(10, 20)
                    print(f"⏳ Waiting {delay:.1f}s before next search...")
                    time.sleep(delay)
                    
            # Save results
            self.save_automation_results(all_products, engagements_made)
            
            print(f"\n🎉 AUTOMATION COMPLETE!")
            print(f"✅ Total engagements: {engagements_made}")
            print(f"📊 Products discovered: {len(all_products)}")
            
            browser.close()
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            
    def save_automation_results(self, products, engagements):
        """Save automation results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_automation_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products_found': len(products),
                    'total_engagements': engagements,
                    'search_terms_used': len(self.search_terms),
                    'success_rate': f"{(engagements/len(products)*100):.1f}%" if products else "0%"
                },
                'products': products,
                'statistics': {
                    'products_by_search_term': {},
                    'engagement_categories': {}
                }
            }
            
            # Calculate statistics
            for product in products:
                search_term = product['search_term']
                results['statistics']['products_by_search_term'][search_term] = \
                    results['statistics']['products_by_search_term'].get(search_term, 0) + 1
                    
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run supercharged Product Hunt automation"""
    
    bot = SuperchargedProductHuntBot()
    
    # Check credentials
    if not bot.email or not bot.password:
        print("❌ Product Hunt credentials not found!")
        print("📝 Please add to your .env file:")
        print("   PRODUCT_HUNT_EMAIL=your_email")
        print("   PRODUCT_HUNT_PASSWORD=your_password")
        print()
        print("🔧 Or use these alternative variable names:")
        print("   PH_EMAIL / PH_PASSWORD")
        print("   EMAIL / PASSWORD")
        print("   USER_EMAIL / USER_PASSWORD")
        return
    
    print("🚀 Starting supercharged Product Hunt automation...")
    print("🎯 Goal: Find 1000+ companies and engage authentically")
    print("🔐 One-time login with persistent session")
    print("⚡ Instant engagement like Twitter automation")
    
    # Run automation
    bot.run_supercharged_automation(target_engagements=1000)

if __name__ == "__main__":
    main()
