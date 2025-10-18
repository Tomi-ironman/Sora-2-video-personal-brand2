#!/usr/bin/env python3
"""
MANUAL GUIDED Product Hunt Engagement - FINAL VERSION
You point to products, automation handles the rest
"""

import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

class ManualGuidedProductHunt:
    def __init__(self):
        self.setup_automation()
        
    def setup_automation(self):
        """Setup manual guided automation"""
        
        # Session persistence with timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.browser_data_dir = f"product_hunt_browser_data_{timestamp}"
        
        # Track commented products
        self.commented_products_file = "product_hunt_commented_history.json"
        self.commented_products = self.load_commented_history()
        
        # ZENYAI STRATEGIC TEMPLATES
        self.zenyai_templates = [
            "This looks amazing! We're building Zenyai to solve similar organization challenges for audio creators 🎧 Check us out if you're dealing with sample/audio file organization!",
            
            "Love seeing innovation in this space! We're tackling a complementary problem at Zenyai - helping music producers and podcasters organize their audio assets with AI-powered metadata management 🎵",
            
            "Great tool! For anyone in audio production reading this, we're building Zenyai specifically to solve the metadata nightmare that every producer knows too well 🚀",
            
            "This is exactly what the community needs! We're solving a similar problem at Zenyai - audio file organization and metadata management for producers who have thousands of samples 🎙️",
            
            "Impressive work! If this tool helps your workflow, you might also want to check out Zenyai - we're solving the audio asset organization problem that every producer faces 💡",
            
            "Nice launch! We're building Zenyai to tackle the specific problem of audio metadata and sample library organization - would love to connect! 🔥"
        ]
        
        print(f"🚀 Manual Guided Product Hunt initialized")
        print(f"💬 {len(self.zenyai_templates)} strategic Zenyai templates")
        print(f"📝 Avoiding {len(self.commented_products)} previously commented products")
        
    def load_commented_history(self):
        """Load commented history"""
        try:
            if os.path.exists(self.commented_products_file):
                with open(self.commented_products_file, 'r') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
            
    def save_commented_history(self):
        """Save commented history"""
        try:
            with open(self.commented_products_file, 'w') as f:
                json.dump(list(self.commented_products), f, indent=2)
        except:
            pass
            
    def setup_browser(self):
        """Setup browser"""
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
            
    def manual_login_and_setup(self, page):
        """Manual login and setup"""
        try:
            print("\n🔐 MANUAL SETUP")
            print("=" * 50)
            print("1. Log into Product Hunt in the browser")
            print("2. Navigate to any page with products")
            print("3. Press ENTER when ready")
            print("=" * 50)
            
            page.goto("https://www.producthunt.com")
            time.sleep(3)
            
            input("🔑 Press ENTER after logging in and ready...")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup error: {e}")
            return False
            
    def analyze_current_page(self, page):
        """Analyze what's on the current page"""
        try:
            print("\n🔍 ANALYZING CURRENT PAGE")
            print("-" * 40)
            
            # Get page info
            title = page.title()
            url = page.url
            print(f"📄 Title: {title}")
            print(f"🌐 URL: {url}")
            
            # Count elements
            all_links = page.locator('a').all()
            buttons = page.locator('button').all()
            textareas = page.locator('textarea').all()
            inputs = page.locator('input').all()
            
            print(f"🔗 Links: {len(all_links)}")
            print(f"🔘 Buttons: {len(buttons)}")
            print(f"📝 Textareas: {len(textareas)}")
            print(f"⌨️ Inputs: {len(inputs)}")
            
            # Look for product-like links
            product_links = []
            for link in all_links[:50]:  # Check first 50 links
                try:
                    href = link.get_attribute('href')
                    text = link.text_content()
                    if href and text:
                        href = href.strip()
                        text = text.strip()
                        if len(text) > 5 and len(text) < 100:
                            product_links.append({
                                'text': text,
                                'href': href
                            })
                except:
                    continue
                    
            print(f"\n🎯 POTENTIAL PRODUCT LINKS (first 10):")
            for i, link in enumerate(product_links[:10]):
                print(f"   {i+1}. {link['text'][:50]} -> {link['href'][:50]}")
                
            return product_links
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return []
            
    def manual_product_selection(self, page):
        """Let user manually select products to engage with"""
        try:
            print("\n🎯 MANUAL PRODUCT SELECTION")
            print("=" * 50)
            print("INSTRUCTIONS:")
            print("1. Navigate to a product page in the browser")
            print("2. Press ENTER here when you're on a product page")
            print("3. I'll automatically post a Zenyai comment")
            print("4. Repeat for as many products as you want")
            print("5. Type 'done' when finished")
            print("=" * 50)
            
            engagements_made = 0
            
            while True:
                user_input = input(f"\nNavigate to product #{engagements_made + 1} and press ENTER (or 'done' to finish): ")
                
                if user_input.lower() == 'done':
                    break
                    
                # Get current URL
                current_url = page.url
                print(f"📍 Current URL: {current_url}")
                
                # Check if we've already commented here
                if current_url in self.commented_products:
                    print("⚠️ Already commented on this product - skipping")
                    continue
                    
                # Try to post comment
                success = self.post_zenyai_comment(page, current_url)
                
                if success:
                    engagements_made += 1
                    self.commented_products.add(current_url)
                    self.save_commented_history()
                    print(f"✅ Success! Total engagements: {engagements_made}")
                else:
                    print("❌ Failed to post comment")
                    
            return engagements_made
            
        except Exception as e:
            print(f"❌ Manual selection error: {e}")
            return 0
            
    def post_zenyai_comment(self, page, product_url):
        """Post strategic Zenyai comment"""
        try:
            print(f"💬 Posting Zenyai comment...")
            
            # Select random template
            comment_text = random.choice(self.zenyai_templates)
            print(f"📝 Comment: {comment_text[:60]}...")
            
            # Find comment input
            comment_input = None
            
            # Try textarea first
            textareas = page.locator('textarea').all()
            print(f"🔍 Found {len(textareas)} textareas")
            
            for textarea in textareas:
                try:
                    if textarea.is_visible():
                        comment_input = textarea
                        print("✅ Using textarea")
                        break
                except:
                    continue
                    
            # Try text inputs
            if not comment_input:
                text_inputs = page.locator('input[type="text"]').all()
                print(f"🔍 Found {len(text_inputs)} text inputs")
                
                for input_elem in text_inputs:
                    try:
                        if input_elem.is_visible():
                            comment_input = input_elem
                            print("✅ Using text input")
                            break
                    except:
                        continue
                        
            # Try any visible input
            if not comment_input:
                all_inputs = page.locator('input').all()
                print(f"🔍 Found {len(all_inputs)} total inputs")
                
                for input_elem in all_inputs:
                    try:
                        if input_elem.is_visible():
                            input_type = input_elem.get_attribute('type') or 'text'
                            if input_type in ['text', 'search', '']:
                                comment_input = input_elem
                                print(f"✅ Using {input_type} input")
                                break
                    except:
                        continue
                        
            if not comment_input:
                print("❌ No comment input found")
                
                # Manual fallback
                manual_input = input("Can you click on the comment box and press ENTER here? (y/n): ")
                if manual_input.lower() == 'y':
                    try:
                        # Try to use focused element
                        page.keyboard.type(comment_text)
                        time.sleep(1)
                        
                        # Try Enter
                        page.keyboard.press('Enter')
                        print("✅ Posted using manual focus + Enter")
                        return True
                    except:
                        print("❌ Manual method failed")
                        return False
                else:
                    return False
                    
            # Type comment
            try:
                comment_input.click()
                time.sleep(1)
                comment_input.fill(comment_text)
                time.sleep(2)
                
                print("✍️ Comment typed successfully")
                
                # Find submit button
                buttons = page.locator('button').all()
                print(f"🔍 Found {len(buttons)} buttons")
                
                for button in buttons:
                    try:
                        button_text = button.text_content()
                        if button_text:
                            button_text_lower = button_text.lower()
                            if any(word in button_text_lower for word in ['comment', 'post', 'submit', 'send', 'reply']):
                                print(f"🎯 Clicking: '{button_text}'")
                                button.click()
                                print("✅ Comment posted!")
                                time.sleep(2)
                                return True
                    except:
                        continue
                        
                # Try Enter key
                print("⌨️ Trying Enter key...")
                comment_input.press('Enter')
                print("✅ Comment posted with Enter!")
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"❌ Comment posting error: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Post comment error: {e}")
            return False
            
    def run_manual_guided_automation(self):
        """Run manual guided automation"""
        try:
            print("🚀 MANUAL GUIDED PRODUCT HUNT AUTOMATION")
            print("=" * 60)
            print("🎯 Strategy: You navigate, I comment")
            print("💬 Goal: Strategic Zenyai mentions")
            print("🔄 Process: Manual navigation + Auto commenting")
            print("=" * 60)
            
            # Setup
            browser, page = self.setup_browser()
            if not browser or not page:
                return
                
            # Manual login
            if not self.manual_login_and_setup(page):
                browser.close()
                return
                
            # Analyze current page
            self.analyze_current_page(page)
            
            # Manual product selection and engagement
            engagements_made = self.manual_product_selection(page)
            
            # Save results
            self.save_results(engagements_made)
            
            print(f"\n🎉 MANUAL GUIDED AUTOMATION COMPLETE!")
            print(f"✅ Total engagements: {engagements_made}")
            print(f"🔥 All comments strategically mention Zenyai!")
            
            input("\nPress ENTER to close...")
            browser.close()
            
        except Exception as e:
            print(f"❌ Manual guided automation error: {e}")
            
    def save_results(self, engagements):
        """Save results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_hunt_manual_guided_{timestamp}.json"
            
            results = {
                'automation_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'successful_engagements': engagements,
                    'strategy': 'manual_guided_engagement',
                    'total_commented_history': len(self.commented_products)
                },
                'zenyai_templates': self.zenyai_templates
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run manual guided automation"""
    
    print("🚀 MANUAL GUIDED PRODUCT HUNT AUTOMATION")
    print("🎯 You navigate to products, I handle the commenting")
    print("💬 Strategic Zenyai mentions on every engagement")
    print("🔄 Perfect for when selectors don't work")
    
    bot = ManualGuidedProductHunt()
    bot.run_manual_guided_automation()

if __name__ == "__main__":
    main()
