#!/usr/bin/env python3
"""
Unified Media Manager
One interface for all free stock media APIs
Handles videos (Pexels, Pixabay), images (Unsplash, Pixabay), and audio (Freesound)
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from .pexels_provider import PexelsProvider
from .pixabay_provider import PixabayProvider
from .freesound_provider import FreesoundProvider
from .unsplash_provider import UnsplashProvider
from .ffmpeg_utils import FFmpegUtils

logger = logging.getLogger(__name__)

class UnifiedMediaManager:
    """
    Unified interface for all media providers
    Automatically tries multiple sources for best results
    """
    
    def __init__(self):
        # Initialize all providers (will raise error if API keys missing)
        self.providers = {}
        
        try:
            self.providers['pexels'] = PexelsProvider()
        except RuntimeError as e:
            logger.warning(f"Pexels not available: {e}")
        
        try:
            self.providers['pixabay'] = PixabayProvider()
        except RuntimeError as e:
            logger.warning(f"Pixabay not available: {e}")
        
        try:
            self.providers['freesound'] = FreesoundProvider()
        except RuntimeError as e:
            logger.warning(f"Freesound not available: {e}")
        
        try:
            self.providers['unsplash'] = UnsplashProvider()
        except RuntimeError as e:
            logger.warning(f"Unsplash not available: {e}")
        
        # Check FFmpeg
        if not FFmpegUtils.check_ffmpeg_installed():
            logger.warning("FFmpeg not installed. Video processing features will be limited.")
        
        if not self.providers:
            raise RuntimeError("No media providers available. Please configure API keys in .env")
    
    def search_videos(
        self,
        query: str,
        num_results: int = 10,
        prefer_provider: Optional[str] = None  # 'pexels' or 'pixabay'
    ) -> List[Dict[str, Any]]:
        """
        Search for videos across all available providers
        
        Args:
            query: Search term
            num_results: Number of results to return
            prefer_provider: Preferred provider to try first
            
        Returns:
            List of video results with metadata
        """
        results = []
        
        # Determine provider order
        if prefer_provider and prefer_provider in self.providers:
            providers = [prefer_provider] + [p for p in ['pexels', 'pixabay'] if p != prefer_provider and p in self.providers]
        else:
            providers = [p for p in ['pexels', 'pixabay'] if p in self.providers]
        
        for provider_name in providers:
            try:
                provider = self.providers[provider_name]
                
                if provider_name == 'pexels':
                    data = provider.search_videos(query=query, per_page=num_results)
                    videos = data.get('videos', [])
                    for video in videos:
                        results.append({
                            'id': f"pexels_{video.get('id')}",
                            'provider': 'pexels',
                            'url': provider.get_best_video_url(video),
                            'duration': video.get('duration'),
                            'width': video.get('width'),
                            'height': video.get('height'),
                            'thumbnail': video.get('image'),
                            'metadata': video
                        })
                
                elif provider_name == 'pixabay':
                    data = provider.search_videos(query=query, per_page=num_results)
                    videos = data.get('hits', [])
                    for video in videos:
                        results.append({
                            'id': f"pixabay_{video.get('id')}",
                            'provider': 'pixabay',
                            'url': provider.get_best_video_url(video),
                            'duration': video.get('duration'),
                            'width': video.get('videos', {}).get('large', {}).get('width'),
                            'height': video.get('videos', {}).get('large', {}).get('height'),
                            'thumbnail': video.get('picture_id'),
                            'metadata': video
                        })
                
                if len(results) >= num_results:
                    break
                    
            except Exception as e:
                logger.error(f"Error searching {provider_name}: {e}")
                continue
        
        return results[:num_results]
    
    def search_images(
        self,
        query: str,
        num_results: int = 10,
        orientation: Optional[str] = None,
        prefer_provider: Optional[str] = None  # 'unsplash' or 'pixabay'
    ) -> List[Dict[str, Any]]:
        """
        Search for images across all available providers
        
        Args:
            query: Search term
            num_results: Number of results
            orientation: Image orientation
            prefer_provider: Preferred provider
            
        Returns:
            List of image results with metadata
        """
        results = []
        
        # Determine provider order
        if prefer_provider and prefer_provider in self.providers:
            providers = [prefer_provider] + [p for p in ['unsplash', 'pixabay'] if p != prefer_provider and p in self.providers]
        else:
            providers = [p for p in ['unsplash', 'pixabay'] if p in self.providers]
        
        for provider_name in providers:
            try:
                provider = self.providers[provider_name]
                
                if provider_name == 'unsplash':
                    data = provider.search_photos(query=query, per_page=num_results, orientation=orientation)
                    photos = data.get('results', [])
                    for photo in photos:
                        results.append({
                            'id': f"unsplash_{photo.get('id')}",
                            'provider': 'unsplash',
                            'url': photo.get('urls', {}).get('regular'),
                            'width': photo.get('width'),
                            'height': photo.get('height'),
                            'thumbnail': photo.get('urls', {}).get('thumb'),
                            'attribution': provider.get_attribution(photo),
                            'metadata': photo
                        })
                
                elif provider_name == 'pixabay':
                    # Convert orientation format
                    pix_orientation = None
                    if orientation == 'landscape':
                        pix_orientation = 'horizontal'
                    elif orientation == 'portrait':
                        pix_orientation = 'vertical'
                    
                    data = provider.search_images(query=query, per_page=num_results, orientation=pix_orientation or 'all')
                    images = data.get('hits', [])
                    for image in images:
                        results.append({
                            'id': f"pixabay_{image.get('id')}",
                            'provider': 'pixabay',
                            'url': provider.get_best_image_url(image),
                            'width': image.get('imageWidth'),
                            'height': image.get('imageHeight'),
                            'thumbnail': image.get('previewURL'),
                            'metadata': image
                        })
                
                if len(results) >= num_results:
                    break
                    
            except Exception as e:
                logger.error(f"Error searching {provider_name}: {e}")
                continue
        
        return results[:num_results]
    
    def search_audio(
        self,
        query: str,
        num_results: int = 10,
        duration_min: Optional[int] = None,
        duration_max: Optional[int] = None,
        audio_type: str = 'any'  # 'music', 'sfx', 'any'
    ) -> List[Dict[str, Any]]:
        """
        Search for audio/music on Freesound
        
        Args:
            query: Search term
            num_results: Number of results
            duration_min: Minimum duration in seconds
            duration_max: Maximum duration in seconds
            audio_type: Type of audio
            
        Returns:
            List of audio results
        """
        if 'freesound' not in self.providers:
            logger.error("Freesound provider not available")
            return []
        
        provider = self.providers['freesound']
        results = []
        
        try:
            # Build filter
            filter_parts = []
            if duration_min or duration_max:
                min_d = duration_min or 0
                max_d = duration_max or 999999
                filter_parts.append(f"duration:[{min_d} TO {max_d}]")
            
            if audio_type == 'music':
                filter_parts.append("tag:music")
            elif audio_type == 'sfx':
                filter_parts.append("tag:sfx OR tag:effect")
            
            filter_str = " ".join(filter_parts) if filter_parts else None
            
            data = provider.search_sounds(
                query=query,
                filter=filter_str,
                page_size=num_results
            )
            
            sounds = data.get('results', [])
            for sound in sounds:
                results.append({
                    'id': f"freesound_{sound.get('id')}",
                    'provider': 'freesound',
                    'name': sound.get('name'),
                    'duration': sound.get('duration'),
                    'preview_url': sound.get('previews', {}).get('preview-hq-mp3'),
                    'download_url': sound.get('download'),
                    'tags': sound.get('tags'),
                    'username': sound.get('username'),
                    'license': sound.get('license'),
                    'metadata': sound
                })
            
        except Exception as e:
            logger.error(f"Error searching Freesound: {e}")
        
        return results
    
    def download_media(
        self,
        media_result: Dict[str, Any],
        save_dir: Path,
        quality: str = 'high'
    ) -> Optional[Path]:
        """
        Download media from a search result
        
        Args:
            media_result: Result dict from search methods
            save_dir: Directory to save file
            quality: Quality preference
            
        Returns:
            Path to downloaded file or None
        """
        provider_name = media_result.get('provider')
        media_id = media_result.get('id')
        
        if not provider_name or provider_name not in self.providers:
            logger.error(f"Provider {provider_name} not available")
            return None
        
        provider = self.providers[provider_name]
        save_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if provider_name == 'pexels':
                video_url = media_result.get('url')
                filename = f"{media_id}.mp4"
                save_path = save_dir / filename
                return provider.download_video(video_url, save_path, quality='hd' if quality == 'high' else 'sd')
            
            elif provider_name == 'pixabay':
                if 'url' in media_result:
                    url = media_result.get('url')
                    ext = 'mp4' if 'videos' in str(media_result.get('metadata', {})) else 'jpg'
                    filename = f"{media_id}.{ext}"
                    save_path = save_dir / filename
                    
                    if ext == 'mp4':
                        return provider.download_video(url, save_path)
                    else:
                        return provider.download_image(url, save_path)
            
            elif provider_name == 'unsplash':
                photo_data = media_result.get('metadata')
                filename = f"{media_id}.jpg"
                save_path = save_dir / filename
                return provider.download_photo(photo_data, save_path, quality='regular' if quality == 'high' else 'small')
            
            elif provider_name == 'freesound':
                sound_id = int(media_id.replace('freesound_', ''))
                filename = f"{media_id}.mp3"
                save_path = save_dir / filename
                return provider.download_sound(sound_id, save_path, preview=True)
        
        except Exception as e:
            logger.error(f"Error downloading from {provider_name}: {e}")
            return None
    
    def get_video_broll(
        self,
        keywords: List[str],
        save_dir: Path,
        clips_per_keyword: int = 2,
        duration_preference: Optional[int] = None
    ) -> List[Path]:
        """
        Get B-roll video clips for multiple keywords
        Perfect for automated video generation
        
        Args:
            keywords: List of search terms
            save_dir: Where to save clips
            clips_per_keyword: How many clips per keyword
            duration_preference: Preferred clip duration in seconds
            
        Returns:
            List of downloaded video paths
        """
        downloaded = []
        
        for keyword in keywords:
            logger.info(f"Searching B-roll for: {keyword}")
            results = self.search_videos(keyword, num_results=clips_per_keyword)
            
            for result in results:
                path = self.download_media(result, save_dir, quality='high')
                if path:
                    downloaded.append(path)
        
        return downloaded
    
    def create_video_from_assets(
        self,
        video_clips: List[Path],
        audio_path: Optional[Path],
        output_path: Path,
        target_duration: Optional[float] = None
    ) -> Path:
        """
        Create final video from downloaded assets
        
        Args:
            video_clips: List of video clip paths
            audio_path: Optional background audio
            output_path: Where to save final video
            target_duration: Target video duration
            
        Returns:
            Path to final video
        """
        if not FFmpegUtils.check_ffmpeg_installed():
            raise RuntimeError("FFmpeg not installed. Run: brew install ffmpeg")
        
        # Concatenate video clips
        temp_video = output_path.parent / 'temp_concat.mp4'
        FFmpegUtils.concatenate_videos(video_clips, temp_video)
        
        # Add audio if provided
        if audio_path:
            FFmpegUtils.add_audio_to_video(temp_video, audio_path, output_path)
            temp_video.unlink()  # Clean up temp file
        else:
            temp_video.rename(output_path)
        
        # Trim to target duration if specified
        if target_duration:
            temp_output = output_path.parent / 'temp_final.mp4'
            FFmpegUtils.trim_video(output_path, temp_output, 0, target_duration)
            output_path.unlink()
            temp_output.rename(output_path)
        
        logger.info(f"Created final video: {output_path}")
        return output_path
