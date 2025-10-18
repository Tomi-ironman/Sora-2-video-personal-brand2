# Free Media Providers Setup Guide

Complete setup for 5 free APIs: **Pexels, Pixabay, Unsplash, Freesound, FFmpeg**

Total Cost: **$0/month** 🎉

---

## Quick Start

### 1. Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get API Keys (5-10 minutes total)

#### 🎥 Pexels (Stock Videos)
1. Visit: https://www.pexels.com/api/new/
2. Sign up (free account)
3. Copy your API key
4. Add to `.env`:
   ```
   PEXELS_API_KEY=your_pexels_key_here
   ```

**Features:**
- 8M+ free stock videos
- 200 requests/hour
- HD & 4K quality
- No attribution required

---

#### 🎬 Pixabay (Videos & Images)
1. Visit: https://pixabay.com/api/docs/
2. Sign up (free account)
3. Copy your API key
4. Add to `.env`:
   ```
   PIXABAY_API_KEY=your_pixabay_key_here
   ```

**Features:**
- 2.5M+ videos, 4.5M+ images
- 5000 requests/hour
- Multiple quality options
- Attribution appreciated (not required)

---

#### 🖼️ Unsplash (High-Quality Images)
1. Visit: https://unsplash.com/oauth/applications
2. Create a new application
3. Copy your "Access Key"
4. Add to `.env`:
   ```
   UNSPLASH_ACCESS_KEY=your_unsplash_key_here
   ```

**Features:**
- 5M+ professional photos
- 50 requests/hour (free tier)
- Highest quality images
- Attribution required (automatically handled)

---

#### 🎵 Freesound (Audio & Music)
1. Visit: https://freesound.org/apiv2/apply/
2. Sign up and create API key
3. Copy your API key
4. Add to `.env`:
   ```
   FREESOUND_API_KEY=your_freesound_key_here
   ```

**Features:**
- 600k+ sounds & music
- 60 requests/minute
- Loops, SFX, background music
- Various Creative Commons licenses

---

### 4. Complete `.env` File

Your `.env` file should have:

```bash
# Existing keys (keep these)
OPENAI_API_KEY=sk-...
GOOGLE_AI_API_KEY=...
RUNWAY_API_KEY=...
ELEVENLABS_API_KEY=...

# New FREE media providers (add these)
PEXELS_API_KEY=your_pexels_key_here
PIXABAY_API_KEY=your_pixabay_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here
FREESOUND_API_KEY=your_freesound_key_here
```

---

## Testing Your Setup

Run the test script:
```bash
python3 test_media_providers.py
```

Expected output:
```
✅ FFmpeg is installed and working
✅ Pexels API working - Found 3 videos
✅ Pixabay API working - Found 3 videos
✅ Unsplash API working - Found 3 images
✅ Freesound API working - Found 3 sounds
✅ Unified Manager working perfectly!

Results: 6/6 tests passed
🎉 All systems operational!
```

---

## Usage Examples

### Example 1: Search & Download Videos
```python
from media_providers import PexelsProvider
from pathlib import Path

provider = PexelsProvider()
save_dir = Path("downloads/videos")

# Search and download
paths = provider.search_and_download(
    query="office workspace",
    save_dir=save_dir,
    num_videos=5,
    quality='hd',
    orientation='landscape'
)

print(f"Downloaded {len(paths)} videos!")
```

### Example 2: Search Images
```python
from media_providers import UnsplashProvider
from pathlib import Path

provider = UnsplashProvider()
save_dir = Path("downloads/images")

# Get high-quality images
results = provider.search_and_download(
    query="modern office",
    save_dir=save_dir,
    num_photos=10,
    quality='regular',
    orientation='landscape'
)

for result in results:
    print(f"Downloaded: {result['path']}")
    print(f"Attribution: {result['attribution']}")
```

### Example 3: Get Background Music
```python
from media_providers import FreesoundProvider
from pathlib import Path

provider = FreesoundProvider()
save_dir = Path("downloads/audio")

# Search for background music
paths = provider.search_and_download(
    query="calm ambient",
    save_dir=save_dir,
    num_sounds=5,
    filter="duration:[10 TO 60] tag:loop"
)

print(f"Downloaded {len(paths)} audio tracks!")
```

### Example 4: Unified Manager (Easiest!)
```python
from media_providers.unified_media_manager import UnifiedMediaManager
from pathlib import Path

manager = UnifiedMediaManager()

# Search across all providers
videos = manager.search_videos("productivity", num_results=10)
images = manager.search_images("workspace", num_results=10)
audio = manager.search_audio("upbeat music", num_results=5)

# Download
save_dir = Path("downloads")
for video in videos[:3]:
    path = manager.download_media(video, save_dir / "videos")
    print(f"Downloaded: {path}")
```

### Example 5: Complete Video Creation
```python
from media_providers.unified_media_manager import UnifiedMediaManager
from pathlib import Path

manager = UnifiedMediaManager()

# Get B-roll clips
keywords = ["office work", "typing laptop", "coffee break"]
clips = manager.get_video_broll(
    keywords=keywords,
    save_dir=Path("broll"),
    clips_per_keyword=2
)

# Search for background music
audio_results = manager.search_audio("upbeat", num_results=1, audio_type='music')
audio_path = manager.download_media(
    audio_results[0], 
    Path("audio")
)

# Create final video
final_video = manager.create_video_from_assets(
    video_clips=clips,
    audio_path=audio_path,
    output_path=Path("final_video.mp4"),
    target_duration=30
)

print(f"Created video: {final_video}")
```

---

## FFmpeg Utilities

Use the FFmpeg utilities for advanced video processing:

```python
from media_providers.ffmpeg_utils import FFmpegUtils
from pathlib import Path

# Resize video
FFmpegUtils.resize_video(
    input_path=Path("input.mp4"),
    output_path=Path("output_1080p.mp4"),
    width=1920,
    height=1080
)

# Trim video
FFmpegUtils.trim_video(
    input_path=Path("long_video.mp4"),
    output_path=Path("clip.mp4"),
    start_time=5.0,  # Start at 5 seconds
    duration=10.0    # 10 second clip
)

# Add audio
FFmpegUtils.add_audio_to_video(
    video_path=Path("video.mp4"),
    audio_path=Path("music.mp3"),
    output_path=Path("video_with_music.mp4"),
    audio_volume=0.5  # 50% volume
)

# Concatenate multiple clips
FFmpegUtils.concatenate_videos(
    input_paths=[Path("clip1.mp4"), Path("clip2.mp4"), Path("clip3.mp4")],
    output_path=Path("combined.mp4")
)

# Compress video
FFmpegUtils.compress_video(
    input_path=Path("large.mp4"),
    output_path=Path("compressed.mp4"),
    crf=23,  # Lower = better quality (18-28 recommended)
    preset='medium'
)
```

---

## Rate Limits

| Provider | Free Tier Limit | Notes |
|----------|----------------|-------|
| Pexels | 200 requests/hour | Very generous |
| Pixabay | 5000 requests/hour | Essentially unlimited |
| Unsplash | 50 requests/hour | Enough for most uses |
| Freesound | 60 requests/minute | 3600/hour! |
| FFmpeg | Unlimited | Local processing |

**Pro Tip:** The Unified Manager automatically rotates between providers to maximize your usage!

---

## Attribution Requirements

- **Pexels:** No attribution required ✅
- **Pixabay:** Attribution appreciated (optional)
- **Unsplash:** Attribution required (auto-handled by provider)
- **Freesound:** Varies by license (check each sound)
- **FFmpeg:** No attribution needed ✅

The Unsplash provider automatically handles attribution and download tracking.

---

## Troubleshooting

### "FFmpeg not found"
```bash
brew install ffmpeg
```

### "API key not configured"
Check your `.env` file has the correct keys.

### "Rate limit exceeded"
Wait an hour or use a different provider via the Unified Manager.

### "No results found"
Try different search terms or check provider status.

---

## Cost Comparison

### Your Setup (Free):
- **Monthly Cost:** $0
- **Videos:** 8M+ (Pexels) + 2.5M (Pixabay)
- **Images:** 5M+ (Unsplash) + 4.5M (Pixabay)
- **Audio:** 600k+ (Freesound)
- **Processing:** Unlimited (FFmpeg)

### Commercial Services:
- **Shutterstock:** $199-499/mo
- **Getty Images:** $499-999/mo
- **Epidemic Sound:** $49-299/mo
- **Adobe Stock:** $29-249/mo

**You just saved $5,000-20,000/year!** 🎉

---

## Integration with Your Platform

These providers integrate seamlessly with your existing video generation:

```
User Prompt → GPT-4 Script → Search Free Media (Pexels/Pixabay)
    → Download B-roll → Add Music (Freesound) → Process (FFmpeg)
    → Add AI Voiceover (ElevenLabs) → Final Video → Sora/Runway Enhancement
```

---

## Next Steps

1. ✅ Run `python3 test_media_providers.py`
2. ✅ Try the example scripts above
3. ✅ Integrate into your video generation pipeline
4. ✅ Build your InVideo competitor with $0 media costs!

---

## Support

- **Pexels API Docs:** https://www.pexels.com/api/documentation/
- **Pixabay API Docs:** https://pixabay.com/api/docs/
- **Unsplash API Docs:** https://unsplash.com/documentation
- **Freesound API Docs:** https://freesound.org/docs/api/
- **FFmpeg Docs:** https://ffmpeg.org/documentation.html

---

**You now have access to 20M+ videos, 10M+ images, and 600k+ audio files for FREE! 🚀**
