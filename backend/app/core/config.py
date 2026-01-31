# backend/app/core/config.py

# from pydantic import BaseSettings, Field
# جدید:
from pydantic_settings import BaseSettings
from pydantic import Field

from typing import List
import os


ENV = os.getenv("ENVIRONMENT", "DEV")

env_file = ".env.dev" if ENV == "DEV" else ".env.production"

class Settings(BaseSettings):

    """
    تنظیمات اصلی پروژه HR
    معادل settings.py در Django
    """

    # ===============================
    # Environment
    # ===============================
    ENVIRONMENT: str = Field(default="DEV", description="DEV | PRODUCTION")
    DEBUG: bool = Field(default=True)

    # ===============================
    # Security
    # ===============================
    SECRET_KEY: str
    JWT_SECRET: str | None = None

    # ===============================
    # Localization
    # ===============================
    LANGUAGE_CODE: str = "fa-ir"
    TIME_ZONE: str = "Asia/Tehran"

    # ===============================
    # Allowed Hosts
    # ===============================
    ALLOWED_HOSTS: List[str] = []

    # ===============================
    # Database (SQL Server)
    # ===============================
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"

    # ===============================
    # Media / Static (برای فایل عکس و ...)
    # ===============================
    BASE_DIR: str = os.getcwd()

    MEDIA_ROOT: str | None = None
    MEDIA_URL: str = "/media/"

    HR_MEDIA_BASE_URL: str | None = None

    # ===============================
    # Logging
    # ===============================
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = "logs/app.log"

    # ===============================
    # Development Only
    # ===============================
    DEV_USER: str | None = None

    class Config:
        """
        بارگذاری متغیرها از فایل env
        """
        env_file = ".env"
        extra = "ignore"  # فیلدهای اضافی را نادیده می‌گیرد
        env_file_encoding = "utf-8"


# ===============================
# Load settings
# ===============================
settings = Settings()


# ===============================
# Post processing
# ===============================

# اگر JWT_SECRET ست نشده، از SECRET_KEY استفاده می‌کنیم
if not settings.JWT_SECRET:
    settings.JWT_SECRET = settings.SECRET_KEY

# MEDIA_ROOT پیش‌فرض
if not settings.MEDIA_ROOT:
    settings.MEDIA_ROOT = os.path.join(
        settings.BASE_DIR,
        "media"
    )

# نمایش اطلاعات محیط (مشابه print های Django)
print("\n[~~~~~~~~ HR CONFIG LOADED ~~~~~~~~]")
print("ENVIRONMENT :", settings.ENVIRONMENT)
print("DEBUG       :", settings.DEBUG)
print("DB HOST     :", settings.DB_HOST)
print("MEDIA ROOT  :", settings.MEDIA_ROOT)
print("[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]\n")
