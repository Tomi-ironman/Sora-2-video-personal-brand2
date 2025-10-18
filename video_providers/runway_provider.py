#!/usr/bin/env python3
"""
Runway Gen-3 Alpha video provider integration.
Real video generation using Runway ML API.
"""
import os
import time
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY')
RUNWAY_API_BASE = 'https://api.runwayml.com/v1'

class RunwayVideoProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or RUNWAY_API_KEY
        if not self.api_key:
            raise RuntimeError('RUNWAY_API_KEY not configured')

    def _headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def start_generation(self, prompt: str, concept_id: str) -> Dict[str, Any]:
        """Start video generation with Runway Gen-3 Alpha"""
        url = f"{RUNWAY_API_BASE}/image_to_video"
        payload = {
            "model": "gen3a_turbo",
            "prompt_text": prompt,
            "duration": 10,  # 10 seconds
            "ratio": "16:9",
            "watermark": False
        }
        
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=60)
        if resp.status_code >= 400:
            logger.error('Runway generation failed: %s %s', resp.status_code, resp.text)
            raise RuntimeError(f'Runway generation failed: {resp.status_code} {resp.text}')
        
        data = resp.json()
        return data

    def poll_status(self, task_id: str, timeout_s: int = 300) -> Dict[str, Any]:
        """Poll task status until completion"""
        url = f"{RUNWAY_API_BASE}/tasks/{task_id}"
        deadline = time.time() + timeout_s
        
        while time.time() < deadline:
            resp = requests.get(url, headers=self._headers(), timeout=30)
            if resp.status_code >= 400:
                raise RuntimeError(f'Runway status check failed: {resp.status_code} {resp.text}')
            
            data = resp.json()
            status = data.get('status')
            
            if status == 'SUCCEEDED':
                return data
            elif status == 'FAILED':
                raise RuntimeError(f'Runway generation failed: {data.get("failure_reason", "Unknown error")}')
            
            time.sleep(5)
        
        raise TimeoutError('Runway generation timed out')

    def generate(self, prompt: str, concept_id: str) -> Dict[str, Any]:
        """Generate video and return final result"""
        task_data = self.start_generation(prompt, concept_id)
        task_id = task_data.get('id')
        
        if not task_id:
            raise RuntimeError('Runway did not return task ID')
        
        final_data = self.poll_status(task_id)
        
        # Extract video URL from response
        output = final_data.get('output', [])
        if not output:
            raise RuntimeError('Runway returned no output')
        
        video_url = output[0] if isinstance(output, list) else output
        
        return {
            'video_url': video_url,
            'duration': 10,
            'provider': 'runway_gen3',
            'task_id': task_id,
        }
