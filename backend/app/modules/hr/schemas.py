# backend/app/modules/hr/schemas.py

"""
Schemas ماژول HR

مسئولیت این فایل:
- تعریف ساختار داده‌های ورودی و خروجی API
- Validation داده‌ها
- مستندسازی خودکار API (Swagger)

معادل در Django:
- serializers.py (DRF)
"""

from pydantic import BaseModel, Field
from typing import Optional


# ======================================================
# Base Schemas
# ======================================================

class HRBaseSchema(BaseModel):
    """
    کلاس پایه برای همه Schemaهای HR

    تنظیمات مشترک:
    - orm_mode برای سازگاری با ORM (اگر بعداً استفاده شد)
    """
    class Config:
        orm_mode = True


# ======================================================
# User Schemas
# ======================================================

class UserMinimal(HRBaseSchema):
    """
    اطلاعات حداقلی کاربر
    استفاده در:
        - لیست کاربران
        - Dropdown ها
    """
    NationalCode: str = Field(..., description="کد ملی")
    FirstName: str = Field(..., description="نام")
    LastName: str = Field(..., description="نام خانوادگی")
    ContractDate: Optional[str] = Field(
        None,
        description="تاریخ شروع همکاری (شمسی)"
    )


class UserFull(HRBaseSchema):
    """
    اطلاعات کامل کاربر
    استفاده در:
        - پروفایل کاربر
        - فرم ویرایش اطلاعات
    """

    # اطلاعات هویتی
    NationalCode: str
    UserName: str
    FirstName: str
    LastName: str

    FirstNameEnglish: Optional[str]
    LastNameEnglish: Optional[str]
    FatherName: Optional[str]

    # اطلاعات شخصی
    Gender: bool
    BirthDate: Optional[str]
    BirthDateMiladi: Optional[str]

    # اطلاعات قرارداد
    ContractDate: Optional[str]
    ContractDateMiladi: Optional[str]
    ContractEndDate: Optional[str]
    ContractEndDateMiladi: Optional[str]

    # وضعیت‌ها
    IsActive: bool
    About: Optional[str]

    # Foreign Keys (به‌صورت ID)
    DegreeType: Optional[int]
    MarriageStatus: Optional[int]
    MilitaryStatus: Optional[int]
    Religion: Optional[int]
    ContractType: Optional[int]
    UserStatus: Optional[int]

    # آدرس‌ها و ارتباطات
    BirthCity: Optional[int]
    IdentityCity: Optional[int]
    LivingAddress: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "NationalCode": "1234567890",
                "UserName": "m.sepahkar@eit",
                "FirstName": "محمد",
                "LastName": "سپهرکار",
                "Gender": True,
                "ContractDate": "1400/01/01",
                "IsActive": True
            }
        }


# ======================================================
# Team Schemas
# ======================================================

class TeamOut(HRBaseSchema):
    """
    اطلاعات تیم
    """
    TeamCode: str = Field(..., description="کد تیم")
    TeamName: str = Field(..., description="نام تیم")

    ActiveInService: bool = Field(
        ...,
        description="فعال در سرویس‌دهی"
    )
    ActiveInEvaluation: bool = Field(
        ...,
        description="فعال در ارزیابی"
    )


# ======================================================
# Role Schemas
# ======================================================

class RoleOut(HRBaseSchema):
    """
    اطلاعات سمت
    """
    RoleId: int = Field(..., description="کد سمت")
    RoleName: str = Field(..., description="نام سمت")

    HasLevel: bool = Field(
        False,
        description="آیا دارای سطح است؟"
    )
    HasSuperior: bool = Field(
        False,
        description="آیا ارشد دارد؟"
    )


# ======================================================
# UserTeamRole Schemas
# ======================================================

class UserTeamRoleOut(HRBaseSchema):
    """
    نقش کاربر در تیم
    """
    NationalCode: str = Field(..., description="کد ملی")
    TeamCode: str = Field(..., description="کد تیم")
    RoleId: int = Field(..., description="کد سمت")

    LevelId: Optional[int] = Field(
        None,
        description="سطح سمت"
    )

    Superior: bool = Field(
        False,
        description="آیا ارشد است؟"
    )

    StartDate: Optional[str] = Field(
        None,
        description="تاریخ شروع"
    )

    EndDate: Optional[str] = Field(
        None,
        description="تاریخ پایان"
    )


# ======================================================
# View Schemas (V_*)
# ======================================================

class ViewRoleTargetOut(HRBaseSchema):
    """
    خروجی View:
        V_HR_RoleTarget
    """
    RoleID: int
    RoleTargetID: int
    RoleTargetName: str

    LevelID: Optional[int]
    LevelIdTargetID: Optional[int]

    Superior: bool
    SuperiorTarget: bool

    Education: bool
    Evaluation: bool
    PmChange: bool
    ITChange: bool

    RequestType: int


# ======================================================
# Generic Response Schemas
# ======================================================

class SuccessResponse(HRBaseSchema):
    """
    پاسخ موفق عمومی
    """
    success: bool = True
    message: Optional[str] = None


class ErrorResponse(HRBaseSchema):
    """
    پاسخ خطای عمومی
    """
    success: bool = False
    message: str
