"""
FFmpeg Video Composition Service
"""
import os
import subprocess
from pathlib import Path


class FFmpegService:
    """Service for video composition using FFmpeg"""

    def __init__(self):
        self._ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def compose_video(
        self,
        image_path: str,
        audio_path: str,
        music_path: str,
        output_path: str,
        duration: int = 10
    ) -> str:
        """
        Compose final video from image, narration, and background music
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._ffmpeg_available:
            return self._fallback_compose(image_path, output_path)

        try:
            cmd = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-i", str(image_path),
                "-i", str(audio_path),
                "-i", str(music_path),
                "-filter_complex",
                f"[1:a]volume=0.7[narration];[2:a]volume=0.3[music];[narration][music]amix=inputs=2:duration=first[audio]",
                "-map", "0:v",
                "-map", "[audio]",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                "-t", str(duration),
                "-shortest",
                str(output_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return self._fallback_compose(image_path, output_path)

            return str(output_path)
        except Exception as e:
            print(f"FFmpeg composition error: {e}")
            return self._fallback_compose(image_path, output_path)

    def _fallback_compose(self, image_path: str, output_path: str) -> str:
        """Fallback: copy image as output"""
        import shutil
        shutil.copy(image_path, output_path)
        return str(output_path)

    def get_video_info(self, video_path: str) -> dict:
        """Get video information using ffprobe"""
        if not self._ffmpeg_available:
            return {}

        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
        except Exception:
            pass

        return {}


# Singleton instance
ffmpeg_service = FFmpegService()
