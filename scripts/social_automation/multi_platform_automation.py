#!/usr/bin/env python3
"""
Multi-Platform Automation Framework
Easily expandable to other platforms beyond Product Hunt
"""

import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MultiPlatformAutomation:
    def __init__(self):
        self.setup_platform_configs()
        self.setup_engagement_strategies()
        
    def setup_platform_configs(self):
        """Configure all supported platforms"""
        self.platforms = {
            "product_hunt": {
                "name": "Product Hunt",
                "status": "active",
                "automation_script": "product_hunt_physical_clicks.py",
                "engagement_types": ["upvote", "comment"],
                "rate_limits": {"requests_per_hour": 60, "engagements_per_day": 50},
                "auth_method": "oauth",
                "difficulty": "medium"
            },
            
            "twitter": {
                "name": "Twitter/X",
                "status": "active", 
                "automation_script": "twitter_video_responder.py",
                "engagement_types": ["reply", "retweet", "like"],
                "rate_limits": {"requests_per_hour": 300, "engagements_per_day": 100},
                "auth_method": "api_key",
                "difficulty": "easy"
            },
            
            "linkedin": {
                "name": "LinkedIn",
                "status": "planned",
                "automation_script": "linkedin_automation.py",
                "engagement_types": ["comment", "connection", "message"],
                "rate_limits": {"requests_per_hour": 30, "engagements_per_day": 20},
                "auth_method": "oauth",
                "difficulty": "hard"
            },
            
            "reddit": {
                "name": "Reddit",
                "status": "possible",
                "automation_script": "reddit_automation.py", 
                "engagement_types": ["comment", "upvote", "post"],
                "rate_limits": {"requests_per_hour": 60, "engagements_per_day": 30},
                "auth_method": "oauth",
                "difficulty": "medium"
            },
            
            "hacker_news": {
                "name": "Hacker News",
                "status": "manual",
                "automation_script": "hackernews_automation.py",
                "engagement_types": ["comment", "upvote"],
                "rate_limits": {"requests_per_hour": 20, "engagements_per_day": 10},
                "auth_method": "session",
                "difficulty": "hard"
            },
            
            "indie_hackers": {
                "name": "Indie Hackers", 
                "status": "manual",
                "automation_script": "indiehackers_automation.py",
                "engagement_types": ["comment", "follow", "message"],
                "rate_limits": {"requests_per_hour": 30, "engagements_per_day": 15},
                "auth_method": "session",
                "difficulty": "medium"
            },
            
            "youtube": {
                "name": "YouTube",
                "status": "active",
                "automation_script": "youtube_video_responder.py", 
                "engagement_types": ["comment", "like", "subscribe"],
                "rate_limits": {"requests_per_hour": 100, "engagements_per_day": 75},
                "auth_method": "oauth",
                "difficulty": "medium"
            },
            
            "discord": {
                "name": "Discord Communities",
                "status": "possible",
                "automation_script": "discord_automation.py",
                "engagement_types": ["message", "react", "join"],
                "rate_limits": {"requests_per_hour": 50, "engagements_per_day": 25},
                "auth_method": "bot_token",
                "difficulty": "easy"
            }
        }
        
    def setup_engagement_strategies(self):
        """Define engagement strategies per platform"""
        self.strategies = {
            "product_hunt": {
                "discovery_method": "daily_launches_api",
                "targeting": "audio_creator_tools",
                "engagement_flow": ["upvote", "authentic_comment"],
                "success_metrics": ["upvotes_given", "comments_posted", "responses_received"]
            },
            
            "twitter": {
                "discovery_method": "keyword_monitoring", 
                "targeting": "creator_pain_points",
                "engagement_flow": ["helpful_reply", "video_share"],
                "success_metrics": ["replies_posted", "retweets", "profile_visits"]
            },
            
            "linkedin": {
                "discovery_method": "company_pages_posts",
                "targeting": "b2b_audio_companies", 
                "engagement_flow": ["professional_comment", "connection_request"],
                "success_metrics": ["comments_posted", "connections_made", "messages_sent"]
            },
            
            "reddit": {
                "discovery_method": "subreddit_monitoring",
                "targeting": "creator_communities",
                "engagement_flow": ["helpful_comment", "resource_share"],
                "success_metrics": ["comments_posted", "upvotes_received", "dm_conversations"]
            }
        }
        
    def get_platform_status(self):
        """Get current status of all platforms"""
        status_report = {
            "active_platforms": [],
            "planned_platforms": [],
            "total_daily_capacity": 0,
            "coverage_analysis": {}
        }
        
        for platform_id, config in self.platforms.items():
            if config["status"] == "active":
                status_report["active_platforms"].append({
                    "name": config["name"],
                    "daily_capacity": config["rate_limits"]["engagements_per_day"],
                    "engagement_types": config["engagement_types"]
                })
                status_report["total_daily_capacity"] += config["rate_limits"]["engagements_per_day"]
                
            elif config["status"] in ["planned", "possible"]:
                status_report["planned_platforms"].append({
                    "name": config["name"],
                    "status": config["status"],
                    "difficulty": config["difficulty"],
                    "potential_capacity": config["rate_limits"]["engagements_per_day"]
                })
                
        return status_report
        
    def calculate_market_coverage(self):
        """Calculate total market coverage across platforms"""
        coverage = {
            "creator_discovery_platforms": 0,
            "b2b_engagement_platforms": 0, 
            "community_platforms": 0,
            "total_daily_engagements": 0,
            "platform_diversity": 0
        }
        
        platform_categories = {
            "creator_discovery": ["product_hunt", "twitter", "youtube"],
            "b2b_engagement": ["linkedin", "product_hunt", "hacker_news"],
            "community": ["reddit", "discord", "indie_hackers"]
        }
        
        active_platforms = [p for p, config in self.platforms.items() if config["status"] == "active"]
        
        for category, platforms in platform_categories.items():
            active_in_category = len([p for p in platforms if p in active_platforms])
            coverage[f"{category}_platforms"] = active_in_category
            
        coverage["total_daily_engagements"] = sum(
            config["rate_limits"]["engagements_per_day"] 
            for config in self.platforms.values() 
            if config["status"] == "active"
        )
        
        coverage["platform_diversity"] = len(active_platforms)
        
        return coverage
        
    def generate_expansion_roadmap(self):
        """Generate roadmap for platform expansion"""
        roadmap = {
            "immediate_opportunities": [],
            "medium_term_goals": [],
            "long_term_vision": [],
            "resource_requirements": {}
        }
        
        # Analyze each platform for expansion priority
        for platform_id, config in self.platforms.items():
            if config["status"] != "active":
                priority_score = self.calculate_expansion_priority(platform_id, config)
                
                expansion_item = {
                    "platform": config["name"],
                    "priority_score": priority_score,
                    "difficulty": config["difficulty"],
                    "potential_daily_engagements": config["rate_limits"]["engagements_per_day"],
                    "implementation_effort": self.estimate_implementation_effort(config)
                }
                
                if priority_score >= 8:
                    roadmap["immediate_opportunities"].append(expansion_item)
                elif priority_score >= 6:
                    roadmap["medium_term_goals"].append(expansion_item)
                else:
                    roadmap["long_term_vision"].append(expansion_item)
                    
        # Sort by priority
        for category in ["immediate_opportunities", "medium_term_goals", "long_term_vision"]:
            roadmap[category].sort(key=lambda x: x["priority_score"], reverse=True)
            
        return roadmap
        
    def calculate_expansion_priority(self, platform_id, config):
        """Calculate priority score for platform expansion"""
        score = 0
        
        # High engagement capacity = higher priority
        daily_capacity = config["rate_limits"]["engagements_per_day"]
        if daily_capacity >= 50:
            score += 3
        elif daily_capacity >= 25:
            score += 2
        else:
            score += 1
            
        # Easier implementation = higher priority
        difficulty_scores = {"easy": 3, "medium": 2, "hard": 1}
        score += difficulty_scores.get(config["difficulty"], 1)
        
        # Multiple engagement types = higher priority
        score += min(len(config["engagement_types"]), 3)
        
        # Platform-specific bonuses
        platform_bonuses = {
            "linkedin": 2,  # B2B focus aligns with Zenyai
            "reddit": 2,    # Large creator communities
            "discord": 1    # Growing creator communities
        }
        score += platform_bonuses.get(platform_id, 0)
        
        return score
        
    def estimate_implementation_effort(self, config):
        """Estimate implementation effort for a platform"""
        base_effort = {"easy": 1, "medium": 3, "hard": 5}[config["difficulty"]]
        
        # OAuth adds complexity
        if config["auth_method"] == "oauth":
            base_effort += 1
            
        # More engagement types = more complexity
        base_effort += len(config["engagement_types"]) * 0.5
        
        return f"{base_effort:.1f} days"
        
    def create_unified_engagement_queue(self):
        """Create unified queue across all active platforms"""
        try:
            # Load engagement data from all platforms
            unified_queue = []
            
            # Product Hunt engagements
            ph_file = "producthunt_zenyai_comments.json"
            if os.path.exists(ph_file):
                with open(ph_file, 'r') as f:
                    ph_data = json.load(f)
                    
                for item in ph_data:
                    if item.get('status') == 'pending':
                        unified_queue.append({
                            'platform': 'product_hunt',
                            'type': 'comment',
                            'target': item['product_name'],
                            'content': item['comment_text'],
                            'url': item['product_url'],
                            'priority': self.calculate_engagement_priority(item),
                            'estimated_time': '2 minutes'
                        })
                        
            # Twitter engagements (if file exists)
            twitter_file = "twitter_engagement_queue.json"
            if os.path.exists(twitter_file):
                with open(twitter_file, 'r') as f:
                    twitter_data = json.load(f)
                    
                for item in twitter_data:
                    if item.get('status') == 'pending':
                        unified_queue.append({
                            'platform': 'twitter',
                            'type': 'reply',
                            'target': item.get('tweet_author', 'Unknown'),
                            'content': item.get('reply_text', ''),
                            'url': item.get('tweet_url', ''),
                            'priority': self.calculate_engagement_priority(item),
                            'estimated_time': '1 minute'
                        })
                        
            # Sort by priority
            unified_queue.sort(key=lambda x: x['priority'], reverse=True)
            
            # Save unified queue
            queue_file = "unified_engagement_queue.json"
            with open(queue_file, 'w') as f:
                json.dump({
                    'created_at': datetime.now().isoformat(),
                    'total_engagements': len(unified_queue),
                    'platforms_included': list(set(item['platform'] for item in unified_queue)),
                    'queue': unified_queue
                }, f, indent=2)
                
            print(f"✅ Created unified queue with {len(unified_queue)} engagements")
            return unified_queue
            
        except Exception as e:
            print(f"❌ Error creating unified queue: {e}")
            return []
            
    def calculate_engagement_priority(self, item):
        """Calculate priority score for an engagement"""
        priority = 5  # Base priority
        
        # Higher engagement targets get higher priority
        if 'votes_count' in item and item['votes_count'] > 100:
            priority += 2
        elif 'votes_count' in item and item['votes_count'] > 50:
            priority += 1
            
        # Newer items get higher priority
        if 'created_at' in item:
            # Recent items get bonus
            priority += 1
            
        return priority
        
    def show_automation_dashboard(self):
        """Display comprehensive automation dashboard"""
        print("🚀 Multi-Platform Automation Dashboard")
        print("=" * 60)
        
        # Platform status
        status = self.get_platform_status()
        print(f"\n📊 Platform Status:")
        print(f"   ✅ Active Platforms: {len(status['active_platforms'])}")
        print(f"   🔧 Planned Platforms: {len(status['planned_platforms'])}")
        print(f"   📈 Total Daily Capacity: {status['total_daily_capacity']} engagements")
        
        # Market coverage
        coverage = self.calculate_market_coverage()
        print(f"\n🎯 Market Coverage:")
        print(f"   🔍 Creator Discovery: {coverage['creator_discovery_platforms']}/3 platforms")
        print(f"   💼 B2B Engagement: {coverage['b2b_engagement_platforms']}/3 platforms") 
        print(f"   👥 Community Platforms: {coverage['community_platforms']}/3 platforms")
        print(f"   🌐 Platform Diversity: {coverage['platform_diversity']} platforms")
        
        # Active platforms detail
        print(f"\n✅ Active Platforms:")
        for platform in status['active_platforms']:
            print(f"   • {platform['name']}: {platform['daily_capacity']} daily engagements")
            print(f"     Types: {', '.join(platform['engagement_types'])}")
            
        # Expansion roadmap
        roadmap = self.generate_expansion_roadmap()
        print(f"\n🚀 Expansion Opportunities:")
        
        if roadmap['immediate_opportunities']:
            print("   🔥 Immediate (High Priority):")
            for opp in roadmap['immediate_opportunities'][:3]:
                print(f"      • {opp['platform']}: {opp['potential_daily_engagements']} daily capacity ({opp['implementation_effort']})")
                
        if roadmap['medium_term_goals']:
            print("   📅 Medium Term:")
            for goal in roadmap['medium_term_goals'][:2]:
                print(f"      • {goal['platform']}: {goal['potential_daily_engagements']} daily capacity ({goal['implementation_effort']})")

def main():
    """Show multi-platform automation dashboard"""
    automation = MultiPlatformAutomation()
    automation.show_automation_dashboard()
    
    # Create unified engagement queue
    print(f"\n🔄 Creating Unified Engagement Queue...")
    queue = automation.create_unified_engagement_queue()
    
    if queue:
        print(f"\n🎯 Next Steps:")
        print(f"   1. Process {len(queue)} pending engagements")
        print(f"   2. Run platform-specific automations")
        print(f"   3. Monitor engagement results")
        print(f"   4. Plan platform expansion")

if __name__ == "__main__":
    main()
