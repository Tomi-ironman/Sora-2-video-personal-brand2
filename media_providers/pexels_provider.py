#!/usr/bin/env python3
"""
Pexels Video API Provider
Access to 8M+ free stock videos
API Docs: https://www.pexels.com/api/documentation/
Rate Limit: 200 requests/hour
"""

import os
import requests
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PEXELS_API_BASE = 'https://api.pexels.com'

class PexelsProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or PEXELS_API_KEY
        if not self.api_key:
            raise RuntimeError('PEXELS_API_KEY not configured in .env')
    
    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': self.api_key,
        }
    
    def search_videos(
        self, 
        query: str, 
        per_page: int = 15,
        page: int = 1,
        orientation: str = 'landscape',  # landscape, portrait, square
        size: str = 'medium',  # large, medium, small
        min_duration: Optional[int] = None,  # in seconds
        max_duration: Optional[int] = None   # in seconds
    ) -> Dict[str, Any]:
        """
        Search for videos on Pexels
        
        Args:
            query: Search term (e.g., "ocean waves", "city traffic")
            per_page: Results per page (1-80)
            page: Page number
            orientation: Video orientation
            size: Video size
            min_duration: Minimum duration in seconds
            max_duration: Maximum duration in seconds
            
        Returns:
            Dict with videos list and metadata
        """
        url = f"{PEXELS_API_BASE}/videos/search"
        params = {
            'query': query,
            'per_page': min(per_page, 80),
            'page': page,
            'orientation': orientation,
            'size': size,
        }
        
        if min_duration:
            params['min_duration'] = min_duration
        if max_duration:
            params['max_duration'] = max_duration
        
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pexels API error: {e}")
            raise RuntimeError(f"Pexels search failed: {e}")
    
    def get_popular_videos(self, per_page: int = 15, page: int = 1) -> Dict[str, Any]:
        """Get popular/curated videos"""
        url = f"{PEXELS_API_BASE}/videos/popular"
        params = {
            'per_page': min(per_page, 80),
            'page': page,
        }
        
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pexels API error: {e}")
            raise RuntimeError(f"Pexels popular videos failed: {e}")
    
    def get_video_by_id(self, video_id: int) -> Dict[str, Any]:
        """Get specific video by ID"""
        url = f"{PEXELS_API_BASE}/videos/videos/{video_id}"
        
        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pexels API error: {e}")
            raise RuntimeError(f"Pexels get video failed: {e}")
    
    def download_video(
        self, 
        video_url: str, 
        save_path: Path,
        quality: str = 'hd'  # hd, sd, or specific height like '720p'
    ) -> Path:
        """
        Download video from Pexels
        
        Args:
            video_url: Direct video URL from search results
            save_path: Where to save the video
            quality: Video quality preference
            
        Returns:
            Path to downloaded video
        """
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded Pexels video to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Video download failed: {e}")
    
    def get_best_video_url(self, video_data: Dict[str, Any], quality: str = 'hd') -> Optional[str]:
        """
        Extract the best video URL from video data
        
        Args:
            video_data: Video object from search results
            quality: Preferred quality (hd, sd)
            
        Returns:
            Video URL string or None
        """
        video_files = video_data.get('video_files', [])
        
        if not video_files:
            return None
        
        # Filter by quality preference
        if quality == 'hd':
            # Try to get highest quality
            hd_videos = [v for v in video_files if v.get('quality') == 'hd' or v.get('height', 0) >= 1080]
            if hd_videos:
                return hd_videos[0].get('link')
        
        elif quality == 'sd':
            sd_videos = [v for v in video_files if v.get('quality') == 'sd' or 720 <= v.get('height', 0) < 1080]
            if sd_videos:
                return sd_videos[0].get('link')
        
        # Fallback to first available
        return video_files[0].get('link')
    
    def search_and_download(
        self,
        query: str,
        save_dir: Path,
        num_videos: int = 5,
        quality: str = 'hd',
        orientation: str = 'landscape'
    ) -> List[Path]:
        """
        Search and download multiple videos in one go
        
        Args:
            query: Search term
            save_dir: Directory to save videos
            num_videos: How many videos to download
            quality: Video quality
            orientation: Video orientation
            
        Returns:
            List of paths to downloaded videos
        """
        results = self.search_videos(
            query=query,
            per_page=num_videos,
            orientation=orientation
        )
        
        videos = results.get('videos', [])
        downloaded_paths = []
        
        for idx, video in enumerate(videos[:num_videos]):
            video_url = self.get_best_video_url(video, quality=quality)
            if not video_url:
                logger.warning(f"No video URL found for {video.get('id')}")
                continue
            
            # Create filename from video ID
            video_id = video.get('id')
            filename = f"pexels_{video_id}.mp4"
            save_path = save_dir / filename
            
            try:
                path = self.download_video(video_url, save_path, quality)
                downloaded_paths.append(path)
            except Exception as e:
                logger.error(f"Failed to download video {video_id}: {e}")
                continue
        
        return downloaded_paths
