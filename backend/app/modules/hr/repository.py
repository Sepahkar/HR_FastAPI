# backend/app/modules/hr/repository.py

"""
Repository لایه‌ی ارتباط با دیتابیس برای ماژول HR

مسئولیت این فایل:
- اجرای SELECT از Table / View
- اجرای Stored Procedure
- هیچ منطق کسب‌وکار (Business Logic) اینجا نوشته نمی‌شود

معادل در Django:
- models.py
- objects.filter(...)
- cursor.execute(...)
"""

from sqlalchemy import text
from typing import List, Dict, Optional

from app.core.database import (
    execute_query,
    execute_query_one,
    execute_sp_with_result
)

# ======================================================
# Users
# ======================================================

def get_all_users_minimal() -> List[Dict]:
    """
    دریافت اطلاعات حداقلی همه کاربران

    معادل:
        Users.objects.only(...)
        یا
        V_AllUserList

    خروجی:
        [
            {
                "NationalCode": "...",
                "FirstName": "...",
                "LastName": "...",
                "Gender": true,
                "ContractDate": "1402/01/01"
            }
        ]
    """
    sql = """
        SELECT
            NationalCode,
            FirstName,
            LastName,
            ContractDate
        FROM V_AllUserList
    """
    return execute_query(sql)


def get_user_by_national_code(national_code: str) -> Optional[Dict]:
    """
    دریافت اطلاعات کامل یک کاربر بر اساس کد ملی

    معادل:
        Users.objects.filter(NationalCode=...).first()
    """
    sql = """
        SELECT *
        FROM Users
        WHERE NationalCode = :national_code
    """
    return execute_query_one(sql, {"national_code": national_code})


def get_user_by_username(username: str) -> Optional[Dict]:
    """
    دریافت اطلاعات کاربر بر اساس نام کاربری

    مثال:
        m.sepahkar@eit
    """
    sql = """
        SELECT *
        FROM Users
        WHERE UserName = :username
    """
    return execute_query_one(sql, {"username": username})


# ======================================================
# Teams
# ======================================================

def get_all_teams() -> List[Dict]:
    """
    دریافت همه تیم‌ها

    معادل:
        Team.objects.all()
    """
    sql = """
        SELECT *
        FROM Team
    """
    return execute_query(sql)


def get_active_service_teams() -> List[Dict]:
    """
    دریافت تیم‌های فعال در سرویس‌دهی

    معادل:
        Team.objects.filter(ActiveInService=True)
    """
    sql = """
        SELECT *
        FROM HR_Team
        WHERE ActiveInService = 1
    """
    return execute_query(sql)


def get_active_evaluation_teams() -> List[Dict]:
    """
    دریافت تیم‌های فعال در ارزیابی
    """
    sql = """
        SELECT *
        FROM Team
        WHERE ActiveInEvaluation = 1
    """
    return execute_query(sql)


# ======================================================
# Roles
# ======================================================

def get_all_roles() -> List[Dict]:
    """
    دریافت همه سمت‌ها
    """
    sql = """
        SELECT *
        FROM Role
    """
    return execute_query(sql)


def get_user_roles_by_national_code(national_code: str) -> List[int]:
    """
    دریافت لیست RoleId های یک کاربر بر اساس کد ملی

    معادل:
        UserTeamRole.objects.filter(...).values_list("RoleId")
    """
    sql = """
        SELECT RoleId
        FROM UserTeamRole
        WHERE NationalCode = :national_code
    """
    rows = execute_query(sql, {"national_code": national_code})
    return [row["RoleId"] for row in rows]


# ======================================================
# UserTeamRole
# ======================================================

def get_user_team_roles(national_code: str) -> List[Dict]:
    """
    دریافت نقش‌های فعلی کاربر در تیم‌ها

    معادل:
        UserTeamRole.objects.filter(NationalCode=...)
    """
    sql = """
        SELECT *
        FROM UserTeamRole
        WHERE NationalCode = :national_code
          AND EndDate IS NULL
    """
    return execute_query(sql, {"national_code": national_code})


def get_all_user_team_roles() -> List[Dict]:
    """
    دریافت همه نقش‌های کاربران (فعال و غیرفعال)
    """
    sql = """
        SELECT *
        FROM V_UserTeamRole
    """
    return execute_query(sql)


# ======================================================
# Views (V_*)
# ======================================================

def get_view_role_target(filters: Dict) -> List[Dict]:
    """
    دریافت اطلاعات ویو V_HR_RoleTarget با فیلتر داینامیک

    filters مثال:
        {
            "RoleID": 12,
            "RequestType": 1
        }
    """

    where_clauses = []
    params = {}

    for key, value in filters.items():
        if value not in ("", None):
            where_clauses.append(f"{key} = :{key}")
            params[key] = value

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT *
        FROM V_HR_RoleTarget
        {where_sql}
    """

    return execute_query(sql, params)


def get_view_role_team(role_ids: List[int], team_code: str) -> List[int]:
    """
    بررسی اینکه چه Role هایی در یک تیم وجود دارند

    معادل:
        V_RoleTeam.objects.filter(...)
    """
    sql = """
        SELECT RoleID
        FROM V_RoleTeam
        WHERE TeamCode = :team_code
          AND RoleID IN :role_ids
    """
    rows = execute_query(sql, {
        "team_code": team_code,
        "role_ids": tuple(role_ids)
    })
    return [row["RoleID"] for row in rows]


# ======================================================
# Stored Procedures (HR)
# ======================================================

def sp_get_target_role(info_id: int, request_type: int):
    """
    اجرای SP:
        HR_GetTargetRole

    معادل:
        CallSpGetTargetRole
    """
    return execute_sp_with_result(
        "dbo.HR_GetTargetRole",
        {
            "ID": info_id,
            "Type": request_type
        }
    )


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
    اجرای SP:
        HR_GetAssessorsAndEducators
    """
    return execute_sp_with_result(
        "dbo.HR_GetAssessorsAndEducators",
        {
            "TeamCode": team_code,
            "InfoID": info_id,
            "RoleIdTarget": role_id_target,
            "LevelIdTarget": level_id_target,
            "SuperiorTarget": superior_target,
            "Temporary": temporary,
            "Type": type_
        }
    )


def sp_get_team_manager(role_id: int, team_code: str):
    """
    اجرای SP:
        HR_GetTeamManager
    """
    return execute_sp_with_result(
        "dbo.HR_GetTeamManager",
        {
            "RoleId": role_id,
            "TeamCode": team_code
        }
    )
