# 🎬 SadTalker Lip-Sync - Setup Guide

## What is SadTalker?

Turn any photo of yourself into a talking head video with your cloned voice!

**Perfect for Zenyai:**
- Professional founder introduction videos
- Product demos with your face
- Social media content
- Investor presentations
- Marketing videos with personal touch

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: Install Dependencies (In Progress)
```bash
source venv_chatterbox/bin/activate
cd SadTalker && pip install -r requirements.txt
```
**Status:** ⏳ Installing now...

### Step 2: Download Models (5-10 min)
```bash
./setup_sadtalker.sh
```
This downloads ~3-4 GB of AI models (one-time only)

### Step 3: Create Your First Talking Video!
```bash
python create_talking_video.py
```

---

## 📋 What You Need

### 1. Your Photo
- ✅ Headshot (front-facing)
- ✅ Good lighting
- ✅ Clear face
- ✅ Any resolution (will be processed)
- ✅ JPG, PNG, or any image format

### 2. Your Audio
- ✅ Already have: `narrations/tomi_zenyai_test.wav`
- ✅ Or use: `~/Desktop/Tomi_Zenyai_Voice_Test.wav`
- ✅ Any voice audio works!

---

## 🎯 How to Use

### Method 1: Interactive (Easiest)
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py
```

**Follow the prompts:**
1. Enter path to your photo
2. Enter path to your audio
3. Choose face enhancement (yes/no)
4. Wait 1-3 minutes
5. Video ready!

---

### Method 2: Command Line (Fast)
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py your_photo.jpg narrations/tomi_zenyai_test.wav
```

---

### Method 3: Python Script (Most Flexible)
```python
from create_talking_video import create_talking_video
from pathlib import Path

# Create talking video
video = create_talking_video(
    image_path="photos/tomi_headshot.jpg",
    audio_path="narrations/tomi_zenyai_test.wav",
    output_path="videos/welcome_to_zenyai.mp4",
    enhancer="gfpgan"  # Enhance face quality
)

print(f"Video saved: {video}")
```

---

## 🎬 Example Use Cases

### 1. "Welcome to Zenyai" Video
```bash
# Your headshot + your cloned voice
python create_talking_video.py \
    photos/tomi_professional.jpg \
    narrations/tomi_zenyai_test.wav
```
**Result:** You introducing Zenyai in your own voice!

### 2. Product Demo
```bash
# Create custom narration first
source venv_chatterbox/bin/activate
python -c "
from voice_providers.chatterbox_provider import ChatterboxProvider
from pathlib import Path

provider = ChatterboxProvider()
provider.generate_with_voice(
    text='Zenyai revolutionizes audio storage with AI-powered search and organization.',
    voice_name='Tomi_Zenyai',
    output_path=Path('narrations/product_demo.wav')
)
"

# Then create video
python create_talking_video.py \
    photos/tomi.jpg \
    narrations/product_demo.wav
```

### 3. Social Media Content (Weekly)
```bash
# Create 5 different videos for the week
for topic in "welcome" "features" "pricing" "testimonial" "update"; do
    # Generate voice
    python -c "from voice_providers.chatterbox_provider import ChatterboxProvider; from pathlib import Path; ChatterboxProvider().generate_with_voice(text='...', voice_name='Tomi_Zenyai', output_path=Path('narrations/${topic}.wav'))"
    
    # Create video
    python create_talking_video.py photos/tomi.jpg narrations/${topic}.wav
done
```

---

## ⚙️ Options & Settings

### Face Enhancement
- **`gfpgan`** (recommended) - Enhances face quality, removes blemishes
- **`none`** - No enhancement, faster processing

### Video Quality
- Automatically optimized for best quality
- Output: 512x512 or 256x256 (adjustable)
- Format: MP4 H.264

### Processing Time
- **First run:** 2-5 minutes (downloads models)
- **Subsequent runs:** 30-90 seconds

---

## 💾 Storage Requirements

| Component | Size |
|-----------|------|
| SadTalker code | ~100 MB |
| AI Models | ~3-4 GB |
| **Total** | **~4 GB** |

**One-time download, use forever!**

---

## 🎯 Quality Tips

### For Best Results:

1. **Photo Quality**
   - ✅ High resolution (at least 512x512)
   - ✅ Front-facing, looking at camera
   - ✅ Good lighting (no shadows on face)
   - ✅ Neutral expression or slight smile
   - ✅ Clear, not blurry

2. **Audio Quality**
   - ✅ Clear speech
   - ✅ Good volume level
   - ✅ Minimal background noise
   - ✅ Natural pacing

3. **Best Practices**
   - ✅ Use professional headshots
   - ✅ Keep audio under 2 minutes for best sync
   - ✅ Enable face enhancement for polished look
   - ✅ Test with short clips first

---

## 🔧 Integration with Your Platform

### Complete Workflow:

```
1. Record your script
   ↓
2. Clone your voice (Chatterbox) → FREE
   ↓
3. Generate speech with emotion control → FREE
   ↓
4. Create talking video (SadTalker) → FREE
   ↓
5. Add to video with stock footage → FREE
   ↓
6. Professional marketing video → $0!
```

### Example: Complete Zenyai Video
```python
from voice_providers.chatterbox_provider import ChatterboxProvider
from create_talking_video import create_talking_video
from hybrid_video_generator import HybridVideoGenerator
from pathlib import Path

# 1. Generate voiceover
provider = ChatterboxProvider()
audio = provider.generate_with_voice(
    text="Welcome to Zenyai, the future of audio storage.",
    voice_name="Tomi_Zenyai",
    output_path=Path("narrations/intro.wav")
)

# 2. Create talking head
talking_video = create_talking_video(
    image_path="photos/tomi.jpg",
    audio_path=audio
)

# 3. Combine with stock footage
generator = HybridVideoGenerator()
final_video = generator.create_complete_video(
    topic="Zenyai Introduction",
    duration=30,
    add_music=True
)
```

---

## 📊 Cost Comparison

### Your Setup:
| Component | Cost |
|-----------|------|
| SadTalker (lip-sync) | $0 |
| Chatterbox (voice) | $0 |
| Stock footage | $0 |
| Video editing | $0 |
| **Total** | **$0/month** |

### Commercial Alternative:
| Service | Cost |
|---------|------|
| D-ID or Synthesia | $29-99/month |
| ElevenLabs (voice) | $22-99/month |
| Stock footage | $199/month |
| **Total** | **$250-397/month** |

**Annual savings: $3,000-4,764** 🎉

---

## 🚀 Use Cases for Zenyai

### 1. Founder Introduction
- Your face + your voice
- Personal connection with users
- Build trust and authenticity

### 2. Product Demos
- Explain features with your face
- Tutorial-style videos
- Walkthrough demonstrations

### 3. Investor Pitches
- Professional presentation
- Your voice narrating slides
- Face-to-camera pitch

### 4. Social Media
- Quick updates
- Weekly tips
- Behind-the-scenes

### 5. Marketing Campaigns
- Consistent brand voice (yours!)
- Multiple videos quickly
- A/B testing different scripts

---

## ⚡ Quick Commands

### Create talking video (interactive):
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py
```

### Create talking video (fast):
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py \
    my_photo.jpg \
    my_audio.wav \
    output.mp4
```

### Test with your voice:
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py \
    photos/me.jpg \
    ~/Desktop/Tomi_Zenyai_Voice_Test.wav
```

---

## 🐛 Troubleshooting

### "Module not found"
- Make sure you activated the environment:
  ```bash
  source venv_chatterbox/bin/activate
  ```

### "Checkpoints not found"
- Run the model download:
  ```bash
  ./setup_sadtalker.sh
  ```

### "Out of memory"
- Close other applications
- Use smaller image (resize to 512x512)
- Process one video at a time

### Video quality not good
- Enable face enhancement: `enhancer="gfpgan"`
- Use higher resolution source photo
- Ensure good lighting in photo

---

## 📁 File Structure

```
Sora-2-video-personal-brand2/
├── SadTalker/              # SadTalker repository
│   ├── checkpoints/        # AI models (~3-4 GB)
│   ├── gfpgan/            # Face enhancement
│   └── inference.py       # Main script
│
├── create_talking_video.py # Easy-to-use wrapper
├── setup_sadtalker.sh      # Model download script
│
├── photos/                 # Your headshots (create this)
├── narrations/            # Voice audio files
│   └── tomi_zenyai_test.wav
│
└── talking_videos/        # Generated videos
    └── talking_*.mp4
```

---

## ✅ Setup Checklist

### Initial Setup (One-Time):
- [⏳] Install dependencies (in progress)
- [ ] Download AI models: `./setup_sadtalker.sh`
- [ ] Prepare your headshot photo
- [ ] Test: `python create_talking_video.py`

### For Each Video:
- [ ] Activate environment: `source venv_chatterbox/bin/activate`
- [ ] Have photo ready
- [ ] Have audio ready (use voice cloning!)
- [ ] Run: `python create_talking_video.py`
- [ ] Wait 30-90 seconds
- [ ] Video ready!

---

## 🎉 What You'll Be Able to Do

After setup, you can:
- ✅ Turn any photo into a talking video
- ✅ Use your cloned voice for narration
- ✅ Create unlimited videos ($0 cost!)
- ✅ Professional quality output
- ✅ Fast generation (30-90 seconds)
- ✅ Full control over content
- ✅ Perfect for Zenyai marketing

---

## 🔜 Next Steps

### After Dependencies Install:
1. ✅ Run `./setup_sadtalker.sh` to download models
2. ✅ Prepare a professional headshot
3. ✅ Create your first talking video!

### First Video:
```bash
source venv_chatterbox/bin/activate
python create_talking_video.py \
    your_photo.jpg \
    ~/Desktop/Tomi_Zenyai_Voice_Test.wav
```

---

**Your complete FREE talking head video system is almost ready!** 🎬✨

Just need to:
1. Wait for dependencies to finish installing
2. Download models with `./setup_sadtalker.sh`
3. Create your first video!

**Total time remaining: ~10-15 minutes**
