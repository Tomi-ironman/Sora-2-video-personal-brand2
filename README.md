# Personal Brand Video Generator

Generate hyper-realistic videos with **native audio** using **Google Veo 3** for personal brand content.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your Google AI API key:**
```bash
# Edit .env file
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
```
Get your API key from: https://aistudio.google.com/app/apikey

## Usage

### Google Veo 3 Generator (Latest & Best)
```bash
python3 veo3_generator.py
```

### Command Line Mode
```bash
python3 veo3_generator.py "Professional personal brand video with sound design elements"
```

### Alternative Generators
```bash
python3 veo_generator.py    # Veo 2 concepts
python3 sora_generator.py   # Sora (when available)
```

## Features

- ✅ **Simple CLI interface** - No complex setup
- ✅ **Interactive prompts** - Easy video generation
- ✅ **Automatic downloads** - Videos saved locally
- ✅ **Video gallery** - List all generated videos
- ✅ **Customizable settings** - Resolution, duration, quality
- ✅ **Personal brand focused** - Perfect for content creation

## Video Settings

- **Resolutions:** 1920x1080 (landscape), 1080x1920 (portrait), 1280x720 (HD)
- **Duration:** 5-20 seconds
- **Quality:** Standard or HD
- **Model:** sora-1.0-turbo

## Generated Videos

All videos are saved in the `~/Desktop/AI-video-Generation/` folder with timestamps and prompt names for easy access.

## Example Prompts

- "Professional headshot video with subtle background movement"
- "Modern office setup with soft lighting and minimal motion"
- "Creative workspace with gentle camera movement"
- "Personal brand intro with elegant transitions"

## Requirements

- Python 3.8+
- OpenAI API key with Sora access
- Internet connection for API calls