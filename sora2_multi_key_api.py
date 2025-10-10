#!/usr/bin/env python3
"""
Enhanced Sora 2 API with Multi-Key Support
Automatically rotates through your company's API keys for maximum content output
"""

import os
import time
import requests
from typing import Optional
from api_key_manager import get_next_api_key, print_key_stats

class Sora2MultiKeyAPI:
    def __init__(self):
        self.base_url = "https://api.openai.com/v1/videos"
        self.output_dir = os.path.expanduser("~/Desktop/AI-video-Generation")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_video(self, prompt: str, seconds: int = 8, size: str = "720x1280", max_retries: int = 5) -> Optional[object]:
        """Generate video with automatic key rotation on failures"""
        
        for attempt in range(max_retries):
            # Get next working API key
            api_key = get_next_api_key()
            if not api_key:
                print(f"❌ No working API keys available (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    return None
            
            try:
                print(f"🎬 Generating video with Sora 2 (key: {api_key[-8:]}...)...")
                print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
                print(f"Settings: {size}, {seconds}s")
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "sora-2",
                    "prompt": prompt,
                    "size": size,
                    "seconds": str(seconds)
                }
                
                # Make the request
                response = requests.post(self.base_url, headers=headers, json=data, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Sora 2 API returns a job ID that we need to poll
                    if 'id' in result:
                        video_id = result['id']
                        print(f"✅ Video job created: {video_id}")
                        video_result = self._poll_for_completion(video_id, api_key, prompt)
                        if video_result:
                            return video_result
                
                elif response.status_code == 429:
                    print(f"⚠️ Rate limit hit on key {api_key[-8:]}..., trying next key")
                    continue
                    
                elif response.status_code == 401:
                    print(f"❌ Invalid API key {api_key[-8:]}..., trying next key")
                    continue
                    
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    if attempt < max_retries - 1:
                        print(f"Retrying with different key... ({attempt + 1}/{max_retries})")
                        continue
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Request timeout on key {api_key[-8:]}..., trying next key")
                continue
                
            except Exception as e:
                print(f"❌ Error with key {api_key[-8:]}...: {str(e)}")
                if attempt < max_retries - 1:
                    continue
        
        print(f"❌ Failed after {max_retries} attempts with different keys")
        print_key_stats()
        return None
    
    def _poll_for_completion(self, job_id: str, api_key: str, prompt: str, max_polls: int = 60) -> Optional[object]:
        """Poll for video completion"""
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        for poll in range(max_polls):
            try:
                response = requests.get(f"{self.base_url}/{job_id}", headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    current_status = result.get('status')
                    progress_pct = result.get('progress', 0)
                    
                    if current_status == 'completed':
                        print("⠸ Complete!")
                        # Download the video
                        download_response = requests.get(f"{self.base_url}/{job_id}/content", headers=headers, timeout=300)
                        if download_response.status_code == 200:
                            return self._save_video(download_response.content, prompt)
                        else:
                            print(f"❌ Download failed: {download_response.text}")
                            return None
                    
                    elif current_status == 'failed':
                        error_info = result.get('error', 'Unknown error')
                        print(f"❌ Video generation failed: {error_info}")
                        return None
                    
                    # Still processing
                    spinner = ["⠸", "⠋", "⠙", "⠹"][poll % 4]
                    print(f"{spinner} Generating... {progress_pct}% ({current_status})")
                    time.sleep(5)
                    
                else:
                    print(f"❌ Polling error {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                print(f"❌ Polling error: {str(e)}")
                time.sleep(5)
        
        print("⏰ Polling timeout - video may still be processing")
        return None
    
    def _save_video(self, video_content: bytes, prompt: str) -> Optional[object]:
        """Save video content to file"""
        try:
            # Generate filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"sora2_{timestamp}_{safe_prompt}.mp4"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(video_content)
            
            print(f"✅ Video saved: {filename}")
            print("📁 Location: ~/Desktop/AI-video-Generation/")
            
            # Create result object
            class VideoResult:
                def __init__(self, name, path):
                    self.name = name
                    self.path = path
            
            return VideoResult(filename, filepath)
                
        except Exception as e:
            print(f"❌ Save error: {str(e)}")
            return None


# Global instance for easy import
sora2_multi = Sora2MultiKeyAPI()

def generate_video_multi_key(prompt: str, seconds: int = 8, size: str = "720x1280") -> Optional[object]:
    """Convenience function for video generation with multi-key support"""
    return sora2_multi.generate_video(prompt, seconds, size)


if __name__ == "__main__":
    # Test the multi-key system
    test_prompt = "A purple clay octopus waving at the camera in a miniature city, Claymation style, 8 seconds"
    
    print("🧪 Testing Multi-Key Sora 2 API...")
    result = generate_video_multi_key(test_prompt, seconds=8, size="720x1280")
    
    if result:
        print(f"✅ Test successful: {result.name}")
    else:
        print("❌ Test failed")
    
    print_key_stats()
