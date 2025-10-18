#!/usr/bin/env python3
"""
REAL COMPETITOR INTELLIGENCE SYSTEM
Tracks actual competitor data from multiple sources with real scraping
"""

import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import urljoin, urlparse
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompetitorIntelligence:
    def __init__(self):
        self.competitors = self._load_competitor_database()
        self.cache = {}
        self.cache_duration = timedelta(hours=6)
        
    def _load_competitor_database(self) -> Dict[str, Any]:
        """Load structured competitor database"""
        return {
            # AI Audio Tools
            "descript": {
                "name": "Descript",
                "category": "AI Audio Editing",
                "url": "https://www.descript.com",
                "domain_focus": ["Podcasting", "Video Editing", "Transcription"],
                "funding": "$100M+ (Series C)",
                "founded": 2017,
                "employees": "100-250",
                "pricing_known": True,
                "linkedin": "descript",
                "twitter": "DescriptApp",
                "product_hunt": "descript"
            },
            "riverside": {
                "name": "Riverside.fm",
                "category": "Podcast Recording",
                "url": "https://riverside.fm",
                "domain_focus": ["Podcasting", "Remote Recording", "Video"],
                "funding": "$40M+ (Series B)",
                "founded": 2019,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "riverside-fm",
                "twitter": "riverside_fm",
                "product_hunt": "riverside-fm"
            },
            "splice": {
                "name": "Splice",
                "category": "Sample Library",
                "url": "https://splice.com",
                "domain_focus": ["Samples", "Plugins", "Collaboration"],
                "funding": "$110M+ (Series C)",
                "founded": 2013,
                "employees": "100-250",
                "pricing_known": True,
                "linkedin": "splice",
                "twitter": "splice",
                "product_hunt": "splice"
            },
            "landr": {
                "name": "LANDR",
                "category": "AI Mastering",
                "url": "https://www.landr.com",
                "domain_focus": ["Mastering", "Distribution", "Plugins"],
                "funding": "$30M+",
                "founded": 2014,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "landr",
                "twitter": "landr",
                "product_hunt": "landr"
            },
            "soundtrap": {
                "name": "Soundtrap",
                "category": "Cloud DAW",
                "url": "https://www.soundtrap.com",
                "domain_focus": ["Cloud DAW", "Education", "Collaboration"],
                "funding": "Acquired by Spotify",
                "founded": 2012,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "soundtrap",
                "twitter": "soundtrap",
                "product_hunt": "soundtrap"
            },
            "auphonic": {
                "name": "Auphonic",
                "category": "Audio Post-Production",
                "url": "https://auphonic.com",
                "domain_focus": ["Podcasting", "Audio Processing", "Automation"],
                "funding": "Bootstrapped",
                "founded": 2011,
                "employees": "10-50",
                "pricing_known": True,
                "linkedin": "auphonic",
                "twitter": "auphonic",
                "product_hunt": "auphonic"
            },
            "cleanfeed": {
                "name": "Cleanfeed",
                "category": "Remote Recording",
                "url": "https://cleanfeed.net",
                "domain_focus": ["Broadcasting", "Remote Recording", "Live Audio"],
                "funding": "Bootstrapped",
                "founded": 2015,
                "employees": "10-50",
                "pricing_known": True,
                "linkedin": "cleanfeed",
                "twitter": "cleanfeed",
                "product_hunt": "cleanfeed"
            },
            "izotope": {
                "name": "iZotope",
                "category": "Audio Plugins",
                "url": "https://www.izotope.com",
                "domain_focus": ["Audio Repair", "Mastering", "Mixing"],
                "funding": "Acquired by Native Instruments",
                "founded": 2001,
                "employees": "100-250",
                "pricing_known": True,
                "linkedin": "izotope",
                "twitter": "iZotope",
                "product_hunt": "izotope"
            },
            "wavve": {
                "name": "Wavve",
                "category": "Audio to Video",
                "url": "https://wavve.co",
                "domain_focus": ["Social Media", "Audiograms", "Marketing"],
                "funding": "Bootstrapped",
                "founded": 2017,
                "employees": "10-50",
                "pricing_known": True,
                "linkedin": "wavve",
                "twitter": "wavve",
                "product_hunt": "wavve"
            },
            "headliner": {
                "name": "Headliner",
                "category": "Audio to Video",
                "url": "https://www.headliner.app",
                "domain_focus": ["Audiograms", "Social Media", "Podcasting"],
                "funding": "Acquired by Podomatic",
                "founded": 2016,
                "employees": "10-50",
                "pricing_known": True,
                "linkedin": "headliner-app",
                "twitter": "headlinerapp",
                "product_hunt": "headliner"
            },
            "sonix": {
                "name": "Sonix",
                "category": "Transcription",
                "url": "https://sonix.ai",
                "domain_focus": ["Transcription", "Subtitles", "AI"],
                "funding": "$15M+",
                "founded": 2017,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "sonix-ai",
                "twitter": "sonix_ai",
                "product_hunt": "sonix"
            },
            "otter": {
                "name": "Otter.ai",
                "category": "AI Transcription",
                "url": "https://otter.ai",
                "domain_focus": ["Transcription", "Meetings", "Collaboration"],
                "funding": "$63M+ (Series B)",
                "founded": 2016,
                "employees": "100-250",
                "pricing_known": True,
                "linkedin": "otter-ai",
                "twitter": "otter_ai",
                "product_hunt": "otter-ai"
            },
            "resemble": {
                "name": "Resemble AI",
                "category": "Voice Cloning",
                "url": "https://www.resemble.ai",
                "domain_focus": ["Voice Synthesis", "AI", "Text-to-Speech"],
                "funding": "$8M+ (Series A)",
                "founded": 2019,
                "employees": "10-50",
                "pricing_known": True,
                "linkedin": "resemble-ai",
                "twitter": "resembleai",
                "product_hunt": "resemble-ai"
            },
            "murf": {
                "name": "Murf AI",
                "category": "AI Voice Generator",
                "url": "https://murf.ai",
                "domain_focus": ["Text-to-Speech", "Voiceovers", "AI"],
                "funding": "$10M+ (Series A)",
                "founded": 2020,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "murf-ai",
                "twitter": "murf_ai",
                "product_hunt": "murf-ai"
            },
            "podcastle": {
                "name": "Podcastle",
                "category": "Podcast Studio",
                "url": "https://podcastle.ai",
                "domain_focus": ["Podcasting", "Recording", "Editing"],
                "funding": "$13.5M (Series A)",
                "founded": 2020,
                "employees": "50-100",
                "pricing_known": True,
                "linkedin": "podcastle",
                "twitter": "podcastle_ai",
                "product_hunt": "podcastle"
            }
        }
    
    def scrape_competitor_website(self, competitor_key: str) -> Dict[str, Any]:
        """Scrape real data from competitor website"""
        competitor = self.competitors.get(competitor_key)
        if not competitor:
            return {"error": "Competitor not found"}
        
        # Check cache
        cache_key = f"website_{competitor_key}"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                logger.info(f"Using cached data for {competitor['name']}")
                return cached_data
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(competitor['url'], headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract pricing information
            pricing_info = self._extract_pricing(soup)
            
            # Extract features
            features = self._extract_features(soup)
            
            # Extract recent updates
            updates = self._extract_updates(soup, competitor['url'])
            
            # Extract meta information
            meta_description = soup.find('meta', {'name': 'description'})
            description = meta_description['content'] if meta_description else ""
            
            # Count specific keywords
            page_text = soup.get_text().lower()
            ai_mentions = page_text.count('ai') + page_text.count('artificial intelligence')
            
            result = {
                "competitor": competitor['name'],
                "category": competitor['category'],
                "url": competitor['url'],
                "scraped_at": datetime.now().isoformat(),
                "pricing": pricing_info,
                "features": features,
                "recent_updates": updates,
                "description": description[:200],
                "ai_mentions": ai_mentions,
                "page_size_kb": len(response.text) / 1024,
                "status": "active",
                "confidence": 90
            }
            
            # Cache the result
            self.cache[cache_key] = (result, datetime.now())
            
            return result
            
        except Exception as e:
            logger.error(f"Error scraping {competitor['name']}: {str(e)}")
            return {
                "competitor": competitor['name'],
                "error": str(e),
                "status": "error",
                "confidence": 0
            }
    
    def _extract_pricing(self, soup: BeautifulSoup) -> List[str]:
        """Extract pricing information from page"""
        pricing = []
        
        # Look for common pricing patterns
        price_patterns = [
            r'\$\d+(?:\.\d{2})?(?:/mo|/month|/year)?',
            r'€\d+(?:\.\d{2})?(?:/mo|/month|/year)?',
            r'£\d+(?:\.\d{2})?(?:/mo|/month|/year)?'
        ]
        
        text = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text)
            pricing.extend(matches[:5])  # Limit to 5 prices
        
        # Look for pricing keywords
        pricing_sections = soup.find_all(['div', 'section'], class_=re.compile(r'pric', re.I))
        for section in pricing_sections[:3]:
            text = section.get_text(strip=True)
            if len(text) < 200:
                pricing.append(text[:100])
        
        return list(set(pricing))[:5]
    
    def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        """Extract feature mentions from page"""
        features = []
        
        # Common audio/AI feature keywords
        feature_keywords = [
            'AI', 'transcription', 'editing', 'collaboration', 'cloud',
            'recording', 'mastering', 'mixing', 'organization', 'library',
            'search', 'tagging', 'metadata', 'automation', 'workflow'
        ]
        
        text = soup.get_text().lower()
        for keyword in feature_keywords:
            if keyword.lower() in text:
                features.append(keyword)
        
        # Look for feature lists
        feature_lists = soup.find_all(['ul', 'ol'], class_=re.compile(r'feature', re.I))
        for feature_list in feature_lists[:2]:
            items = feature_list.find_all('li')
            for item in items[:5]:
                feature_text = item.get_text(strip=True)
                if len(feature_text) < 100:
                    features.append(feature_text)
        
        return list(set(features))[:10]
    
    def _extract_updates(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract recent updates/blog posts"""
        updates = []
        
        # Look for blog/news links
        blog_links = soup.find_all('a', href=re.compile(r'blog|news|update|changelog', re.I))
        
        for link in blog_links[:5]:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            if href and title and len(title) > 10:
                full_url = urljoin(base_url, href)
                updates.append({
                    "title": title[:100],
                    "url": full_url,
                    "detected_at": datetime.now().isoformat()
                })
        
        return updates[:3]
    
    def get_linkedin_data(self, competitor_key: str) -> Dict[str, Any]:
        """Get LinkedIn company data (employee count, growth)"""
        competitor = self.competitors.get(competitor_key)
        if not competitor:
            return {"error": "Competitor not found"}
        
        # For now, return structured data based on known info
        # In production, integrate with LinkedIn API or scraping
        
        employee_ranges = {
            "10-50": 30,
            "50-100": 75,
            "100-250": 175,
            "250-500": 375
        }
        
        estimated_employees = employee_ranges.get(competitor.get('employees', '50-100'), 75)
        
        return {
            "company": competitor['name'],
            "linkedin_url": f"https://linkedin.com/company/{competitor.get('linkedin', '')}",
            "estimated_employees": estimated_employees,
            "employee_range": competitor.get('employees', 'Unknown'),
            "growth_indicators": {
                "hiring_posts": "Check LinkedIn directly",
                "recent_hires": "Requires LinkedIn API",
                "job_openings": "Check careers page"
            },
            "confidence": 70,
            "note": "For real-time data, integrate LinkedIn API"
        }
    
    def get_crunchbase_data(self, competitor_key: str) -> Dict[str, Any]:
        """Get funding and company data"""
        competitor = self.competitors.get(competitor_key)
        if not competitor:
            return {"error": "Competitor not found"}
        
        return {
            "company": competitor['name'],
            "funding": competitor.get('funding', 'Unknown'),
            "founded": competitor.get('founded', 'Unknown'),
            "category": competitor['category'],
            "domain_focus": competitor['domain_focus'],
            "crunchbase_url": f"https://www.crunchbase.com/organization/{competitor_key}",
            "confidence": 85,
            "note": "For real-time funding data, integrate Crunchbase API"
        }
    
    def get_product_hunt_data(self, competitor_key: str) -> Dict[str, Any]:
        """Get Product Hunt launch and engagement data"""
        competitor = self.competitors.get(competitor_key)
        if not competitor:
            return {"error": "Competitor not found"}
        
        # Try to scrape Product Hunt page
        try:
            ph_slug = competitor.get('product_hunt', competitor_key)
            url = f"https://www.producthunt.com/products/{ph_slug}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract upvotes (look for numbers in specific patterns)
                page_text = soup.get_text()
                upvote_match = re.search(r'(\d+)\s*upvote', page_text, re.I)
                upvotes = int(upvote_match.group(1)) if upvote_match else 0
                
                return {
                    "company": competitor['name'],
                    "product_hunt_url": url,
                    "estimated_upvotes": upvotes,
                    "status": "found",
                    "confidence": 75
                }
            else:
                return {
                    "company": competitor['name'],
                    "product_hunt_url": url,
                    "status": "not_found",
                    "confidence": 30
                }
                
        except Exception as e:
            logger.error(f"Error fetching Product Hunt data: {str(e)}")
            return {
                "company": competitor['name'],
                "error": str(e),
                "confidence": 0
            }
    
    def analyze_competitor_activity(self, competitor_key: str) -> Dict[str, Any]:
        """Comprehensive competitor analysis"""
        
        logger.info(f"Analyzing competitor: {competitor_key}")
        
        # Gather all data
        website_data = self.scrape_competitor_website(competitor_key)
        linkedin_data = self.get_linkedin_data(competitor_key)
        funding_data = self.get_crunchbase_data(competitor_key)
        ph_data = self.get_product_hunt_data(competitor_key)
        
        # Calculate activity score
        activity_score = self._calculate_activity_score(website_data, linkedin_data, ph_data)
        
        # Generate summary
        summary = self._generate_summary(competitor_key, website_data, funding_data)
        
        return {
            "competitor": self.competitors[competitor_key]['name'],
            "category": self.competitors[competitor_key]['category'],
            "activity_score": activity_score,
            "website_analysis": website_data,
            "linkedin_analysis": linkedin_data,
            "funding_analysis": funding_data,
            "product_hunt_analysis": ph_data,
            "summary": summary,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _calculate_activity_score(self, website_data: Dict, linkedin_data: Dict, ph_data: Dict) -> int:
        """Calculate overall activity score (0-100)"""
        score = 50  # Base score
        
        # Website activity
        if website_data.get('recent_updates'):
            score += 15
        if website_data.get('ai_mentions', 0) > 10:
            score += 10
        
        # LinkedIn activity
        if linkedin_data.get('estimated_employees', 0) > 100:
            score += 10
        
        # Product Hunt presence
        if ph_data.get('estimated_upvotes', 0) > 500:
            score += 15
        
        return min(score, 100)
    
    def _generate_summary(self, competitor_key: str, website_data: Dict, funding_data: Dict) -> str:
        """Generate AI-style summary"""
        competitor = self.competitors[competitor_key]
        
        summary_parts = []
        
        # Company intro
        summary_parts.append(f"{competitor['name']} is a {competitor['category']} company")
        
        # Funding
        if funding_data.get('funding'):
            summary_parts.append(f"with {funding_data['funding']} in funding")
        
        # Features
        if website_data.get('features'):
            top_features = website_data['features'][:3]
            summary_parts.append(f"focusing on {', '.join(top_features)}")
        
        # Recent activity
        if website_data.get('recent_updates'):
            summary_parts.append(f"Recently active with {len(website_data['recent_updates'])} updates detected")
        
        return ". ".join(summary_parts) + "."
    
    def get_all_competitors_overview(self) -> Dict[str, Any]:
        """Get overview of all competitors"""
        
        overview = {
            "total_competitors": len(self.competitors),
            "categories": {},
            "by_funding": {},
            "by_size": {},
            "competitors": []
        }
        
        # Categorize
        for key, comp in self.competitors.items():
            category = comp['category']
            overview['categories'][category] = overview['categories'].get(category, 0) + 1
            
            # Add to list
            overview['competitors'].append({
                "key": key,
                "name": comp['name'],
                "category": category,
                "url": comp['url'],
                "funding": comp.get('funding', 'Unknown'),
                "employees": comp.get('employees', 'Unknown')
            })
        
        return overview
    
    def rank_competitors(self, criteria: str = 'activity') -> List[Dict[str, Any]]:
        """Rank competitors by various criteria"""
        
        rankings = []
        
        for key in list(self.competitors.keys())[:5]:  # Limit to 5 for demo
            analysis = self.analyze_competitor_activity(key)
            rankings.append({
                "rank": 0,  # Will be set after sorting
                "competitor": analysis['competitor'],
                "category": analysis['category'],
                "activity_score": analysis['activity_score'],
                "summary": analysis['summary']
            })
            
            # Rate limiting
            time.sleep(2)
        
        # Sort by activity score
        rankings.sort(key=lambda x: x['activity_score'], reverse=True)
        
        # Assign ranks
        for i, item in enumerate(rankings):
            item['rank'] = i + 1
        
        return rankings


if __name__ == "__main__":
    # Test the system
    intel = CompetitorIntelligence()
    
    print("🔍 Testing Competitor Intelligence System\n")
    
    # Test single competitor
    print("📊 Analyzing Descript...")
    result = intel.analyze_competitor_activity('descript')
    print(json.dumps(result, indent=2))
    
    print("\n📈 Getting all competitors overview...")
    overview = intel.get_all_competitors_overview()
    print(f"Total competitors tracked: {overview['total_competitors']}")
    print(f"Categories: {list(overview['categories'].keys())}")
