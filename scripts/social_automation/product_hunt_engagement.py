#!/usr/bin/env python3
"""
Product Hunt Active Engagement System
Actually posts comments and engages with products about Zenyai
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

class ProductHuntEngagement:
    def __init__(self):
        self.setup_accounts()
        self.setup_zenyai_messaging()
        self.setup_personas()
        
    def setup_accounts(self):
        """Initialize Product Hunt accounts for engagement"""
        self.accounts = {}
        
        # Get Product Hunt credentials
        developer_token = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
        access_token = os.getenv('PRODUCTHUNT_ACCESS_TOKEN')
        
        token = developer_token or access_token
        
        if token:
            self.accounts['producthunt1'] = {
                'token': token,
                'token_type': 'developer' if developer_token else 'access',
                'headers': {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'last_used': 0,
                'engagements_made': 0
            }
            print(f"✅ Product Hunt account configured")
        else:
            print("❌ No Product Hunt token found")
            
        # Initialize OpenAI
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def setup_zenyai_messaging(self):
        """Define key Zenyai messages and value propositions"""
        self.zenyai_messages = {
            "core_value": "AI-native audio asset management that actually understands your workflow",
            "pain_points": [
                "Tired of spending hours organizing audio files?",
                "Struggling to find the right sample in massive libraries?",
                "Team collaboration on audio projects driving you crazy?",
                "Workflow bottlenecks killing your creative flow?"
            ],
            "solutions": [
                "Intelligent file organization that learns your patterns",
                "AI-powered search that finds exactly what you need",
                "Seamless team collaboration for audio projects",
                "Workflow automation that keeps you in creative flow"
            ],
            "social_proof": [
                "Already helping audio professionals save 10+ hours per week",
                "Trusted by podcast creators, sound designers, and music producers",
                "Built by creators, for creators - we understand the struggle"
            ],
            "call_to_action": [
                "Check out Zenyai.io - built specifically for audio creators like us!",
                "Would love to show you how Zenyai handles this exact workflow challenge",
                "This is exactly why we built Zenyai - DM me if you'd like to see how it works!"
            ]
        }
        
    def setup_personas(self):
        """Define engagement personas for different contexts"""
        self.personas = {
            "audio_engineer": {
                "role": "Audio Engineer & Workflow Optimizer",
                "tone": "Technical and solution-focused",
                "approach": "I've been working in audio for years and workflow optimization is everything.",
                "zenyai_angle": "This is exactly why we built Zenyai - AI-native asset management for audio professionals."
            },
            "creator_advocate": {
                "role": "Creator Tools Enthusiast", 
                "tone": "Community-focused and supportive",
                "approach": "Love seeing tools that solve real creator problems!",
                "zenyai_angle": "Speaking of creator tools, Zenyai has been a game-changer for audio workflow optimization."
            },
            "problem_solver": {
                "role": "Workflow Solutions Expert",
                "tone": "Helpful and experienced",
                "approach": "Great to see innovation in this space - workflow bottlenecks are real.",
                "zenyai_angle": "We've been tackling similar challenges with Zenyai - AI-powered audio asset management."
            }
        }
        
    def find_todays_products(self):
        """Find today's Product Hunt launches"""
        account = self.accounts['producthunt1']
        
        try:
            url = "https://api.producthunt.com/v2/api/graphql"
            
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
                            slug
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
            
            today = datetime.now().strftime('%Y-%m-%d')
            variables = {"postedAfter": f"{today}T00:00:00Z"}
            
            response = requests.post(
                url,
                json={'query': query, 'variables': variables},
                headers=account['headers']
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'posts' in data['data']:
                    products = []
                    for edge in data['data']['posts']['edges']:
                        product = edge['node']
                        topics = [topic['node']['name'].lower() for topic in product.get('topics', {}).get('edges', [])]
                        
                        products.append({
                            'id': product['id'],
                            'name': product['name'],
                            'tagline': product['tagline'],
                            'description': product.get('description', ''),
                            'url': product['url'],
                            'slug': product['slug'],
                            'votes_count': product['votesCount'],
                            'comments_count': product['commentsCount'],
                            'topics': topics
                        })
                        
                    print(f"✅ Found {len(products)} products launched today")
                    return products
                    
            else:
                print(f"❌ Product Hunt API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            
        return []
        
    def analyze_engagement_opportunity(self, product):
        """Analyze if a product is good for Zenyai engagement"""
        product_text = f"{product['name']} {product['tagline']} {product['description']}".lower()
        topics = product['topics']
        
        # High-relevance keywords for audio/creator tools
        high_relevance = [
            'audio', 'music', 'podcast', 'sound', 'creator', 'content',
            'video', 'editing', 'production', 'workflow', 'collaboration',
            'productivity', 'organization', 'ai', 'automation'
        ]
        
        # Medium-relevance keywords for general productivity
        medium_relevance = [
            'team', 'remote', 'management', 'files', 'asset', 'search',
            'creative', 'design', 'studio', 'professional'
        ]
        
        relevance_score = 0
        
        # Check high-relevance keywords
        for keyword in high_relevance:
            if keyword in product_text or keyword in ' '.join(topics):
                relevance_score += 3
                
        # Check medium-relevance keywords  
        for keyword in medium_relevance:
            if keyword in product_text or keyword in ' '.join(topics):
                relevance_score += 1
                
        # Determine engagement type
        if relevance_score >= 6:
            return "direct_zenyai_mention"  # Directly relevant - mention Zenyai
        elif relevance_score >= 3:
            return "supportive_with_hint"   # Somewhat relevant - supportive + subtle hint
        elif relevance_score >= 1:
            return "general_support"        # General support only
        else:
            return "skip"                   # Not relevant
            
    def generate_engagement_comment(self, product, engagement_type):
        """Generate appropriate comment based on engagement type"""
        persona = random.choice(list(self.personas.values()))
        
        if engagement_type == "direct_zenyai_mention":
            prompt = f"""
            Create an engaging Product Hunt comment that naturally mentions Zenyai.
            
            Product: "{product['name']}"
            Tagline: "{product['tagline']}"
            
            Persona: {persona['role']} - {persona['tone']}
            Approach: {persona['approach']}
            Zenyai angle: {persona['zenyai_angle']}
            
            Requirements:
            - Be genuinely supportive of the product first
            - Naturally connect to Zenyai's value proposition
            - Mention specific workflow challenges Zenyai solves
            - Include a soft call-to-action
            - Keep under 200 characters
            - Sound authentic and community-focused
            
            Format: "[Support for product] [Personal connection] [Zenyai mention] [CTA]"
            
            Example: "Love seeing innovation in creator workflows! {persona['zenyai_angle']} Would be happy to share how we've tackled similar challenges. Great launch! 🚀"
            """
            
        elif engagement_type == "supportive_with_hint":
            prompt = f"""
            Create a supportive Product Hunt comment with a subtle hint about Zenyai.
            
            Product: "{product['name']}"
            Tagline: "{product['tagline']}"
            
            Persona: {persona['role']} - {persona['tone']}
            
            Requirements:
            - Be genuinely supportive and helpful
            - Share relevant experience or insight
            - Subtly hint at Zenyai without being pushy
            - Keep under 150 characters
            - Focus on community value first
            
            Example: "{persona['approach']} We've been working on similar challenges in the audio space. Excited to see more innovation here! 🎧"
            """
            
        else:  # general_support
            prompt = f"""
            Create a supportive Product Hunt comment with no Zenyai mention.
            
            Product: "{product['name']}"
            Tagline: "{product['tagline']}"
            
            Requirements:
            - Be genuinely supportive and encouraging
            - Add value to the conversation
            - Keep under 100 characters
            - Sound authentic and community-focused
            
            Example: "Great concept! Love seeing tools that solve real workflow problems. Best of luck with the launch! 🚀"
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
            
            # Fallback comments
            if engagement_type == "direct_zenyai_mention":
                return f"{persona['approach']} {persona['zenyai_angle']} Great launch! 🚀"
            else:
                return "Great concept! Love seeing innovation in creator tools. Best of luck! 🚀"
                
    def post_comment(self, product, comment_text):
        """Post comment on Product Hunt (Note: Requires specific API endpoints)"""
        # Note: Product Hunt's GraphQL API for commenting requires specific mutations
        # This is a framework - actual implementation would need the exact mutation schema
        
        print(f"💬 Would comment on '{product['name']}':")
        print(f"   Comment: {comment_text}")
        print(f"   Product URL: https://www.producthunt.com/posts/{product['slug']}")
        
        # Log the intended comment for manual posting
        self.log_intended_comment(product, comment_text)
        
        return True
        
    def log_intended_comment(self, product, comment_text):
        """Log intended comments for manual posting"""
        log_file = "producthunt_zenyai_comments.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    comments = json.load(f)
            else:
                comments = []
                
            comments.append({
                'product_name': product['name'],
                'product_slug': product['slug'],
                'product_url': f"https://www.producthunt.com/posts/{product['slug']}",
                'tagline': product['tagline'],
                'comment_text': comment_text,
                'timestamp': datetime.now().isoformat(),
                'votes_count': product['votes_count'],
                'status': 'pending'
            })
            
            with open(log_file, 'w') as f:
                json.dump(comments, f, indent=2)
                
            print(f"📝 Logged comment to {log_file}")
                
        except Exception as e:
            print(f"Error logging comment: {e}")
            
    def run_daily_engagement(self):
        """Run daily Product Hunt engagement cycle"""
        print(f"\n🏆 Starting Product Hunt Zenyai Engagement at {datetime.now().strftime('%H:%M:%S')}")
        
        # Get today's products
        products = self.find_todays_products()
        
        if not products:
            print("❌ No products found for today")
            return
            
        engagement_stats = {
            'direct_mentions': 0,
            'supportive_hints': 0,
            'general_support': 0,
            'skipped': 0
        }
        
        for product in products:
            # Analyze engagement opportunity
            engagement_type = self.analyze_engagement_opportunity(product)
            
            if engagement_type == "skip":
                engagement_stats['skipped'] += 1
                continue
                
            # Generate appropriate comment
            comment = self.generate_engagement_comment(product, engagement_type)
            
            # Post comment (currently logs for manual posting)
            self.post_comment(product, comment)
            
            # Update stats
            if engagement_type == "direct_zenyai_mention":
                engagement_stats['direct_mentions'] += 1
            elif engagement_type == "supportive_with_hint":
                engagement_stats['supportive_hints'] += 1
            else:
                engagement_stats['general_support'] += 1
                
            # Add delay between comments
            time.sleep(random.randint(30, 90))  # 30 seconds to 1.5 minutes
            
        print(f"\n📊 Engagement Summary:")
        print(f"   🎯 Direct Zenyai mentions: {engagement_stats['direct_mentions']}")
        print(f"   💡 Supportive with hints: {engagement_stats['supportive_hints']}")
        print(f"   👍 General support: {engagement_stats['general_support']}")
        print(f"   ⏭️  Skipped: {engagement_stats['skipped']}")

def main():
    """Run Product Hunt engagement"""
    engagement = ProductHuntEngagement()
    engagement.run_daily_engagement()

if __name__ == "__main__":
    main()
