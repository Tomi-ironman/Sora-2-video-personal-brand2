#!/usr/bin/env python3
"""
Twitter Optimization System (Read-Only Mode)
Optimizes Twitter monitoring and analysis while permissions are being upgraded
"""

import tweepy
import os
import time
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class TwitterOptimizer:
    def __init__(self):
        self.setup_apis()
        self.setup_targeting()
        self.setup_analytics()
        
    def setup_apis(self):
        """Initialize Twitter API for read-only operations"""
        try:
            self.twitter_api = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                wait_on_rate_limit=True
            )
            
            self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            print("✅ APIs initialized (read-only mode)")
            
        except Exception as e:
            print(f"❌ API setup failed: {e}")
            
    def setup_targeting(self):
        """Advanced targeting for Zenyai's market"""
        self.target_profiles = {
            "audio_professionals": {
                "keywords": ["audio engineer", "sound designer", "mixing", "mastering", "studio"],
                "hashtags": ["#audioengineering", "#sounddesign", "#mixing", "#mastering"],
                "pain_points": ["workflow", "organization", "files", "deadline", "burnout"]
            },
            "podcast_creators": {
                "keywords": ["podcast", "podcasting", "episode", "show", "creator"],
                "hashtags": ["#podcast", "#podcasting", "#creator", "#content"],
                "pain_points": ["editing", "workflow", "team", "collaboration", "files"]
            },
            "music_producers": {
                "keywords": ["music producer", "beat maker", "production", "samples"],
                "hashtags": ["#musicproducer", "#beatmaker", "#production", "#samples"],
                "pain_points": ["sample library", "organization", "workflow", "collaboration"]
            },
            "content_creators": {
                "keywords": ["content creator", "youtuber", "video creator", "influencer"],
                "hashtags": ["#contentcreator", "#youtube", "#creator", "#video"],
                "pain_points": ["audio quality", "editing", "workflow", "team"]
            }
        }
        
    def setup_analytics(self):
        """Setup analytics tracking"""
        self.analytics = {
            "tweets_analyzed": 0,
            "relevant_tweets_found": 0,
            "high_priority_targets": 0,
            "engagement_opportunities": 0,
            "top_pain_points": {},
            "best_times_to_post": [],
            "most_active_creators": []
        }
        
    def advanced_tweet_search(self, profile_type, hours_back=24):
        """Advanced search for specific creator profiles"""
        try:
            profile = self.target_profiles[profile_type]
            
            # Create sophisticated search queries
            search_queries = []
            
            # Pain point focused searches
            for pain_point in profile["pain_points"]:
                for keyword in profile["keywords"][:2]:  # Limit to avoid too many queries
                    query = f'"{keyword}" "{pain_point}" -is:retweet -is:reply lang:en'
                    search_queries.append(query)
                    
            # Hashtag searches
            hashtag_query = f'({" OR ".join(profile["hashtags"])}) -is:retweet lang:en'
            search_queries.append(hashtag_query)
            
            all_tweets = []
            
            for query in search_queries[:3]:  # Limit queries to avoid rate limits
                try:
                    print(f"🔍 Searching: {query[:50]}...")
                    
                    tweets = self.twitter_api.search_recent_tweets(
                        query=query,
                        max_results=20,  # Increased from 10
                        tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations'],
                        user_fields=['username', 'name', 'public_metrics', 'description']
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data:
                            tweet_data = {
                                'id': tweet.id,
                                'text': tweet.text,
                                'author_id': tweet.author_id,
                                'created_at': tweet.created_at,
                                'retweet_count': tweet.public_metrics['retweet_count'],
                                'like_count': tweet.public_metrics['like_count'],
                                'reply_count': tweet.public_metrics['reply_count'],
                                'profile_type': profile_type,
                                'search_query': query,
                                'relevance_score': 0
                            }
                            all_tweets.append(tweet_data)
                            
                    time.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"❌ Search error for {query}: {e}")
                    time.sleep(5)
                    
            print(f"✅ Found {len(all_tweets)} tweets for {profile_type}")
            return all_tweets
            
        except Exception as e:
            print(f"❌ Advanced search error: {e}")
            return []
            
    def analyze_tweet_relevance(self, tweet_data):
        """AI-powered relevance analysis"""
        try:
            prompt = f"""
            Analyze this tweet for relevance to Zenyai's AI-native audio asset management platform:
            
            Tweet: "{tweet_data['text']}"
            Profile Type: {tweet_data['profile_type']}
            Engagement: {tweet_data['like_count']} likes, {tweet_data['reply_count']} replies
            
            Zenyai Context:
            - AI-native audio asset management
            - Workflow automation for audio professionals
            - Team collaboration for creative projects
            - File organization and search
            
            Rate relevance 1-10 and provide analysis in JSON:
            {{
                "relevance_score": [1-10],
                "pain_points_mentioned": ["list of pain points"],
                "engagement_opportunity": "specific way to help",
                "priority_level": "high/medium/low",
                "best_response_approach": "how to respond helpfully",
                "collaboration_potential": "potential for business collaboration"
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content.strip())
            tweet_data['ai_analysis'] = analysis
            tweet_data['relevance_score'] = analysis.get('relevance_score', 0)
            
            return analysis.get('relevance_score', 0) >= 6  # Threshold for relevance
            
        except Exception as e:
            print(f"❌ AI analysis error: {e}")
            return False
            
    def generate_engagement_strategy(self, tweet_data):
        """Generate specific engagement strategy for each tweet"""
        try:
            analysis = tweet_data.get('ai_analysis', {})
            
            strategy = {
                'tweet_id': tweet_data['id'],
                'author_id': tweet_data['author_id'],
                'priority': analysis.get('priority_level', 'medium'),
                'approach': analysis.get('best_response_approach', 'helpful comment'),
                'pain_points': analysis.get('pain_points_mentioned', []),
                'collaboration_potential': analysis.get('collaboration_potential', 'low'),
                'suggested_response': self.generate_response_text(tweet_data),
                'best_video_match': self.match_video_to_tweet(tweet_data),
                'timing_recommendation': self.calculate_best_response_time(tweet_data)
            }
            
            return strategy
            
        except Exception as e:
            print(f"❌ Strategy generation error: {e}")
            return None
            
    def generate_response_text(self, tweet_data):
        """Generate authentic response text"""
        try:
            analysis = tweet_data.get('ai_analysis', {})
            
            prompt = f"""
            Create an authentic, helpful response to this tweet:
            
            Tweet: "{tweet_data['text']}"
            Pain Points: {analysis.get('pain_points_mentioned', [])}
            Engagement Opportunity: {analysis.get('engagement_opportunity', '')}
            
            Requirements:
            - Be genuinely helpful and empathetic
            - Reference their specific problem
            - Mention Zenyai naturally as a solution
            - Keep under 280 characters
            - Don't be salesy
            - Include relevant emoji
            - Sound like a real person who understands their business
            
            Response:
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Response generation error: {e}")
            return "I totally understand this challenge! We've been working on similar solutions at Zenyai. Would love to share some insights that might help! 🎧"
            
    def match_video_to_tweet(self, tweet_data):
        """Match appropriate video to tweet content"""
        video_library = {
            "file_organization": ["file", "organize", "chaos", "mess", "folders", "library"],
            "sound_design": ["sound design", "audio search", "samples", "effects"],
            "audio_professional": ["audio professional", "burnout", "deadline", "mixing"],
            "podcast_workflow": ["podcast", "episode", "workflow", "team", "collaboration"]
        }
        
        tweet_text = tweet_data['text'].lower()
        
        for video_type, keywords in video_library.items():
            if any(keyword in tweet_text for keyword in keywords):
                return video_type
                
        return "general_workflow"  # Default
        
    def calculate_best_response_time(self, tweet_data):
        """Calculate optimal time to respond"""
        created_at = tweet_data['created_at']
        
        # Respond within 2-6 hours for maximum visibility
        min_delay = 2 * 60 * 60  # 2 hours
        max_delay = 6 * 60 * 60  # 6 hours
        
        optimal_delay = random.randint(min_delay, max_delay)
        response_time = created_at + timedelta(seconds=optimal_delay)
        
        return response_time.isoformat()
        
    def run_optimization_cycle(self):
        """Run one optimization cycle"""
        print("🚀 Starting Twitter Optimization Cycle")
        print("=" * 50)
        
        all_strategies = []
        
        # Search each profile type
        for profile_type in self.target_profiles.keys():
            print(f"\n🎯 Analyzing {profile_type.replace('_', ' ').title()}")
            
            tweets = self.advanced_tweet_search(profile_type)
            self.analytics["tweets_analyzed"] += len(tweets)
            
            relevant_tweets = []
            
            # Analyze each tweet
            for tweet in tweets:
                if self.analyze_tweet_relevance(tweet):
                    relevant_tweets.append(tweet)
                    self.analytics["relevant_tweets_found"] += 1
                    
                    # Generate engagement strategy
                    strategy = self.generate_engagement_strategy(tweet)
                    if strategy:
                        all_strategies.append(strategy)
                        
                        if strategy['priority'] == 'high':
                            self.analytics["high_priority_targets"] += 1
                            
                time.sleep(0.5)  # Small delay between analyses
                
            print(f"   ✅ {len(relevant_tweets)} relevant tweets found")
            
        # Sort strategies by priority
        high_priority = [s for s in all_strategies if s['priority'] == 'high']
        medium_priority = [s for s in all_strategies if s['priority'] == 'medium']
        
        # Save engagement queue
        engagement_queue = {
            'created_at': datetime.now().isoformat(),
            'total_strategies': len(all_strategies),
            'high_priority': len(high_priority),
            'medium_priority': len(medium_priority),
            'strategies': all_strategies
        }
        
        with open('twitter_engagement_queue.json', 'w') as f:
            json.dump(engagement_queue, f, indent=2)
            
        print(f"\n📊 Optimization Results:")
        print(f"   🎯 Total Strategies: {len(all_strategies)}")
        print(f"   🔥 High Priority: {len(high_priority)}")
        print(f"   📈 Medium Priority: {len(medium_priority)}")
        print(f"   💾 Saved to twitter_engagement_queue.json")
        
        return all_strategies
        
    def run_continuous_optimization(self, cycle_interval=1800):  # 30 minutes
        """Run continuous optimization for 7 hours"""
        print("🔄 Starting 7-Hour Twitter Optimization")
        print("=" * 50)
        
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=7)
        
        cycle_count = 0
        total_strategies = 0
        
        while datetime.now() < end_time:
            cycle_count += 1
            print(f"\n🔄 CYCLE {cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
            
            try:
                strategies = self.run_optimization_cycle()
                total_strategies += len(strategies)
                
                # Show progress
                remaining_time = end_time - datetime.now()
                hours_left = remaining_time.total_seconds() / 3600
                
                print(f"\n⏰ Progress Update:")
                print(f"   🕐 Time Remaining: {hours_left:.1f} hours")
                print(f"   📊 Total Strategies Generated: {total_strategies}")
                print(f"   🎯 Strategies This Cycle: {len(strategies)}")
                
                if hours_left > 0.5:  # If more than 30 minutes left
                    print(f"   😴 Sleeping for {cycle_interval/60:.0f} minutes...")
                    time.sleep(cycle_interval)
                else:
                    break
                    
            except KeyboardInterrupt:
                print("🛑 Optimization stopped by user")
                break
            except Exception as e:
                print(f"❌ Cycle error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
                
        # Final summary
        print(f"\n🎉 7-Hour Optimization Complete!")
        print(f"📊 Final Results:")
        print(f"   🔄 Cycles Completed: {cycle_count}")
        print(f"   🎯 Total Strategies: {total_strategies}")
        print(f"   📈 Tweets Analyzed: {self.analytics['tweets_analyzed']}")
        print(f"   ✅ Relevant Tweets: {self.analytics['relevant_tweets_found']}")
        
        return total_strategies

def main():
    """Run Twitter optimization"""
    optimizer = TwitterOptimizer()
    
    print("🐦 Twitter Optimization System (Read-Only Mode)")
    print("=" * 60)
    print("📋 This system will:")
    print("   🔍 Search for relevant tweets from audio professionals")
    print("   🤖 Analyze tweets with AI for relevance and pain points")
    print("   📝 Generate engagement strategies and responses")
    print("   💾 Save everything to engagement queue")
    print("   ⏰ Run continuously for 7 hours")
    print("\n🔧 Once Twitter permissions are upgraded, we can auto-post!")
    
    input("\nPress ENTER to start 7-hour optimization...")
    
    total_strategies = optimizer.run_continuous_optimization()
    
    print(f"\n🚀 Ready for next phase!")
    print(f"✅ Generated {total_strategies} engagement strategies")
    print(f"🎯 Next: Upgrade Twitter permissions and auto-engage")
    print(f"📊 Then: Process 50+ companies with Product Hunt")

if __name__ == "__main__":
    main()
