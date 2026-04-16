"""
MusicGen Music Generation Service
"""
import os
import numpy as np


class MusicGenService:
    """Service for generating background music using Meta MusicGen"""

    def __init__(self):
        self.model = None
        self._initialized = False
        import torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """Lazy load model on first use"""
        if self._initialized:
            return

        try:
            print(f"Loading MusicGen model on {self.device}...")
            from audiocraft.models import musicgen
            from app.core.config import settings

            self.model = musicgen.MusicGen.get_pretrained(settings.MUSICGEN_MODEL, device=self.device)
            self.model.set_generation_params(duration=10)
            self._initialized = True
            print("MusicGen model loaded")
        except Exception as e:
            print(f"Warning: Could not load MusicGen model: {e}")
            self._initialized = True

    def generate_music(self, description: str, output_path: str, duration: int = 10, music_style: str = "gentle") -> str:
        """
        Generate background music based on description

        Args:
            description: Text description of desired music style
            output_path: Path to save WAV file
            duration: Duration in seconds
            music_style: Style of music (gentle, cheerful, melancholy, epic)

        Returns:
            Path to generated WAV file
        """
        self.load_model()

        if self.model is None:
            return self._fallback_generate(output_path, duration)

        try:
            # Map music styles to descriptions
            style_prompts = {
                "gentle": f"{description}, soft, gentle piano, relaxing",
                "cheerful": f"{description}, upbeat, happy, cheerful melody",
                "melancholy": f"{description}, sad, emotional, melancholic tone",
                "epic": f"{description}, epic, orchestral, cinematic atmosphere",
            }

            prompt = style_prompts.get(music_style, description)

            self.model.set_generation_params(duration=duration)
            output = self.model.generate([prompt], progress=False)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save using scipy
            from scipy.io import wavfile
            audio_data = output[0].cpu().numpy()
            if len(audio_data.shape) == 1:
                audio_data = np.stack([audio_data, audio_data], axis=1)
            wavfile.write(output_path, 32000, audio_data)

            return output_path
        except Exception as e:
            print(f"MusicGen error: {e}")
            return self._fallback_generate(output_path, duration)

    def _fallback_generate(self, output_path: str, duration: int = 10) -> str:
        """Fallback when MusicGen is not available"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate simple sine wave as placeholder
        sample_rate = 32000
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A4 note
        audio_data = 0.3 * np.sin(2 * np.pi * frequency * t)
        audio_data = np.stack([audio_data, audio_data], axis=1)

        try:
            from scipy.io import wavfile
            wavfile.write(output_path, sample_rate, audio_data.astype(np.float32))
        except Exception as e:
            print(f"Failed to write audio file: {e}")
            # If scipy fails, create empty file
            with open(output_path, 'wb') as f:
                f.write(b'RIFF' + (len(audio_data) * 4 + 36).to_bytes(4, 'little'))
                f.write(b'WAVEfmt ' + (16).to_bytes(4, 'little'))
                f.write((1).to_bytes(2, 'little'))
                f.write((2).to_bytes(2, 'little'))
                f.write((sample_rate).to_bytes(4, 'little'))
                f.write((sample_rate * 4).to_bytes(4, 'little'))

        return output_path


# Singleton instance
music_service = MusicGenService()
