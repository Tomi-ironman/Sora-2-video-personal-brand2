#!/usr/bin/env python3
"""
COMPREHENSIVE Multi-Source Market Research
Integrates 15+ data sources for deep market intelligence
"""

import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MultiSourceResearcher:
    def __init__(self):
        self.setup_data_sources()
        
    def setup_data_sources(self):
        """Setup all available data sources"""
        
        self.data_sources = {
            # SEARCH & TRENDS
            "google_trends": {
                "api": "pytrends",
                "description": "Search trends and volume",
                "setup_required": False
            },
            
            "semrush": {
                "api": "semrush_api", 
                "description": "Keyword research, competition analysis",
                "setup_required": True,
                "api_key": os.getenv('SEMRUSH_API_KEY')
            },
            
            "ahrefs": {
                "api": "ahrefs_api",
                "description": "Backlink analysis, keyword difficulty", 
                "setup_required": True,
                "api_key": os.getenv('AHREFS_API_KEY')
            },
            
            "ubersuggest": {
                "api": "ubersuggest_api",
                "description": "Keyword suggestions, search volume",
                "setup_required": True,
                "api_key": os.getenv('UBERSUGGEST_API_KEY')
            },
            
            # SOCIAL MEDIA
            "reddit": {
                "api": "praw",
                "description": "Community discussions, pain points",
                "setup_required": True,
                "client_id": os.getenv('REDDIT_CLIENT_ID'),
                "client_secret": os.getenv('REDDIT_CLIENT_SECRET')
            },
            
            "twitter": {
                "api": "tweepy",
                "description": "Real-time conversations, sentiment",
                "setup_required": True,
                "bearer_token": os.getenv('TWITTER_BEARER_TOKEN')
            },
            
            "youtube": {
                "api": "youtube_v3",
                "description": "Video content analysis, comments",
                "setup_required": True,
                "api_key": os.getenv('YOUTUBE_API_KEY')
            },
            
            # FORUMS & COMMUNITIES
            "discord": {
                "api": "discord_py",
                "description": "Community servers, discussions",
                "setup_required": True,
                "bot_token": os.getenv('DISCORD_BOT_TOKEN')
            },
            
            "stack_overflow": {
                "api": "stack_exchange",
                "description": "Technical questions, developer pain",
                "setup_required": False
            },
            
            # MARKET INTELLIGENCE
            "crunchbase": {
                "api": "crunchbase_api",
                "description": "Startup funding, market size",
                "setup_required": True,
                "api_key": os.getenv('CRUNCHBASE_API_KEY')
            },
            
            "pitchbook": {
                "api": "pitchbook_api", 
                "description": "Private market data",
                "setup_required": True,
                "api_key": os.getenv('PITCHBOOK_API_KEY')
            },
            
            # E-COMMERCE & REVIEWS
            "amazon": {
                "api": "amazon_paapi",
                "description": "Product reviews, market demand",
                "setup_required": True,
                "access_key": os.getenv('AMAZON_ACCESS_KEY'),
                "secret_key": os.getenv('AMAZON_SECRET_KEY')
            },
            
            "app_store": {
                "api": "app_store_connect",
                "description": "App reviews, feature requests",
                "setup_required": False
            },
            
            "google_play": {
                "api": "google_play_scraper",
                "description": "Android app data, reviews",
                "setup_required": False
            },
            
            # SURVEY & ANALYTICS
            "typeform": {
                "api": "typeform_api",
                "description": "Custom surveys, user feedback",
                "setup_required": True,
                "api_key": os.getenv('TYPEFORM_API_KEY')
            },
            
            "surveymonkey": {
                "api": "surveymonkey_api",
                "description": "Market research surveys",
                "setup_required": True,
                "api_key": os.getenv('SURVEYMONKEY_API_KEY')
            }
        }
        
        print(f"🔍 {len(self.data_sources)} data sources configured")
        
    def check_available_sources(self):
        """Check which data sources are available"""
        available = []
        unavailable = []
        
        for source, config in self.data_sources.items():
            if not config["setup_required"]:
                available.append(source)
            else:
                # Check if API keys exist
                has_keys = True
                for key in ["api_key", "client_id", "bearer_token", "access_key", "bot_token"]:
                    if key in config and not config[key]:
                        has_keys = False
                        break
                        
                if has_keys:
                    available.append(source)
                else:
                    unavailable.append(source)
                    
        return available, unavailable
        
    def research_google_trends_advanced(self, terms):
        """Advanced Google Trends research"""
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='en-US', tz=360)
            results = {}
            
            for term in terms[:5]:  # Batch limit
                try:
                    pytrends.build_payload([term], timeframe='today 12-m')
                    
                    # Interest over time
                    interest_data = pytrends.interest_over_time()
                    
                    # Related queries
                    related = pytrends.related_queries()
                    
                    # Interest by region
                    geo_data = pytrends.interest_by_region()
                    
                    results[term] = {
                        'avg_interest': interest_data[term].mean() if not interest_data.empty else 0,
                        'related_queries': related[term]['top']['query'].tolist()[:10] if term in related and related[term]['top'] is not None else [],
                        'top_regions': geo_data[term].nlargest(5).to_dict() if not geo_data.empty else {}
                    }
                    
                    time.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ Google Trends error for {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Google Trends setup error: {e}")
            return {}
            
    def research_reddit_communities(self, subreddits, keywords):
        """Research Reddit communities"""
        try:
            import praw
            
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent='MarketResearch/1.0'
            )
            
            results = {}
            
            for subreddit_name in subreddits:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    
                    # Search for keyword-related posts
                    posts = []
                    for keyword in keywords:
                        search_results = subreddit.search(keyword, limit=50, time_filter='month')
                        for post in search_results:
                            posts.append({
                                'title': post.title,
                                'score': post.score,
                                'num_comments': post.num_comments,
                                'created': post.created_utc,
                                'keyword': keyword
                            })
                            
                    results[subreddit_name] = {
                        'total_posts': len(posts),
                        'avg_score': sum(p['score'] for p in posts) / len(posts) if posts else 0,
                        'avg_comments': sum(p['num_comments'] for p in posts) / len(posts) if posts else 0,
                        'top_posts': sorted(posts, key=lambda x: x['score'], reverse=True)[:5]
                    }
                    
                except Exception as e:
                    print(f"   ⚠️ Reddit error for r/{subreddit_name}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Reddit setup error: {e}")
            return {}
            
    def research_youtube_content(self, search_terms):
        """Research YouTube content and comments"""
        try:
            from googleapiclient.discovery import build
            
            youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            results = {}
            
            for term in search_terms:
                try:
                    # Search for videos
                    search_response = youtube.search().list(
                        q=term,
                        part='snippet',
                        maxResults=25,
                        type='video',
                        order='relevance'
                    ).execute()
                    
                    videos = []
                    for item in search_response['items']:
                        video_id = item['id']['videoId']
                        
                        # Get video statistics
                        stats_response = youtube.videos().list(
                            part='statistics',
                            id=video_id
                        ).execute()
                        
                        if stats_response['items']:
                            stats = stats_response['items'][0]['statistics']
                            videos.append({
                                'title': item['snippet']['title'],
                                'views': int(stats.get('viewCount', 0)),
                                'likes': int(stats.get('likeCount', 0)),
                                'comments': int(stats.get('commentCount', 0))
                            })
                            
                    results[term] = {
                        'total_videos': len(videos),
                        'avg_views': sum(v['views'] for v in videos) / len(videos) if videos else 0,
                        'avg_engagement': sum(v['likes'] + v['comments'] for v in videos) / len(videos) if videos else 0,
                        'top_videos': sorted(videos, key=lambda x: x['views'], reverse=True)[:3]
                    }
                    
                except Exception as e:
                    print(f"   ⚠️ YouTube error for {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ YouTube setup error: {e}")
            return {}
            
    def research_stack_overflow(self, tags):
        """Research Stack Overflow questions"""
        try:
            results = {}
            
            for tag in tags:
                try:
                    url = f"https://api.stackexchange.com/2.3/questions"
                    params = {
                        'order': 'desc',
                        'sort': 'votes',
                        'tagged': tag,
                        'site': 'stackoverflow',
                        'pagesize': 100
                    }
                    
                    response = requests.get(url, params=params)
                    data = response.json()
                    
                    if 'items' in data:
                        questions = data['items']
                        
                        results[tag] = {
                            'total_questions': len(questions),
                            'avg_score': sum(q['score'] for q in questions) / len(questions) if questions else 0,
                            'avg_views': sum(q['view_count'] for q in questions) / len(questions) if questions else 0,
                            'top_questions': sorted(questions, key=lambda x: x['score'], reverse=True)[:3]
                        }
                        
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ Stack Overflow error for {tag}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Stack Overflow error: {e}")
            return {}
            
    def research_app_stores(self, search_terms):
        """Research app store data"""
        try:
            from google_play_scraper import search, app
            
            results = {}
            
            for term in search_terms:
                try:
                    # Search Google Play Store
                    apps = search(term, lang='en', country='us', n_hits=20)
                    
                    app_data = []
                    for app_info in apps[:5]:  # Top 5 apps
                        try:
                            detailed = app(app_info['appId'])
                            app_data.append({
                                'title': detailed['title'],
                                'rating': detailed.get('score', 0),
                                'reviews': detailed.get('reviews', 0),
                                'installs': detailed.get('realInstalls', 0)
                            })
                        except:
                            continue
                            
                    results[term] = {
                        'total_apps': len(app_data),
                        'avg_rating': sum(a['rating'] for a in app_data) / len(app_data) if app_data else 0,
                        'total_reviews': sum(a['reviews'] for a in app_data),
                        'top_apps': sorted(app_data, key=lambda x: x['reviews'], reverse=True)[:3]
                    }
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ App store error for {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ App store setup error: {e}")
            return {}
            
    def run_comprehensive_research(self, profession_data):
        """Run comprehensive multi-source research"""
        try:
            print("🌐 COMPREHENSIVE MULTI-SOURCE RESEARCH")
            print("=" * 60)
            
            available_sources, unavailable_sources = self.check_available_sources()
            
            print(f"✅ Available sources: {len(available_sources)}")
            print(f"❌ Unavailable sources: {len(unavailable_sources)}")
            print()
            
            all_results = {}
            
            for profession, data in profession_data.items():
                print(f"🔍 RESEARCHING: {profession.upper()}")
                print("-" * 40)
                
                profession_results = {}
                
                # Google Trends
                if 'google_trends' in available_sources:
                    print("📈 Google Trends...")
                    profession_results['google_trends'] = self.research_google_trends_advanced(
                        data.get('search_terms', [])
                    )
                    
                # Reddit
                if 'reddit' in available_sources:
                    print("📱 Reddit Communities...")
                    profession_results['reddit'] = self.research_reddit_communities(
                        data.get('subreddits', []),
                        data.get('keywords', [])
                    )
                    
                # YouTube
                if 'youtube' in available_sources:
                    print("🎥 YouTube Content...")
                    profession_results['youtube'] = self.research_youtube_content(
                        data.get('search_terms', [])
                    )
                    
                # Stack Overflow
                if 'stack_overflow' in available_sources:
                    print("💻 Stack Overflow...")
                    profession_results['stack_overflow'] = self.research_stack_overflow(
                        data.get('tech_tags', [])
                    )
                    
                # App Stores
                if 'app_store' in available_sources:
                    print("📱 App Stores...")
                    profession_results['app_stores'] = self.research_app_stores(
                        data.get('app_terms', [])
                    )
                    
                all_results[profession] = profession_results
                print(f"✅ {profession} research complete\n")
                
            return all_results
            
        except Exception as e:
            print(f"❌ Comprehensive research error: {e}")
            return {}
            
    def save_comprehensive_results(self, results):
        """Save comprehensive research results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"COMPREHENSIVE_research_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"💾 Comprehensive results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run comprehensive multi-source research"""
    
    # Define research targets
    research_targets = {
        "audio_professionals": {
            "search_terms": ["audio organization", "sample library", "music workflow"],
            "subreddits": ["WeAreTheMusicMakers", "edmproduction", "trapproduction"],
            "keywords": ["audio chaos", "sample management", "workflow"],
            "tech_tags": ["audio", "music-production", "daw"],
            "app_terms": ["audio editor", "music production", "sample library"]
        }
    }
    
    researcher = MultiSourceResearcher()
    
    # Run comprehensive research
    results = researcher.run_comprehensive_research(research_targets)
    
    if results:
        researcher.save_comprehensive_results(results)
        print("🎉 COMPREHENSIVE RESEARCH COMPLETE!")
    else:
        print("❌ Research failed")

if __name__ == "__main__":
    main()
