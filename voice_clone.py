"""
ElevenLabs voice cloning + audio replace utilities.

Setup:
- Put ELEVENLABS_API_KEY in .env
- Optionally set ELEVENLABS_VOICE_ID in .env (existing cloned voice). If not set, falls back to a stock voice.
- Provide dialogue text to synthesize.

Functions:
- synthesize_voice(text, out_wav_path) -> str path
- replace_video_audio(video_path, audio_path, out_path) -> str path
"""
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Optional

# Third-party
try:
    from elevenlabs import ElevenLabs
    from moviepy.editor import VideoFileClip, AudioFileClip
    VOICE_CLONE_AVAILABLE = True
except ImportError as e:
    print(f"Voice cloning dependencies not available: {e}")
    VOICE_CLONE_AVAILABLE = False

load_dotenv()


def synthesize_voice(text: str, out_wav_path: str, voice_id: Optional[str] = None) -> str:
    if not VOICE_CLONE_AVAILABLE:
        raise RuntimeError("Voice cloning dependencies not available. Install: pip install elevenlabs moviepy")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    client = ElevenLabs(api_key=api_key)
    voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")

    # Fallback to a high-quality stock voice if no custom voice provided
    # Users should set ELEVENLABS_VOICE_ID to their cloned voice for best match
    if not voice_id:
        # Common stock voice id can vary across accounts; using name works in SDK
        voice_settings = {"stability": 0.5, "similarity_boost": 0.75}
        audio = client.generate(text=text, voice="Adam", model="eleven_multilingual_v2")
    else:
        audio = client.generate(text=text, voice=voice_id, model="eleven_multilingual_v2")

    out_wav = Path(out_wav_path)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    with open(out_wav, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return str(out_wav)


def replace_video_audio(video_path: str, audio_path: str, out_path: str) -> str:
    if not VOICE_CLONE_AVAILABLE:
        raise RuntimeError("Voice cloning dependencies not available. Install: pip install elevenlabs moviepy")
    
    video_file = Path(video_path)
    audio_file = Path(audio_path)
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with VideoFileClip(str(video_file)) as v:
        with AudioFileClip(str(audio_file)) as a:
            v = v.set_audio(a)
            v.write_videofile(str(out_file), codec="libx264", audio_codec="aac")
    return str(out_file)
