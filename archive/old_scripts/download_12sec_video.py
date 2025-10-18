#!/usr/bin/env python3
import os
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
video_id = 'video_68eb33a80e988193b306a4e841e1ec370ebef575400d4633'
base_url = f'https://api.openai.com/v1/videos/{video_id}'
headers = {'Authorization': f'Bearer {api_key}'}

print('⏳ Monitoring 12-second video progress...')
print('=' * 60)

while True:
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        status = data.get('status')
        progress = data.get('progress', 0)
        
        print(f'📊 Status: {status} | Progress: {progress}%', end='\r')
        
        if status == 'completed':
            print()
            print('✅ 12-SECOND VIDEO COMPLETED!')
            
            # Download
            download_url = f'https://api.openai.com/v1/videos/{video_id}/content'
            videos_dir = Path.home() / 'Desktop' / 'AI-video-Generation'
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'Zenyai_EndlessSearch_12sec_COMPLETE_{timestamp}.mp4'
            filepath = videos_dir / filename
            
            print('📥 Downloading...')
            dl_response = requests.get(download_url, headers=headers, stream=True)
            
            if dl_response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in dl_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = filepath.stat().st_size / (1024 * 1024)
                print(f'✅ DOWNLOADED!')
                print(f'📁 {filepath}')
                print(f'📊 Size: {file_size:.2f} MB')
                print(f'⏱️  Duration: 12 seconds (50% longer - complete story!)')
            break
        elif status == 'failed':
            print()
            print(f'❌ Failed: {data.get("error")}')
            break
        
        time.sleep(5)
    else:
        print(f'❌ Error: {response.status_code}')
        break
