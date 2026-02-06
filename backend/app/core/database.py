# backend/app/core/database.py

"""
این فایل مسئول:
- ایجاد اتصال به دیتابیس SQL Server
- مدیریت Session و Connection
- اجرای Query، View و Stored Procedure
است.

معادل بخش‌های زیر در Django:
- settings.py → DATABASES
- django.db.connections
- cursor.execute
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.core.config import settings


# ======================================================
# ساخت Connection String برای SQL Server
# ======================================================
"""
فرمت Connection String:

mssql+pyodbc://USER:PASSWORD@HOST:PORT/DB_NAME?driver=ODBC+Driver+17+for+SQL+Server

نکات مهم:
- حتماً ODBC Driver 17 یا 18 روی ویندوز نصب باشد
- fast_executemany برای Performance بهتر فعال شده
"""

#تنظیمات دیتابیس از فایل .env خوانده می‌شود و Connection String ساخته می‌شود
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}"
    f"?driver={settings.DB_DRIVER}"
)

# ======================================================
# ایجاد Engine (هسته‌ی اتصال به دیتابیس)
# ======================================================
engine: Engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,        # در حالت DEBUG کوئری‌ها چاپ می‌شوند
    pool_pre_ping=True,         # چک اتصال قبل از استفاده
    fast_executemany=True       # بسیار مهم برای SQL Server
)


# ======================================================
# Session Factory (برای ORM یا Transaction)
# ======================================================
"""
در این پروژه:
- ORM استفاده‌ی محدود دارد
- بیشتر View و SP داریم
اما Session برای Transaction لازم است
"""

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ======================================================
# Context Manager برای Session
# ======================================================
@contextmanager
def get_db_session():
    """
    این Context Manager معادل:

    with transaction.atomic():
        ...

    در Django است.

    استفاده:
        with get_db_session() as db:
            db.execute(...)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ======================================================
# اجرای Query ساده (SELECT از View یا Table)
# ======================================================
def execute_query(sql: str, params: dict | None = None):
    """
    اجرای Query ساده (SELECT)

    مناسب برای:
    - View ها (V_*)
    - SELECT از Table

    پارامترها:
        sql: متن Query
        params: پارامترهای Query (اختیاری)

    خروجی:
        لیست دیکشنری (mapping)
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return result.mappings().all()


# ======================================================
# اجرای Query تکی (یک رکورد)
# ======================================================
def execute_query_one(sql: str, params: dict | None = None):
    """
    اجرای Query که فقط یک رکورد برمی‌گرداند

    خروجی:
        dict | None
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return result.mappings().first()


# ======================================================
# اجرای Stored Procedure (بدون خروجی خاص)
# ======================================================
def execute_sp(sp_name: str, params: dict | None = None):
    """
    اجرای Stored Procedure که خروجی خاصی ندارد
    (مثلاً INSERT / UPDATE)

    مثال:
        EXEC HR_UpdateUser @NationalCode=:nc
    """
    sql = f"EXEC {sp_name}"
    if params:
        param_str = ", ".join([f"@{k}=:{k}" for k in params.keys()])
        sql = f"{sql} {param_str}"

    with engine.connect() as conn:
        conn.execute(text(sql), params or {})
        conn.commit()


# ======================================================
# اجرای Stored Procedure با خروجی
# ======================================================
def execute_sp_with_result(sp_name: str, params: dict | None = None):
    """
    اجرای Stored Procedure که خروجی دارد

    مناسب برای:
    - HR_GetTargetRole
    - HR_GetAssessorsAndEducators
    - سایر SP های HR

    خروجی:
        لیست دیکشنری
    """
    sql = f"EXEC {sp_name}"
    if params:
        param_str = ", ".join([f"@{k}=:{k}" for k in params.keys()])
        sql = f"{sql} {param_str}"

    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return result.mappings().all()


# ======================================================
# تست اتصال دیتابیس (برای health check)
# ======================================================
def test_db_connection() -> bool:
    """
    تست اتصال دیتابیس
    معادل api_ping ولی در سطح دیتابیس
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# ======================================================
# نمونه Query های HR (آموزشی)
# ======================================================
"""
این بخش فقط برای آموزش تیم است
و در پروژه واقعی بهتر است در repository هر ماژول قرار بگیرد
"""

def get_all_users_minimal():
    """
    دریافت اطلاعات حداقلی کاربران
    معادل:
        V_AllUserList
    """
    sql = """
        SELECT
            NationalCode,
            FirstName,
            LastName,
            Gender,
            ContractDate
        FROM V_AllUserList
    """
    return execute_query(sql)


def get_user_by_national_code(national_code: str):
    """
    دریافت اطلاعات کامل یک کاربر بر اساس کد ملی
    """
    sql = """
        SELECT *
        FROM Users
        WHERE NationalCode = :national_code
    """
    return execute_query_one(sql, {"national_code": national_code})
