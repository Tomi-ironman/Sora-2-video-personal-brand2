# Free Media Providers - Quick Reference Card

## 🚀 Get Started in 3 Steps

### 1. Get API Keys (5 minutes)
```bash
✅ Pexels:    https://www.pexels.com/api/new/
✅ Pixabay:   https://pixabay.com/api/docs/
✅ Unsplash:  https://unsplash.com/oauth/applications
✅ Freesound: https://freesound.org/apiv2/apply/
```

### 2. Add to .env
```bash
PEXELS_API_KEY=your_key
PIXABAY_API_KEY=your_key
UNSPLASH_ACCESS_KEY=your_key
FREESOUND_API_KEY=your_key
```

### 3. Test Setup
```bash
python3 test_media_providers.py
```

---

## 📝 Quick Commands

### Auto-Generate Video
```bash
# Interactive mode
python3 auto_video_generator.py

# Quick presets
python3 auto_video_generator.py productivity
python3 auto_video_generator.py tech
python3 auto_video_generator.py business
```

### Test All APIs
```bash
python3 test_media_providers.py
```

---

## 💻 Quick Code Examples

### Search & Download Videos
```python
from media_providers.unified_media_manager import UnifiedMediaManager
from pathlib import Path

manager = UnifiedMediaManager()

# Search
videos = manager.search_videos("office work", num_results=5)

# Download
for video in videos:
    path = manager.download_media(video, Path("downloads"))
```

### Get B-Roll Clips
```python
manager = UnifiedMediaManager()

clips = manager.get_video_broll(
    keywords=["productivity", "laptop", "coffee"],
    save_dir=Path("broll"),
    clips_per_keyword=2
)
```

### Search Images
```python
manager = UnifiedMediaManager()

images = manager.search_images("workspace", num_results=10)
```

### Search Audio/Music
```python
manager = UnifiedMediaManager()

music = manager.search_audio("upbeat", num_results=5, audio_type='music')
```

### Process with FFmpeg
```python
from media_providers.ffmpeg_utils import FFmpegUtils
from pathlib import Path

# Resize
FFmpegUtils.resize_video(
    Path("input.mp4"),
    Path("output.mp4"),
    1920, 1080
)

# Add audio
FFmpegUtils.add_audio_to_video(
    Path("video.mp4"),
    Path("music.mp3"),
    Path("final.mp4")
)

# Concatenate
FFmpegUtils.concatenate_videos(
    [Path("clip1.mp4"), Path("clip2.mp4")],
    Path("combined.mp4")
)
```

---

## 📊 What You Get

| Provider | Content | Count | Cost |
|----------|---------|-------|------|
| Pexels | Videos | 8M+ | FREE |
| Pixabay | Videos & Images | 7M+ | FREE |
| Unsplash | Images | 5M+ | FREE |
| Freesound | Audio/Music | 600k+ | FREE |
| FFmpeg | Processing | ∞ | FREE |
| **TOTAL** | **All Media** | **20M+** | **$0/mo** |

---

## 🎯 Common Use Cases

### 1. Create Marketing Video
```python
manager = UnifiedMediaManager()

# Get B-roll
clips = manager.get_video_broll(
    keywords=["product demo", "happy customer", "success"],
    save_dir=Path("marketing"),
    clips_per_keyword=2
)

# Get music
music = manager.search_audio("upbeat commercial", num_results=1)
music_path = manager.download_media(music[0], Path("audio"))

# Create video
final = manager.create_video_from_assets(
    video_clips=clips,
    audio_path=music_path,
    output_path=Path("marketing_video.mp4"),
    target_duration=30
)
```

### 2. Create Social Media Content
```python
manager = UnifiedMediaManager()

# Get vertical videos (Instagram/TikTok)
videos = manager.search_videos("lifestyle", num_results=3)

# Download
for video in videos:
    manager.download_media(video, Path("social"))
```

### 3. Create Educational Video
```python
manager = UnifiedMediaManager()

# Get relevant footage
clips = manager.get_video_broll(
    keywords=["learning", "studying", "books", "education"],
    save_dir=Path("education"),
    clips_per_keyword=2
)

# Get calm background music
music = manager.search_audio("calm educational", num_results=1)
```

---

## 🆘 Troubleshooting

### FFmpeg not found?
```bash
brew install ffmpeg
```

### API key error?
- Check `.env` file exists
- Verify key names match exactly
- Make sure no extra spaces in keys

### No results?
- Try broader search terms
- Check provider website status
- Try different provider

### Rate limit hit?
- Wait 1 hour for reset
- Use different provider
- Unified Manager auto-rotates providers

---

## 📚 Full Documentation

- **Setup Guide:** `FREE_MEDIA_SETUP_GUIDE.md`
- **Full Summary:** `FREE_MEDIA_PROVIDERS_SUMMARY.md`
- **Test Script:** `test_media_providers.py`
- **Example Generator:** `auto_video_generator.py`

---

## 💰 Value Proposition

**Commercial Alternative:** $5,000-20,000/year  
**Your Cost:** $0/month  
**Savings:** 100% 🎉

---

**Ready to create unlimited videos? Get your API keys and start building!** 🚀
