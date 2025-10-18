#!/usr/bin/env python3
"""
Unsplash API Provider
Access to 5M+ high-quality free images
API Docs: https://unsplash.com/documentation
Rate Limit: 50 requests/hour (free tier)
"""

import os
import requests
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_API_BASE = 'https://api.unsplash.com'

class UnsplashProvider:
    def __init__(self, access_key: Optional[str] = None):
        self.access_key = access_key or UNSPLASH_ACCESS_KEY
        if not self.access_key:
            raise RuntimeError('UNSPLASH_ACCESS_KEY not configured in .env')
    
    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Client-ID {self.access_key}',
        }
    
    def search_photos(
        self,
        query: str,
        per_page: int = 10,
        page: int = 1,
        orientation: Optional[str] = None,  # landscape, portrait, squarish
        color: Optional[str] = None,  # black_and_white, black, white, yellow, orange, red, purple, magenta, green, teal, blue
        order_by: str = 'relevant'  # relevant, latest
    ) -> Dict[str, Any]:
        """
        Search for photos on Unsplash
        
        Args:
            query: Search term
            per_page: Results per page (max 30)
            page: Page number
            orientation: Photo orientation
            color: Filter by color
            order_by: Sort order
            
        Returns:
            Dict with photos list and metadata
        """
        url = f"{UNSPLASH_API_BASE}/search/photos"
        params = {
            'query': query,
            'per_page': min(per_page, 30),
            'page': page,
            'order_by': order_by,
        }
        
        if orientation:
            params['orientation'] = orientation
        if color:
            params['color'] = color
        
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Unsplash API error: {e}")
            raise RuntimeError(f"Unsplash search failed: {e}")
    
    def get_random_photo(
        self,
        query: Optional[str] = None,
        orientation: Optional[str] = None,
        count: int = 1  # 1-30
    ) -> Dict[str, Any]:
        """
        Get random photo(s) from Unsplash
        
        Args:
            query: Optional search term to filter random results
            orientation: Photo orientation
            count: Number of random photos (1-30)
            
        Returns:
            Photo data (single dict if count=1, list if count>1)
        """
        url = f"{UNSPLASH_API_BASE}/photos/random"
        params = {
            'count': min(count, 30),
        }
        
        if query:
            params['query'] = query
        if orientation:
            params['orientation'] = orientation
        
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Unsplash API error: {e}")
            raise RuntimeError(f"Unsplash random photo failed: {e}")
    
    def get_photo_by_id(self, photo_id: str) -> Dict[str, Any]:
        """Get specific photo by ID"""
        url = f"{UNSPLASH_API_BASE}/photos/{photo_id}"
        
        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Unsplash API error: {e}")
            raise RuntimeError(f"Unsplash get photo failed: {e}")
    
    def download_photo(
        self,
        photo_data: Dict[str, Any],
        save_path: Path,
        quality: str = 'regular'  # raw, full, regular, small, thumb
    ) -> Path:
        """
        Download photo from Unsplash
        
        Args:
            photo_data: Photo object from search results
            save_path: Where to save the image
            quality: Image quality/size
            
        Returns:
            Path to downloaded image
        """
        # Get download URL for tracking (required by Unsplash API terms)
        download_location = photo_data.get('links', {}).get('download_location')
        if download_location:
            try:
                # This triggers a download event for Unsplash analytics
                requests.get(download_location, headers=self._headers(), timeout=10)
            except:
                pass  # Non-critical, continue with download
        
        # Get image URL
        urls = photo_data.get('urls', {})
        image_url = urls.get(quality) or urls.get('regular') or urls.get('full')
        
        if not image_url:
            raise RuntimeError("No image URL found")
        
        try:
            response = requests.get(image_url, stream=True, timeout=60)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded Unsplash photo to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Photo download failed: {e}")
    
    def trigger_download(self, photo_data: Dict[str, Any]):
        """
        Trigger download event (required by Unsplash API terms)
        Call this whenever you use an Unsplash photo
        """
        download_location = photo_data.get('links', {}).get('download_location')
        if download_location:
            try:
                requests.get(download_location, headers=self._headers(), timeout=10)
            except Exception as e:
                logger.warning(f"Failed to trigger Unsplash download event: {e}")
    
    def get_attribution(self, photo_data: Dict[str, Any]) -> str:
        """
        Get attribution text for Unsplash photo (required by terms)
        
        Args:
            photo_data: Photo object
            
        Returns:
            Attribution string
        """
        user = photo_data.get('user', {})
        username = user.get('username', 'Unknown')
        name = user.get('name', username)
        user_link = user.get('links', {}).get('html', '')
        photo_link = photo_data.get('links', {}).get('html', '')
        
        return f"Photo by {name} ({username}) on Unsplash - {photo_link}"
    
    def search_and_download(
        self,
        query: str,
        save_dir: Path,
        num_photos: int = 5,
        quality: str = 'regular',
        orientation: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search and download multiple photos
        
        Args:
            query: Search term
            save_dir: Directory to save images
            num_photos: Number of photos to download
            quality: Image quality
            orientation: Photo orientation
            
        Returns:
            List of dicts with 'path' and 'attribution' keys
        """
        results = self.search_photos(
            query=query,
            per_page=num_photos,
            orientation=orientation
        )
        
        photos = results.get('results', [])
        downloaded_data = []
        
        for idx, photo in enumerate(photos[:num_photos]):
            photo_id = photo.get('id')
            
            # Create filename
            filename = f"unsplash_{photo_id}.jpg"
            save_path = save_dir / filename
            
            try:
                path = self.download_photo(photo, save_path, quality)
                attribution = self.get_attribution(photo)
                
                downloaded_data.append({
                    'path': path,
                    'attribution': attribution,
                    'photo_id': photo_id,
                    'photo_data': photo
                })
            except Exception as e:
                logger.error(f"Failed to download photo {photo_id}: {e}")
                continue
        
        return downloaded_data
    
    def get_random_and_download(
        self,
        save_dir: Path,
        query: Optional[str] = None,
        num_photos: int = 5,
        quality: str = 'regular',
        orientation: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get random photos and download them
        
        Args:
            save_dir: Directory to save images
            query: Optional search term filter
            num_photos: Number of photos
            quality: Image quality
            orientation: Photo orientation
            
        Returns:
            List of dicts with 'path' and 'attribution' keys
        """
        photos = self.get_random_photo(
            query=query,
            orientation=orientation,
            count=num_photos
        )
        
        # Handle single photo vs list
        if not isinstance(photos, list):
            photos = [photos]
        
        downloaded_data = []
        
        for photo in photos:
            photo_id = photo.get('id')
            
            filename = f"unsplash_{photo_id}.jpg"
            save_path = save_dir / filename
            
            try:
                path = self.download_photo(photo, save_path, quality)
                attribution = self.get_attribution(photo)
                
                downloaded_data.append({
                    'path': path,
                    'attribution': attribution,
                    'photo_id': photo_id,
                    'photo_data': photo
                })
            except Exception as e:
                logger.error(f"Failed to download photo {photo_id}: {e}")
                continue
        
        return downloaded_data
