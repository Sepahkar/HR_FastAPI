# backend/app/modules/hr/service.py

"""
Service Layer ماژول HR

مسئولیت این فایل:
- پیاده‌سازی منطق کسب‌وکار (Business Logic)
- ترکیب داده‌ها
- اعتبارسنجی سطح بالا
- فراخوانی Repository

معادل در Django:
- business.py
- بخشی از views.py
- بخشی از api.py
"""

from typing import List, Dict, Optional

from app.core.logging import get_logger
from app.modules.hr import repository

logger = get_logger(__name__)


# ======================================================
# Users
# ======================================================

def get_all_users_minimal() -> List[Dict]:
    """
    دریافت اطلاعات حداقلی همه کاربران

    این متد فقط نقش هماهنگ‌کننده دارد
    """
    logger.info("Fetching minimal users list")
    return repository.get_all_users_minimal()


def get_user_by_national_code(national_code: str) -> Optional[Dict]:
    """
    دریافت اطلاعات کامل یک کاربر بر اساس کد ملی

    اینجا می‌توان:
    - بررسی سطح دسترسی
    - ماسک کردن داده‌های حساس
    - محاسبات اضافی
    انجام داد
    """
    logger.info(f"Fetching user by national code: {national_code}")

    user = repository.get_user_by_national_code(national_code)

    if not user:
        logger.warning(f"User not found: {national_code}")
        return None

    return user


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    دریافت اطلاعات کاربر بر اساس نام کاربری
    """
    logger.info(f"Fetching user by username: {username}")
    return repository.get_user_by_username(username)


# ======================================================
# Teams
# ======================================================

def get_all_teams() -> List[Dict]:
    """
    دریافت همه تیم‌ها
    """
    logger.info("Fetching all teams")
    return repository.get_all_teams()


def get_active_service_teams() -> List[Dict]:
    """
    دریافت تیم‌های فعال در سرویس‌دهی
    """
    logger.info("Fetching active service teams")
    return repository.get_active_service_teams()


def get_active_evaluation_teams() -> List[Dict]:
    """
    دریافت تیم‌های فعال در ارزیابی
    """
    logger.info("Fetching active evaluation teams")
    return repository.get_active_evaluation_teams()


# ======================================================
# Roles
# ======================================================

def get_all_roles() -> List[Dict]:
    """
    دریافت همه سمت‌ها
    """
    logger.info("Fetching all roles")
    return repository.get_all_roles()


def get_user_roles_by_national_code(national_code: str) -> List[int]:
    """
    دریافت RoleId های یک کاربر
    """
    logger.info(f"Fetching roles for user {national_code}")
    return repository.get_user_roles_by_national_code(national_code)


# ======================================================
# UserTeamRole
# ======================================================

def get_user_team_roles(national_code: str) -> List[Dict]:
    """
    دریافت نقش‌های فعلی کاربر در تیم‌ها
    """
    logger.info(f"Fetching team roles for user {national_code}")
    return repository.get_user_team_roles(national_code)


def get_all_user_team_roles() -> List[Dict]:
    """
    دریافت همه نقش‌های کاربران
    """
    logger.info("Fetching all user team roles")
    return repository.get_all_user_team_roles()


# ======================================================
# Views (V_*)
# ======================================================

def get_view_role_target(filters: Dict) -> List[Dict]:
    """
    دریافت داده‌های View:
        V_HR_RoleTarget

    اینجا می‌توان:
    - اعتبارسنجی فیلترها
    - حذف فیلترهای غیرمجاز
    را انجام داد
    """
    logger.info(f"Fetching V_HR_RoleTarget with filters: {filters}")
    return repository.get_view_role_target(filters)


def get_view_role_team(role_ids: List[int], team_code: str) -> List[int]:
    """
    بررسی نقش‌های موجود در یک تیم
    """
    logger.info(
        f"Fetching V_RoleTeam for team={team_code}, roles={role_ids}"
    )
    return repository.get_view_role_team(role_ids, team_code)


# ======================================================
# Stored Procedures
# ======================================================

def sp_get_target_role(info_id: int, request_type: int):
    """
    اجرای Stored Procedure:
        HR_GetTargetRole
    """
    logger.info(
        f"Calling SP HR_GetTargetRole (info_id={info_id}, type={request_type})"
    )
    return repository.sp_get_target_role(info_id, request_type)


def sp_get_assessors_educators(
    team_code: str,
    info_id: int,
    role_id_target: int,
    level_id_target: int,
    superior_target: int,
    temporary: int,
    type_: int
):
    """
    اجرای Stored Procedure:
        HR_GetAssessorsAndEducators
    """
    logger.info(
        "Calling SP HR_GetAssessorsAndEducators "
        f"(team={team_code}, role={role_id_target})"
    )

    return repository.sp_get_assessors_educators(
        team_code=team_code,
        info_id=info_id,
        role_id_target=role_id_target,
        level_id_target=level_id_target,
        superior_target=superior_target,
        temporary=temporary,
        type_=type_
    )


def sp_get_team_manager(role_id: int, team_code: str):
    """
    اجرای Stored Procedure:
        HR_GetTeamManager
    """
    logger.info(
        f"Calling SP HR_GetTeamManager (role={role_id}, team={team_code})"
    )
    return repository.sp_get_team_manager(role_id, team_code)
