"""
BLIP-2 Image Analysis Service
"""
import os
from PIL import Image


class BLIP2Service:
    """Service for analyzing images using BLIP-2"""

    def __init__(self):
        self.processor = None
        self.model = None
        self._initialized = False
        self.device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"

    def load_model(self):
        """Lazy load model on first use"""
        if self._initialized:
            return

        try:
            import torch
            from transformers import BlipProcessor, BlipForConditionalGeneration
            from app.core.config import settings

            print(f"Loading BLIP-2 model on {self.device}...")
            self.processor = BlipProcessor.from_pretrained(settings.BLIP_MODEL)
            self.model = BlipForConditionalGeneration.from_pretrained(settings.BLIP_MODEL)
            if self.device == "cuda":
                self.model.to(self.device)
            self._initialized = True
            print("BLIP-2 model loaded")
        except Exception as e:
            print(f"Warning: Could not load BLIP-2 model: {e}")
            self._initialized = True  # Mark as initialized to avoid retry

    def analyze_image(self, image_path: str) -> str:
        """
        Analyze image and generate caption

        Args:
            image_path: Path to the image file

        Returns:
            Chinese description of the image
        """
        self.load_model()

        if self.model is None or self.processor is None:
            # Fallback: return a simple description
            return self._fallback_description(image_path)

        try:
            raw_image = Image.open(image_path).convert('RGB')

            inputs = self.processor(raw_image, return_tensors="pt")
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

            output = self.model.generate(**inputs, max_new_tokens=100)
            caption = self.processor.decode(output[0], skip_special_tokens=True)

            return self._enhance_caption(caption)
        except Exception as e:
            print(f"BLIP-2 inference error: {e}")
            return self._fallback_description(image_path)

    def _fallback_description(self, image_path: str) -> str:
        """Fallback when model is not available"""
        filename = os.path.basename(image_path)
        return f"这张照片记录了一个美好的瞬间，名为{filename}。"

    def _enhance_caption(self, caption: str) -> str:
        """
        Enhance English caption with Chinese context
        """
        enhancements = {
            "a": "一张",
            "an": "一张",
            "the": "",
            "photo of": "",
            "image of": "",
        }

        result = caption
        for eng, chn in enhancements.items():
            result = result.replace(eng, chn)

        result = result.strip()
        if not result.endswith(("。", "！", "？")):
            result = result + "。"

        return result


# Singleton instance
blip2_service = BLIP2Service()
