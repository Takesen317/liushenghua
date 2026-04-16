"""
Application Configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Application
    APP_NAME: str = "留声画"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./liushenghua.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "dev-secret-key-for-development-only"  # Fallback for development
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    def model_post_init(self, *args, **kwargs):
        """Validate configuration for production safety"""
        import warnings

        # Warn if using default SECRET_KEY in production
        if self.SECRET_KEY == "dev-secret-key-for-development-only":
            if not self.DEBUG:
                # In production with default key, raise error
                raise ValueError(
                    "FATAL: Using default SECRET_KEY in production is insecure. "
                    "Set a secure SECRET_KEY via environment variable."
                )
            else:
                warnings.warn("Using default SECRET_KEY in development mode.")

        # Validate SECRET_KEY has minimum length
        if len(self.SECRET_KEY) < 32:
            if not self.DEBUG:
                raise ValueError("SECRET_KEY must be at least 32 characters for security.")
            warnings.warn("SECRET_KEY is shorter than recommended 32 characters.")

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB

    # AI Models
    BLIP_MODEL: str = "salesforce/blip-image-captioning-base"
    MUSICGEN_MODEL: str = "facebook/musicgen-small"

    # Voice
    VOICE: str = "xiaoxiao"
    MUSIC_STYLE: str = "gentle"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://liushenghua.vercel.app",
        "https://liushenghua-git-main-takesen.vercel.app",
        "https://liushenghua-83yr6leyj-takesen.vercel.app",
        "https://liushenghua-pvzziftgj-takesen.vercel.app",
    ]


settings = Settings()
