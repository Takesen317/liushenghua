"""
Edge-TTS Text-to-Speech Service
"""
import asyncio
import os


class EdgeTTSService:
    """Service for text-to-speech using Microsoft Edge TTS"""

    # Voice name mapping
    VOICE_MAP = {
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",
        "yunyang": "zh-CN-YunyangNeural",
        "yunxia": "zh-CN-YunxiaNeural",
        "xiaoyi": "zh-CN-XiaoyiNeural",
        "yunjian": "zh-CN-YunjianNeural",
    }

    def __init__(self):
        self.voice = "zh-CN-XiaoxiaoNeural"

    async def synthesize(self, text: str, output_path: str, voice: str = None) -> str:
        """
        Synthesize text to speech

        Args:
            text: Chinese text to synthesize
            output_path: Path to save MP3 file
            voice: Voice name (xiaoxiao, yunyang, etc.)

        Returns:
            Path to generated MP3 file
        """
        try:
            import edge_tts
        except ImportError:
            print("Warning: edge-tts not installed, using fallback")
            return self._fallback_synthesize(text, output_path)

        voice_name = self.VOICE_MAP.get(voice, self.VOICE_MAP["xiaoxiao"])

        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_path)

        return output_path

    def synthesize_sync(self, text: str, output_path: str, voice: str = None) -> str:
        """
        Synchronous wrapper for synthesize
        """
        try:
            return asyncio.run(self.synthesize(text, output_path, voice))
        except Exception as e:
            print(f"TTS error: {e}")
            return self._fallback_synthesize(text, output_path)

    def _fallback_synthesize(self, text: str, output_path: str) -> str:
        """Fallback when edge-tts is not available"""
        # Create a minimal valid MP3 file placeholder
        # In production, this would use a different TTS engine
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            # Minimal silent MP3 (about 0.1 second)
            f.write(bytes([0xFF, 0xFB, 0x90, 0x00] + [0] * 100))
        return output_path


# Singleton instance
tts_service = EdgeTTSService()
