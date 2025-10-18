#!/usr/bin/env python3
"""
Pixabay API Provider
Access to 2.5M+ free videos and 4.5M+ images
API Docs: https://pixabay.com/api/docs/
Rate Limit: 5000 requests/hour (unlimited with attribution)
"""

import os
import requests
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
PIXABAY_API_BASE = 'https://pixabay.com/api'

class PixabayProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or PIXABAY_API_KEY
        if not self.api_key:
            raise RuntimeError('PIXABAY_API_KEY not configured in .env')
    
    def search_videos(
        self,
        query: str,
        per_page: int = 20,
        page: int = 1,
        video_type: str = 'all',  # all, film, animation
        category: Optional[str] = None,  # backgrounds, fashion, nature, science, etc.
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        order: str = 'popular'  # popular, latest
    ) -> Dict[str, Any]:
        """
        Search for videos on Pixabay
        
        Args:
            query: Search term
            per_page: Results per page (3-200)
            page: Page number
            video_type: Type of video
            category: Video category
            min_width: Minimum width in pixels
            min_height: Minimum height in pixels
            order: Sort order
            
        Returns:
            Dict with videos list and metadata
        """
        url = f"{PIXABAY_API_BASE}/videos/"
        params = {
            'key': self.api_key,
            'q': query,
            'per_page': min(max(per_page, 3), 200),
            'page': page,
            'video_type': video_type,
            'order': order,
        }
        
        if category:
            params['category'] = category
        if min_width:
            params['min_width'] = min_width
        if min_height:
            params['min_height'] = min_height
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pixabay API error: {e}")
            raise RuntimeError(f"Pixabay search failed: {e}")
    
    def search_images(
        self,
        query: str,
        per_page: int = 20,
        page: int = 1,
        image_type: str = 'all',  # all, photo, illustration, vector
        orientation: str = 'all',  # all, horizontal, vertical
        category: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        colors: Optional[str] = None,  # red, orange, yellow, green, etc.
        order: str = 'popular'
    ) -> Dict[str, Any]:
        """
        Search for images on Pixabay
        
        Args:
            query: Search term
            per_page: Results per page (3-200)
            page: Page number
            image_type: Type of image
            orientation: Image orientation
            category: Image category
            min_width: Minimum width
            min_height: Minimum height
            colors: Filter by color
            order: Sort order
            
        Returns:
            Dict with images list and metadata
        """
        url = f"{PIXABAY_API_BASE}/"
        params = {
            'key': self.api_key,
            'q': query,
            'per_page': min(max(per_page, 3), 200),
            'page': page,
            'image_type': image_type,
            'orientation': orientation,
            'order': order,
        }
        
        if category:
            params['category'] = category
        if min_width:
            params['min_width'] = min_width
        if min_height:
            params['min_height'] = min_height
        if colors:
            params['colors'] = colors
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pixabay API error: {e}")
            raise RuntimeError(f"Pixabay image search failed: {e}")
    
    def download_video(
        self,
        video_url: str,
        save_path: Path
    ) -> Path:
        """Download video from Pixabay"""
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded Pixabay video to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Video download failed: {e}")
    
    def download_image(
        self,
        image_url: str,
        save_path: Path
    ) -> Path:
        """Download image from Pixabay"""
        try:
            response = requests.get(image_url, stream=True, timeout=60)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded Pixabay image to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Image download failed: {e}")
    
    def get_best_video_url(self, video_data: Dict[str, Any], quality: str = 'large') -> Optional[str]:
        """
        Extract best video URL from video data
        
        Args:
            video_data: Video object from search results
            quality: Preferred quality (large, medium, small, tiny)
            
        Returns:
            Video URL or None
        """
        videos = video_data.get('videos', {})
        
        # Try preferred quality first
        if quality in videos:
            return videos[quality].get('url')
        
        # Fallback order: large -> medium -> small -> tiny
        for q in ['large', 'medium', 'small', 'tiny']:
            if q in videos:
                return videos[q].get('url')
        
        return None
    
    def get_best_image_url(self, image_data: Dict[str, Any], size: str = 'largeImageURL') -> Optional[str]:
        """
        Extract best image URL from image data
        
        Args:
            image_data: Image object from search results
            size: Size key (largeImageURL, webformatURL, previewURL)
            
        Returns:
            Image URL or None
        """
        return image_data.get(size) or image_data.get('largeImageURL') or image_data.get('webformatURL')
    
    def search_and_download_videos(
        self,
        query: str,
        save_dir: Path,
        num_videos: int = 5,
        quality: str = 'large'
    ) -> List[Path]:
        """
        Search and download multiple videos
        
        Args:
            query: Search term
            save_dir: Directory to save videos
            num_videos: Number of videos to download
            quality: Video quality
            
        Returns:
            List of downloaded video paths
        """
        results = self.search_videos(query=query, per_page=num_videos)
        
        videos = results.get('hits', [])
        downloaded_paths = []
        
        for idx, video in enumerate(videos[:num_videos]):
            video_url = self.get_best_video_url(video, quality=quality)
            if not video_url:
                logger.warning(f"No video URL found for {video.get('id')}")
                continue
            
            video_id = video.get('id')
            filename = f"pixabay_{video_id}.mp4"
            save_path = save_dir / filename
            
            try:
                path = self.download_video(video_url, save_path)
                downloaded_paths.append(path)
            except Exception as e:
                logger.error(f"Failed to download video {video_id}: {e}")
                continue
        
        return downloaded_paths
    
    def search_and_download_images(
        self,
        query: str,
        save_dir: Path,
        num_images: int = 5,
        size: str = 'largeImageURL'
    ) -> List[Path]:
        """
        Search and download multiple images
        
        Args:
            query: Search term
            save_dir: Directory to save images
            num_images: Number of images to download
            size: Image size preference
            
        Returns:
            List of downloaded image paths
        """
        results = self.search_images(query=query, per_page=num_images)
        
        images = results.get('hits', [])
        downloaded_paths = []
        
        for idx, image in enumerate(images[:num_images]):
            image_url = self.get_best_image_url(image, size=size)
            if not image_url:
                logger.warning(f"No image URL found for {image.get('id')}")
                continue
            
            image_id = image.get('id')
            # Get file extension from URL
            ext = image_url.split('.')[-1].split('?')[0] or 'jpg'
            filename = f"pixabay_{image_id}.{ext}"
            save_path = save_dir / filename
            
            try:
                path = self.download_image(image_url, save_path)
                downloaded_paths.append(path)
            except Exception as e:
                logger.error(f"Failed to download image {image_id}: {e}")
                continue
        
        return downloaded_paths
