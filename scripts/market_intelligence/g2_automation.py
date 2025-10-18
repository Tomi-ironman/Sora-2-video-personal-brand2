#!/usr/bin/env python3
"""
G2 Multi-Account Automation System
Monitors G2 for audio/creator software reviews and engages with helpful responses
"""

import os
import time
import json
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

class G2Automation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_categories()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all G2 accounts"""
        self.accounts = {}
        
        # G2 doesn't have a public API, so we'll use account credentials for web scraping
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('G2') and key.endswith('_EMAIL'):
                if key == 'G2_EMAIL':
                    account_numbers.append('')
                else:
                    account_numbers.append(key.replace('G2', '').replace('_EMAIL', ''))
        
        print(f"🔍 Found {len(account_numbers)} G2 accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account
                email = os.getenv(f'G2{suffix}_EMAIL')
                password = os.getenv(f'G2{suffix}_PASSWORD')
                
                if email and password:
                    account_name = f"g2{suffix}" if suffix else "g2_1"
                    
                    self.accounts[account_name] = {
                        'email': email,
                        'password': password,
                        'session': requests.Session(),
                        'last_used': 0,
                        'requests_made': 0,
                        'logged_in': False
                    }
                    
                    print(f"✅ {account_name}: {email}")
                    
            except Exception as e:
                print(f"❌ Failed to setup g2{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization and workflow management solutions",
                "keywords": ["organize", "workflow", "files", "productivity", "management", "asset"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound design and audio creation software",
                "keywords": ["sound", "audio", "design", "creative", "music", "effects"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Professional audio and studio software", 
                "keywords": ["audio", "professional", "studio", "mixing", "mastering", "production"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast creation and content management tools",
                "keywords": ["podcast", "content", "creator", "recording", "editing", "publishing"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each G2 account"""
        self.personas = {
            "g2_1": {
                "role": "Audio Engineer & Software Evaluator",
                "tone": "Technical and detailed",
                "style": "As an audio engineer, I've evaluated many tools in this space.",
                "expertise": "Professional audio production workflows"
            },
            "g2_2": {
                "role": "Content Creator & Podcaster", 
                "tone": "Practical and user-focused",
                "style": "Fellow creator here - I've struggled with similar workflow challenges.",
                "expertise": "Content creation and podcast production"
            },
            "g2_3": {
                "role": "Studio Manager & Tech Lead",
                "tone": "Strategic and efficiency-focused", 
                "style": "From a studio management perspective, workflow optimization is critical.",
                "expertise": "Team workflows and studio operations"
            }
        }
        
    def setup_categories(self):
        """G2 categories to monitor for relevant software"""
        self.target_categories = [
            # Audio & Music Software
            "audio-editing-software",
            "music-production-software", 
            "podcast-software",
            "digital-audio-workstation-daw-software",
            "audio-conferencing-software",
            
            # Creative & Content Tools
            "video-editing-software",
            "content-creation-software",
            "creative-software",
            "media-and-entertainment-software",
            
            # Productivity & Workflow
            "project-management-software",
            "workflow-management-software",
            "file-management-software",
            "collaboration-software",
            "productivity-software",
            
            # Team & Remote Work
            "team-collaboration-software",
            "remote-work-software",
            "communication-software"
        ]
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (G2 rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 1800:  # Wait at least 30 minutes between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def login_to_g2(self, account_name, account):
        """Login to G2 with account credentials"""
        if account['logged_in']:
            return True
            
        try:
            print(f"🔐 Logging into G2 with {account_name}...")
            
            # Get login page
            login_url = "https://www.g2.com/login"
            response = account['session'].get(login_url)
            
            if response.status_code != 200:
                print(f"❌ Failed to access G2 login page")
                return False
                
            # Parse login form (simplified - actual implementation would need CSRF tokens, etc.)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Login data (this is a simplified example)
            login_data = {
                'user[email]': account['email'],
                'user[password]': account['password']
            }
            
            # Submit login (Note: G2 has anti-bot measures, this is conceptual)
            login_response = account['session'].post(
                "https://www.g2.com/sessions",
                data=login_data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Referer': login_url
                }
            )
            
            if "dashboard" in login_response.url or login_response.status_code == 200:
                account['logged_in'] = True
                print(f"✅ Successfully logged into G2 as {account['email']}")
                return True
            else:
                print(f"❌ G2 login failed for {account['email']}")
                return False
                
        except Exception as e:
            print(f"❌ Error logging into G2: {e}")
            return False
            
    def search_relevant_reviews(self, category):
        """Search for relevant reviews in a G2 category"""
        # Get account for searching
        account_name, account = self.get_next_account()
        
        if not self.login_to_g2(account_name, account):
            return []
            
        try:
            print(f"🔍 Searching G2 category: {category} with {account_name}...")
            
            # Search category page
            category_url = f"https://www.g2.com/categories/{category}"
            response = account['session'].get(category_url)
            
            if response.status_code != 200:
                print(f"❌ Failed to access G2 category: {category}")
                return []
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find software products in category (simplified parsing)
            products = []
            
            # Look for product cards or listings
            product_elements = soup.find_all('div', class_=['product-listing', 'product-card'])
            
            for element in product_elements[:5]:  # Limit to 5 products per category
                try:
                    # Extract product info (this would need to be adapted to G2's actual HTML structure)
                    name_element = element.find('h3') or element.find('a')
                    if name_element:
                        product_name = name_element.get_text(strip=True)
                        product_url = name_element.get('href', '')
                        
                        if product_url and not product_url.startswith('http'):
                            product_url = f"https://www.g2.com{product_url}"
                            
                        products.append({
                            'name': product_name,
                            'url': product_url,
                            'category': category,
                            'found_by': account_name
                        })
                        
                except Exception as e:
                    continue
                    
            account['last_used'] = time.time()
            account['requests_made'] += 1
            
            print(f"✅ Found {len(products)} products in {category}")
            return products
            
        except Exception as e:
            print(f"❌ Error searching G2 category {category}: {e}")
            return []
            
    def analyze_software_context(self, name, category):
        """Use AI to analyze software and determine relevance"""
        prompt = f"""
        Analyze this G2 software listing and determine which category it best fits:
        
        Software: "{name}"
        G2 Category: "{category}"
        
        Categories:
        1. file_organization - File management, workflow, productivity, organization tools
        2. sound_design - Sound design, music creation, audio effects, creative audio
        3. audio_professional - Professional audio, mixing, mastering, studio software
        4. podcast_workflow - Podcast creation, content creation, recording, editing
        
        Return only the category name that best matches, or "none" if not relevant.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            return category if category in self.video_library else None
            
        except Exception as e:
            print(f"Error analyzing software: {e}")
            return None
            
    def generate_helpful_review_comment(self, software_data, video_category, account_name):
        """Generate a helpful G2 review or comment"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['g2_1'])
        
        prompt = f"""
        Create a helpful G2 review comment for this software.
        
        Software: "{software_data['name']}"
        Category: "{software_data['category']}"
        Solution category: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        Expertise: {persona['expertise']}
        
        Requirements:
        - Be genuinely helpful and detailed (G2 review style)
        - Reference specific workflow challenges this type of software addresses
        - Mention having experience with similar tools
        - Offer insights about workflow optimization
        - Keep under 300 characters for comment, longer for review
        - Sound professional and credible
        - Focus on practical value
        
        Format: "[Professional opener] [Specific experience] [Workflow insight] [Value assessment]"
        
        Example: "{persona['style']} The workflow optimization features look promising for teams dealing with complex audio asset management. Would be interested in seeing how it handles large file libraries."
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"{persona['style']} This looks like it could address some key workflow challenges in our industry."
            
    def log_intended_engagement(self, software_data, comment_text, account_name):
        """Log intended engagements for manual posting"""
        log_file = "g2_intended_engagements.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    engagements = json.load(f)
            else:
                engagements = []
                
            engagements.append({
                'software_name': software_data['name'],
                'software_url': software_data['url'],
                'category': software_data['category'],
                'comment_text': comment_text,
                'account_name': account_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            })
            
            with open(log_file, 'w') as f:
                json.dump(engagements, f, indent=2)
                
            print(f"📝 Logged intended engagement to {log_file}")
                
        except Exception as e:
            print(f"Error logging engagement: {e}")
            
    def run_monitoring_cycle(self):
        """Run one cycle of G2 monitoring"""
        print(f"\n🔄 Starting G2 monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        print(f"🎯 Target categories: {len(self.target_categories)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: {account['email']} ({account['requests_made']} requests)")
        
        # Monitor a subset of categories each cycle
        categories_to_check = random.sample(self.target_categories, min(3, len(self.target_categories)))
        
        total_products_found = 0
        engagements_planned = 0
        
        for category in categories_to_check:
            products = self.search_relevant_reviews(category)
            total_products_found += len(products)
            
            for product in products[:2]:  # Limit to 2 products per category
                # Analyze product relevance
                video_category = self.analyze_software_context(product['name'], product['category'])
                
                if video_category:
                    # Get account for engagement
                    account_name, account = self.get_next_account()
                    
                    # Generate helpful comment
                    comment = self.generate_helpful_review_comment(product, video_category, account_name)
                    
                    print(f"💬 Would engage with '{product['name']}' using {account_name}:")
                    print(f"   Comment: {comment[:100]}...")
                    print(f"   Software: {product['url']}")
                    
                    # Log intended engagement
                    self.log_intended_engagement(product, comment, account_name)
                    engagements_planned += 1
                    
                    # Add delay between engagements
                    time.sleep(random.randint(120, 300))  # 2-5 minutes
                    
        print(f"🎯 Found {total_products_found} potentially relevant software products")
        print(f"📊 Planned {engagements_planned} engagements this cycle")
        
    def run_continuous_monitoring(self, check_interval=21600):  # 6 hours
        """Run continuous G2 monitoring"""
        print("🚀 Starting G2 Multi-Account Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎯 Target categories: {len(self.target_categories)}")
        print(f"⏰ Check interval: {check_interval/3600} hours")
        print("")
        print("📝 Note: Engagements are logged for manual posting")
        print("⚠️  G2 has anti-bot measures - use responsibly")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/3600} hours...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 G2 monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(3600)  # Wait 1 hour before retrying

def main():
    """Run the G2 automation"""
    print("📊 G2 Automation Framework")
    print("Note: G2 has anti-bot measures - this is a conceptual framework")
    
    automation = G2Automation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
