# backend/app/core/logging.py

"""
این فایل مسئول:
- پیکربندی سیستم لاگ پروژه HR
- ذخیره لاگ‌ها در فایل
- چاپ لاگ‌ها در کنسول (در حالت DEV)

معادل در Django:
- settings.py → LOGGING
- فولدر logs/
"""

import logging
from logging.handlers import RotatingFileHandler
import os

from app.core.config import settings


# ======================================================
# اطمینان از وجود فولدر logs
# ======================================================
"""
اگر فولدر logs وجود نداشته باشد،
در اولین اجرای برنامه ساخته می‌شود.
"""

LOG_DIR = os.path.dirname(settings.LOG_PATH)

if LOG_DIR and not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# ======================================================
# فرمت لاگ‌ها
# ======================================================
"""
فرمت استاندارد لاگ:
- زمان
- سطح لاگ
- نام ماژول
- پیام

مثال:
2026-01-23 10:15:30 | INFO | hr.router | User fetched successfully
"""

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ======================================================
# تنظیم Root Logger
# ======================================================
logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)


# ======================================================
# File Handler (ذخیره در فایل)
# ======================================================
"""
RotatingFileHandler:
- وقتی فایل لاگ به حجم مشخص برسد
- فایل جدید ساخته می‌شود
- فایل‌های قدیمی نگه داشته می‌شوند

این کار از پر شدن دیسک جلوگیری می‌کند
"""

file_handler = RotatingFileHandler(
    filename=settings.LOG_PATH,
    maxBytes=10 * 1024 * 1024,   # 10 MB
    backupCount=10,              # نگه داشتن 10 فایل قدیمی
    encoding="utf-8"
)

file_handler.setLevel(settings.LOG_LEVEL)
file_handler.setFormatter(
    logging.Formatter(LOG_FORMAT, DATE_FORMAT)
)


# ======================================================
# Console Handler (فقط برای DEV)
# ======================================================
"""
در محیط DEV:
- لاگ‌ها در کنسول هم نمایش داده می‌شوند
در Production:
- فقط فایل لاگ
"""

console_handler = logging.StreamHandler()
console_handler.setLevel(settings.LOG_LEVEL)
console_handler.setFormatter(
    logging.Formatter(LOG_FORMAT, DATE_FORMAT)
)


# ======================================================
# اضافه کردن Handlerها
# ======================================================
if not logger.handlers:
    logger.addHandler(file_handler)

    if settings.DEBUG:
        logger.addHandler(console_handler)


# ======================================================
# Loggerهای اختصاصی ماژول‌ها
# ======================================================
"""
به جای استفاده مستقیم از logging.info(...)
در هر فایل از این الگو استفاده کنید:

logger = logging.getLogger(__name__)
"""

def get_logger(name: str) -> logging.Logger:
    """
    گرفتن logger اختصاصی برای هر ماژول

    استفاده:
        logger = get_logger(__name__)
        logger.info("پیام تست")
    """
    return logging.getLogger(name)


# ======================================================
# تست اولیه لاگ (در زمان Startup)
# ======================================================
startup_logger = get_logger("startup")

startup_logger.info("HR Logging system initialized")
startup_logger.info(f"Environment: {settings.ENVIRONMENT}")
startup_logger.info(f"Log level: {settings.LOG_LEVEL}")
startup_logger.info(f"Log file: {settings.LOG_PATH}")
