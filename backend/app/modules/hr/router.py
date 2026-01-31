# backend/app/modules/hr/router.py

"""
Router ماژول HR

مسئولیت این فایل:
- تعریف API Endpoint ها
- دریافت ورودی از Request
- فراخوانی Service Layer
- اعمال احراز هویت

معادل در Django:
- HR/urls.py
- HR/api.py (APIView ها)
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Optional

from app.core.auth import get_current_user, AuthenticatedUser
from app.core.logging import get_logger
from app.modules.hr import service
from app.modules.hr.schemas import (
    UserMinimal,
    UserFull,
    TeamOut,
    RoleOut
)

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/hr",
    tags=["HR"]
)

# ======================================================
# Users
# ======================================================

@router.get(
    "/users",
    response_model=List[UserMinimal]
)
def get_all_users(
    user: AuthenticatedUser = Depends(get_current_user),
    return_dict: bool = Query(False)
):
    """
    دریافت لیست همه کاربران (اطلاعات حداقلی)

    معادل:
        GET /api/all-users/
    """
    logger.info(f"User [{user.username}] requested all users")

    users = service.get_all_users_minimal()

    if return_dict:
        return {
            u["NationalCode"]: u
            for u in users
        }

    return users


@router.get(
    "/users/{national_code}",
    response_model=UserFull
)
def get_user_by_national_code(
    national_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    دریافت اطلاعات کامل یک کاربر بر اساس کد ملی

    معادل:
        GET /api/get-user/<national_code>/v2/
    """
    logger.info(
        f"User [{user.username}] requested user [{national_code}]"
    )

    result = service.get_user_by_national_code(national_code)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="کاربر یافت نشد"
        )

    return result


# ======================================================
# Teams
# ======================================================



# ======================================================
# Roles
# ======================================================

@router.get(
    "/roles",
    response_model=List[RoleOut]
)
def get_all_roles(
    user: AuthenticatedUser = Depends(get_current_user),
    return_dict: bool = Query(False)
):
    """
    دریافت لیست همه سمت‌ها

    معادل:
        GET /api/get-all-roles/
    """
    roles = service.get_all_roles()

    if return_dict:
        return {
            r["RoleId"]: r
            for r in roles
        }

    return roles


@router.get(
    "/users/{national_code}/roles",
    response_model=List[int]
)
def get_user_roles(
    national_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    دریافت RoleId های یک کاربر

    معادل:
        get-user-roles/<national_code>/v2/
    """
    return service.get_user_roles_by_national_code(national_code)


# ======================================================
# UserTeamRole
# ======================================================

@router.get(
    "/users/{national_code}/team-roles"
)
def get_user_team_roles(
    national_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    دریافت نقش‌های کاربر در تیم‌ها

    معادل:
        get-user-team-role/<national_code>/v2/
    """
    return service.get_user_team_roles(national_code)


# ======================================================
# Views (V_*)
# ======================================================

@router.post(
    "/view/role-target"
)
def get_view_role_target(
    filters: Dict,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    دریافت اطلاعات ویو V_HR_RoleTarget با فیلتر داینامیک

    معادل:
        get-v-role-target
    """
    logger.info(
        f"User [{user.username}] requested V_HR_RoleTarget"
    )
    return service.get_view_role_target(filters)


@router.post(
    "/view/role-team"
)
def get_view_role_team(
    role_ids: List[int],
    team_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    بررسی نقش‌های موجود در یک تیم

    معادل:
        get-v-role-team
    """
    return service.get_view_role_team(role_ids, team_code)


# ======================================================
# Stored Procedures
# ======================================================

@router.post(
    "/sp/get-target-role"
)
def call_sp_get_target_role(
    info_id: int,
    request_type: int,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    اجرای SP:
        HR_GetTargetRole

    معادل:
        call-sp-get-target-role
    """
    logger.info(
        f"User [{user.username}] called HR_GetTargetRole"
    )
    return service.sp_get_target_role(info_id, request_type)


@router.post(
    "/sp/get-assessors-educators"
)
def call_sp_get_assessors_educators(
    team_code: str,
    info_id: int,
    role_id_target: int,
    level_id_target: int,
    superior_target: int,
    temporary: int = 0,
    type_: int = 0,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    اجرای SP:
        HR_GetAssessorsAndEducators
    """
    return service.sp_get_assessors_educators(
        team_code=team_code,
        info_id=info_id,
        role_id_target=role_id_target,
        level_id_target=level_id_target,
        superior_target=superior_target,
        temporary=temporary,
        type_=type_
    )


@router.get("/me")
def get_current_user_info(
    user: AuthenticatedUser = Depends(get_current_user)
):
    return {
        "username": user.username,
        "full_name": user.full_username
    }
