#!/usr/bin/env python3
"""
Product Hunt Multi-Account Automation System
Monitors Product Hunt for audio/creator tools and engages with helpful responses
"""

import os
import time
import json
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductHuntAutomation:
    def __init__(self):
        self.setup_accounts()
        self.setup_video_library()
        self.setup_personas()
        self.setup_keywords()
        self.current_account_index = 0
        
    def setup_accounts(self):
        """Initialize all Product Hunt accounts"""
        self.accounts = {}
        
        # Get all available Product Hunt accounts from environment
        account_numbers = []
        for key in os.environ.keys():
            if key.startswith('PRODUCTHUNT') and (key.endswith('_ACCESS_TOKEN') or key.endswith('_DEVELOPER_TOKEN')):
                if key in ['PRODUCTHUNT_ACCESS_TOKEN', 'PRODUCTHUNT_DEVELOPER_TOKEN']:
                    account_numbers.append('')
                else:
                    suffix = key.replace('PRODUCTHUNT', '').replace('_ACCESS_TOKEN', '').replace('_DEVELOPER_TOKEN', '')
                    if suffix not in account_numbers:
                        account_numbers.append(suffix)
        
        print(f"🔍 Found {len(account_numbers)} Product Hunt accounts")
        
        for account_num in account_numbers:
            try:
                suffix = account_num if account_num else ''
                
                # Get credentials for this account (prefer developer token)
                developer_token = os.getenv(f'PRODUCTHUNT{suffix}_DEVELOPER_TOKEN')
                access_token = os.getenv(f'PRODUCTHUNT{suffix}_ACCESS_TOKEN')
                
                token = developer_token or access_token
                
                if token:
                    account_name = f"producthunt{suffix}" if suffix else "producthunt1"
                    
                    self.accounts[account_name] = {
                        'token': token,
                        'token_type': 'developer' if developer_token else 'access',
                        'last_used': 0,
                        'requests_made': 0,
                        'headers': {
                            'Authorization': f'Bearer {token}',
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }
                    }
                    
                    print(f"✅ {account_name}: Access token configured")
                    
            except Exception as e:
                print(f"❌ Failed to setup producthunt{suffix}: {e}")
                
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_video_library(self):
        """Map pain points to our existing video commercials"""
        self.video_library = {
            "file_organization": {
                "file": "sora2_20251010_031253_Create_a_dramatic_8-second_co.mp4",
                "description": "File organization and workflow optimization tools",
                "keywords": ["organize", "workflow", "files", "productivity", "management"]
            },
            "sound_design": {
                "file": "sora2_20251010_023908_Create_an_intense_relatable.mp4",
                "description": "Sound design and audio creation tools",
                "keywords": ["sound", "audio", "design", "creative", "music"]
            },
            "audio_professional": {
                "file": "sora2_20251010_022243_Create_an_intense_relatable.mp4",
                "description": "Professional audio and studio tools", 
                "keywords": ["audio", "professional", "studio", "mixing", "production"]
            },
            "podcast_workflow": {
                "file": "sora2_20251010_030604_Create_a_dramatic_8-second_co.mp4",
                "description": "Podcast creation and content tools",
                "keywords": ["podcast", "content", "creator", "recording", "editing"]
            }
        }
        
    def setup_personas(self):
        """Define different personas for each Product Hunt account"""
        self.personas = {
            "producthunt1": {
                "role": "Audio Engineer & Early Adopter",
                "tone": "Technical and enthusiastic",
                "style": "Love seeing new audio tools! As an engineer, workflow optimization is crucial.",
                "expertise": "Professional audio production"
            },
            "producthunt2": {
                "role": "Podcast Creator", 
                "tone": "Community-focused and supportive",
                "style": "Fellow creator here! Always excited to discover tools that solve real problems.",
                "expertise": "Content creation and podcasting"
            },
            "producthunt3": {
                "role": "Tech Enthusiast & Sound Designer",
                "tone": "Creative and forward-thinking", 
                "style": "This looks promising! Sound design workflows need more innovation like this.",
                "expertise": "Creative audio and emerging tech"
            }
        }
        
    def setup_keywords(self):
        """Keywords to monitor for relevant Product Hunt launches"""
        self.target_keywords = [
            # Audio & Music
            "audio", "music", "sound", "podcast", "recording", "mixing", "mastering",
            "studio", "producer", "musician", "composer", "sound design",
            
            # Creator Tools
            "creator", "content", "video", "editing", "production", "workflow",
            "collaboration", "team", "remote", "creative",
            
            # Productivity & Organization
            "productivity", "organization", "workflow", "automation", "AI",
            "management", "files", "asset", "library", "search",
            
            # Specific Tool Types
            "DAW", "VST", "plugin", "effect", "synthesizer", "sampler",
            "streaming", "broadcast", "live", "performance"
        ]
        
    def get_next_account(self):
        """Get the next account to use (round-robin with rate limiting)"""
        account_names = list(self.accounts.keys())
        
        for _ in range(len(account_names)):
            account_name = account_names[self.current_account_index]
            account = self.accounts[account_name]
            
            # Check if this account can be used (Product Hunt rate limiting)
            time_since_last = time.time() - account['last_used']
            
            if time_since_last > 900:  # Wait at least 15 minutes between uses
                self.current_account_index = (self.current_account_index + 1) % len(account_names)
                return account_name, account
                
            self.current_account_index = (self.current_account_index + 1) % len(account_names)
            
        # If all accounts are rate limited, use the first one anyway
        account_name = account_names[0]
        return account_name, self.accounts[account_name]
        
    def search_relevant_products(self):
        """Search for relevant products on Product Hunt"""
        relevant_products = []
        
        # Get account for searching
        account_name, account = self.get_next_account()
        
        try:
            print(f"🔍 Searching Product Hunt with {account_name}...")
            
            # Get today's products
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"https://api.producthunt.com/v2/api/graphql"
            
            # GraphQL query for today's posts
            query = """
            query($postedAfter: DateTime!) {
                posts(postedAfter: $postedAfter, first: 20) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            description
                            url
                            votesCount
                            commentsCount
                            topics {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """
            
            variables = {
                "postedAfter": f"{today}T00:00:00Z"
            }
            
            response = requests.post(
                url,
                json={'query': query, 'variables': variables},
                headers=account['headers']
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'posts' in data['data']:
                    for edge in data['data']['posts']['edges']:
                        product = edge['node']
                        
                        # Check if product is relevant to our keywords
                        product_text = f"{product['name']} {product['tagline']} {product.get('description', '')}".lower()
                        
                        topics = [topic['node']['name'].lower() for topic in product.get('topics', {}).get('edges', [])]
                        
                        if any(keyword in product_text or keyword in ' '.join(topics) 
                               for keyword in self.target_keywords):
                            relevant_products.append({
                                'id': product['id'],
                                'name': product['name'],
                                'tagline': product['tagline'],
                                'description': product.get('description', ''),
                                'url': product['url'],
                                'votes_count': product['votesCount'],
                                'comments_count': product['commentsCount'],
                                'topics': topics,
                                'found_by': account_name
                            })
                            
                print(f"✅ Found {len(relevant_products)} relevant products")
                
            else:
                print(f"❌ Product Hunt API error: {response.status_code}")
                
            account['last_used'] = time.time()
            account['requests_made'] += 1
            
        except Exception as e:
            print(f"❌ Error searching Product Hunt: {e}")
            
        return relevant_products
        
    def analyze_product_context(self, name, tagline, description, topics):
        """Use AI to analyze product and determine relevance"""
        combined_text = f"{name} {tagline} {description} {' '.join(topics)}"
        
        prompt = f"""
        Analyze this Product Hunt launch and determine which category it best fits:
        
        Product: "{name}"
        Tagline: "{tagline}"
        Description: "{description[:200]}..."
        Topics: {topics}
        
        Categories:
        1. file_organization - Workflow, productivity, file management, organization tools
        2. sound_design - Sound design, music creation, audio effects, creative audio
        3. audio_professional - Professional audio, mixing, mastering, studio tools
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
            print(f"Error analyzing product: {e}")
            return None
            
    def generate_engaging_comment(self, product_data, video_category, account_name):
        """Generate an engaging Product Hunt comment"""
        video_info = self.video_library[video_category]
        persona = self.personas.get(account_name, self.personas['producthunt1'])
        
        prompt = f"""
        Create an engaging Product Hunt comment for this product launch.
        
        Product: "{product_data['name']}"
        Tagline: "{product_data['tagline']}"
        Solution category: {video_info['description']}
        
        Persona: {persona['role']} - {persona['tone']}
        Style: {persona['style']}
        Expertise: {persona['expertise']}
        
        Requirements:
        - Be genuinely enthusiastic and supportive (Product Hunt community style)
        - Reference the specific product and its value
        - Mention having experience with similar workflow challenges
        - Offer to share a helpful resource if relevant
        - Keep under 200 characters
        - Sound authentic and community-focused
        - Include relevant emojis
        
        Format: "[Enthusiastic opener] [Personal connection] [Value recognition] [Resource offer if appropriate] [Emoji]"
        
        Example: "{persona['style']} I've been looking for exactly this kind of solution! Would love to share some workflow insights if helpful 🎧"
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"{persona['style']} This looks like a great solution for workflow optimization! 🚀"
            
    def log_intended_engagement(self, product_data, comment_text, account_name):
        """Log intended engagements for manual posting or API integration"""
        log_file = "producthunt_intended_engagements.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    engagements = json.load(f)
            else:
                engagements = []
                
            engagements.append({
                'product_id': product_data['id'],
                'product_name': product_data['name'],
                'product_url': product_data['url'],
                'tagline': product_data['tagline'],
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
        """Run one cycle of Product Hunt monitoring"""
        print(f"\n🔄 Starting Product Hunt monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Active accounts: {len(self.accounts)}")
        print(f"🎯 Target keywords: {len(self.target_keywords)}")
        
        # Show account status
        for name, account in self.accounts.items():
            print(f"   {name}: {account['requests_made']} requests made")
        
        products = self.search_relevant_products()
        print(f"🎯 Found {len(products)} potentially relevant products")
        
        engagements_planned = 0
        
        for product in products[:3]:  # Limit to 3 engagements per cycle
            # Analyze product relevance
            category = self.analyze_product_context(
                product['name'], 
                product['tagline'], 
                product['description'], 
                product['topics']
            )
            
            if category:
                # Get account for engagement
                account_name, account = self.get_next_account()
                
                # Generate engaging comment
                comment = self.generate_engaging_comment(product, category, account_name)
                
                print(f"💬 Would engage with '{product['name']}' using {account_name}:")
                print(f"   Comment: {comment}")
                print(f"   Product: {product['url']}")
                
                # Log intended engagement
                self.log_intended_engagement(product, comment, account_name)
                engagements_planned += 1
                
                # Add delay between engagements
                time.sleep(random.randint(60, 180))  # 1-3 minutes
                
        print(f"📊 Planned {engagements_planned} engagements this cycle")
        
    def run_continuous_monitoring(self, check_interval=3600):  # 1 hour
        """Run continuous Product Hunt monitoring"""
        print("🚀 Starting Product Hunt Multi-Account Automation")
        print("=" * 60)
        print(f"📊 Accounts: {len(self.accounts)}")
        print(f"🎯 Target keywords: {len(self.target_keywords)}")
        print(f"⏰ Check interval: {check_interval/3600} hours")
        print("")
        print("📝 Note: Engagements are logged for manual posting initially")
        
        while True:
            try:
                self.run_monitoring_cycle()
                print(f"\n😴 Sleeping for {check_interval/3600} hours...")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Product Hunt monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring cycle: {e}")
                time.sleep(1800)  # Wait 30 minutes before retrying

def main():
    """Run the Product Hunt automation"""
    automation = ProductHuntAutomation()
    automation.run_continuous_monitoring()

if __name__ == "__main__":
    main()
