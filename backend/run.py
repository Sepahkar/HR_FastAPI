# backend/run.py

"""
فایل اجرای پروژه HR

مسئولیت این فایل:
- اجرای برنامه FastAPI با Uvicorn
- تشخیص محیط DEV / PRODUCTION
- تعیین Host و Port
- جایگزین manage.py در Django

نحوه اجرا:
    python run.py
"""

import uvicorn
from app.core.config import settings


def main():
    """
    نقطه شروع اجرای برنامه
    """

    # ===============================
    # تنظیمات اجرای سرور
    # ===============================

    # در DEV معمولاً روی localhost
    # در PROD روی 127.0.0.1 پشت IIS
    host = "127.0.0.1"
    port = 8000

    # در محیط توسعه:
    # - reload فعال
    # - یک worker
    if settings.ENVIRONMENT == "DEV":
        reload = True
        workers = 1
    else:
        # در Production:
        # - reload خاموش
        # - workers = 1 (روی ویندوز پایدارتر)
        reload = False
        workers = 1

    # ===============================
    # اجرای Uvicorn
    # ===============================
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level="info"
    )


if __name__ == "__main__":
    main()
