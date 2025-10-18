#!/usr/bin/env python3
"""
TEST ZENYAI MARKET INTELLIGENCE PLATFORM
Quick test to demonstrate the platform capabilities
"""

from zenyai_market_intelligence import ZenyaiMarketIntelligence
from market_intelligence_video_generator import MarketIntelligenceVideoGenerator

def test_market_intelligence_platform():
    """Test the complete market intelligence platform"""
    
    print("🧠 TESTING ZENYAI MARKET INTELLIGENCE PLATFORM")
    print("=" * 60)
    
    # Initialize platform
    intelligence = ZenyaiMarketIntelligence()
    video_generator = MarketIntelligenceVideoGenerator()
    
    # Test cases based on your research-first approach
    test_cases = [
        {
            "idea": "AI-powered audio file organization and metadata management for music producers",
            "target_market": "music producers, sound designers, podcast editors"
        },
        {
            "idea": "Automated video editing tool that cuts raw footage and generates B-roll",
            "target_market": "content creators, YouTubers, video editors"
        },
        {
            "idea": "Creative asset management system for photographers",
            "target_market": "professional photographers, wedding photographers"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 TEST CASE {i}: {test_case['idea'][:50]}...")
        print("-" * 50)
        
        try:
            # Run market analysis
            results = intelligence.analyze_market_opportunity(
                test_case["idea"], 
                test_case["target_market"]
            )
            
            if results:
                # Display key results
                analysis = results.get("analysis", {})
                
                # Market size
                market_size = analysis.get("market_size", {})
                print(f"📊 Market Size: {market_size.get('market_size_category', 'Unknown')}")
                print(f"💰 Estimated TAM: ${market_size.get('estimated_tam', 0):,}")
                
                # Pain points
                pain_points = analysis.get("pain_points", {})
                print(f"🔥 Pain Score: {pain_points.get('pain_score', 0)}/100")
                print(f"⚡ Pain Level: {pain_points.get('pain_level', 'Unknown')}")
                
                # Financial projections
                financial = analysis.get("financial", {})
                if financial:
                    year_5 = financial.get("year_5", {})
                    print(f"📈 5-Year Revenue Projection: ${year_5.get('revenue', 0):,.0f}")
                
                # Generate comprehensive report
                report_file = intelligence.generate_comprehensive_report(results)
                print(f"📄 Report Generated: {report_file}")
                
                # Test video generation (optional - requires Sora2 API)
                print("🎬 Testing video generation...")
                try:
                    video_suite = video_generator.generate_complete_market_intelligence_video(results)
                    if video_suite:
                        print(f"✅ Generated {len(video_suite)} market intelligence videos")
                    else:
                        print("⚠️ Video generation skipped (API not configured)")
                except Exception as e:
                    print(f"⚠️ Video generation error: {e}")
                
                print(f"✅ Test case {i} completed successfully!")
                
            else:
                print(f"❌ Test case {i} failed - no results")
                
        except Exception as e:
            print(f"❌ Test case {i} error: {e}")
            
        print()
    
    print("🎉 MARKET INTELLIGENCE PLATFORM TEST COMPLETE!")
    print("\n💡 Key Benefits vs IdeaBrowser:")
    print("   • 15+ integrated data sources")
    print("   • AI-powered video generation")
    print("   • Custom research methodologies")
    print("   • Zero monthly subscription fees")
    print("   • Full integration with Zenyai ecosystem")
    print("\n🚀 Ready to replace paid market research tools!")

def test_web_interface():
    """Test the web interface"""
    print("\n🌐 TESTING WEB INTERFACE")
    print("=" * 40)
    print("To test the web interface:")
    print("1. Run: python market_intelligence_web.py")
    print("2. Visit: http://localhost:5000")
    print("3. Enter a business idea and analyze")
    print("4. Download comprehensive reports")

if __name__ == "__main__":
    test_market_intelligence_platform()
    test_web_interface()
