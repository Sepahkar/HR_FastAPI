# backend/app/main.py

"""
نقطه ورود (Entry Point) برنامه FastAPI پروژه HR

مسئولیت این فایل:
- ساخت شیء FastAPI
- بارگذاری تنظیمات
- ثبت Router ها
- ثبت Middleware ها
- Health Check
- Startup / Shutdown Events

معادل در Django:
- manage.py
- urls.py
- بخشی از settings.py
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import get_logger
from app.core.database import test_db_connection
from app.modules.hr.router import router as hr_router

logger = get_logger(__name__)


# ======================================================
# ایجاد برنامه FastAPI
# ======================================================
app = FastAPI(
    title="HR System",
    description="سامانه منابع انسانی شرکت فناوران اطلاعات خبره",
    version="1.0.0",
    debug=settings.DEBUG
)


# ======================================================
# Middleware ها
# ======================================================

"""
CORS:
- برای اتصال Frontend (Vue)
- در محیط DEV معمولاً آزاد
- در Production محدود به دامنه‌های مشخص
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================================
# Exception Handler عمومی
# ======================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    مدیریت خطاهای پیش‌بینی‌نشده
    جلوگیری از نمایش StackTrace به کاربر
    """
    logger.exception(
        f"Unhandled exception on path {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "خطای داخلی سرور"
        }
    )


# ======================================================
# ثبت Router ها
# ======================================================

"""
در آینده اگر ماژول‌های دیگری اضافه شوند:
- finance
- workflow
- evaluation
اینجا register می‌شوند
"""

app.include_router(hr_router)


# ======================================================
# Health Check API
# ======================================================

@app.get("/health", tags=["System"])
def health_check():
    """
    بررسی وضعیت سیستم

    استفاده:
    - مانیتورینگ
    - Load Balancer
    - تست اولیه IIS
    """
    db_ok = test_db_connection()

    return {
        "status": "ok" if db_ok else "error",
        "database": "connected" if db_ok else "disconnected",
        "environment": settings.ENVIRONMENT
    }


# ======================================================
# Startup Event
# ======================================================

@app.on_event("startup")
def on_startup():
    """
    رویداد اجرای اولیه برنامه
    """
    logger.info("===================================")
    logger.info(" HR SYSTEM STARTING ")
    logger.info("===================================")
    logger.info(f"Environment : {settings.ENVIRONMENT}")
    logger.info(f"Debug       : {settings.DEBUG}")

    # تست اتصال دیتابیس
    if test_db_connection():
        logger.info("Database connection OK")
    else:
        logger.error("Database connection FAILED")


# ======================================================
# Shutdown Event
# ======================================================

@app.on_event("shutdown")
def on_shutdown():
    """
    رویداد خاموش شدن برنامه
    """
    logger.info("HR SYSTEM SHUTDOWN")
