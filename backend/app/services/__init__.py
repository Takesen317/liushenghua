"""
AI Services - Unified interface
"""
from app.services.blip2_service import blip2_service, BLIP2Service
from app.services.tts_service import tts_service, EdgeTTSService
from app.services.music_service import music_service, MusicGenService
from app.services.video_service import ffmpeg_service, FFmpegService

__all__ = [
    "blip2_service",
    "BLIP2Service",
    "tts_service",
    "EdgeTTSService",
    "music_service",
    "MusicGenService",
    "ffmpeg_service",
    "FFmpegService",
]


def process_narration(image_path: str, style: str, voice: str, music_style: str, output_dir: str) -> dict:
    """
    Complete narration pipeline

    Args:
        image_path: Path to input image
        style: Narration style (warm, lively, lyrical, documentary)
        voice: Voice type (xiaoxiao, yunyang, yunxia)
        music_style: Music style (gentle, cheerful, melancholy, epic)
        output_dir: Directory to save outputs

    Returns:
        Dictionary with paths to generated files and AI description
    """
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: BLIP-2 Image Analysis
    ai_description = blip2_service.analyze_image(image_path)

    # Step 2: Enhance description based on style
    enhanced_description = _enhance_with_style(ai_description, style)

    # Step 3: Edge-TTS Voice Synthesis
    audio_path = output_dir / "narration.mp3"
    tts_service.synthesize_sync(enhanced_description, str(audio_path), voice)

    # Step 4: MusicGen Background Music
    music_path = output_dir / "music.wav"
    music_service.generate_music(ai_description, str(music_path), music_style=music_style)

    # Step 5: FFmpeg Video Composition
    video_path = output_dir / "output.mp4"
    ffmpeg_service.compose_video(
        str(image_path),
        str(audio_path),
        str(music_path),
        str(video_path),
        duration=10
    )

    return {
        "ai_description": ai_description,
        "enhanced_description": enhanced_description,
        "audio_path": str(audio_path),
        "music_path": str(music_path),
        "video_path": str(video_path)
    }


def _enhance_with_style(base_description: str, style: str) -> str:
    """Add style-specific flavor to description"""
    style_prefixes = {
        "warm": "亲爱的朋友，",
        "lively": "嗨，大家好！",
        "lyrical": "在那温暖的记忆里，",
        "documentary": "",
    }

    prefix = style_prefixes.get(style, "")
    return prefix + base_description
