# Chatterbox Voice Cloning Setup Guide

**FREE voice cloning with unlimited usage!** Chatterbox runs locally on your machine.

---

## ⚠️ Python Version Requirement

**Chatterbox requires Python 3.10 or 3.11** (not 3.13).

You currently have **Python 3.13**, so you'll need to set up a separate environment.

---

## 🚀 Quick Setup (10 Minutes)

### Option 1: Using Conda (Recommended)

```bash
# Install conda if you don't have it
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create Python 3.11 environment
conda create -n chatterbox python=3.11 -y
conda activate chatterbox

# Navigate to project
cd /Users/tomi/Documents/GitHub/Video_-Analyzer/Sora-2-video-personal-brand2

# Install Chatterbox
cd chatterbox
pip install -e .

# Install your project dependencies
cd ..
pip install -r requirements.txt

# Test it works
python3 test_chatterbox.py
```

### Option 2: Using pyenv

```bash
# Install pyenv if you don't have it
brew install pyenv

# Install Python 3.11
pyenv install 3.11.7

# Create virtual environment
pyenv virtualenv 3.11.7 chatterbox-env
pyenv activate chatterbox-env

# Navigate to project
cd /Users/tomi/Documents/GitHub/Video_-Analyzer/Sora-2-video-personal-brand2

# Install Chatterbox
cd chatterbox
pip install -e .

# Install your project dependencies
cd ..
pip install -r requirements.txt

# Test it works
python3 test_chatterbox.py
```

---

## 🎯 Quick Test

Once installed, test it:

```bash
# Activate your Python 3.11 environment first!
conda activate chatterbox  # or pyenv activate chatterbox-env

# Run test
python3 test_chatterbox.py
```

Expected output:
```
✅ Chatterbox initialized successfully
✅ Generated test speech: test_output.wav
✅ Voice cloning ready!
```

---

## 🎙️ Clone Your Voice (5 Minutes)

### 1. Record Your Voice Sample

Record 10-30 seconds of clear speech:
- Speak naturally and clearly
- No background noise
- Include varied emotions/tones
- Save as WAV file

**Example script to record:**
> "Hi, I'm Tomi from Zenyai. We're building the future of AI-powered audio storage for professionals. Our platform helps audio engineers, producers, and creators manage their sound libraries with natural language. This is the kind of voice I want for all my videos."

Save as: `voice_samples/tomi_zenyai.wav`

### 2. Clone Your Voice

```python
from voice_providers.chatterbox_provider import ChatterboxProvider
from pathlib import Path

# Initialize
provider = ChatterboxProvider()

# Clone your voice
provider.clone_voice(
    name="Tomi_Zenyai",
    audio_sample_path=Path("voice_samples/tomi_zenyai.wav"),
    description="Tomi's voice for Zenyai videos"
)

# Test it
audio_path = provider.generate_with_voice(
    text="Welcome to Zenyai, the AI-powered audio storage platform.",
    voice_name="Tomi_Zenyai"
)

print(f"Generated with your voice: {audio_path}")
```

---

## 🎬 Use in Video Generation

### Automatic Integration

The hybrid video generator already supports Chatterbox:

```python
from hybrid_video_generator import HybridVideoGenerator

generator = HybridVideoGenerator()

# Create video with YOUR voice
generator.create_complete_video(
    topic="Zenyai Product Demo",
    duration=30,
    add_music=True,
    add_voiceover=True,
    voice_name="Tomi_Zenyai"  # Your cloned voice!
)
```

### Manual Control

```python
from voice_providers.chatterbox_provider import ChatterboxProvider
from pathlib import Path

provider = ChatterboxProvider()

# Generate narration for video
narration = provider.generate_narration_for_video(
    script="Welcome to Zenyai. We help audio professionals manage their sound libraries with AI.",
    voice_name="Tomi_Zenyai",
    exaggeration=0.5,  # Natural emotion
    output_dir=Path("narrations")
)

# Use in video
from media_providers.ffmpeg_utils import FFmpegUtils

FFmpegUtils.add_audio_to_video(
    video_path=Path("video.mp4"),
    audio_path=narration,
    output_path=Path("video_with_voiceover.mp4")
)
```

---

## 🌍 Multilingual Support

Chatterbox supports 23 languages!

```python
# Initialize multilingual model
provider = ChatterboxProvider(multilingual=True)

# Spanish
provider.generate(
    text="Bienvenido a Zenyai, la plataforma de almacenamiento de audio impulsada por IA.",
    voice_name="Tomi_Zenyai",
    language_id="es"
)

# French
provider.generate(
    text="Bienvenue chez Zenyai, la plateforme de stockage audio alimentée par l'IA.",
    voice_name="Tomi_Zenyai",
    language_id="fr"
)

# Supported: ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh
```

---

## 🎭 Emotion Control

Control emotion/exaggeration for different video styles:

```python
# Natural, conversational (default)
provider.generate_with_voice(
    text="Let me show you how Zenyai works.",
    voice_name="Tomi_Zenyai",
    exaggeration=0.5  # Natural
)

# More dramatic, energetic
provider.generate_with_voice(
    text="Transform your audio workflow with Zenyai!",
    voice_name="Tomi_Zenyai",
    exaggeration=0.8,  # More dramatic
    cfg_weight=0.3     # Slower, more deliberate
)

# Calm, educational
provider.generate_with_voice(
    text="Here's how our AI storage system organizes your sounds.",
    voice_name="Tomi_Zenyai",
    exaggeration=0.3,  # Calm
    cfg_weight=0.7     # More controlled
)
```

---

## 💰 Cost Comparison

| Provider | Monthly Cost | Characters | Voice Clones | Latency |
|----------|-------------|------------|--------------|---------|
| **Chatterbox** | **$0** | **Unlimited** | **Unlimited** | **Instant** |
| ElevenLabs Free | $0 | 10,000 | 1 | ~2s |
| ElevenLabs Creator | $5 | 30,000 | 10 | ~2s |
| ElevenLabs Pro | $22 | 100,000 | 30 | ~1s |
| ElevenLabs Scale | $99 | 500,000 | 160 | ~1s |

**Annual Savings: $60-1,200+ with Chatterbox!**

---

## 🔥 Advanced Features

### Batch Voice Generation

```python
scripts = [
    "Welcome to Zenyai",
    "Let me show you our features",
    "Transform your audio workflow",
    "Join thousands of audio professionals",
    "Start your free trial today"
]

for idx, script in enumerate(scripts):
    provider.generate_with_voice(
        text=script,
        voice_name="Tomi_Zenyai",
        output_path=Path(f"narrations/clip_{idx}.wav")
    )
```

### Multiple Voice Characters

```python
# Clone multiple voices for different content
provider.clone_voice("Tomi_Professional", Path("samples/professional.wav"))
provider.clone_voice("Tomi_Casual", Path("samples/casual.wav"))
provider.clone_voice("Tomi_Energetic", Path("samples/energetic.wav"))

# Use different voices for different videos
provider.generate_with_voice(text="...", voice_name="Tomi_Professional")
provider.generate_with_voice(text="...", voice_name="Tomi_Casual")
```

### Voice Library Management

```python
# List all voices
voices = provider.list_voices()
for voice in voices:
    print(f"{voice['name']}: {voice['description']}")

# Output:
# Tomi_Zenyai: Tomi's voice for Zenyai videos
# Tomi_Professional: Professional demos
# Tomi_Casual: Social media content
```

---

## 🎬 Complete Video Pipeline

```python
from hybrid_video_generator import HybridVideoGenerator
from voice_providers.chatterbox_provider import ChatterboxProvider

# Setup voice
voice_provider = ChatterboxProvider()
voice_provider.clone_voice(
    name="Tomi_Zenyai",
    audio_sample_path=Path("voice_samples/tomi.wav")
)

# Create video with your voice
generator = HybridVideoGenerator()
generator.create_complete_video(
    topic="Zenyai: AI Audio Storage Platform",
    duration=45,
    add_music=True,
    add_voiceover=True,
    voice_name="Tomi_Zenyai"
)

# Result: Professional video with YOUR voice, $0 cost!
```

---

## 🔧 Hardware Requirements

### Minimum:
- CPU: Any modern processor
- RAM: 8GB
- Storage: 5GB for model weights
- Works on: Mac (M1/M2/Intel), Linux, Windows

### Recommended:
- GPU: NVIDIA GPU (CUDA) or Apple Silicon (MPS)
- RAM: 16GB+
- Significantly faster generation with GPU

### Performance:
- CPU: ~5-10 seconds per sentence
- GPU: ~1-2 seconds per sentence
- Apple Silicon (MPS): ~2-4 seconds per sentence

---

## 🐛 Troubleshooting

### "Python version error"
You need Python 3.10 or 3.11. Create conda/pyenv environment.

### "CUDA not available"
That's fine! Will use CPU or MPS (Apple Silicon).

### "Out of memory"
Reduce batch size or use CPU mode.

### "Import error"
Make sure you're in the Python 3.11 environment:
```bash
conda activate chatterbox
# or
pyenv activate chatterbox-env
```

---

## 🎯 Next Steps

1. ✅ Set up Python 3.11 environment (10 min)
2. ✅ Install Chatterbox (5 min)
3. ✅ Record your voice sample (5 min)
4. ✅ Clone your voice (2 min)
5. ✅ Create first video with your voice! (2 min)

**Total: 24 minutes to unlimited free voice cloning!**

---

## 📊 Complete Platform Cost

### With Chatterbox Integration:

| Component | Provider | Cost |
|-----------|----------|------|
| Stock Videos | Pexels/Pixabay | $0 |
| Stock Images | Unsplash | $0 |
| Background Music | Freesound | $0 |
| Voice Generation | **Chatterbox** | **$0** |
| Video Processing | FFmpeg | $0 |
| Script Generation | GPT-4 | ~$5/mo |
| **TOTAL** | | **~$5/mo** |

### Commercial Equivalent:
- Stock media: $300-500/mo
- Voice generation: $22-99/mo
- Video tools: $99-499/mo
- **Total commercial: $421-1,098/mo**

**Your savings: $416-1,093/month = $5,000-13,000/year!** 🎉

---

## 🌟 Why Chatterbox is Perfect for Zenyai

1. **Brand Consistency** - Use YOUR voice in every video
2. **Unlimited Usage** - No character limits, no monthly fees
3. **Privacy** - Everything runs locally, no data sent to APIs
4. **Quality** - Beats ElevenLabs in side-by-side tests
5. **Multilingual** - Create content in 23 languages
6. **Fast** - Instant generation, no API latency
7. **Customizable** - Full control over emotion and style

---

**Ready to clone your voice? Set up Python 3.11 and run the test!** 🎙️✨
