#!/usr/bin/env python3
"""
MARKET INTELLIGENCE VIDEO GENERATOR
Generate videos and images for market research insights
"""

import os
import json
from datetime import datetime
from sora2_direct_api import Sora2DirectAPI

class MarketIntelligenceVideoGenerator:
    def __init__(self):
        self.sora_api = Sora2DirectAPI()
        
    def generate_market_opportunity_video(self, analysis_results):
        """Generate video showcasing market opportunity"""
        try:
            idea = analysis_results.get('idea_description', 'Business Idea')
            opportunity_rating = analysis_results.get('analysis', {}).get('executive_summary', {}).get('opportunity_rating', 'Unknown')
            
            # Create compelling video prompt based on analysis
            if 'EXCELLENT' in opportunity_rating:
                video_prompt = f"""
                Cinematic shot of a golden sunrise over a vast digital landscape representing unlimited market potential. 
                Text overlay: "{idea}" appears in elegant typography. 
                Camera slowly zooms through floating data visualizations, charts trending upward, and glowing opportunity indicators. 
                Professional, inspiring, high-tech aesthetic with purple and blue color scheme matching Zenyai branding.
                8 seconds, 4K quality, smooth camera movements.
                """
            elif 'GOOD' in opportunity_rating:
                video_prompt = f"""
                Dynamic shot of a modern city skyline at dawn with digital overlays showing market data and growth charts.
                Text: "{idea}" appears with professional animation.
                Camera moves through holographic market indicators and positive trend lines.
                Clean, professional look with blue and purple gradients.
                8 seconds, cinematic quality.
                """
            else:
                video_prompt = f"""
                Steady shot of a professional office environment with subtle market research elements.
                Text: "{idea}" displayed cleanly.
                Gentle camera movement revealing charts and data visualizations.
                Professional, measured tone with neutral color palette.
                8 seconds, high quality.
                """
                
            # Generate video
            video_result = self.sora_api.generate_video(
                prompt=video_prompt,
                duration=8,
                aspect_ratio="16:9"
            )
            
            return video_result
            
        except Exception as e:
            print(f"❌ Video generation error: {e}")
            return None
            
    def generate_pain_point_visualization(self, pain_analysis):
        """Generate video visualizing pain points"""
        try:
            pain_score = pain_analysis.get('pain_score', 0)
            pain_level = pain_analysis.get('pain_level', 'Unknown')
            
            if pain_score >= 80:
                # High pain = dramatic visualization
                video_prompt = """
                Dramatic cinematic shot of a person drowning in an ocean of scattered digital files and documents.
                The person reaches desperately toward the surface where a bright light (representing the solution) shines down.
                Dark, moody underwater cinematography with rays of hope breaking through.
                Metaphorical representation of overwhelming digital chaos and the need for organization.
                8 seconds, cinematic quality, emotional impact.
                """
            elif pain_score >= 60:
                # Medium pain = cluttered workspace
                video_prompt = """
                Time-lapse shot of a creative professional's workspace becoming increasingly cluttered with files, papers, and digital chaos.
                Camera slowly pulls back to reveal the overwhelming mess, then cuts to a clean, organized workspace.
                Professional lighting, clean aesthetic, showing before/after transformation.
                8 seconds, high quality.
                """
            else:
                # Low pain = subtle challenges
                video_prompt = """
                Gentle shot of a professional working at a clean desk, occasionally pausing to search through organized files.
                Subtle indication of minor workflow inefficiencies.
                Bright, professional environment with soft lighting.
                8 seconds, clean aesthetic.
                """
                
            video_result = self.sora_api.generate_video(
                prompt=video_prompt,
                duration=8,
                aspect_ratio="16:9"
            )
            
            return video_result
            
        except Exception as e:
            print(f"❌ Pain visualization error: {e}")
            return None
            
    def generate_financial_projection_video(self, financial_data):
        """Generate video showing financial projections"""
        try:
            year_5_revenue = financial_data.get('year_5', {}).get('revenue', 0)
            
            video_prompt = f"""
            Sleek 3D animation of financial charts and graphs growing upward over time.
            Camera moves through floating holographic revenue projections and market data.
            Professional blue and purple color scheme with golden accents for growth indicators.
            Text overlays showing key financial milestones: Year 1, Year 3, Year 5.
            Modern, high-tech aesthetic with smooth transitions and professional typography.
            8 seconds, 4K quality, corporate presentation style.
            """
            
            video_result = self.sora_api.generate_video(
                prompt=video_prompt,
                duration=8,
                aspect_ratio="16:9"
            )
            
            return video_result
            
        except Exception as e:
            print(f"❌ Financial video error: {e}")
            return None
            
    def generate_competitor_analysis_video(self, competitor_data):
        """Generate video showing competitive landscape"""
        try:
            video_prompt = """
            Bird's eye view of a strategic game board with chess pieces representing different companies.
            Camera slowly moves across the board showing competitive positioning.
            Some pieces glow with opportunity light while others cast shadows.
            Professional, strategic atmosphere with dark background and dramatic lighting.
            Represents competitive analysis and market positioning.
            8 seconds, cinematic quality, strategic theme.
            """
            
            video_result = self.sora_api.generate_video(
                prompt=video_prompt,
                duration=8,
                aspect_ratio="16:9"
            )
            
            return video_result
            
        except Exception as e:
            print(f"❌ Competitor video error: {e}")
            return None
            
    def generate_complete_market_intelligence_video(self, analysis_results):
        """Generate comprehensive market intelligence video"""
        try:
            print("🎬 Generating Market Intelligence Video Suite...")
            
            video_suite = {}
            
            # Market Opportunity Video
            print("📊 Creating market opportunity video...")
            video_suite['market_opportunity'] = self.generate_market_opportunity_video(analysis_results)
            
            # Pain Point Visualization
            if 'pain_points' in analysis_results.get('analysis', {}):
                print("💥 Creating pain point visualization...")
                video_suite['pain_points'] = self.generate_pain_point_visualization(
                    analysis_results['analysis']['pain_points']
                )
                
            # Financial Projections
            if 'financial' in analysis_results.get('analysis', {}):
                print("💰 Creating financial projections video...")
                video_suite['financial'] = self.generate_financial_projection_video(
                    analysis_results['analysis']['financial']
                )
                
            # Competitor Analysis
            if 'competitors' in analysis_results.get('analysis', {}):
                print("🏢 Creating competitor analysis video...")
                video_suite['competitors'] = self.generate_competitor_analysis_video(
                    analysis_results['analysis']['competitors']
                )
                
            # Save video suite metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            metadata_file = f"market_intelligence_videos_{timestamp}.json"
            
            with open(metadata_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'idea': analysis_results.get('idea_description'),
                    'videos_generated': list(video_suite.keys()),
                    'video_details': video_suite
                }, f, indent=2)
                
            print(f"🎉 Video suite generated! Metadata saved: {metadata_file}")
            return video_suite
            
        except Exception as e:
            print(f"❌ Video suite generation error: {e}")
            return {}
            
    def create_market_research_presentation(self, analysis_results):
        """Create a complete video presentation of market research"""
        try:
            idea = analysis_results.get('idea_description', 'Business Idea')
            
            presentation_prompt = f"""
            Professional business presentation style video showcasing market research results.
            
            Scene 1 (0-2s): Title slide with "{idea}" in elegant typography over a clean, modern background
            Scene 2 (2-4s): Market size visualization with growing charts and positive indicators  
            Scene 3 (4-6s): Pain point analysis with visual metaphors of problems being solved
            Scene 4 (6-8s): Financial projections with upward trending graphs and success indicators
            
            Consistent professional branding throughout with Zenyai purple/blue color scheme.
            Clean, corporate presentation aesthetic with smooth transitions.
            8 seconds total, 4K quality, presentation style.
            """
            
            presentation_video = self.sora_api.generate_video(
                prompt=presentation_prompt,
                duration=8,
                aspect_ratio="16:9"
            )
            
            return presentation_video
            
        except Exception as e:
            print(f"❌ Presentation creation error: {e}")
            return None

def main():
    """Test market intelligence video generation"""
    
    # Sample analysis results
    sample_analysis = {
        'idea_description': 'AI-powered audio file organization for music producers',
        'analysis': {
            'executive_summary': {
                'opportunity_rating': '🔥 EXCELLENT OPPORTUNITY'
            },
            'pain_points': {
                'pain_score': 85,
                'pain_level': 'Extreme Pain - High Opportunity'
            },
            'financial': {
                'year_5': {'revenue': 5000000}
            },
            'competitors': {}
        }
    }
    
    # Generate videos
    generator = MarketIntelligenceVideoGenerator()
    video_suite = generator.generate_complete_market_intelligence_video(sample_analysis)
    
    if video_suite:
        print("✅ Market intelligence videos generated successfully!")
        for video_type, video_data in video_suite.items():
            if video_data:
                print(f"   📹 {video_type}: Generated")
            else:
                print(f"   ❌ {video_type}: Failed")
    else:
        print("❌ Video generation failed")

if __name__ == "__main__":
    main()
