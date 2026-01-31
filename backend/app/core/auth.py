# backend/app/core/auth.py

"""
این فایل مسئول احراز هویت (Authentication) کاربران است.

معادل در Django:
- RemoteUserAuthentication
- CustomRemoteUserMiddleware
- request.user

در معماری جدید:
- IIS مسئول احراز هویت ویندوز است
- FastAPI فقط هدرها را می‌خواند
"""

from fastapi import Request, HTTPException, Depends
from typing import Optional

from app.core.config import settings


# ======================================================
# مدل ساده کاربر احراز هویت شده
# ======================================================
class AuthenticatedUser:
    """
    معادل request.user در Django
    """

    def __init__(
        self,
        username: str,
        full_username: str | None = None,
        national_code: str | None = None,
    ):
        self.username = username              # مثلا: m.sepahkar
        self.full_username = full_username    # مثلا: m.sepahkar@eit
        self.national_code = national_code    # بعداً از DB پر می‌شود

    def __repr__(self):
        return f"<User {self.full_username}>"



# ======================================================
# استخراج نام کاربری از IIS (Windows Auth)
# ======================================================
def get_username_from_iis(request: Request):
    """
    دریافت نام کاربر از IIS یا Fake Header
    """

    headers = request.headers

    # همه headerها lowercase و dash-style هستند
    raw_user = (
        headers.get("x-windows-user")       # Fake Header یا IIS
        or headers.get("remote-user")       # IIS واقعی
        or headers.get("logon-user")        # IIS واقعی
    )

    print("RAW USER FROM HEADERS:", raw_user)

    if not raw_user:
        return None

    # فقط نام کاربر بدون دامنه
    if "\\" in raw_user:
        raw_user = raw_user.split("\\")[-1]

    if "@" in raw_user:
        raw_user = raw_user.split("@")[0]

    return raw_user.lower()





# ======================================================
# Dependency اصلی احراز هویت
# ======================================================
def get_current_user(request: Request) -> AuthenticatedUser:
    """
    Dependency اصلی FastAPI
    معادل request.user در Django

    استفاده در Router:
        @router.get("/users")
        def get_users(user: AuthenticatedUser = Depends(get_current_user)):
            ...
    """
    # ===============================
    # حالت DEV (بدون IIS)
    # ===============================
    if settings.ENVIRONMENT == "DEV":
        if not settings.DEV_USER:
            raise HTTPException(
                status_code=500,
                detail="DEV_USER در env تنظیم نشده است"
            )

        username = settings.DEV_USER.split("@")[0]

        return AuthenticatedUser(
            username=username,
            full_username=settings.DEV_USER
        )

    # ===============================
    # حالت PRODUCTION (IIS)
    # ===============================
    username = get_username_from_iis(request)
    if not username:
        raise HTTPException(
            status_code=401,
            detail="کاربر احراز هویت نشده است (IIS)"
        )

    return AuthenticatedUser(
        username=username,
        full_username=f"{username}@eit"
    )



# ======================================================
# Dependency اختیاری (اگر فقط لاگین مهم نیست)
# ======================================================
def get_optional_user(request: Request) -> Optional[AuthenticatedUser]:
    """
    اگر کاربر لاگین نبود، None برمی‌گرداند
    (مثلا برای api_ping)
    """

    try:
        return get_current_user(request)
    except HTTPException:
        return None
