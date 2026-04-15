"""
Test script to verify backend can start
Run with: python test_startup.py
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        from app.core.config import settings
        print(f"  [OK] config loaded: {settings.APP_NAME}")

        from app.core.database import Base, engine
        print(f"  [OK] database loaded")

        from app.core.security import verify_password, get_password_hash
        print(f"  [OK] security loaded")

        from app.models import User, File, Task, Share
        print(f"  [OK] models loaded")

        from app.schemas import UserCreate, TaskCreate
        print(f"  [OK] schemas loaded")

        from app.services import blip2_service, tts_service, music_service, ffmpeg_service
        print(f"  [OK] services loaded")

        return True
    except Exception as e:
        print(f"  [FAIL] Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database table creation"""
    print("\nTesting database...")

    try:
        from app.core.database import engine, Base
        import app.models

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(f"  [OK] Tables created successfully")

        return True
    except Exception as e:
        print(f"  [FAIL] Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fastapi():
    """Test FastAPI app creation"""
    print("\nTesting FastAPI app...")

    try:
        from app.main import app

        print(f"  [OK] FastAPI app created")
        print(f"    Routes: {len(app.routes)}")

        # List some routes
        count = 0
        for route in app.routes:
            if hasattr(route, 'path') and '/api/' in route.path:
                print(f"    - {route.path}")
                count += 1
                if count >= 5:
                    break

        return True
    except Exception as e:
        print(f"  [FAIL] FastAPI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 50)
    print("Liushenghua Backend Startup Test")
    print("=" * 50)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("FastAPI", test_fastapi()))

    print("\n" + "=" * 50)
    print("Results:")
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}: {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 50)

    if all_passed:
        print("\n[PASS] All tests passed! Backend is ready to run.")
        print("\nTo start the server:")
        print("  uvicorn app.main:app --reload --port 8000")
    else:
        print("\n[FAIL] Some tests failed. Please fix the issues above.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
