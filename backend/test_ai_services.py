"""
AI Services Test Script
Tests each AI service independently to verify they work correctly.
"""
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_blip2():
    """Test BLIP-2 image analysis"""
    print("\n" + "=" * 50)
    print("Testing BLIP-2 Image Analysis")
    print("=" * 50)

    from app.services.blip2_service import blip2_service

    # Use a sample image path - create one if needed
    test_image = os.path.join(os.path.dirname(__file__), "test_image.jpg")

    # If no test image exists, create a simple one
    if not os.path.exists(test_image):
        print("Creating test image...")
        from PIL import Image
        img = Image.new('RGB', (400, 300), color=(100, 150, 200))
        img.save(test_image)
        print(f"Test image saved to {test_image}")

    start = time.time()
    description = blip2_service.analyze_image(test_image)
    elapsed = time.time() - start

    print(f"Result: {description}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Status: {'PASS' if description else 'FAIL'}")
    return description is not None


def test_tts():
    """Test Edge-TTS voice synthesis"""
    print("\n" + "=" * 50)
    print("Testing Edge-TTS Voice Synthesis")
    print("=" * 50)

    from app.services.tts_service import tts_service

    test_text = "这是一段测试语音，留声画让照片开口说话。"
    output_path = os.path.join(os.path.dirname(__file__), "test_output.mp3")

    start = time.time()
    result = tts_service.synthesize_sync(test_text, output_path, voice="xiaoxiao")
    elapsed = time.time() - start

    success = os.path.exists(result) and os.path.getsize(result) > 100
    print(f"Output: {result}")
    print(f"File size: {os.path.getsize(result) if success else 0} bytes")
    print(f"Time: {elapsed:.2f}s")
    print(f"Status: {'PASS' if success else 'FAIL'}")
    return success


def test_music():
    """Test MusicGen music generation"""
    print("\n" + "=" * 50)
    print("Testing MusicGen Music Generation")
    print("=" * 50)

    from app.services.music_service import music_service

    description = "relaxing, gentle, piano music"
    output_path = os.path.join(os.path.dirname(__file__), "test_music.wav")

    start = time.time()
    result = music_service.generate_music(description, output_path, duration=5)
    elapsed = time.time() - start

    success = os.path.exists(result) and os.path.getsize(result) > 1000
    print(f"Output: {result}")
    print(f"File size: {os.path.getsize(result) if success else 0} bytes")
    print(f"Time: {elapsed:.2f}s")
    print(f"Status: {'PASS' if success else 'FAIL'}")
    return success


def test_ffmpeg():
    """Test FFmpeg video composition"""
    print("\n" + "=" * 50)
    print("Testing FFmpeg Video Composition")
    print("=" * 50)

    from app.services.video_service import ffmpeg_service

    # Check if FFmpeg is available
    if not ffmpeg_service._ffmpeg_available:
        print("FFmpeg not found, testing fallback...")
        # Create test files first
        test_image = os.path.join(os.path.dirname(__file__), "test_image.jpg")
        test_audio = os.path.join(os.path.dirname(__file__), "test_output.mp3")
        test_music = os.path.join(os.path.dirname(__file__), "test_music.wav")

        # Ensure files exist
        if not os.path.exists(test_image):
            from PIL import Image
            img = Image.new('RGB', (400, 300), color=(100, 150, 200))
            img.save(test_image)

        output_path = os.path.join(os.path.dirname(__file__), "test_video.mp4")
        result = ffmpeg_service.compose_video(
            test_image,
            test_audio,
            test_music,
            output_path,
            duration=5
        )
    else:
        print("FFmpeg is available, testing composition...")
        test_image = os.path.join(os.path.dirname(__file__), "test_image.jpg")
        test_audio = os.path.join(os.path.dirname(__file__), "test_output.mp3")
        test_music = os.path.join(os.path.dirname(__file__), "test_music.wav")
        output_path = os.path.join(os.path.dirname(__file__), "test_video.mp4")

        if not all(os.path.exists(p) for p in [test_image, test_audio, test_music]):
            print("Some input files missing, creating...")
            from PIL import Image
            Image.new('RGB', (400, 300), color=(100, 150, 200)).save(test_image)

        result = ffmpeg_service.compose_video(
            test_image,
            test_audio,
            test_music,
            output_path,
            duration=5
        )

    success = os.path.exists(result)
    print(f"Output: {result}")
    print(f"Status: {'PASS' if success else 'FAIL'}")
    return success


def test_full_pipeline():
    """Test the complete narration pipeline"""
    print("\n" + "=" * 50)
    print("Testing Full Narration Pipeline")
    print("=" * 50)

    from app.services import process_narration

    # Create test image if needed
    test_image = os.path.join(os.path.dirname(__file__), "test_image.jpg")
    if not os.path.exists(test_image):
        from PIL import Image
        Image.new('RGB', (400, 300), color=(100, 150, 200)).save(test_image)

    output_dir = os.path.join(os.path.dirname(__file__), "pipeline_output")
    os.makedirs(output_dir, exist_ok=True)

    start = time.time()
    try:
        result = process_narration(
            image_path=test_image,
            style="warm",
            voice="xiaoxiao",
            music_style="gentle",
            output_dir=output_dir
        )
        elapsed = time.time() - start

        print(f"AI Description: {result.get('ai_description', 'N/A')}")
        print(f"Enhanced: {result.get('enhanced_description', 'N/A')}")
        print(f"Audio: {result.get('audio_path', 'N/A')}")
        print(f"Music: {result.get('music_path', 'N/A')}")
        print(f"Video: {result.get('video_path', 'N/A')}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Status: PASS")
        return True
    except Exception as e:
        print(f"Pipeline error: {e}")
        print(f"Status: FAIL")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print(" 留声画 AI Services Test Suite")
    print("=" * 60)

    results = {}

    # Test each service
    results['BLIP-2'] = test_blip2()
    results['Edge-TTS'] = test_tts()
    results['MusicGen'] = test_music()
    results['FFmpeg'] = test_ffmpeg()

    # Test full pipeline
    results['Pipeline'] = test_full_pipeline()

    # Summary
    print("\n" + "=" * 60)
    print(" Test Summary")
    print("=" * 60)
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")

    passed = sum(results.values())
    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
