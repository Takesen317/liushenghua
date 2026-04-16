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
        """Warn if using default SECRET_KEY in production"""
        import warnings
        if self.SECRET_KEY == "dev-secret-key-for-development-only" and not self.DEBUG:
            warnings.warn("Using default SECRET_KEY in production is insecure. Set a secure value via environment variable.")

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
