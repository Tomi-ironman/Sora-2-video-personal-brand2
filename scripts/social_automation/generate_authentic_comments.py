#!/usr/bin/env python3
"""
Generate authentic, business-focused Product Hunt comments
No quotes, sounds like a real human who understands business
"""

import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AuthenticCommentGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.setup_business_personas()
        self.setup_zenyai_context()
        
    def setup_business_personas(self):
        """Business-focused personas that understand different industries"""
        self.personas = {
            "audio_entrepreneur": {
                "background": "Audio industry entrepreneur who's built workflow solutions",
                "tone": "Strategic and collaborative",
                "approach": "Focuses on business model, market fit, and partnership opportunities"
            },
            "workflow_consultant": {
                "background": "Workflow optimization consultant for creative teams",
                "tone": "Analytical and solution-oriented", 
                "approach": "Discusses efficiency gains, team collaboration, and scalability"
            },
            "creator_economy_expert": {
                "background": "Creator economy strategist who understands monetization",
                "tone": "Forward-thinking and market-aware",
                "approach": "Connects to creator pain points and revenue opportunities"
            }
        }
        
    def setup_zenyai_context(self):
        """Zenyai business context for authentic mentions"""
        self.zenyai_context = {
            "core_business": "AI-native audio asset management platform",
            "target_market": "Audio professionals, podcast creators, sound designers, music producers",
            "key_differentiator": "Intelligent workflow automation that learns user patterns",
            "business_model": "SaaS platform focused on creative workflow optimization",
            "collaboration_angles": [
                "Integration partnerships with creator tools",
                "Workflow optimization consulting",
                "Creator community building",
                "Audio industry market insights",
                "Team collaboration solutions"
            ]
        }
        
    def analyze_product_business_model(self, product_name, tagline, description):
        """Analyze product to understand business model and opportunities"""
        combined_text = f"{product_name} {tagline} {description}".lower()
        
        business_categories = {
            "creator_tools": ["creator", "content", "video", "audio", "podcast", "design", "creative"],
            "workflow_automation": ["workflow", "automation", "productivity", "team", "collaboration"],
            "ai_platform": ["ai", "machine learning", "intelligent", "smart", "automated"],
            "saas_business": ["platform", "software", "service", "tool", "solution"],
            "marketplace": ["marketplace", "community", "network", "connect", "discover"]
        }
        
        detected_categories = []
        for category, keywords in business_categories.items():
            if any(keyword in combined_text for keyword in keywords):
                detected_categories.append(category)
                
        return detected_categories
        
    def generate_authentic_comment(self, product_name, tagline, description=""):
        """Generate authentic business comment without quotes"""
        
        # Analyze business model
        business_categories = self.analyze_product_business_model(product_name, tagline, description)
        
        # Select appropriate persona
        persona = random.choice(list(self.personas.values()))
        
        # Determine collaboration angle
        collab_angle = random.choice(self.zenyai_context["collaboration_angles"])
        
        prompt = f"""
        You are a {persona['background']} commenting on a Product Hunt launch.
        
        Product: {product_name}
        Tagline: {tagline}
        Business Categories: {', '.join(business_categories)}
        
        Your persona:
        - Background: {persona['background']}
        - Tone: {persona['tone']}
        - Approach: {persona['approach']}
        
        Your company context:
        - You work with Zenyai: {self.zenyai_context['core_business']}
        - Target market: {self.zenyai_context['target_market']}
        - Key differentiator: {self.zenyai_context['key_differentiator']}
        
        Collaboration opportunity: {collab_angle}
        
        Write a comment that:
        1. Shows genuine understanding of their business model
        2. Identifies a specific collaboration or learning opportunity
        3. Mentions Zenyai naturally as a relevant solution in the space
        4. Sounds like a real business professional, not marketing copy
        5. NO quotes or quotation marks anywhere
        6. Keep under 200 characters
        7. End with a question or collaboration invitation
        
        Examples of authentic business tone:
        - "Interesting approach to the creator workflow problem. We've been tackling similar challenges with Zenyai's AI-native asset management. Would love to explore potential integrations - DM me?"
        - "This could be huge for podcast creators. At Zenyai we see the same workflow bottlenecks daily. How are you handling large audio file libraries? Always looking to learn from other solutions."
        - "Smart positioning in the audio tools space. We're solving adjacent problems with Zenyai's intelligent workflow automation. Curious about your user acquisition strategy - coffee chat sometime?"
        
        Write the comment (no quotes, no quotation marks):
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8
            )
            
            comment = response.choices[0].message.content.strip()
            
            # Remove any quotes that might have been added
            comment = comment.replace('"', '').replace("'", '').replace('"', '').replace('"', '')
            
            return comment
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            
            # Fallback authentic comments
            fallbacks = [
                f"Interesting take on workflow optimization. We're tackling similar challenges at Zenyai with AI-native audio asset management. Would love to compare notes on user adoption strategies?",
                f"This looks promising for the creator economy. At Zenyai we see these workflow pain points constantly. How are you approaching team collaboration features?",
                f"Smart approach to the productivity space. We're building complementary solutions with Zenyai's intelligent workflow automation. Open to exploring potential partnerships?",
                f"Great execution on the user experience. We're solving adjacent problems in audio workflow management at Zenyai. Curious about your technical architecture - always learning from other builders."
            ]
            
            return random.choice(fallbacks)
            
    def update_existing_comments(self):
        """Update existing comments to be more authentic"""
        comments_file = "producthunt_zenyai_comments.json"
        
        if not os.path.exists(comments_file):
            print("❌ No comments file found")
            return
            
        with open(comments_file, 'r') as f:
            comments = json.load(f)
            
        updated_count = 0
        
        for comment_data in comments:
            if comment_data.get('status') == 'pending':
                # Generate new authentic comment
                new_comment = self.generate_authentic_comment(
                    comment_data['product_name'],
                    comment_data['tagline']
                )
                
                # Update comment
                comment_data['comment_text'] = new_comment
                comment_data['updated_at'] = datetime.now().isoformat()
                comment_data['comment_type'] = 'authentic_business'
                
                updated_count += 1
                
                print(f"✅ Updated comment for {comment_data['product_name']}")
                print(f"   New comment: {new_comment}")
                
        # Save updated comments
        with open(comments_file, 'w') as f:
            json.dump(comments, f, indent=2)
            
        print(f"\n🎉 Updated {updated_count} comments to be more authentic!")
        
def main():
    """Update comments to be more authentic"""
    generator = AuthenticCommentGenerator()
    generator.update_existing_comments()

if __name__ == "__main__":
    main()
