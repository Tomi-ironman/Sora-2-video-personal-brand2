#!/usr/bin/env python3
"""
ZENYAI VIRAL MARKETING VIDEO GENERATOR
AI-powered video concepts based on real pain points and viral hooks
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViralMarketingGenerator:
    def __init__(self):
        self.viral_hooks = [
            "POV: You're a music producer and...",
            "This is why 90% of producers fail...",
            "I spent $10,000 learning this the hard way...",
            "Nobody talks about this producer secret...",
            "The one thing Splice doesn't want you to know...",
            "Why your beats sound amateur (it's not what you think)...",
            "I wish someone told me this 5 years ago...",
            "This 30-second trick changed my entire workflow...",
            "Producer reacts to his old beats...",
            "The sample organization method that went viral...",
            "What happens when you have 50,000 unorganized samples...",
            "This AI just organized 10 years of samples in 5 minutes...",
            "Producer discovers his samples have been tagged wrong...",
            "The moment I realized I was wasting 3 hours a day...",
            "This is what 10TB of samples looks like...",
            "When the AI finds the perfect sample before you do...",
            "Producer tries to find ONE sample for 2 hours...",
            "The sample library that broke the internet...",
            "Why famous producers organize samples differently...",
            "This workflow hack saved my music career..."
        ]
        
        self.pain_point_scenarios = {
            "organization": [
                "Producer spends entire session looking for samples",
                "10,000 samples with names like 'untitled_1.wav'",
                "Accidentally deleting organized folder after 3 months of work",
                "Finding the perfect sample but forgetting where you saved it",
                "Having 15 different 'Sample Packs' folders",
                "Downloading same sample pack 3 times because you forgot"
            ],
            "time_waste": [
                "3 hours searching, 30 minutes actually producing",
                "Missing deadline because you couldn't find the right kick",
                "Scrolling through 500 samples to find 'that one sound'",
                "Starting 10 beats but finishing none due to sample chaos",
                "Spending studio time organizing instead of creating",
                "Client waiting while you search for the sample you played yesterday"
            ],
            "workflow_disruption": [
                "Losing creative flow while hunting for samples",
                "Forgetting your idea while searching for sounds",
                "Breaking the vibe to organize mid-session",
                "Collaborator can't find anything in your project",
                "Switching between 5 different sample apps",
                "Creative block caused by decision paralysis from too many options"
            ],
            "metadata_chaos": [
                "Samples with no BPM or key information",
                "Everything labeled 'Loop_1', 'Loop_2', 'Loop_3'",
                "Mixing 140 BPM samples with 70 BPM beats",
                "No genre tags so everything sounds random together",
                "Samples from 2019 mixed with 2024 trends",
                "Vocal samples with no lyrics or language info"
            ]
        }
        
        self.viral_formats = [
            {
                "name": "Before/After Transformation",
                "structure": "Show chaotic sample library → AI organization → clean result",
                "hook_style": "transformation",
                "duration": "15-30 seconds"
            },
            {
                "name": "Producer Reaction",
                "structure": "Producer reacts to AI organizing their samples in real-time",
                "hook_style": "reaction",
                "duration": "30-60 seconds"
            },
            {
                "name": "Time-lapse Challenge",
                "structure": "Finding sample manually vs AI finding it instantly",
                "hook_style": "comparison",
                "duration": "15-30 seconds"
            },
            {
                "name": "POV Storytelling",
                "structure": "POV: You're a producer with 50,000 unorganized samples",
                "hook_style": "pov",
                "duration": "30-45 seconds"
            },
            {
                "name": "Tutorial Hook",
                "structure": "This trick will change your production workflow forever",
                "hook_style": "educational",
                "duration": "45-60 seconds"
            },
            {
                "name": "Emotional Journey",
                "structure": "Frustration → Discovery → Relief → Success",
                "hook_style": "emotional",
                "duration": "30-60 seconds"
            }
        ]
        
        self.visual_metaphors = [
            "Samples floating in digital space getting organized by AI",
            "Messy desk transforming into organized studio",
            "Producer drowning in samples, AI throws life preserver",
            "Sample library as chaotic city, AI as urban planner",
            "Samples as puzzle pieces finding their perfect place",
            "Producer as detective, AI as super-powered assistant",
            "Sample chaos as storm, AI as calm after the storm",
            "Samples as wild animals, AI as gentle trainer",
            "Producer lost in sample maze, AI as GPS guide",
            "Samples as ingredients, AI as master chef organizing kitchen"
        ]
    
    def generate_video_concept(self, pain_point_category: str = None) -> Dict[str, Any]:
        """Generate a viral video concept based on pain points"""
        
        # Select pain point category
        if not pain_point_category:
            pain_point_category = random.choice(list(self.pain_point_scenarios.keys()))
        
        # Select specific scenario
        scenario = random.choice(self.pain_point_scenarios[pain_point_category])
        
        # Select viral hook
        hook = random.choice(self.viral_hooks)
        
        # Select format
        format_info = random.choice(self.viral_formats)
        
        # Select visual metaphor
        visual_metaphor = random.choice(self.visual_metaphors)
        
        # Generate concept
        concept = {
            "id": f"concept_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            "pain_point_category": pain_point_category,
            "scenario": scenario,
            "hook": hook,
            "format": format_info,
            "visual_metaphor": visual_metaphor,
            "target_platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"],
            "estimated_engagement": self.calculate_engagement_potential(pain_point_category, format_info["name"]),
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate detailed prompt
        concept["sora_prompt"] = self.generate_sora_prompt(concept)
        concept["gemini_prompt"] = self.generate_gemini_prompt(concept)
        
        return concept
    
    def generate_sora_prompt(self, concept: Dict[str, Any]) -> str:
        """Generate Sora-optimized video prompt"""
        
        pain_point = concept["pain_point_category"].replace("_", " ")
        scenario = concept["scenario"]
        visual = concept["visual_metaphor"]
        
        prompt = f"""Create a {concept["format"]["duration"]} video showing:

HOOK (First 3 seconds): {concept["hook"]}

VISUAL STORY: {visual}

SCENARIO: {scenario}

STYLE: Cinematic, modern, high-energy with smooth transitions. Use dramatic lighting and dynamic camera movements. Color palette: deep blues and electric greens for tech/AI elements, warm oranges for human/creative elements.

PACING: Fast-paced with quick cuts, synchronized to upbeat electronic music. Build tension in first half, release with satisfying organization reveal.

TEXT OVERLAYS: Bold, modern font with key phrases like "3 HOURS WASTED", "AI ORGANIZES IN 30 SECONDS", "ZENYAI SAVES THE DAY"

ENDING: Clear Zenyai branding with call-to-action "Try Zenyai Free"

Technical specs: 1080x1920 (vertical), 30fps, vibrant colors, professional lighting"""

        return prompt
    
    def generate_gemini_prompt(self, concept: Dict[str, Any]) -> str:
        """Generate Gemini-optimized video prompt"""
        
        pain_point = concept["pain_point_category"].replace("_", " ")
        scenario = concept["scenario"]
        
        prompt = f"""Generate a viral marketing video concept:

CONCEPT: {concept["hook"]} - {scenario}

VIDEO STRUCTURE:
1. HOOK (0-3s): Attention-grabbing opening showing the pain point
2. PROBLEM (3-15s): Demonstrate the frustration and time waste
3. SOLUTION (15-25s): Introduce Zenyai AI organization
4. TRANSFORMATION (25-30s): Show the amazing results
5. CTA (30s): "Try Zenyai Free - Link in Bio"

VISUAL METAPHOR: {concept["visual_metaphor"]}

EMOTIONAL ARC: Frustration → Hope → Satisfaction → Excitement

TARGET AUDIENCE: Music producers, beatmakers, content creators aged 18-35

PLATFORM OPTIMIZATION: {", ".join(concept["target_platforms"])}

ENGAGEMENT HOOKS:
- Relatable pain point that makes viewers say "that's so me"
- Satisfying transformation that provides dopamine hit
- Clear value proposition with immediate benefit
- Strong call-to-action for conversion

MUSIC: Trending audio or original beat that matches the energy

Make it authentic, relatable, and shareable. Focus on the emotional connection with the pain point."""

        return prompt
    
    def calculate_engagement_potential(self, pain_point: str, format_name: str) -> Dict[str, Any]:
        """Calculate estimated engagement potential"""
        
        # Base engagement rates by format
        format_multipliers = {
            "Before/After Transformation": 1.8,
            "Producer Reaction": 1.6,
            "Time-lapse Challenge": 1.4,
            "POV Storytelling": 1.7,
            "Tutorial Hook": 1.3,
            "Emotional Journey": 1.9
        }
        
        # Pain point relevance scores
        pain_relevance = {
            "organization": 0.92,  # Highest pain score
            "time_waste": 0.89,
            "workflow_disruption": 0.85,
            "metadata_chaos": 0.78
        }
        
        base_engagement = 1000  # Base expected views
        multiplier = format_multipliers.get(format_name, 1.0) * pain_relevance.get(pain_point, 0.5)
        
        estimated_views = int(base_engagement * multiplier * random.uniform(0.8, 2.5))
        estimated_likes = int(estimated_views * random.uniform(0.08, 0.15))
        estimated_shares = int(estimated_views * random.uniform(0.02, 0.05))
        estimated_comments = int(estimated_views * random.uniform(0.01, 0.03))
        
        return {
            "estimated_views": estimated_views,
            "estimated_likes": estimated_likes,
            "estimated_shares": estimated_shares,
            "estimated_comments": estimated_comments,
            "engagement_rate": round((estimated_likes + estimated_shares + estimated_comments) / estimated_views * 100, 2),
            "viral_potential": "High" if multiplier > 1.5 else "Medium" if multiplier > 1.0 else "Low"
        }
    
    def generate_multiple_concepts(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple video concepts"""
        concepts = []
        
        # Ensure we cover different pain points
        pain_points = list(self.pain_point_scenarios.keys())
        
        for i in range(count):
            pain_point = pain_points[i % len(pain_points)]
            concept = self.generate_video_concept(pain_point)
            concepts.append(concept)
        
        # Sort by engagement potential
        concepts.sort(key=lambda x: x["estimated_engagement"]["estimated_views"], reverse=True)
        
        return concepts
    
    def regenerate_concept(self, concept_id: str, keep_pain_point: bool = True) -> Dict[str, Any]:
        """Regenerate a concept with new elements"""
        # For now, generate a new concept
        # In a real implementation, you'd store and modify existing concepts
        return self.generate_video_concept()

def main():
    """Test the viral marketing generator"""
    generator = ViralMarketingGenerator()
    
    print("\n" + "="*60)
    print("🎬 VIRAL MARKETING VIDEO GENERATOR")
    print("="*60)
    
    # Generate multiple concepts
    concepts = generator.generate_multiple_concepts(3)
    
    for i, concept in enumerate(concepts, 1):
        print(f"\n📹 CONCEPT {i}: {concept['hook']}")
        print(f"🎯 Pain Point: {concept['pain_point_category'].replace('_', ' ').title()}")
        print(f"📱 Format: {concept['format']['name']}")
        print(f"👀 Est. Views: {concept['estimated_engagement']['estimated_views']:,}")
        print(f"🔥 Viral Potential: {concept['estimated_engagement']['viral_potential']}")
        print(f"🎨 Visual: {concept['visual_metaphor']}")
        print(f"⏱️ Duration: {concept['format']['duration']}")
        print(f"📊 Engagement Rate: {concept['estimated_engagement']['engagement_rate']}%")
        
    print("\n" + "="*60)
    print("🚀 Ready to generate viral marketing videos!")
    print("="*60)

if __name__ == "__main__":
    main()
