#!/usr/bin/env python3
"""
FREE Market Research Sources (No API Keys Required)
Uses Twitter API + Free scraping sources
"""

import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FreeSourcesResearcher:
    def __init__(self):
        self.setup_free_sources()
        
    def setup_free_sources(self):
        """Setup all FREE data sources"""
        
        self.free_sources = {
            "google_trends": {
                "method": "pytrends_scraping",
                "description": "Search trends (FREE scraping)",
                "available": True
            },
            
            "twitter": {
                "method": "twitter_api", 
                "description": "Real-time conversations",
                "available": bool(os.getenv('TWITTER_BEARER_TOKEN'))
            },
            
            "reddit": {
                "method": "reddit_scraping",
                "description": "Community discussions (FREE scraping)", 
                "available": True
            },
            
            "stack_overflow": {
                "method": "public_api",
                "description": "Technical questions (FREE API)",
                "available": True
            },
            
            "google_play": {
                "method": "scraping",
                "description": "App store data (FREE scraping)",
                "available": True
            },
            
            "hacker_news": {
                "method": "public_api", 
                "description": "Tech community (FREE API)",
                "available": True
            },
            
            "product_hunt": {
                "method": "scraping",
                "description": "Product launches (FREE scraping)",
                "available": True
            }
        }
        
        available_count = sum(1 for source in self.free_sources.values() if source["available"])
        print(f"🆓 {available_count}/{len(self.free_sources)} FREE sources available")
        
    def research_google_trends_free(self, terms):
        """Google Trends without API key (FREE scraping)"""
        try:
            from pytrends.request import TrendReq
            
            print("📈 Google Trends (FREE scraping)...")
            pytrends = TrendReq(hl='en-US', tz=360)
            results = {}
            
            # Process in small batches to avoid rate limits
            for i, term in enumerate(terms[:3]):  # Limit to 3 terms
                try:
                    pytrends.build_payload([term], timeframe='today 12-m', geo='US')
                    
                    # Get interest over time
                    interest_data = pytrends.interest_over_time()
                    
                    if not interest_data.empty:
                        avg_interest = interest_data[term].mean()
                        max_interest = interest_data[term].max()
                        
                        results[term] = {
                            'avg_interest': avg_interest,
                            'max_interest': max_interest,
                            'estimated_searches': avg_interest * 1000  # Rough estimate
                        }
                        
                        print(f"   📊 {term}: {avg_interest:.1f} avg interest")
                    
                    time.sleep(3)  # Longer delay for free scraping
                    
                except Exception as e:
                    print(f"   ⚠️ Error with {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Google Trends error: {e}")
            return {}
            
    def research_twitter_existing_api(self, search_terms):
        """Use existing Twitter API"""
        try:
            import tweepy
            
            print("🐦 Twitter (using your existing API)...")
            
            client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                wait_on_rate_limit=True
            )
            
            results = {}
            
            for term in search_terms[:3]:  # Limit to avoid rate limits
                try:
                    # Search recent tweets
                    tweets = client.search_recent_tweets(
                        query=f"{term} -is:retweet lang:en",
                        max_results=100,
                        tweet_fields=['created_at', 'author_id', 'public_metrics']
                    )
                    
                    if tweets.data:
                        total_engagement = 0
                        sentiment_scores = []
                        
                        for tweet in tweets.data:
                            metrics = tweet.public_metrics
                            engagement = (
                                metrics['like_count'] + 
                                metrics['reply_count'] + 
                                metrics['retweet_count']
                            )
                            total_engagement += engagement
                            
                            # Simple sentiment analysis
                            text = tweet.text.lower()
                            negative_words = ['problem', 'issue', 'difficult', 'hard', 'struggle', 'pain', 'frustrating']
                            positive_words = ['love', 'great', 'awesome', 'easy', 'simple', 'perfect']
                            
                            sentiment = sum(1 for word in negative_words if word in text) - sum(1 for word in positive_words if word in text)
                            sentiment_scores.append(sentiment)
                            
                        results[term] = {
                            'tweet_count': len(tweets.data),
                            'total_engagement': total_engagement,
                            'avg_engagement': total_engagement / len(tweets.data),
                            'avg_sentiment': sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
                            'pain_indicator': sum(1 for s in sentiment_scores if s > 0) / len(sentiment_scores) if sentiment_scores else 0
                        }
                        
                        print(f"   🐦 {term}: {len(tweets.data)} tweets, {total_engagement} total engagement")
                        
                    time.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ Twitter error for {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Twitter setup error: {e}")
            return {}
            
    def research_reddit_free_scraping(self, subreddits, keywords):
        """Reddit scraping without API (FREE)"""
        try:
            print("📱 Reddit (FREE scraping)...")
            
            results = {}
            
            for subreddit in subreddits[:2]:  # Limit to 2 subreddits
                try:
                    # Use Reddit's JSON API (no auth required)
                    url = f"https://www.reddit.com/r/{subreddit}/search.json"
                    
                    subreddit_results = []
                    
                    for keyword in keywords[:3]:  # Limit keywords
                        params = {
                            'q': keyword,
                            'restrict_sr': 'on',
                            'sort': 'relevance',
                            'limit': 25
                        }
                        
                        headers = {'User-Agent': 'MarketResearch/1.0'}
                        response = requests.get(url, params=params, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            for post in data['data']['children']:
                                post_data = post['data']
                                subreddit_results.append({
                                    'title': post_data['title'],
                                    'score': post_data['score'],
                                    'num_comments': post_data['num_comments'],
                                    'keyword': keyword
                                })
                                
                        time.sleep(2)  # Rate limiting
                        
                    if subreddit_results:
                        results[subreddit] = {
                            'total_posts': len(subreddit_results),
                            'avg_score': sum(p['score'] for p in subreddit_results) / len(subreddit_results),
                            'avg_comments': sum(p['num_comments'] for p in subreddit_results) / len(subreddit_results),
                            'top_posts': sorted(subreddit_results, key=lambda x: x['score'], reverse=True)[:3]
                        }
                        
                        print(f"   📱 r/{subreddit}: {len(subreddit_results)} posts found")
                        
                except Exception as e:
                    print(f"   ⚠️ Reddit error for r/{subreddit}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Reddit scraping error: {e}")
            return {}
            
    def research_stack_overflow_free(self, tags):
        """Stack Overflow public API (FREE)"""
        try:
            print("💻 Stack Overflow (FREE API)...")
            
            results = {}
            
            for tag in tags[:3]:  # Limit tags
                try:
                    url = "https://api.stackexchange.com/2.3/questions"
                    params = {
                        'order': 'desc',
                        'sort': 'votes', 
                        'tagged': tag,
                        'site': 'stackoverflow',
                        'pagesize': 50
                    }
                    
                    response = requests.get(url, params=params)
                    data = response.json()
                    
                    if 'items' in data:
                        questions = data['items']
                        
                        results[tag] = {
                            'total_questions': len(questions),
                            'avg_score': sum(q['score'] for q in questions) / len(questions) if questions else 0,
                            'avg_views': sum(q['view_count'] for q in questions) / len(questions) if questions else 0,
                            'pain_questions': [q for q in questions if any(word in q['title'].lower() for word in ['problem', 'issue', 'error', 'help'])]
                        }
                        
                        print(f"   💻 {tag}: {len(questions)} questions, {len(results[tag]['pain_questions'])} pain-related")
                        
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ Stack Overflow error for {tag}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ Stack Overflow error: {e}")
            return {}
            
    def research_app_stores_free(self, search_terms):
        """App store scraping (FREE)"""
        try:
            print("📱 App Stores (FREE scraping)...")
            
            # Install if needed
            try:
                from google_play_scraper import search, app
            except ImportError:
                print("   📦 Installing google-play-scraper...")
                os.system("pip install google-play-scraper")
                from google_play_scraper import search, app
                
            results = {}
            
            for term in search_terms[:2]:  # Limit terms
                try:
                    apps = search(term, lang='en', country='us', n_hits=10)
                    
                    app_data = []
                    for app_info in apps[:3]:  # Top 3 apps
                        try:
                            detailed = app(app_info['appId'])
                            app_data.append({
                                'title': detailed['title'],
                                'rating': detailed.get('score', 0),
                                'reviews': detailed.get('reviews', 0),
                                'category': detailed.get('genre', 'Unknown')
                            })
                        except:
                            continue
                            
                    results[term] = {
                        'total_apps': len(app_data),
                        'avg_rating': sum(a['rating'] for a in app_data) / len(app_data) if app_data else 0,
                        'total_reviews': sum(a['reviews'] for a in app_data),
                        'categories': list(set(a['category'] for a in app_data))
                    }
                    
                    print(f"   📱 {term}: {len(app_data)} apps analyzed")
                    
                    time.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"   ⚠️ App store error for {term}: {e}")
                    
            return results
            
        except Exception as e:
            print(f"❌ App store error: {e}")
            return {}
            
    def calculate_free_pain_score(self, all_data):
        """Calculate pain score from FREE sources"""
        try:
            score_components = []
            
            # Google Trends component
            if 'google_trends' in all_data:
                trends_data = all_data['google_trends']
                if trends_data:
                    avg_interest = sum(data['avg_interest'] for data in trends_data.values()) / len(trends_data)
                    score_components.append(min(avg_interest * 2, 25))  # Max 25 points
                    
            # Twitter component  
            if 'twitter' in all_data:
                twitter_data = all_data['twitter']
                if twitter_data:
                    pain_indicators = sum(data['pain_indicator'] for data in twitter_data.values()) / len(twitter_data)
                    score_components.append(pain_indicators * 30)  # Max 30 points
                    
            # Reddit component
            if 'reddit' in all_data:
                reddit_data = all_data['reddit']
                if reddit_data:
                    avg_engagement = sum(data['avg_score'] + data['avg_comments'] for data in reddit_data.values()) / len(reddit_data)
                    score_components.append(min(avg_engagement / 10, 25))  # Max 25 points
                    
            # Stack Overflow component
            if 'stack_overflow' in all_data:
                so_data = all_data['stack_overflow']
                if so_data:
                    pain_ratio = sum(len(data['pain_questions']) / max(data['total_questions'], 1) for data in so_data.values()) / len(so_data)
                    score_components.append(pain_ratio * 20)  # Max 20 points
                    
            total_score = sum(score_components)
            return min(total_score, 100)  # Cap at 100
            
        except Exception as e:
            print(f"❌ Pain score calculation error: {e}")
            return 0
            
    def run_free_research(self):
        """Run comprehensive FREE research"""
        try:
            print("🆓 FREE MARKET RESEARCH (No API Keys Required)")
            print("=" * 60)
            
            # Audio professionals research
            research_data = {
                'search_terms': ['audio organization', 'sample library', 'music workflow'],
                'subreddits': ['WeAreTheMusicMakers', 'edmproduction'],
                'keywords': ['audio chaos', 'sample management', 'workflow'],
                'stack_tags': ['audio', 'music-production'],
                'app_terms': ['audio editor', 'music production']
            }
            
            all_results = {}
            
            # Google Trends (FREE)
            all_results['google_trends'] = self.research_google_trends_free(
                research_data['search_terms']
            )
            
            # Twitter (using your existing API)
            if self.free_sources['twitter']['available']:
                all_results['twitter'] = self.research_twitter_existing_api(
                    research_data['search_terms']
                )
            
            # Reddit (FREE scraping)
            all_results['reddit'] = self.research_reddit_free_scraping(
                research_data['subreddits'],
                research_data['keywords']
            )
            
            # Stack Overflow (FREE API)
            all_results['stack_overflow'] = self.research_stack_overflow_free(
                research_data['stack_tags']
            )
            
            # App Stores (FREE scraping)
            all_results['app_stores'] = self.research_app_stores_free(
                research_data['app_terms']
            )
            
            # Calculate overall pain score
            pain_score = self.calculate_free_pain_score(all_results)
            
            print(f"\n📊 FREE RESEARCH RESULTS:")
            print("=" * 40)
            print(f"🎯 Audio Professional Pain Score: {pain_score:.1f}/100")
            print(f"📈 Data Sources Used: {len([k for k, v in all_results.items() if v])}")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FREE_research_{timestamp}.json"
            
            output = {
                'research_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'methodology': 'FREE sources only (no paid APIs)',
                    'sources_used': list(all_results.keys()),
                    'pain_score': pain_score
                },
                'detailed_results': all_results
            }
            
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2)
                
            print(f"💾 Results saved to: {filename}")
            
            return all_results
            
        except Exception as e:
            print(f"❌ Free research error: {e}")
            return {}

def main():
    """Run FREE market research"""
    researcher = FreeSourcesResearcher()
    
    results = researcher.run_free_research()
    
    if results:
        print("\n🎉 FREE RESEARCH COMPLETE!")
        print("💡 No API keys required - all data from free sources!")
    else:
        print("❌ Free research failed")

if __name__ == "__main__":
    main()
