#!/usr/bin/env python3
"""
Chatterbox Voice Provider
FREE voice cloning and TTS using Resemble AI's Chatterbox
Requires: Python 3.10 or 3.11
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import torch

logger = logging.getLogger(__name__)

class ChatterboxProvider:
    """
    FREE Voice Cloning Provider using Chatterbox
    - Zero cost, unlimited usage
    - Runs locally (no API calls)
    - Supports 23 languages
    - Emotion/exaggeration control
    - High quality, production-ready
    """
    
    def __init__(self, device: Optional[str] = None, multilingual: bool = False):
        """
        Initialize Chatterbox Provider
        
        Args:
            device: 'cuda', 'mps', or 'cpu'. Auto-detects if None.
            multilingual: Use multilingual model (23 languages) or English-only
        """
        # Import here to avoid dependency issues
        try:
            import torchaudio as ta
            from chatterbox.tts import ChatterboxTTS
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS
            
            self.ta = ta
            self.ChatterboxTTS = ChatterboxTTS
            self.ChatterboxMultilingualTTS = ChatterboxMultilingualTTS
        except ImportError as e:
            raise RuntimeError(
                "Chatterbox not installed. Requires Python 3.10 or 3.11.\n"
                "See CHATTERBOX_SETUP.md for installation instructions."
            ) from e
        
        # Auto-detect device
        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
        
        self.device = device
        self.multilingual = multilingual
        
        logger.info(f"Initializing Chatterbox on device: {device}")
        
        # Load model
        if multilingual:
            self.model = self.ChatterboxMultilingualTTS.from_pretrained(device=device)
            logger.info("Loaded multilingual model (23 languages)")
        else:
            self.model = self.ChatterboxTTS.from_pretrained(device=device)
            logger.info("Loaded English-only model")
        
        # Voice library (for saved voice clones)
        self.voice_library = {}
    
    def generate(
        self,
        text: str,
        audio_prompt_path: Optional[Path] = None,
        language_id: Optional[str] = None,
        exaggeration: float = 0.5,
        cfg_weight: float = 0.5,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate speech from text
        
        Args:
            text: Text to synthesize
            audio_prompt_path: Reference audio for voice cloning (5-30 seconds)
            language_id: Language code for multilingual model (e.g., 'en', 'es', 'fr')
            exaggeration: Emotion intensity (0.0-1.0, default 0.5)
            cfg_weight: Classifier-free guidance (0.0-1.0, default 0.5)
            output_path: Where to save audio (auto-generated if None)
            
        Returns:
            Path to generated audio file
        """
        try:
            # Generate speech
            if self.multilingual and language_id:
                wav = self.model.generate(
                    text,
                    audio_prompt_path=str(audio_prompt_path) if audio_prompt_path else None,
                    language_id=language_id,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            else:
                wav = self.model.generate(
                    text,
                    audio_prompt_path=str(audio_prompt_path) if audio_prompt_path else None,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            
            # Save to file
            if output_path is None:
                output_path = Path(f"chatterbox_output_{id(wav)}.wav")
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.ta.save(str(output_path), wav, self.model.sr)
            
            logger.info(f"Generated speech: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate speech: {e}")
            raise RuntimeError(f"Speech generation failed: {e}")
    
    def clone_voice(
        self,
        name: str,
        audio_sample_path: Path,
        description: Optional[str] = None
    ):
        """
        Save a voice clone to the library
        
        Args:
            name: Voice name (e.g., 'Tomi_Zenyai')
            audio_sample_path: Path to reference audio (5-30 seconds, clear speech)
            description: Optional description
        """
        if not audio_sample_path.exists():
            raise FileNotFoundError(f"Audio sample not found: {audio_sample_path}")
        
        self.voice_library[name] = {
            'path': audio_sample_path,
            'description': description or f"Voice clone: {name}"
        }
        
        logger.info(f"Voice '{name}' added to library")
    
    def generate_with_voice(
        self,
        text: str,
        voice_name: str = "Tomi_Zenyai",
        language_id: Optional[str] = None,
        exaggeration: float = 0.5,
        cfg_weight: float = 0.5,
        output_path: Optional[Path] = None,
        reference_audio: Optional[Path] = None
    ) -> Path:
        """
        Generate speech using a saved voice clone
        
        Args:
            text: Text to synthesize
            voice_name: Name of voice from library
            language_id: Language code (for multilingual)
            exaggeration: Emotion intensity
            cfg_weight: CFG weight
            output_path: Output file path
            
        Returns:
            Path to generated audio
        """
        # Use provided reference audio or fall back to default
        if reference_audio is None:
            reference_audio = Path("narrations/tomi_reference_voice.wav")
        
        # Check if voice is in library
        if voice_name in self.voice_library:
            voice_info = self.voice_library[voice_name]
            audio_prompt_path = voice_info['path']
        else:
            # Use the reference audio directly
            audio_prompt_path = reference_audio
        
        return self.generate(
            text=text,
            audio_prompt_path=audio_prompt_path,
            language_id=language_id,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            output_path=output_path
        )
    
    def list_voices(self) -> List[Dict[str, Any]]:
        """List all saved voice clones"""
        return [
            {
                'name': name,
                'path': str(info['path']),
                'description': info['description']
            }
            for name, info in self.voice_library.items()
        ]
    
    def generate_narration_for_video(
        self,
        script: str,
        voice_name: Optional[str] = None,
        audio_prompt_path: Optional[Path] = None,
        language_id: str = 'en',
        exaggeration: float = 0.5,
        output_dir: Path = Path("narrations")
    ) -> Path:
        """
        Generate narration for video from script
        Perfect for auto video generation
        
        Args:
            script: Full narration script
            voice_name: Voice from library (if None, uses audio_prompt_path or default)
            audio_prompt_path: Reference audio (if not using saved voice)
            language_id: Language code
            exaggeration: Emotion level (0.5 = natural, 0.7+ = more dramatic)
            output_dir: Where to save narration
            
        Returns:
            Path to narration audio file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"narration_{id(script)}.wav"
        
        if voice_name:
            return self.generate_with_voice(
                text=script,
                voice_name=voice_name,
                language_id=language_id,
                exaggeration=exaggeration,
                output_path=output_path
            )
        else:
            return self.generate(
                text=script,
                audio_prompt_path=audio_prompt_path,
                language_id=language_id,
                exaggeration=exaggeration,
                output_path=output_path
            )
    
    @staticmethod
    def get_supported_languages() -> List[str]:
        """Get list of supported languages for multilingual model"""
        return [
            'ar',  # Arabic
            'da',  # Danish
            'de',  # German
            'el',  # Greek
            'en',  # English
            'es',  # Spanish
            'fi',  # Finnish
            'fr',  # French
            'he',  # Hebrew
            'hi',  # Hindi
            'it',  # Italian
            'ja',  # Japanese
            'ko',  # Korean
            'ms',  # Malay
            'nl',  # Dutch
            'no',  # Norwegian
            'pl',  # Polish
            'pt',  # Portuguese
            'ru',  # Russian
            'sv',  # Swedish
            'sw',  # Swahili
            'tr',  # Turkish
            'zh',  # Chinese
        ]
    
    def detect_watermark(self, audio_path: Path) -> float:
        """
        Check if audio has Chatterbox watermark
        Returns 1.0 if watermarked, 0.0 if not
        """
        try:
            import librosa
            import perth
            
            # Load audio
            audio, sr = librosa.load(str(audio_path), sr=None)
            
            # Initialize watermarker
            watermarker = perth.PerthImplicitWatermarker()
            
            # Extract watermark
            watermark = watermarker.get_watermark(audio, sample_rate=sr)
            
            return watermark
            
        except Exception as e:
            logger.warning(f"Could not detect watermark: {e}")
            return -1.0  # Unknown
