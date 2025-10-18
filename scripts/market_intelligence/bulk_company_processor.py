#!/usr/bin/env python3
"""
Bulk Company Processing System
Finds 50+ relevant companies, researches them, and engages across platforms
"""

import os
import time
import json
import random
import asyncio
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class BulkCompanyProcessor:
    def __init__(self):
        self.setup_credentials()
        self.setup_zenyai_context()
        self.setup_search_parameters()
        self.batch_size = 50
        
    def setup_credentials(self):
        """Setup API credentials"""
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.producthunt_token = os.getenv('PRODUCTHUNT_DEVELOPER_TOKEN')
        
    def setup_zenyai_context(self):
        """Define Zenyai's business context for targeting"""
        self.zenyai_context = {
            "industry": "Audio & Creative Technology",
            "target_segments": [
                "Audio professionals", "Podcast creators", "Sound designers", 
                "Music producers", "Content creators", "Creative teams",
                "Audio engineers", "Radio producers", "Voice actors"
            ],
            "solution_categories": [
                "Workflow automation", "Asset management", "Team collaboration",
                "File organization", "Creative productivity", "AI-powered tools"
            ],
            "competitor_keywords": [
                "audio", "podcast", "sound", "music", "creative", "workflow",
                "asset", "management", "collaboration", "productivity", "AI",
                "automation", "team", "creator", "content", "studio"
            ]
        }
        
    def setup_search_parameters(self):
        """Setup search parameters for finding relevant companies"""
        self.search_queries = [
            # Direct competitors
            "audio asset management platform",
            "podcast workflow automation",
            "creative team collaboration tools",
            "sound design workflow software",
            "music production asset management",
            
            # Adjacent markets
            "creator economy platforms",
            "content creation workflow tools",
            "team productivity for creatives",
            "AI-powered creative tools",
            "digital asset management for media",
            
            # Broader market
            "workflow automation for teams",
            "file organization software",
            "collaboration tools for creators",
            "productivity platforms",
            "AI workflow optimization"
        ]
        
    def search_product_hunt_companies(self, days_back=30):
        """Search Product Hunt for relevant companies from recent launches"""
        try:
            print("🔍 Searching Product Hunt for relevant companies...")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = "https://api.producthunt.com/v2/api/graphql"
            
            query = """
            query($postedAfter: DateTime!, $first: Int!) {
                posts(postedAfter: $postedAfter, first: $first) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            description
                            url
                            slug
                            votesCount
                            commentsCount
                            createdAt
                            topics {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                            makers {
                                edges {
                                    node {
                                        name
                                        username
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """
            
            variables = {
                "postedAfter": start_date.isoformat(),
                "first": 100  # Get more companies
            }
            
            headers = {
                'Authorization': f'Bearer {self.producthunt_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                companies = []
                
                if 'data' in data and 'posts' in data['data']:
                    for edge in data['data']['posts']['edges']:
                        product = edge['node']
                        
                        # Extract company info
                        company_info = {
                            'id': product['id'],
                            'name': product['name'],
                            'tagline': product['tagline'],
                            'description': product.get('description', ''),
                            'url': product['url'],
                            'slug': product['slug'],
                            'votes_count': product['votesCount'],
                            'comments_count': product['commentsCount'],
                            'created_at': product['createdAt'],
                            'topics': [topic['node']['name'] for topic in product.get('topics', {}).get('edges', [])],
                            'makers': [maker['node']['name'] for maker in product.get('makers', {}).get('edges', [])],
                            'platform': 'product_hunt',
                            'relevance_score': 0
                        }
                        
                        companies.append(company_info)
                        
                print(f"✅ Found {len(companies)} companies from Product Hunt")
                return companies
                
            else:
                print(f"❌ Product Hunt API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching Product Hunt: {e}")
            return []
            
    def analyze_company_relevance(self, company):
        """Analyze how relevant a company is to Zenyai's market"""
        try:
            # Combine all text for analysis
            company_text = f"{company['name']} {company['tagline']} {company['description']} {' '.join(company['topics'])}".lower()
            
            relevance_score = 0
            matched_keywords = []
            
            # Check for direct keyword matches
            for keyword in self.zenyai_context['competitor_keywords']:
                if keyword in company_text:
                    relevance_score += 1
                    matched_keywords.append(keyword)
                    
            # Bonus for high engagement (popular products)
            if company['votes_count'] > 100:
                relevance_score += 2
            elif company['votes_count'] > 50:
                relevance_score += 1
                
            # Use AI for deeper relevance analysis
            if relevance_score > 0:  # Only for potentially relevant companies
                ai_analysis = self.get_ai_relevance_analysis(company)
                relevance_score += ai_analysis.get('ai_score', 0)
                
            company['relevance_score'] = relevance_score
            company['matched_keywords'] = matched_keywords
            
            return relevance_score > 2  # Threshold for relevance
            
        except Exception as e:
            print(f"❌ Error analyzing relevance for {company['name']}: {e}")
            return False
            
    def get_ai_relevance_analysis(self, company):
        """Use AI to analyze company relevance and generate engagement strategy"""
        try:
            prompt = f"""
            Analyze this company for relevance to Zenyai's business:
            
            Company: {company['name']}
            Tagline: {company['tagline']}
            Description: {company['description'][:200]}
            Topics: {', '.join(company['topics'])}
            
            Zenyai Context:
            - Industry: {self.zenyai_context['industry']}
            - Target segments: {', '.join(self.zenyai_context['target_segments'])}
            - Solution categories: {', '.join(self.zenyai_context['solution_categories'])}
            
            Provide analysis in JSON format:
            {{
                "ai_score": [0-5 relevance score],
                "relevance_reason": "why this company is relevant",
                "collaboration_opportunity": "specific collaboration angle",
                "engagement_priority": "high/medium/low",
                "business_model_similarity": "how similar to Zenyai"
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            # Parse JSON response
            import json
            analysis = json.loads(response.choices[0].message.content.strip())
            return analysis
            
        except Exception as e:
            print(f"❌ AI analysis error: {e}")
            return {"ai_score": 0}
            
    def generate_bulk_engagement_strategy(self, companies):
        """Generate engagement strategy for bulk processing"""
        try:
            print("🎯 Generating bulk engagement strategy...")
            
            # Sort companies by relevance score
            companies.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Group into batches
            batches = []
            for i in range(0, len(companies), self.batch_size):
                batch = companies[i:i + self.batch_size]
                
                batch_info = {
                    'batch_number': len(batches) + 1,
                    'companies': batch,
                    'total_companies': len(batch),
                    'avg_relevance': sum(c['relevance_score'] for c in batch) / len(batch),
                    'high_priority': [c for c in batch if c.get('engagement_priority') == 'high'],
                    'processing_status': 'pending'
                }
                
                batches.append(batch_info)
                
            print(f"📊 Created {len(batches)} batches of companies")
            
            # Save strategy to file
            strategy_file = "bulk_engagement_strategy.json"
            with open(strategy_file, 'w') as f:
                json.dump({
                    'created_at': datetime.now().isoformat(),
                    'total_companies': len(companies),
                    'total_batches': len(batches),
                    'batch_size': self.batch_size,
                    'batches': batches
                }, f, indent=2)
                
            print(f"✅ Strategy saved to {strategy_file}")
            return batches
            
        except Exception as e:
            print(f"❌ Error generating strategy: {e}")
            return []
            
    def process_company_batch(self, batch):
        """Process a batch of companies for engagement"""
        try:
            print(f"\n🚀 Processing Batch {batch['batch_number']}")
            print(f"📊 Companies in batch: {batch['total_companies']}")
            print(f"📈 Average relevance: {batch['avg_relevance']:.1f}")
            
            engagement_results = []
            
            for company in batch['companies']:
                print(f"\n🎯 Processing: {company['name']}")
                print(f"   Relevance: {company['relevance_score']}")
                print(f"   Keywords: {', '.join(company['matched_keywords'])}")
                
                # Generate engagement comment
                comment = self.generate_company_comment(company)
                
                # Create engagement plan
                engagement_plan = {
                    'company': company,
                    'comment': comment,
                    'platforms': ['product_hunt'],  # Can expand to other platforms
                    'priority': company.get('engagement_priority', 'medium'),
                    'status': 'ready'
                }
                
                engagement_results.append(engagement_plan)
                
                # Small delay between companies
                time.sleep(0.5)
                
            batch['processing_status'] = 'completed'
            batch['engagement_results'] = engagement_results
            
            print(f"✅ Batch {batch['batch_number']} processed - {len(engagement_results)} engagements ready")
            return engagement_results
            
        except Exception as e:
            print(f"❌ Error processing batch: {e}")
            return []
            
    def generate_company_comment(self, company):
        """Generate authentic comment for a specific company"""
        try:
            prompt = f"""
            Generate an authentic business comment for this Product Hunt company:
            
            Company: {company['name']}
            Tagline: {company['tagline']}
            Description: {company['description'][:150]}
            Relevance Score: {company['relevance_score']}
            Matched Keywords: {', '.join(company['matched_keywords'])}
            
            Your context:
            - You work with Zenyai: AI-native audio asset management platform
            - Target market: Audio professionals, podcast creators, sound designers
            - Looking for collaboration opportunities and partnerships
            
            Write a comment that:
            1. Shows understanding of their specific business model
            2. Identifies a concrete collaboration opportunity
            3. Mentions Zenyai naturally in context
            4. Sounds like a real business professional
            5. NO quotes or quotation marks
            6. Keep under 180 characters
            7. End with a question or collaboration invitation
            
            Comment:
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.7
            )
            
            comment = response.choices[0].message.content.strip()
            comment = comment.replace('"', '').replace("'", '')
            
            return comment
            
        except Exception as e:
            print(f"❌ Error generating comment: {e}")
            return f"Interesting approach to workflow optimization. At Zenyai we're solving similar challenges in audio asset management. Would love to explore potential synergies?"
            
    def run_bulk_discovery_and_processing(self):
        """Main function to discover and process companies in bulk"""
        try:
            print("🚀 Starting Bulk Company Discovery & Processing")
            print("=" * 60)
            
            # Step 1: Discover companies
            print("\n📍 STEP 1: Company Discovery")
            companies = self.search_product_hunt_companies(days_back=60)  # Look back further
            
            if not companies:
                print("❌ No companies found")
                return
                
            # Step 2: Analyze relevance
            print(f"\n📍 STEP 2: Relevance Analysis ({len(companies)} companies)")
            relevant_companies = []
            
            for i, company in enumerate(companies):
                print(f"   Analyzing {i+1}/{len(companies)}: {company['name']}")
                
                if self.analyze_company_relevance(company):
                    relevant_companies.append(company)
                    print(f"   ✅ Relevant (score: {company['relevance_score']})")
                else:
                    print(f"   ❌ Not relevant (score: {company['relevance_score']})")
                    
            print(f"\n📊 Found {len(relevant_companies)} relevant companies")
            
            if not relevant_companies:
                print("❌ No relevant companies found")
                return
                
            # Step 3: Generate engagement strategy
            print(f"\n📍 STEP 3: Engagement Strategy Generation")
            batches = self.generate_bulk_engagement_strategy(relevant_companies)
            
            # Step 4: Process first batch as demo
            if batches:
                print(f"\n📍 STEP 4: Processing First Batch (Demo)")
                first_batch = batches[0]
                engagement_results = self.process_company_batch(first_batch)
                
                # Save results
                results_file = "bulk_engagement_results.json"
                with open(results_file, 'w') as f:
                    json.dump({
                        'processed_at': datetime.now().isoformat(),
                        'batch_processed': first_batch['batch_number'],
                        'total_engagements': len(engagement_results),
                        'results': engagement_results
                    }, f, indent=2)
                    
                print(f"\n🎉 Bulk processing complete!")
                print(f"📊 Results saved to {results_file}")
                print(f"✅ Ready to engage with {len(engagement_results)} companies")
                
                return engagement_results
                
        except Exception as e:
            print(f"❌ Bulk processing error: {e}")
            
    def expand_to_other_platforms(self):
        """Framework for expanding to other platforms"""
        platforms = {
            "product_hunt": {
                "implemented": True,
                "engagement_type": "upvote + comment",
                "api_available": True,
                "automation_level": "full"
            },
            "twitter": {
                "implemented": True,
                "engagement_type": "reply + retweet",
                "api_available": True,
                "automation_level": "full"
            },
            "linkedin": {
                "implemented": False,
                "engagement_type": "comment + connection",
                "api_available": "limited",
                "automation_level": "manual"
            },
            "reddit": {
                "implemented": False,
                "engagement_type": "comment + upvote",
                "api_available": True,
                "automation_level": "possible"
            },
            "hacker_news": {
                "implemented": False,
                "engagement_type": "comment",
                "api_available": "limited",
                "automation_level": "manual"
            },
            "indie_hackers": {
                "implemented": False,
                "engagement_type": "comment + follow",
                "api_available": False,
                "automation_level": "manual"
            }
        }
        
        print("\n🌐 Platform Expansion Opportunities:")
        for platform, info in platforms.items():
            status = "✅" if info["implemented"] else "🔧"
            print(f"   {status} {platform.title()}: {info['engagement_type']} ({info['automation_level']})")
            
        return platforms

def main():
    """Run bulk company processing"""
    processor = BulkCompanyProcessor()
    
    # Show platform capabilities
    processor.expand_to_other_platforms()
    
    # Run bulk discovery and processing
    results = processor.run_bulk_discovery_and_processing()
    
    if results:
        print(f"\n🚀 Next step: Run the Product Hunt automation to engage with {len(results)} companies!")
        print("Command: python3 product_hunt_physical_clicks.py")

if __name__ == "__main__":
    main()
