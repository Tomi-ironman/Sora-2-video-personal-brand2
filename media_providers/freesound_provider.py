#!/usr/bin/env python3
"""
Freesound API Provider
Access to 600k+ royalty-free sounds and music
API Docs: https://freesound.org/docs/api/
Rate Limit: 60 requests/minute for authenticated requests
"""

import os
import requests
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

FREESOUND_API_KEY = os.getenv('FREESOUND_API_KEY')
FREESOUND_API_BASE = 'https://freesound.org/apiv2'

class FreesoundProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or FREESOUND_API_KEY
        if not self.api_key:
            raise RuntimeError('FREESOUND_API_KEY not configured in .env')
    
    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Token {self.api_key}',
        }
    
    def search_sounds(
        self,
        query: str,
        filter: Optional[str] = None,  # e.g., "duration:[5 TO 30] tag:loop"
        sort: str = 'score',  # score, rating_desc, downloads_desc, duration_desc, etc.
        page_size: int = 15,
        page: int = 1,
        fields: Optional[str] = None  # comma-separated: id,name,tags,duration,download,preview
    ) -> Dict[str, Any]:
        """
        Search for sounds on Freesound
        
        Args:
            query: Search term (e.g., "background music", "ambient", "drums")
            filter: Advanced filter (e.g., "duration:[5 TO 30]" for 5-30 second sounds)
            sort: Sort order
            page_size: Results per page (max 150)
            page: Page number
            fields: Which fields to return
            
        Returns:
            Dict with sounds list and metadata
        """
        url = f"{FREESOUND_API_BASE}/search/text/"
        params = {
            'query': query,
            'page_size': min(page_size, 150),
            'page': page,
            'sort': sort,
        }
        
        if filter:
            params['filter'] = filter
        if fields:
            params['fields'] = fields
        else:
            # Default useful fields
            params['fields'] = 'id,name,tags,duration,download,previews,username,license'
        
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Freesound API error: {e}")
            raise RuntimeError(f"Freesound search failed: {e}")
    
    def get_sound_by_id(self, sound_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific sound"""
        url = f"{FREESOUND_API_BASE}/sounds/{sound_id}/"
        
        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Freesound API error: {e}")
            raise RuntimeError(f"Freesound get sound failed: {e}")
    
    def download_sound(
        self,
        sound_id: int,
        save_path: Path,
        preview: bool = False  # True = download preview (mp3), False = download original
    ) -> Path:
        """
        Download sound from Freesound
        
        Args:
            sound_id: Sound ID
            save_path: Where to save the file
            preview: If True, download preview quality; if False, download original
            
        Returns:
            Path to downloaded file
        """
        # Get sound details first
        sound_info = self.get_sound_by_id(sound_id)
        
        if preview:
            # Download preview (always available, usually mp3)
            download_url = sound_info.get('previews', {}).get('preview-hq-mp3')
            if not download_url:
                download_url = sound_info.get('previews', {}).get('preview-lq-mp3')
        else:
            # Download original (requires OAuth for some sounds)
            download_url = sound_info.get('download')
        
        if not download_url:
            raise RuntimeError(f"No download URL found for sound {sound_id}")
        
        try:
            # Freesound requires the API key for downloads
            response = requests.get(
                download_url,
                headers=self._headers(),
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded Freesound audio to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Sound download failed: {e}")
    
    def search_background_music(
        self,
        mood: str = 'calm',  # calm, happy, energetic, dark, etc.
        duration_min: int = 10,
        duration_max: int = 120,
        page_size: int = 15
    ) -> Dict[str, Any]:
        """
        Search for background music suitable for videos
        
        Args:
            mood: Music mood/style
            duration_min: Minimum duration in seconds
            duration_max: Maximum duration in seconds
            page_size: Number of results
            
        Returns:
            Search results
        """
        # Create filter for duration and loop capability
        filter_str = f"duration:[{duration_min} TO {duration_max}] tag:music"
        
        return self.search_sounds(
            query=mood,
            filter=filter_str,
            sort='rating_desc',
            page_size=page_size
        )
    
    def search_sound_effects(
        self,
        effect_type: str,  # e.g., "click", "whoosh", "notification"
        duration_max: int = 5,
        page_size: int = 15
    ) -> Dict[str, Any]:
        """
        Search for short sound effects
        
        Args:
            effect_type: Type of sound effect
            duration_max: Maximum duration
            page_size: Number of results
            
        Returns:
            Search results
        """
        filter_str = f"duration:[0 TO {duration_max}]"
        
        return self.search_sounds(
            query=effect_type,
            filter=filter_str,
            sort='downloads_desc',
            page_size=page_size
        )
    
    def search_loops(
        self,
        style: str = 'electronic',
        duration_min: int = 2,
        duration_max: int = 30,
        page_size: int = 15
    ) -> Dict[str, Any]:
        """
        Search for loopable audio (great for background music)
        
        Args:
            style: Music style
            duration_min: Minimum duration
            duration_max: Maximum duration
            page_size: Number of results
            
        Returns:
            Search results
        """
        filter_str = f"duration:[{duration_min} TO {duration_max}] tag:loop"
        
        return self.search_sounds(
            query=style,
            filter=filter_str,
            sort='rating_desc',
            page_size=page_size
        )
    
    def search_and_download(
        self,
        query: str,
        save_dir: Path,
        num_sounds: int = 5,
        filter: Optional[str] = None,
        preview: bool = True  # Use preview by default to avoid OAuth complexity
    ) -> List[Path]:
        """
        Search and download multiple sounds
        
        Args:
            query: Search term
            save_dir: Directory to save audio files
            num_sounds: Number of sounds to download
            filter: Advanced filter string
            preview: Download preview quality (True) or original (False)
            
        Returns:
            List of downloaded file paths
        """
        results = self.search_sounds(
            query=query,
            filter=filter,
            page_size=num_sounds
        )
        
        sounds = results.get('results', [])
        downloaded_paths = []
        
        for idx, sound in enumerate(sounds[:num_sounds]):
            sound_id = sound.get('id')
            sound_name = sound.get('name', f'sound_{sound_id}')
            
            # Sanitize filename
            safe_name = "".join(c for c in sound_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            
            # Determine file extension
            if preview:
                ext = 'mp3'
            else:
                # Try to get original format
                original_filename = sound.get('name', 'audio.wav')
                ext = original_filename.split('.')[-1] if '.' in original_filename else 'wav'
            
            filename = f"freesound_{sound_id}_{safe_name[:50]}.{ext}"
            save_path = save_dir / filename
            
            try:
                path = self.download_sound(sound_id, save_path, preview=preview)
                downloaded_paths.append(path)
            except Exception as e:
                logger.error(f"Failed to download sound {sound_id}: {e}")
                continue
        
        return downloaded_paths
