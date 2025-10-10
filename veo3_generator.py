#!/usr/bin/env python3
"""
Google Veo 3 Video Generator
Generate hyper-realistic videos with native audio using Google's Veo 3 model for personal brand content.
"""

import os
import tempfile
import sys
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import base64
from rich.console import Console
from rich.prompt import Prompt
from voice_clone import synthesize_voice, replace_video_audio
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

# Load environment variables
load_dotenv()

console = Console()

class Veo3VideoGenerator:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            console.print("[red]Error: GOOGLE_AI_API_KEY not found in .env file[/red]")
            console.print("[dim]Get your API key from: https://aistudio.google.com/app/apikey[/dim]")
            sys.exit(1)
        
        self.client = genai.Client(api_key=self.api_key)
        
        # Setup directories
        self.output_dir = Path.home() / "Desktop" / "AI-video-Generation"
        self.output_dir.mkdir(exist_ok=True)
        
        # Reference images are in the project's "Reference Character" folder
        self.reference_dir = Path(__file__).parent / "Reference Character"
    
    def generate_video(self, prompt, aspect_ratio="9:16", resolution="1080p", negative_prompt=None, reference_image=None, use_character_consistency=True):
        """Generate a video using Google Veo 3 with optional character consistency"""
        console.print(f"\n[cyan]🎬 Generating video with Google Veo 3...[/cyan]")
        console.print(f"[dim]Prompt: {prompt}[/dim]")
        console.print(f"[dim]Settings: {aspect_ratio}, {resolution}[/dim]")
        if negative_prompt:
            console.print(f"[dim]Negative prompt: {negative_prompt}[/dim]")
        
        # Auto-add character consistency for regular videos if no reference image provided
        if use_character_consistency and not reference_image:
            reference_image_path = self.get_best_reference_image()
            if reference_image_path:
                console.print(f"[cyan]🎯 Adding character consistency with: {reference_image_path.name}[/cyan]")
                reference_image = self.load_reference_image(reference_image_path)
                
                # Enhance prompt with character AND environment details
                character_desc = self.get_character_description()
                environment_desc = self.get_professional_environment_description()
                prompt = f"""
                {prompt}
                
                CHARACTER CONSISTENCY REQUIRED:
                {character_desc.strip()}
                
                PROFESSIONAL ENVIRONMENT CONSISTENCY REQUIRED:
                {environment_desc.strip()}
                
                Ensure the person in the video matches the reference image exactly and is in the professional studio environment.
                """
        
        console.print()
        
        # Single attempt only - no retry logic
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Starting video generation...", total=None)
                
                # Generate video with Veo 3
                config = types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                    resolution=resolution,
                )
                
                if negative_prompt:
                    config.negative_prompt = negative_prompt
                
                # Prepare generation parameters
                generation_params = {
                    "model": "veo-3.0-generate-001",
                    "prompt": prompt,
                    "config": config,
                }
                
                # Add reference image if provided
                if reference_image:
                    console.print(f"[cyan]📸 Using reference image for character consistency[/cyan]")
                    generation_params["image"] = reference_image
                
                operation = self.client.models.generate_videos(**generation_params)
                
                progress.update(task, description="Video generation in progress...")
                
                # Poll the operation status until the video is ready
                while not operation.done:
                    progress.update(task, description="Generating video... (this may take several minutes)")
                    time.sleep(10)
                    operation = self.client.operations.get(operation)
                
                progress.update(task, description="Video generated! Downloading...")
                
                # Download the generated video
                generated_video = operation.response.generated_videos[0]
                
                # Create filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')
                filename = f"veo3_{timestamp}_{safe_prompt}.mp4"
                filepath = self.output_dir / filename
                
                # Download and save the video
                self.client.files.download(file=generated_video.video)
                generated_video.video.save(str(filepath))
                progress.update(task, description="Complete!")
        
            console.print(f"[green]✅ Video saved: {filename}[/green]")
            console.print(f"[cyan]📁 Location: ~/Desktop/AI-video-Generation/[/cyan]")
            console.print(f"[cyan]🎵 Native audio included![/cyan]")
            return filepath
                    
        except Exception as e:
            err = str(e)
            console.print(f"[red]❌ Error generating video: {err}[/red]")
            
            # Check for common issues but don't retry
            if "billing" in err.lower() or "quota" in err.lower():
                console.print("[yellow]💡 Tip: Make sure you have billing enabled and sufficient quota[/yellow]")
            elif "permission" in err.lower() or "access" in err.lower():
                console.print("[yellow]💡 Tip: Veo 3 requires paid tier access[/yellow]")
            elif "429" in err or "RESOURCE_EXHAUSTED" in err:
                console.print("[yellow]💡 Rate limit hit - service may be experiencing issues[/yellow]")
            
            return None
    
    def load_reference_image(self, image_path):
        """Load and prepare reference image for character consistency"""
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                console.print(f"[red]❌ Image not found: {image_path}[/red]")
                return None
            
            # Load image in correct format for Google AI API
            import mimetypes
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(image_path))
            if not mime_type:
                if str(image_path).lower().endswith(('.jpg', '.jpeg')):
                    mime_type = "image/jpeg"
                elif str(image_path).lower().endswith('.png'):
                    mime_type = "image/png"
                else:
                    mime_type = "image/jpeg"  # Default fallback
            
            # Read image bytes
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Create proper image object for Veo 3 API
            image_obj = {
                "imageBytes": image_bytes,
                "mimeType": mime_type
            }
            
            console.print(f"[green]✅ Reference image loaded: {image_path.name} ({mime_type})[/green]")
            return image_obj
            
        except Exception as e:
            console.print(f"[red]❌ Error loading reference image: {str(e)}[/red]")
            return None

    def load_reference_images(self, filenames):
        """Load multiple reference images from `self.reference_dir` by filename list.
        Returns list of {imageBytes, mimeType} dicts, preserving order of `filenames` that exist.
        """
        loaded = []
        for name in filenames:
            path = self.reference_dir / name
            img = self.load_reference_image(path)
            if img:
                loaded.append((name, img))
            else:
                console.print(f"[yellow]⚠️ Skipped missing or invalid reference: {name}[/yellow]")
        return loaded
    
    def get_character_description(self):
        """Get highly detailed character description for maximum consistency"""
        return """
        EXACT SPECIFIC CHARACTER FEATURES (MUST MATCH PRECISELY - THIS SPECIFIC INDIVIDUAL):
        - Young professional Black man, approximately 25-30 years old
        - Short, well-groomed dark hair with precise fade/taper cut, styled neatly
        - Clean-shaven with smooth, clear facial skin
        - Distinctive angular facial structure with prominent, well-defined cheekbones
        - Warm, intelligent dark brown eyes with engaging direct gaze and expressive eyebrows
        - Rich dark brown skin tone with healthy, even complexion
        - Strong, well-defined square jawline and masculine facial bone structure
        - Straight, proportioned nose with specific bridge and nostril shape
        - Genuine, confident smile revealing well-aligned natural teeth
        - Professional, approachable demeanor with confident, upright posture
        - Athletic/fit build with broad shoulders and good physical presence
        - Modern, clean-cut professional appearance with attention to grooming
        - Specific facial proportions: balanced forehead, defined temples, strong chin
        - Distinctive almond-shaped eyes with natural arch to eyebrows
        - Full, well-shaped lips with natural definition
        - Exact rich chocolate brown skin tone with warm undertones
        - Sharp facial contours and defined facial planes
        - Youthful but mature professional appearance
        - Confident, intelligent expression with slight natural smile
        
        CLOTHING & STYLE:
        - Professional casual attire (navy blue t-shirt, button-down shirts, or modern polo shirts)
        - Clean, modern aesthetic with neutral colors
        - Well-fitted clothing in professional colors (navy, black, gray, white)
        - Tech-savvy, creative professional appearance
        - Audio/video industry professional style
        
        PERSONALITY & PRESENTATION:
        - Confident and articulate speaker
        - Engaging eye contact with camera
        - Natural hand gestures while speaking (open palm gestures, pointing, explanatory movements)
        - Enthusiastic but professional tone
        - Educational and informative speaking style
        - Expert in audio/video technology and sound design
        - Personal brand focused on creative technology solutions
        """
    
    def get_professional_environment_description(self):
        """Get highly detailed professional studio environment for consistency"""
        return """
        PROFESSIONAL AUDIO/VIDEO STUDIO ENVIRONMENT:
        
        BACKGROUND SETUP:
        - Modern professional audio studio with acoustic treatment
        - Dark charcoal/black acoustic panels on the walls
        - Symmetrical studio monitor speakers with distinctive yellow/gold cones positioned on both sides
        - Professional studio monitors (KRK Rokit or similar) for audio production credibility
        
        LIGHTING DESIGN:
        - Warm ambient table lamps with soft yellow/golden light on both sides
        - Blue/teal accent lighting washing the background walls
        - Professional three-point lighting setup with soft, even illumination on subject
        - No harsh shadows, perfectly balanced lighting for video production
        - Warm color temperature (3000K-3200K) for professional yet approachable feel
        
        FURNITURE & PROPS:
        - Natural wood desk/table in the foreground (oak or similar warm wood tone)
        - Clean, organized workspace suggesting audio/video expertise
        - Framed artwork or certificates on the walls (slightly blurred in background)
        - Professional, minimalist aesthetic without clutter
        
        COLOR PALETTE:
        - Primary: Deep navy/charcoal background
        - Accent: Warm blue/teal lighting (#1E3A8A to #0891B2)
        - Warm tones: Golden yellow lamp light (#FCD34D)
        - Natural: Warm wood tones (#92400E to #A16207)
        - Speaker accents: Bright yellow/gold cones (#FDE047)
        
        TECHNICAL DETAILS:
        - Professional depth of field with subject in sharp focus
        - Background slightly blurred to emphasize the speaker
        - Studio-quality lighting with no visible light sources in frame
        - Vertical composition optimized for mobile/social media (9:16 portrait)
        - Subject positioned in upper two-thirds of frame for portrait format
        - Audio industry credibility through visible professional equipment
        - Framing shows studio monitors and lighting in background context
        
        ATMOSPHERE:
        - Serious but approachable professional environment
        - High-end audio/video production facility
        - Creative technology workspace
        - Educational content creation studio
        - Personal brand headquarters for audio/video expertise
        """
    
    def get_best_reference_image(self):
        """Get the best reference image for maximum character consistency"""
        # Check project reference folder first
        if self.reference_dir.exists():
            # Prioritize the BEST headshot images for character consistency
            # These are ranked by clarity, lighting, and front-facing angle
            priority_images = [
                "IMG_1169.JPG",    # Clear professional headshot, good lighting
                "IMG_1382.JPG",    # Clean front-facing shot, professional
                "IMG_4325.jpg",    # High quality, clear features
                "IMG_2589.JPG",    # Good angle and lighting
                "IMG_9706.jpg",    # Clear facial features
                "IMG_2785.JPG",    # Backup option
                "80BA1D56-15B8-4832-A255-CEA8576E6BCC.JPG"  # Additional backup
            ]
            
            console.print("[cyan]🔍 Searching for optimal reference image...[/cyan]")
            
            for image_name in priority_images:
                image_path = self.reference_dir / image_name
                if image_path.exists():
                    console.print(f"[green]✅ Selected optimal reference: {image_name}[/green]")
                    console.print(f"[dim]   Reason: High-quality headshot for character consistency[/dim]")
                    return image_path
            
            # Fallback to any available image
            all_images = (
                list(self.reference_dir.glob("*.JPG")) + 
                list(self.reference_dir.glob("*.jpg")) +
                list(self.reference_dir.glob("*.PNG")) + 
                list(self.reference_dir.glob("*.png"))
            )
            
            if all_images:
                selected = all_images[0]
                console.print(f"[yellow]⚠️  Using fallback reference: {selected.name}[/yellow]")
                return selected
        
        # Check desktop reference folder as final fallback
        images = self.list_reference_images()
        if images:
            console.print(f"[yellow]⚠️  Using desktop reference: {images[0].name}[/yellow]")
            return images[0]
        
        console.print("[red]❌ No reference images found![/red]")
        return None
    
    def generate_talking_video(self, dialogue_text, character_description="", reference_image_path=None, aspect_ratio="9:16"):
        """Generate a video with a talking character using your appearance - ALWAYS with reference image"""
        
        # ALWAYS get the detailed character description and environment
        character_description = self.get_character_description()
        environment_description = self.get_professional_environment_description()
        
        # ALWAYS use the best reference image for consistency
        if not reference_image_path:
            reference_image_path = self.get_best_reference_image()
        
        if not reference_image_path:
            console.print("[red]❌ ERROR: No reference image available for character consistency![/red]")
            console.print("[yellow]💡 Please add reference images to ensure character accuracy[/yellow]")
            return None
        
        console.print(f"[cyan]📸 Using reference image: {reference_image_path.name}[/cyan]")
        console.print("[cyan]🎯 Applying detailed character + environment descriptions for maximum consistency[/cyan]")
        console.print("[cyan]🏢 Professional audio studio environment with exact color matching[/cyan]")
        
        # HIGHLY SPECIFIC prompt for maximum character AND environment consistency
        talking_prompt = f"""
        CRITICAL: EXACT FACIAL MATCH REQUIRED - Must replicate the EXACT person from the reference image with precise facial features, bone structure, skin tone, and all distinctive characteristics. NOT a generic person, but THIS SPECIFIC INDIVIDUAL:
        
        {character_description.strip()}
        
        EXACT PROFESSIONAL STUDIO ENVIRONMENT REQUIRED:
        {environment_description.strip()}
        
        DIALOGUE TO SPEAK WITH PERFECT LIP SYNC:
        "{dialogue_text}"
        
        CRITICAL REQUIREMENTS:
        - EXACT facial features, bone structure, and skin tone matching the reference image precisely
        - Must be the SAME PERSON as shown in the reference image, not a similar-looking person
        - Replicate the exact nose shape, eye shape, jawline, and facial proportions
        - Match the specific skin tone and facial contours exactly
        - Perfect lip synchronization with the spoken dialogue
        - Natural facial expressions and micro-expressions while speaking
        - Engaging, direct eye contact with the camera throughout
        - Professional hand gestures that complement the speech
        - Confident, articulate delivery matching the character's personality
        - High-quality, clear audio with professional voice tone
        - Consistent character appearance from start to finish matching reference image
        - Natural breathing and speaking rhythm
        - Professional posture and body language
        - Smooth transitions between words and phrases
        - Maintain exact facial identity throughout the entire video
        
        TECHNICAL SPECIFICATIONS:
        - 1080p resolution with crisp detail
        - Professional color grading and lighting
        - Clear audio with no background noise
        - Stable camera work with no shake
        - Perfect focus on the speaker's face
        """
        
        # ALWAYS load the reference image
        reference_image = self.load_reference_image(reference_image_path)
        if not reference_image:
            console.print("[red]❌ ERROR: Failed to load reference image![/red]")
            return None
        
        return self.generate_video(
            prompt=talking_prompt,
            aspect_ratio=aspect_ratio,
            resolution="1080p",
            reference_image=reference_image,
            use_character_consistency=False  # Already handled in this function
        )
    
    def generate_professional_studio_video(self, video_concept, dialogue_text="", aspect_ratio="9:16"):
        """Generate a professional studio video with your exact setup and character"""
        
        character_description = self.get_character_description()
        environment_description = self.get_professional_environment_description()
        
        # Get the best reference image
        reference_image_path = self.get_best_reference_image()
        if not reference_image_path:
            console.print("[red]❌ ERROR: No reference image available![/red]")
            return None
        
        console.print(f"[cyan]🎬 Creating professional studio video with exact environment match[/cyan]")
        console.print(f"[cyan]📸 Using reference: {reference_image_path.name}[/cyan]")
        
        # Create comprehensive prompt for professional studio content
        if dialogue_text:
            studio_prompt = f"""
            PROFESSIONAL AUDIO/VIDEO STUDIO CONTENT CREATION:
            
            EXACT CHARACTER MATCH REQUIRED:
            {character_description.strip()}
            
            EXACT STUDIO ENVIRONMENT REQUIRED:
            {environment_description.strip()}
            
            VIDEO CONCEPT:
            {video_concept}
            
            SPOKEN DIALOGUE WITH PERFECT LIP SYNC:
            "{dialogue_text}"
            
            PROFESSIONAL REQUIREMENTS:
            - Expert-level presentation on audio/video technology
            - Natural hand gestures explaining technical concepts
            - Confident, educational delivery style
            - Perfect lip synchronization with dialogue
            - Professional eye contact and engagement
            - Studio environment showcasing audio expertise
            - Consistent lighting and color palette throughout
            - High-end production quality matching the reference setup
            """
        else:
            studio_prompt = f"""
            PROFESSIONAL AUDIO/VIDEO STUDIO CONTENT CREATION:
            
            EXACT CHARACTER MATCH REQUIRED:
            {character_description.strip()}
            
            EXACT STUDIO ENVIRONMENT REQUIRED:
            {environment_description.strip()}
            
            VIDEO CONCEPT:
            {video_concept}
            
            PROFESSIONAL REQUIREMENTS:
            - Expert-level presentation on audio/video technology
            - Natural hand gestures and professional body language
            - Confident, educational presentation style
            - Professional eye contact and camera engagement
            - Studio environment showcasing audio expertise
            - Consistent lighting and color palette throughout
            - High-end production quality matching the reference setup
            - Demonstrating expertise in sound design and video production
            """
        
        # Load reference image
        reference_image = self.load_reference_image(reference_image_path)
        if not reference_image:
            console.print("[red]❌ ERROR: Failed to load reference image![/red]")
            return None
        
        return self.generate_video(
            prompt=studio_prompt,
            aspect_ratio=aspect_ratio,
            resolution="1080p",
            reference_image=reference_image,
            use_character_consistency=False  # Already handled in this function
        )
    
    def generate_image_to_video(self, main_concept, dialogue_text="", aspect_ratio="9:16"):
        """Generate a video by animating your reference image with dialogue and movement"""
        
        character_description = self.get_character_description()
        environment_description = self.get_professional_environment_description()
        
        # Load multiple references for identity lock
        preferred = [
            "IMG_1169.JPG",
            "IMG_1382.JPG",
            "IMG_9706.jpg",
            "IMG_2589.JPG",
            "IMG_1283.PNG",
        ]
        refs = self.load_reference_images(preferred)
        if not refs:
            console.print("[red]❌ ERROR: No reference images available![/red]")
            return None
        primary_name, primary_ref = refs[0]
        
        console.print(f"[cyan]🎬 Creating image-to-video animation from your reference photo(s)[/cyan]")
        console.print(f"[cyan]📸 Primary reference: {primary_name}  | Additional: {[n for n,_ in refs[1:]]}[/cyan]")
        
        # Create focused image-to-video prompt (NO titles, NO B-roll)
        animation_prompt = f"""
        ANIMATE THE PROVIDED REFERENCE IMAGE INTO A SPEAKING VIDEO:
        
        IDENTITY LOCK (CRITICAL):
        - Use ALL provided reference images. These are the SAME person from different angles and lighting.
        - Identity must remain INVARIANT across every frame.
        - Do NOT alter proportions of nose, eyes, jawline, lips, or bone structure.
        - Match skin tone and facial contours exactly.

        CRITICAL REQUIREMENTS:
        - The person in the reference image must remain EXACTLY the same throughout the video
        - Maintain the exact facial features, skin tone, and appearance from the reference image
        - NO character changes or transitions to different people
        - The reference image person should come to life and speak naturally
        
        ANIMATION REQUIREMENTS:
        - Natural head movements and subtle body language while speaking
        - Realistic lip synchronization with the spoken dialogue
        - Natural eye movements and facial expressions
        - Slight breathing movements and micro-expressions
        - Professional posture and confident demeanor
        - Maintain the exact lighting and composition from the reference image
        
        SPOKEN DIALOGUE WITH PERFECT LIP SYNC:
        "{dialogue_text}"
        
        ENVIRONMENT CONSISTENCY:
        {environment_description.strip()}
        
        VIDEO CONCEPT:
        {main_concept}
        
        TECHNICAL SPECIFICATIONS:
        - High resolution output with crisp detail
        - Smooth, natural animation without jarring movements
        - Professional video quality with stable framing
        - Clear audio with perfect lip synchronization
        - Consistent character appearance from start to finish
        - Mobile-optimized composition for {aspect_ratio} format
        - NO titles, NO graphics, NO B-roll - just the animated person speaking
        - Focus entirely on bringing the reference image to life naturally
        """
        
        # Use primary reference image for the API; others strengthen the prompt context
        reference_image = primary_ref
        console.print("[green]✅ Reference images loaded successfully for character consistency[/green]")
        
        output_path = self.generate_video(
            prompt=animation_prompt,
            aspect_ratio=aspect_ratio,
            resolution="720p",  # Use 720p for 9:16 compatibility (highest available for portrait)
            reference_image=reference_image,
            use_character_consistency=False  # Already handled in this function
        )
        
        if not output_path:
            return None
        
        # Optional: clone voice and replace audio if ELEVENLABS_API_KEY is set
        if os.getenv("ELEVENLABS_API_KEY") and dialogue_text.strip():
            try:
                console.print("[cyan]🗣️ Cloning voice with ElevenLabs and replacing audio...[/cyan]")
                tmp_dir = Path(tempfile.gettempdir())
                voice_wav = tmp_dir / "cloned_voice.wav"
                synthesize_voice(dialogue_text, str(voice_wav))
                out_with_voice = Path(output_path).with_name(Path(output_path).stem + "_voice.mp4")
                replace_video_audio(str(output_path), str(voice_wav), str(out_with_voice))
                console.print(f"[green]✅ Voice-cloned video saved: {out_with_voice.name}[/green]")
                return out_with_voice
            except Exception as e:
                console.print(f"[yellow]⚠️ Voice cloning failed: {e}[/yellow]")
                return output_path
        
        return output_path
    
    def generate_talk_from_specific_image(self, image_name: str, dialogue_text: str = "", aspect_ratio: str = "9:16"):
        """Animate a SINGLE specified image exactly as-is.
        - Uses the exact photo at `Reference Character/<image_name>`
        - Preserves original background and composition
        - Only subtle head/eye/mouth movements and perfect lip-sync
        """
        image_path = (self.reference_dir / image_name)
        if not image_path.exists():
            console.print(f"[red]❌ Image not found: {image_path}[/red]")
            return None
        
        console.print("[cyan]🎬 Creating exact image-to-video animation[/cyan]")
        console.print(f"[cyan]📸 Using EXACT image: {image_path.name}[/cyan]")
        
        animation_prompt = """
        ANIMATE THIS EXACT IMAGE INTO A SPEAKING VIDEO (NO CHANGES TO IMAGE CONTENT):
        
        RULES (STRICT):
        - Use THIS exact image as the visual base for the entire video
        - DO NOT change background, framing, composition, or lighting
        - DO NOT alter the person's identity, facial proportions, or skin tone
        - Only animate natural mouth, eye, and subtle head movements
        - Maintain the photo's look; do NOT rebuild the environment
        - Perfect lip synchronization to the provided dialogue
        """
        
        if dialogue_text.strip():
            animation_prompt += f"\nSPOKEN DIALOGUE (SYNC EXACTLY):\n\n{dialogue_text.strip()}\n"
        
        reference_image = self.load_reference_image(image_path)
        if not reference_image:
            return None
        
        output_path = self.generate_video(
            prompt=animation_prompt,
            aspect_ratio=aspect_ratio,
            resolution="720p",
            reference_image=reference_image,
            use_character_consistency=False
        )
        
        if not output_path:
            return None
        
        # Optional: voice cloning swap if dependencies exist
        if os.getenv("ELEVENLABS_API_KEY") and dialogue_text.strip():
            try:
                console.print("[cyan]🗣️ Cloning voice with ElevenLabs and replacing audio...[/cyan]")
                from voice_clone import synthesize_voice, replace_video_audio  # local import to avoid hard dependency
                import tempfile as _tmp
                tmp_dir = Path(_tmp.gettempdir())
                voice_wav = tmp_dir / "cloned_voice.wav"
                synthesize_voice(dialogue_text, str(voice_wav))
                out_with_voice = Path(output_path).with_name(Path(output_path).stem + "_voice.mp4")
                replace_video_audio(str(output_path), str(voice_wav), str(out_with_voice))
                console.print(f"[green]✅ Voice-cloned video saved: {out_with_voice.name}[/green]")
                return out_with_voice
            except Exception as e:
                console.print(f"[yellow]⚠️ Voice cloning failed: {e}[/yellow]")
                return output_path
        
        return output_path
    
    def list_reference_images(self):
        """List available reference images"""
        images = list(self.reference_dir.glob("*"))
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        images = [img for img in images if img.suffix.lower() in image_extensions]
        
        if not images:
            console.print("[yellow]No reference images found.[/yellow]")
            console.print(f"[dim]Add images to: {self.reference_dir}[/dim]")
            return []
        
        table = Table(title="Reference Images")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="yellow")
        
        for img in sorted(images, key=lambda x: x.stat().st_mtime, reverse=True):
            size_kb = img.stat().st_size / 1024
            modified = datetime.fromtimestamp(img.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            table.add_row(img.name, f"{size_kb:.1f} KB", modified)
        
        console.print(table)
        return images
    
    def list_videos(self):
        """List all generated videos"""
        videos = list(self.output_dir.glob("*.mp4"))
        
        if not videos:
            console.print("[yellow]No videos found. Generate your first video![/yellow]")
            return
        
        table = Table(title="Generated Videos")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Created", style="yellow")
        
        for video in sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True):
            size_mb = video.stat().st_size / (1024 * 1024)
            created = datetime.fromtimestamp(video.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            table.add_row(video.name, f"{size_mb:.1f} MB", created)
        
        console.print(table)
    
    def interactive_mode(self):
        """Interactive CLI mode"""
        console.print(Panel.fit(
            "[bold cyan]🎬 Google Veo 3 Video Generator[/bold cyan]\n"
            "[dim]Generate hyper-realistic videos with native audio for your personal brand[/dim]",
            border_style="cyan"
        ))
        
        while True:
            console.print("\n[bold]What would you like to do?[/bold]")
            console.print("1. Generate new video")
            console.print("2. Generate talking character video (with your appearance)")
            console.print("3. Generate professional studio video (exact environment match)")
            console.print("4. Generate image-to-video (animate your photo)")
            console.print("5. Generate attention-grabbing video (with fantasy cutaways)")
            console.print("6. List generated videos")
            console.print("7. List reference images")
            console.print("8. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")
            
            if choice == "1":
                self.generate_interactive()
            elif choice == "2":
                self.generate_talking_interactive()
            elif choice == "3":
                self.generate_studio_interactive()
            elif choice == "4":
                self.generate_image_to_video_interactive()
            elif choice == "5":
                self.generate_attention_video_interactive()
            elif choice == "6":
                self.list_videos()
            elif choice == "7":
                self.list_reference_images()
            elif choice == "8":
                console.print("[cyan]👋 Goodbye![/cyan]")
                break
    
    def generate_interactive(self):
        """Interactive video generation"""
        console.print("\n[bold]Veo 3 Video Generation[/bold]")
        console.print("[dim]Perfect for 30-second personal brand videos![/dim]\n")
        
        prompt = Prompt.ask("Enter your video prompt")
        
        # Settings
        console.print("\n[dim]Optional settings (press Enter for defaults):[/dim]")
        
        aspect_options = ["9:16", "16:9"]
        aspect_ratio = Prompt.ask("Aspect ratio", choices=aspect_options, default="9:16")
        
        resolution_options = ["720p", "1080p"]
        resolution = Prompt.ask("Resolution", choices=resolution_options, default="1080p")
        
        # Optional negative prompt
        use_negative = Prompt.ask("Add negative prompt? (y/n)", default="n")
        negative_prompt = None
        if use_negative.lower() == 'y':
            negative_prompt = Prompt.ask("Enter negative prompt (what to avoid)")
        
        # Generate
        console.print(f"\n[yellow]⚠️  Note: Veo 3 requires paid tier access and may take several minutes[/yellow]")
        confirm = Prompt.ask("Continue? (y/n)", default="y")
        
        if confirm.lower() == 'y':
            self.generate_video(prompt, aspect_ratio, resolution, negative_prompt)
    
    def generate_talking_interactive(self):
        """Interactive talking character video generation"""
        console.print("\n[bold]🗣️  Talking Character Video Generation[/bold]")
        console.print("[dim]Create videos with lip-sync using your appearance![/dim]\n")
        
        # Check for reference images
        images = self.list_reference_images()
        
        dialogue_text = Prompt.ask("Enter what you want to say in the video")
        
        character_description = Prompt.ask(
            "Describe your appearance/style (optional)", 
            default=""
        )
        
        # Reference image selection
        reference_image_path = None
        if images:
            use_reference = Prompt.ask("Use a reference image for your appearance? (y/n)", default="y")
            if use_reference.lower() == 'y':
                image_names = [img.name for img in images]
                selected_image = Prompt.ask(
                    "Choose reference image", 
                    choices=image_names,
                    default=image_names[0] if image_names else None
                )
                reference_image_path = self.reference_dir / selected_image
        else:
            console.print("[yellow]💡 Tip: Add reference images to ~/Desktop/AI-video-Generation/reference_images/[/yellow]")
        
        # Settings
        aspect_options = ["9:16", "16:9"]
        aspect_ratio = Prompt.ask("Aspect ratio", choices=aspect_options, default="9:16")
        
        # Generate
        console.print(f"\n[yellow]⚠️  Note: This will create a talking video with lip-sync[/yellow]")
        confirm = Prompt.ask("Continue? (y/n)", default="y")
        
        if confirm.lower() == 'y':
            self.generate_talking_video(
                dialogue_text=dialogue_text,
                character_description=character_description,
                reference_image_path=reference_image_path,
                aspect_ratio=aspect_ratio
            )
    
    def generate_studio_interactive(self):
        """Interactive professional studio video generation"""
        console.print("\n[bold]🏢 Professional Studio Video Generation[/bold]")
        console.print("[dim]Create videos with your exact studio environment![/dim]\n")
        
        video_concept = Prompt.ask("Enter your video concept/topic")
        
        # Optional dialogue
        add_dialogue = Prompt.ask("Add spoken dialogue? (y/n)", default="n")
        dialogue_text = ""
        if add_dialogue.lower() == 'y':
            dialogue_text = Prompt.ask("Enter what you want to say")
        
        # Settings
        aspect_options = ["9:16", "16:9"]
        aspect_ratio = Prompt.ask("Aspect ratio", choices=aspect_options, default="9:16")
        
        # Generate
        console.print(f"\n[yellow]⚠️  Note: This will create a professional studio video with exact environment match[/yellow]")
        confirm = Prompt.ask("Continue? (y/n)", default="y")
        
        if confirm.lower() == 'y':
            self.generate_professional_studio_video(
                video_concept=video_concept,
                dialogue_text=dialogue_text,
                aspect_ratio=aspect_ratio
            )
    
    def generate_image_to_video_interactive(self):
        """Interactive image-to-video generation"""
        console.print("\n[bold]📸 Image-to-Video Animation[/bold]")
        console.print("[dim]Animate your reference photo with dialogue and natural movement![/dim]\n")
        
        main_concept = Prompt.ask("Enter your video concept/topic")
        
        # Dialogue (recommended for image-to-video)
        dialogue_text = Prompt.ask("Enter what you want to say in the video")
        
        # Settings
        aspect_options = ["9:16", "16:9"]
        aspect_ratio = Prompt.ask("Aspect ratio", choices=aspect_options, default="9:16")
        
        # Generate
        console.print(f"\n[yellow]⚠️  Note: This will animate your reference photo with 720p resolution (highest for 9:16)[/yellow]")
        console.print("[cyan]🎯 NO titles or B-roll - just your photo coming to life with speech[/cyan]")
        confirm = Prompt.ask("Continue? (y/n)", default="y")
        
        if confirm.lower() == 'y':
            self.generate_image_to_video(
                main_concept=main_concept,
                dialogue_text=dialogue_text,
                aspect_ratio=aspect_ratio
            )
    
    def generate_attention_video_interactive(self):
        """Interactive attention-grabbing video with fantasy cutaways"""
        console.print("\n[bold]⚡ Attention-Grabbing Video Generator[/bold]")
        console.print("[dim]Create scroll-stopping content with fantasy cutaways![/dim]\n")
        
        main_concept = Prompt.ask("Enter your main message/concept")
        dialogue_text = Prompt.ask("Enter what you want to say")
        
        # Cutaway style selection
        console.print("\n[bold]Choose cutaway style:[/bold]")
        console.print("1. Neon Magic (lanterns + sound waves)")
        console.print("2. Forest Dreams (bioluminescent + mystical)")
        console.print("3. Noir Future (red/black + teal/crimson)")
        console.print("4. Cosmic Vibes (space + crystals)")
        console.print("5. Full Spectrum (mix of all styles)")
        
        style_choice = Prompt.ask("Cutaway style", choices=["1", "2", "3", "4", "5"], default="1")
        
        console.print(f"\n[yellow]⚠️  This will generate multiple videos and assemble them[/yellow]")
        console.print("[cyan]🎯 Pattern: You → Fantasy → You → Fantasy → You[/cyan]")
        confirm = Prompt.ask("Continue? (y/n)", default="y")
        
        if confirm.lower() == 'y':
            # Import and run the attention video generator
            try:
                import subprocess
                result = subprocess.run([
                    "python3", "test_attention_video.py"
                ], cwd=Path(__file__).parent, capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print("[green]✅ Attention-grabbing video generated![/green]")
                else:
                    console.print(f"[red]❌ Error: {result.stderr}[/red]")
            except Exception as e:
                console.print(f"[red]❌ Failed to generate attention video: {e}[/red]")

def main():
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        generator = Veo3VideoGenerator()
        generator.generate_video(prompt)
    else:
        # Interactive mode
        generator = Veo3VideoGenerator()
        generator.interactive_mode()

if __name__ == "__main__":
    main()
