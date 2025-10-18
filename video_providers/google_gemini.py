#!/usr/bin/env python3
"""
Google Gemini/Veo video provider integration.
Notes:
- Requires GOOGLE_AI_API_KEY in environment.
- Model defaults to 'veo-2' via GOOGLE_AI_MODEL.
- Uses Google Generative Language API v1beta long-running operations style.

This implementation assumes access to Google's video generation endpoint.
If your account lacks access, the API will return 403/404. In that case,
please request access in Google AI Studio or provide an alternative provider key.
"""
from __future__ import annotations
import os
import time
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_AI_API_KEY')
GOOGLE_VIDEO_MODEL = os.getenv('GOOGLE_AI_MODEL', 'veo-2')
GOOGLE_API_BASE = os.getenv('GOOGLE_AI_API_BASE', 'https://generativelanguage.googleapis.com')

class GeminiVideoProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GOOGLE_API_KEY
        if not self.api_key:
            raise RuntimeError('GOOGLE_AI_API_KEY not configured')

    def _headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
        }

    def start_generation(self, prompt: str, concept_id: str) -> Dict[str, Any]:
        """
        Starts a video generation job with Google model (e.g., 'veo-2').
        Returns an operation object: { name: op_name }
        """
        model = GOOGLE_VIDEO_MODEL
        url = f"{GOOGLE_API_BASE}/v1beta/models/{model}:generateVideo?key={self.api_key}"
        payload = {
            'prompt': {
                'text': prompt
            },
            # Optional parameters if supported by your model access
            'config': {
                'aspectRatio': 'PORTRAIT_9_16',
                'durationSeconds': 30
            },
            'requestId': concept_id,
        }
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=60)
        if resp.status_code >= 400:
            logger.error('Gemini/Veo start failed: %s %s', resp.status_code, resp.text)
            raise RuntimeError(f'Gemini/Veo start failed: {resp.status_code} {resp.text}')
        data = resp.json()
        # Expect { 'name': 'operations/...' }
        return data

    def poll_operation(self, op_name: str, timeout_s: int = 600, interval_s: int = 5) -> Dict[str, Any]:
        """
        Polls long-running operation until done.
        Returns the full operation JSON, expected to contain final video URI(s).
        """
        url = f"{GOOGLE_API_BASE}/v1beta/{op_name}?key={self.api_key}"
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            r = requests.get(url, timeout=30)
            if r.status_code >= 400:
                logger.error('Gemini/Veo poll failed: %s %s', r.status_code, r.text)
                raise RuntimeError(f'Gemini/Veo poll failed: {r.status_code} {r.text}')
            op = r.json()
            if op.get('done'):
                return op
            time.sleep(interval_s)
        raise TimeoutError('Gemini/Veo operation timed out')

    def generate(self, prompt: str, concept_id: str) -> Dict[str, Any]:
        op = self.start_generation(prompt, concept_id)
        op_name = op.get('name') or op.get('operation') or op.get('id')
        if not op_name:
            raise RuntimeError('Gemini/Veo did not return operation name')
        final = self.poll_operation(op_name)
        # Expected structure example:
        # {
        #   'done': True,
        #   'response': {
        #      'videos': [{ 'uri': 'https://storage.googleapis.com/...mp4', 'thumbnailUri': '...jpg', 'duration': 30 }]
        #   }
        # }
        response = final.get('response', {})
        videos = response.get('videos') or response.get('results') or []
        if not videos:
            raise RuntimeError('Gemini/Veo returned no videos')
        v0 = videos[0]
        return {
            'video_url': v0.get('uri') or v0.get('videoUri'),
            'thumbnail_url': v0.get('thumbnailUri'),
            'duration': v0.get('duration') or response.get('durationSeconds', 30),
            'provider': 'google_gemini',
            'operation': op_name,
        }
