#!/usr/bin/env python3
"""
REAL Market Research with Google Trends API
Legitimate data analysis for creative metadata pain points
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pytrends.request import TrendReq

load_dotenv()

class RealMarketResearcher:
    def __init__(self):
        self.setup_apis()
        self.setup_research_terms()
        
    def setup_apis(self):
        """Setup real APIs"""
        try:
            # Google Trends (free, no API key needed)
            self.pytrends = TrendReq(hl='en-US', tz=360)
            print("✅ Google Trends API ready")
            
            # Reddit API (if you have credentials)
            self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
            self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            
            if self.reddit_client_id and self.reddit_client_secret:
                print("✅ Reddit API credentials found")
            else:
                print("⚠️ Reddit API credentials not found (optional)")
                
            # Twitter API (if you have credentials)
            self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN')
            if self.twitter_bearer:
                print("✅ Twitter API credentials found")
            else:
                print("⚠️ Twitter API credentials not found (optional)")
                
        except Exception as e:
            print(f"❌ API setup error: {e}")
            
    def setup_research_terms(self):
        """Setup real search terms for each creative profession"""
        
        self.profession_search_terms = {
            "audio_professionals": [
                "audio file organization",
                "sample library management", 
                "audio metadata",
                "music production workflow",
                "audio asset management",
                "sound library organization",
                "audio file tagging",
                "music producer workflow"
            ],
            
            "photographers": [
                "photo organization software",
                "lightroom catalog management",
                "photo metadata",
                "image library organization", 
                "photo tagging software",
                "photography workflow",
                "photo asset management",
                "image file organization"
            ],
            
            "video_editors": [
                "video file organization",
                "footage management software",
                "video asset management",
                "media library organization",
                "video editing workflow",
                "clip organization",
                "video metadata management",
                "media asset management"
            ],
            
            "graphic_designers": [
                "design asset management",
                "creative file organization",
                "design library software",
                "graphic design workflow",
                "design asset organization",
                "creative asset management",
                "design file management",
                "brand asset management"
            ],
            
            "content_creators": [
                "content library organization",
                "creator asset management",
                "social media asset organization",
                "content workflow management",
                "creator file organization",
                "content planning software",
                "media content organization",
                "creator productivity tools"
            ]
        }
        
        print(f"🔍 Research terms loaded for {len(self.profession_search_terms)} professions")
        
    def get_real_google_trends_data(self, search_terms, profession):
        """Get REAL Google Trends data"""
        try:
            print(f"📈 Getting REAL Google Trends data for {profession}...")
            
            all_results = []
            
            # Process terms in batches (Google Trends limit is 5 terms per request)
            for i in range(0, len(search_terms), 5):
                batch = search_terms[i:i+5]
                
                try:
                    # Build payload for Google Trends
                    self.pytrends.build_payload(
                        batch, 
                        cat=0, 
                        timeframe='today 12-m',  # Last 12 months
                        geo='US',  # United States
                        gprop=''
                    )
                    
                    # Get interest over time
                    interest_data = self.pytrends.interest_over_time()
                    
                    if not interest_data.empty:
                        # Calculate average interest for each term
                        for term in batch:
                            if term in interest_data.columns:
                                avg_interest = interest_data[term].mean()
                                max_interest = interest_data[term].max()
                                
                                all_results.append({
                                    'term': term,
                                    'avg_interest': avg_interest,
                                    'max_interest': max_interest,
                                    'total_searches': avg_interest * 1000  # Rough estimate
                                })
                                
                                print(f"   📊 {term}: {avg_interest:.1f} avg interest")
                    
                    # Delay to avoid rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"   ⚠️ Error with batch {batch}: {e}")
                    continue
                    
            # Calculate profession totals
            if all_results:
                total_avg_interest = sum(r['avg_interest'] for r in all_results)
                total_searches = sum(r['total_searches'] for r in all_results)
                
                return {
                    'terms_analyzed': len(all_results),
                    'total_avg_interest': total_avg_interest,
                    'total_estimated_searches': total_searches,
                    'individual_terms': all_results,
                    'data_source': 'real_google_trends'
                }
            else:
                return {
                    'terms_analyzed': 0,
                    'total_avg_interest': 0,
                    'total_estimated_searches': 0,
                    'individual_terms': [],
                    'data_source': 'real_google_trends'
                }
                
        except Exception as e:
            print(f"❌ Google Trends error for {profession}: {e}")
            return {
                'terms_analyzed': 0,
                'total_avg_interest': 0,
                'total_estimated_searches': 0,
                'individual_terms': [],
                'error': str(e),
                'data_source': 'real_google_trends'
            }
            
    def get_related_queries(self, main_term):
        """Get related queries from Google Trends"""
        try:
            print(f"🔗 Getting related queries for: {main_term}")
            
            self.pytrends.build_payload([main_term], timeframe='today 12-m')
            
            # Get related queries
            related_queries = self.pytrends.related_queries()
            
            if main_term in related_queries and related_queries[main_term]['top'] is not None:
                top_related = related_queries[main_term]['top']['query'].tolist()[:10]
                print(f"   🔍 Found {len(top_related)} related queries")
                return top_related
            else:
                print(f"   ⚠️ No related queries found for {main_term}")
                return []
                
        except Exception as e:
            print(f"❌ Related queries error: {e}")
            return []
            
    def analyze_search_seasonality(self, search_terms, profession):
        """Analyze seasonal trends"""
        try:
            print(f"📅 Analyzing seasonality for {profession}...")
            
            # Use top 3 terms for seasonality analysis
            top_terms = search_terms[:3]
            
            self.pytrends.build_payload(
                top_terms,
                timeframe='today 24-m',  # 2 years for seasonality
                geo='US'
            )
            
            interest_data = self.pytrends.interest_over_time()
            
            if not interest_data.empty:
                # Calculate monthly averages
                monthly_data = interest_data.groupby(interest_data.index.month).mean()
                
                # Find peak months
                peak_months = {}
                for term in top_terms:
                    if term in monthly_data.columns:
                        peak_month = monthly_data[term].idxmax()
                        peak_value = monthly_data[term].max()
                        peak_months[term] = {
                            'month': peak_month,
                            'value': peak_value
                        }
                        
                return {
                    'monthly_averages': monthly_data.to_dict(),
                    'peak_months': peak_months,
                    'has_seasonality': len(peak_months) > 0
                }
            else:
                return {'has_seasonality': False}
                
        except Exception as e:
            print(f"❌ Seasonality analysis error: {e}")
            return {'has_seasonality': False, 'error': str(e)}
            
    def get_geographic_interest(self, search_terms, profession):
        """Get geographic distribution of interest"""
        try:
            print(f"🌍 Analyzing geographic interest for {profession}...")
            
            # Use top term for geo analysis
            main_term = search_terms[0]
            
            self.pytrends.build_payload([main_term], timeframe='today 12-m')
            
            # Get interest by region
            geo_data = self.pytrends.interest_by_region(resolution='COUNTRY')
            
            if not geo_data.empty and main_term in geo_data.columns:
                # Get top 10 countries
                top_countries = geo_data[main_term].nlargest(10).to_dict()
                
                return {
                    'top_countries': top_countries,
                    'global_distribution': geo_data[main_term].to_dict()
                }
            else:
                return {'top_countries': {}, 'global_distribution': {}}
                
        except Exception as e:
            print(f"❌ Geographic analysis error: {e}")
            return {'top_countries': {}, 'global_distribution': {}, 'error': str(e)}
            
    def run_comprehensive_real_research(self):
        """Run comprehensive research with REAL data"""
        try:
            print("🔬 COMPREHENSIVE REAL MARKET RESEARCH")
            print("=" * 60)
            print("📊 Using REAL Google Trends API data")
            print("🌍 Global search volume analysis")
            print("📅 Seasonality analysis")
            print("🗺️ Geographic distribution")
            print("=" * 60)
            
            research_results = {}
            
            for profession, search_terms in self.profession_search_terms.items():
                print(f"\n🔍 RESEARCHING: {profession.upper().replace('_', ' ')}")
                print("-" * 50)
                
                # Get real Google Trends data
                trends_data = self.get_real_google_trends_data(search_terms, profession)
                
                # Get related queries for main term
                related_queries = self.get_related_queries(search_terms[0])
                
                # Analyze seasonality
                seasonality_data = self.analyze_search_seasonality(search_terms, profession)
                
                # Get geographic distribution
                geo_data = self.get_geographic_interest(search_terms, profession)
                
                # Calculate pain score based on REAL data
                pain_score = self.calculate_real_pain_score(trends_data, related_queries)
                
                research_results[profession] = {
                    'search_terms': search_terms,
                    'google_trends': trends_data,
                    'related_queries': related_queries,
                    'seasonality': seasonality_data,
                    'geographic_distribution': geo_data,
                    'calculated_pain_score': pain_score,
                    'data_timestamp': datetime.now().isoformat()
                }
                
                print(f"📊 REAL Pain Score: {pain_score:.1f}/100")
                print(f"📈 Total Estimated Searches: {trends_data.get('total_estimated_searches', 0):,.0f}")
                
                # Delay between professions
                time.sleep(3)
                
            return research_results
            
        except Exception as e:
            print(f"❌ Comprehensive research error: {e}")
            return {}
            
    def calculate_real_pain_score(self, trends_data, related_queries):
        """Calculate pain score based on REAL data"""
        try:
            # Base score from search volume
            search_volume = trends_data.get('total_estimated_searches', 0)
            volume_score = min(search_volume / 1000, 50)  # Max 50 points from volume
            
            # Score from average interest
            avg_interest = trends_data.get('total_avg_interest', 0)
            interest_score = min(avg_interest / 2, 30)  # Max 30 points from interest
            
            # Score from related queries (indicates problem complexity)
            related_score = min(len(related_queries) * 2, 20)  # Max 20 points from related queries
            
            total_score = volume_score + interest_score + related_score
            
            return min(total_score, 100)  # Cap at 100
            
        except Exception as e:
            print(f"❌ Pain score calculation error: {e}")
            return 0
            
    def save_real_research_results(self, research_results):
        """Save real research results"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"REAL_market_research_{timestamp}.json"
            
            # Add metadata
            output_data = {
                'research_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'real_google_trends_api',
                    'professions_analyzed': len(research_results),
                    'methodology': 'Real Google Trends API calls with 12-month data',
                    'geographic_scope': 'United States',
                    'time_period': '12 months'
                },
                'results': research_results,
                'ranking': sorted(
                    [(prof, data['calculated_pain_score']) for prof, data in research_results.items()],
                    key=lambda x: x[1],
                    reverse=True
                )
            }
            
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
                
            print(f"\n💾 REAL research results saved to: {filename}")
            
            # Print summary
            print(f"\n📊 REAL RESEARCH SUMMARY:")
            print("=" * 40)
            
            for i, (profession, score) in enumerate(output_data['ranking'], 1):
                searches = research_results[profession]['google_trends'].get('total_estimated_searches', 0)
                print(f"{i:2d}. {profession.replace('_', ' ').title():<20} | {score:5.1f}/100 | {searches:8,.0f} searches")
                
        except Exception as e:
            print(f"❌ Save error: {e}")

def main():
    """Run REAL market research"""
    print("🚀 REAL Market Research with Google Trends API")
    print("=" * 50)
    
    # Check if pytrends is installed
    try:
        import pytrends
        print("✅ pytrends library found")
    except ImportError:
        print("❌ pytrends library not found!")
        print("📦 Install with: pip install pytrends")
        return
        
    researcher = RealMarketResearcher()
    
    # Run real research
    results = researcher.run_comprehensive_real_research()
    
    if results:
        researcher.save_real_research_results(results)
        print("\n🎉 REAL market research complete!")
    else:
        print("❌ Real research failed")

if __name__ == "__main__":
    main()
