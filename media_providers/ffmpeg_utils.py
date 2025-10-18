#!/usr/bin/env python3
"""
FFmpeg Utilities
Video processing, encoding, and manipulation using FFmpeg
Requires: ffmpeg installed via brew (brew install ffmpeg)
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

class FFmpegUtils:
    """Utility class for FFmpeg video processing operations"""
    
    @staticmethod
    def check_ffmpeg_installed() -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def get_video_info(video_path: Path) -> dict:
        """
        Get video metadata using ffprobe
        
        Returns dict with: duration, width, height, fps, codec, bitrate
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            import json
            data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'video'),
                None
            )
            
            if not video_stream:
                raise RuntimeError("No video stream found")
            
            # Parse FPS
            fps_parts = video_stream.get('r_frame_rate', '30/1').split('/')
            fps = int(fps_parts[0]) / int(fps_parts[1])
            
            return {
                'duration': float(data.get('format', {}).get('duration', 0)),
                'width': int(video_stream.get('width', 0)),
                'height': int(video_stream.get('height', 0)),
                'fps': fps,
                'codec': video_stream.get('codec_name', 'unknown'),
                'bitrate': int(data.get('format', {}).get('bit_rate', 0))
            }
            
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            raise RuntimeError(f"FFprobe failed: {e}")
    
    @staticmethod
    def resize_video(
        input_path: Path,
        output_path: Path,
        width: int,
        height: int,
        maintain_aspect: bool = True
    ) -> Path:
        """
        Resize video to specified dimensions
        
        Args:
            input_path: Input video file
            output_path: Output video file
            width: Target width
            height: Target height
            maintain_aspect: If True, pad to maintain aspect ratio
        """
        try:
            if maintain_aspect:
                scale_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
            else:
                scale_filter = f"scale={width}:{height}"
            
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-vf', scale_filter,
                '-c:a', 'copy',
                '-y',  # Overwrite output
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Resized video to {width}x{height}: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg resize failed: {e.stderr.decode()}")
            raise RuntimeError(f"Video resize failed: {e}")
    
    @staticmethod
    def trim_video(
        input_path: Path,
        output_path: Path,
        start_time: float,
        duration: float
    ) -> Path:
        """
        Trim video to specified duration
        
        Args:
            input_path: Input video file
            output_path: Output video file
            start_time: Start time in seconds
            duration: Duration in seconds
        """
        try:
            cmd = [
                'ffmpeg',
                '-ss', str(start_time),
                '-i', str(input_path),
                '-t', str(duration),
                '-c', 'copy',
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Trimmed video: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg trim failed: {e.stderr.decode()}")
            raise RuntimeError(f"Video trim failed: {e}")
    
    @staticmethod
    def concatenate_videos(
        input_paths: List[Path],
        output_path: Path,
        transition_duration: float = 0.5
    ) -> Path:
        """
        Concatenate multiple videos with optional crossfade transitions
        
        Args:
            input_paths: List of video files to concatenate
            output_path: Output video file
            transition_duration: Duration of crossfade transition in seconds
        """
        try:
            # Create concat file
            concat_file = output_path.parent / 'concat_list.txt'
            with open(concat_file, 'w') as f:
                for path in input_paths:
                    f.write(f"file '{path.absolute()}'\n")
            
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            concat_file.unlink()  # Clean up
            
            logger.info(f"Concatenated {len(input_paths)} videos: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg concatenate failed: {e.stderr.decode()}")
            raise RuntimeError(f"Video concatenation failed: {e}")
    
    @staticmethod
    def add_audio_to_video(
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        audio_volume: float = 1.0
    ) -> Path:
        """
        Add audio track to video (replaces existing audio)
        
        Args:
            video_path: Input video file
            audio_path: Input audio file
            output_path: Output video file
            audio_volume: Audio volume multiplier (1.0 = original)
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-i', str(audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-filter:a', f'volume={audio_volume}',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',  # End when shortest input ends
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Added audio to video: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg add audio failed: {e.stderr.decode()}")
            raise RuntimeError(f"Add audio failed: {e}")
    
    @staticmethod
    def add_subtitles(
        video_path: Path,
        subtitle_path: Path,
        output_path: Path,
        subtitle_style: Optional[str] = None
    ) -> Path:
        """
        Burn subtitles into video
        
        Args:
            video_path: Input video file
            subtitle_path: SRT subtitle file
            output_path: Output video file
            subtitle_style: Optional ASS subtitle style
        """
        try:
            if subtitle_style:
                cmd = [
                    'ffmpeg',
                    '-i', str(video_path),
                    '-vf', f"subtitles={subtitle_path}:force_style='{subtitle_style}'",
                    '-c:a', 'copy',
                    '-y',
                    str(output_path)
                ]
            else:
                cmd = [
                    'ffmpeg',
                    '-i', str(video_path),
                    '-vf', f"subtitles={subtitle_path}",
                    '-c:a', 'copy',
                    '-y',
                    str(output_path)
                ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Added subtitles to video: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg add subtitles failed: {e.stderr.decode()}")
            raise RuntimeError(f"Add subtitles failed: {e}")
    
    @staticmethod
    def extract_audio(
        video_path: Path,
        output_path: Path,
        audio_format: str = 'mp3'
    ) -> Path:
        """
        Extract audio from video
        
        Args:
            video_path: Input video file
            output_path: Output audio file
            audio_format: Audio format (mp3, wav, aac, etc.)
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'libmp3lame' if audio_format == 'mp3' else audio_format,
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Extracted audio: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg extract audio failed: {e.stderr.decode()}")
            raise RuntimeError(f"Extract audio failed: {e}")
    
    @staticmethod
    def create_thumbnail(
        video_path: Path,
        output_path: Path,
        time_seconds: float = 1.0
    ) -> Path:
        """
        Create thumbnail image from video
        
        Args:
            video_path: Input video file
            output_path: Output image file
            time_seconds: Time position to capture thumbnail
        """
        try:
            cmd = [
                'ffmpeg',
                '-ss', str(time_seconds),
                '-i', str(video_path),
                '-vframes', '1',
                '-q:v', '2',  # Quality (2-5 is good)
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Created thumbnail: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg thumbnail failed: {e.stderr.decode()}")
            raise RuntimeError(f"Thumbnail creation failed: {e}")
    
    @staticmethod
    def compress_video(
        input_path: Path,
        output_path: Path,
        crf: int = 23,  # 0-51, lower = better quality
        preset: str = 'medium'  # ultrafast, fast, medium, slow, veryslow
    ) -> Path:
        """
        Compress video using H.264 codec
        
        Args:
            input_path: Input video file
            output_path: Output video file
            crf: Constant Rate Factor (18-28 recommended)
            preset: Encoding speed preset
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-c:v', 'libx264',
                '-crf', str(crf),
                '-preset', preset,
                '-c:a', 'aac',
                '-b:a', '128k',
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Compressed video: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg compress failed: {e.stderr.decode()}")
            raise RuntimeError(f"Video compression failed: {e}")
