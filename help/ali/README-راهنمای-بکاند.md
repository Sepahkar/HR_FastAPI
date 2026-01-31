# 📚 راهنمای سامانه بک‌اند HR

یک راهنمای جامع برای درک و کار با معماری بک‌اند سامانه منابع انسانی

---

## 📋 فهرست مطالب

1. [معماری کلی سیستم](#معماری-کلی-سیستم)
2. [ساختار پروژه](#ساختار-پروژه)
3. [شرح فایل‌ها و مسئولیت‌ها](#شرح-فایل‌ها-و-مسئولیت‌ها)
4. [جریان درخواست (Request Flow)](#جریان-درخواست--request-flow)
5. [مثال‌های عملی](#مثال‌های-عملی)
6. [راهنمای توسعه](#راهنمای-توسعه)

---

## معماری کلی سیستم

### 🏗️ لایه‌های معماری

```
Frontend (Vue.js)
       ↓
API Gateway / Router (FastAPI Router)
       ↓
Service Layer (Business Logic)
       ↓
Repository Layer (Data Access)
       ↓
Database (SQL Server)
```

### 🔑 اصول طراحی

1. **Separation of Concerns**: هر لایه یک مسئولیت خاص دارد
2. **Dependency Injection**: وابستگی‌ها به صورت پارامتر ارسال می‌شوند
3. **Type Safety**: استفاده از Type Hints برای امنیت نوع
4. **Windows Authentication**: احراز هویت از طریق IIS

---

## ساختار پروژه

```
backend/
├── run.py                          # نقطه شروع برنامه
├── app/
│   ├── __init__.py
│   ├── main.py                     # تنظیم FastAPI App
│   ├── core/                       # لایه‌های پایه‌ای
│   │   ├── config.py               # تنظیمات پروژه
│   │   ├── database.py             # اتصال دیتابیس
│   │   ├── auth.py                 # احراز هویت
│   │   ├── logging.py              # سیستم logging
│   │   └── __init__.py
│   ├── modules/                    # ماژول‌های کاری
│   │   ├── __init__.py
│   │   └── hr/                     # ماژول منابع انسانی
│   │       ├── __init__.py
│   │       ├── router.py           # API Endpoints
│   │       ├── service.py          # Business Logic
│   │       ├── repository.py       # Database Queries
│   │       ├── schemas.py          # Pydantic Models
│   │       └── __pycache__/
│   └── shared/                     # ابزارها و توابع مشترک
│       └── utils.py
└── logs/                           # فایل‌های Log

```

---

## شرح فایل‌ها و مسئولیت‌ها

### 🚀 فایل‌های اجرایی و تنظیمات

#### `backend/run.py`
**نقطه شروع برنامه (Entry Point)**

**مسئولیت:**
- اجرای برنامه FastAPI با Uvicorn
- تشخیص محیط DEV یا PRODUCTION
- تعیین Host و Port
- تنظیم تعداد Workers

**نحوه استفاده:**
```bash
# اجرا از ریشه پروژه:
python backend/run.py

# یا برای توسعه:
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

**معادل در Django:**
- `manage.py runserver`

---

#### `backend/app/main.py`
**تنظیم برنامه FastAPI**

**مسئولیت:**
- ایجاد شیء FastAPI
- ثبت Router ها
- تنظیم CORS برای Frontend
- تنظیم Middleware ها
- Event Handlers (Startup/Shutdown)
- Health Check Endpoint

**اجزای کلیدی:**
```python
app = FastAPI(title="HR System")

# Router ها:
app.include_router(hr_router)  # ماژول HR

# CORS برای اتصال Frontend Vue:
CORSMiddleware(...)

# Health Check:
@app.get("/health")
```

**معادل در Django:**
- `urls.py` برای ثبت URL ها
- `settings.py` برای تنظیمات Middleware
- `wsgi.py` برای ایجاد App

---

#### `backend/app/core/config.py`
**تنظیمات پروژه (Settings)**

**مسئولیت:**
- مدیریت تمام تنظیمات پروژه
- خواندن متغیرهای محیطی (.env)
- تمییز بین DEV و PRODUCTION

**متغیرهای مهم:**
- `ENVIRONMENT`: DEV یا PRODUCTION
- `DEBUG`: فعال/خاموش کردن حالت Debug
- `SECRET_KEY`: کلید رمزنگاری
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: تنظیمات دیتابیس
- `LANGUAGE_CODE`, `TIME_ZONE`: تنظیمات محلی‌سازی

**نحوه استفاده:**
```python
from app.core.config import settings

if settings.ENVIRONMENT == "DEV":
    # کار خاص برای محیط توسعه
    pass
```

**معادل در Django:**
- `settings.py`

---

### 🗄️ لایه دیتابیس

#### `backend/app/core/database.py`
**مدیریت اتصال دیتابیس**

**مسئولیت:**
- ایجاد Connection String برای SQL Server
- ایجاد Engine (SQLAlchemy)
- ایجاد Session Manager
- فراهم‌سازی متدهای اجرای Query

**متدهای مهم:**

1. **`execute_query(sql)`**
   - اجرای SELECT که چند ردیف برمی‌گرداند
   ```python
   results = execute_query("SELECT * FROM Users")
   # خروجی: [{'Name': 'علی', ...}, ...]
   ```

2. **`execute_query_one(sql)`**
   - اجرای SELECT که یک ردیف برمی‌گرداند
   ```python
   user = execute_query_one("SELECT * FROM Users WHERE ID = 1")
   # خروجی: {'Name': 'علی', ...}
   ```

3. **`execute_sp_with_result(sp_name, params)`**
   - اجرای Stored Procedure
   ```python
   result = execute_sp_with_result("SP_GetUserReport", {"UserID": 1})
   ```

**معادل در Django:**
- `django.db.connections`
- `Model.objects.raw(sql)`
- `cursor.execute()`

---

### 🔐 احراز هویت

#### `backend/app/core/auth.py`
**سیستم احراز هویت (Authentication)**

**مسئولیت:**
- خواندن اطلاعات کاربر از IIS
- ایجاد کاربر احراز هویت شده
- بررسی دسترسی (Authorization)

**نحوه کار:**

IIS مسئول Windows Authentication است → هدر `Remote-User` را می‌فرستد → FastAPI آن را می‌خواند

**متدهای مهم:**

1. **`get_username_from_iis(request)`**
   ```python
   # خواندن نام کاربری از هدر IIS
   username = get_username_from_iis(request)
   # نتیجه: "m.sepahkar" یا "m.sepahkar@eit"
   ```

2. **`get_current_user(request)`**
   ```python
   # استخراج کاربر فعلی (برای Dependency Injection)
   user = get_current_user(request)
   # نتیجه: AuthenticatedUser(username="m.sepahkar")
   ```

**استفاده در Router:**
```python
@router.get("/users")
def get_users(user: AuthenticatedUser = Depends(get_current_user)):
    # کاربر فعلی خودکار چک می‌شود
    return [...]
```

**معادل در Django:**
- `RemoteUserAuthentication`
- `request.user`
- `@login_required` Decorator

---

#### `backend/app/core/logging.py`
**سیستم Log‌گیری**

**مسئولیت:**
- تنظیم Logger برای رویدادهای مختلف
- ذخیره Log ها در فایل و Console

**استفاده:**
```python
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("پیام معلومات")
logger.error("پیام خطا")
```

---

### 📡 ماژول HR (منابع انسانی)

هر ماژول دارای 4 لایه است:

#### `backend/app/modules/hr/schemas.py`
**تعریف ساختار داده‌ها**

**مسئولیت:**
- تعریف ساختار ورودی و خروجی API
- Validation خودکار داده‌ها
- مستندسازی Swagger

**مثال:**
```python
class UserMinimal(BaseModel):
    """اطلاعات حداقلی کاربر"""
    NationalCode: str
    FirstName: str
    LastName: str
    ContractDate: Optional[str]
```

**استفاده در Router:**
```python
@router.get("/users", response_model=List[UserMinimal])
def get_users():
    return [...]  # FastAPI خودکار validate می‌کند
```

**معادل در Django:**
- `serializers.py` (Django REST Framework)

---

#### `backend/app/modules/hr/router.py`
**تعریف API Endpoints**

**مسئولیت:**
- تعریف تمام API Endpoint های ماژول
- Parsing ورودی‌ها (Query, Body, Header)
- فراخوانی Service Layer
- بررسی احراز هویت

**ساختار Endpoint:**
```python
@router.get("/users", response_model=List[UserMinimal])
def get_all_users(
    user: AuthenticatedUser = Depends(get_current_user),
    return_dict: bool = Query(False)
):
    """
    GET /api/hr/users
    - Query: return_dict
    - Authorization: Windows Auth
    """
    return service.get_all_users_minimal()
```

**Prefix تمام Route ها:**
```python
router = APIRouter(
    prefix="/api/hr",
    tags=["HR"]
)
# نتیجه: /api/hr/users, /api/hr/user/{id}, ...
```

**معادل در Django:**
- `urls.py`
- `views.py` (APIView ها)
- `viewsets.py` (GenericViewSet ها)

---

#### `backend/app/modules/hr/service.py`
**منطق کسب‌وکار (Business Logic)**

**مسئولیت:**
- پیاده‌سازی قوانین تجاری
- ترکیب داده‌های مختلف
- Validation سطح بالا
- فراخوانی Repository

**ویژگی:**
- **بدون دانش از HTTP**: فقط داده و منطق
- **بدون دانش از SQL**: از Repository استفاده می‌کند
- **پیاده‌سازی قوانین تجاری**

**مثال:**
```python
def get_all_users_minimal() -> List[Dict]:
    """
    اگر نیاز باشد:
    - بررسی سطح دسترسی
    - ماسک کردن داده‌های حساس
    - محاسبات اضافی
    """
    return repository.get_all_users_minimal()
```

**معادل در Django:**
- `business.py` (اگر وجود داشته باشد)
- بخشی از `views.py`

---

#### `backend/app/modules/hr/repository.py`
**دسترسی به داده‌ها (Data Access Layer)**

**مسئولیت:**
- نوشتن Query های SQL
- اجرای Stored Procedure ها
- **بدون هیچ منطق کسب‌وکار**

**متدها:**
```python
def get_all_users_minimal() -> List[Dict]:
    """نمونه: SELECT اطلاعات حداقلی کاربران"""
    sql = "SELECT NationalCode, FirstName, LastName FROM V_AllUserList"
    return execute_query(sql)

def get_user_by_national_code(national_code: str) -> Optional[Dict]:
    """نمونه: SELECT یک کاربر"""
    sql = """
    SELECT * FROM Users WHERE NationalCode = :nc
    """
    return execute_query_one(sql, {"nc": national_code})

def get_employee_report(year: int) -> List[Dict]:
    """نمونه: اجرای Stored Procedure"""
    return execute_sp_with_result(
        "SP_EmployeeAnnualReport",
        {"Year": year}
    )
```

**معادل در Django:**
- `models.py` و ORM
- `cursor.execute()`
- `Model.objects.filter(...)`

---

### 🛠️ ابزارها و توابع مشترک

#### `backend/app/shared/utils.py`
**توابع مشترک برای کل پروژه**

**استفاده برای:**
- تبدیل تاریخ (میلادی ↔ شمسی)
- فرمت‌کردن شماره‌ها
- محاسبات مشترک
- توابع کمکی

---

## جریان درخواست (Request Flow)

### مثال: دریافت لیست کاربران

```
1. Frontend (Vue.js)
   ↓
   GET /api/hr/users?return_dict=false
   ↓
2. Router: backend/app/modules/hr/router.py
   - دریافت query parameter
   - بررسی احراز هویت
   - فراخوانی Service
   ↓
3. Service: backend/app/modules/hr/service.py
   - پیاده‌سازی منطق تجاری
   - فراخوانی Repository
   ↓
4. Repository: backend/app/modules/hr/repository.py
   - نوشتن SQL Query
   - اجرای Query روی دیتابیس
   ↓
5. Database: SQL Server
   - بازگرداندن داده‌ها
   ↓
6. Response Flow (برگشت)
   Repository → Service → Router → Schema Validation → JSON Response
   ↓
7. Frontend
   - دریافت JSON
   - نمایش در Vue Component
```

### Diagram تفصیلی

```
┌─────────────────┐
│   Frontend      │
│   (Vue.js)      │
└────────┬────────┘
         │ HTTP GET /api/hr/users
         │
┌────────▼────────┐
│   main.py       │ ← تعریف FastAPI App
│  (تنطیم های کلی)  │
└────────┬────────┘
         │
┌────────▼────────────────────┐
│   hr/router.py              │ ← @router.get("/users")
│   • دریافت ورودی            │
│   • بررسی احراز هویت          │
│   • فراخوانی Service         │
└────────┬────────────────────┘
         │ return service.get_all_users_minimal()
         │
┌────────▼────────────────────┐
│   hr/service.py             │ ← get_all_users_minimal()
│   • منطق کسب‌وکار            │
│   • Validation سطح بالا      │
│   • فراخوانی Repository      │
└────────┬────────────────────┘
         │ return repository.get_all_users_minimal()
         │
┌────────▼────────────────────┐
│   hr/repository.py          │ ← get_all_users_minimal()
│   • نوشتن SQL Query         │
│   • اجرای Query             │
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│   core/database.py          │ ← execute_query(sql)
│   • اتصال به دیتابیس         │
│   • اجرای Query             │
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│   SQL Server                │
│   • V_AllUserList           │
└────────┬────────────────────┘
         │ List[Dict] → [{...}, {...}]
         │
┌────────▼────────────────────┐
│   hr/schemas.py             │ ← List[UserMinimal]
│   • Validation و تبدیل      │
└────────┬────────────────────┘
         │ List[UserMinimal]
         │
┌────────▼────────────────────┐
│   HTTP Response             │
│   [                         │
│     {                       │
│       "NationalCode": "...", │
│       "FirstName": "...",    │
│       "LastName": "..."      │
│     }                       │
│   ]                         │
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│   Frontend (Vue.js)         │
│   نمایش داده‌ها              │
└─────────────────────────────┘
```

---

## مثال‌های عملی

### 🎯 مثال 1: افزودن Endpoint جدید برای دریافت کاربر با کد ملی

**مرحله 1: تعریف Schema** (`hr/schemas.py`)
```python
class UserFull(BaseModel):
    """تمام اطلاعات کاربر"""
    NationalCode: str
    FirstName: str
    LastName: str
    Email: str
    Position: str
    Department: str
    ContractDate: str
```

**مرحله 2: اضافه کردن متد به Repository** (`hr/repository.py`)
```python
def get_user_by_national_code(national_code: str) -> Optional[Dict]:
    """دریافت یک کاربر با کد ملی"""
    sql = """
    SELECT 
        NationalCode,
        FirstName,
        LastName,
        Email,
        Position,
        Department,
        ContractDate
    FROM Users
    WHERE NationalCode = :nc
    """
    return execute_query_one(sql, {"nc": national_code})
```

**مرحله 3: اضافه کردن متد به Service** (`hr/service.py`)
```python
def get_user_by_national_code(national_code: str) -> Optional[Dict]:
    """دریافت یک کاربر"""
    logger.info(f"Fetching user: {national_code}")
    return repository.get_user_by_national_code(national_code)
```

**مرحله 4: اضافه کردن Endpoint به Router** (`hr/router.py`)
```python
@router.get("/user/{national_code}", response_model=UserFull)
def get_user(
    national_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    دریافت اطلاعات کامل یک کاربر
    GET /api/hr/user/0012345678
    """
    result = service.get_user_by_national_code(national_code)
    if not result:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    return result
```

### 🎯 مثال 2: اجرای Stored Procedure

**مرحله 1: Repository** (`hr/repository.py`)
```python
def get_employee_salary_report(year: int) -> List[Dict]:
    """دریافت گزارش حقوق سالانه"""
    return execute_sp_with_result(
        "SP_EmployeeSalaryReport",
        {"Year": year}
    )
```

**مرحله 2: Service** (`hr/service.py`)
```python
def get_salary_report(year: int) -> List[Dict]:
    """گزارش حقوق"""
    logger.info(f"Fetching salary report for year {year}")
    return repository.get_employee_salary_report(year)
```

**مرحله 3: Router** (`hr/router.py`)
```python
@router.get("/reports/salary")
def get_salary_report(
    year: int = Query(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    گزارش حقوق کاربران
    GET /api/hr/reports/salary?year=1403
    """
    return service.get_salary_report(year)
```

---

## راهنمای توسعه

### ✅ چک‌لیست برای افزودن Feature جدید

- [ ] **1. Schema بسازید** (`hr/schemas.py`)
  ```python
  class NewFeatureSchema(BaseModel):
      field1: str
      field2: int
  ```

- [ ] **2. Repository متد بسازید** (`hr/repository.py`)
  ```python
  def get_new_feature_data() -> List[Dict]:
      sql = "SELECT ... FROM ..."
      return execute_query(sql)
  ```

- [ ] **3. Service متد بسازید** (`hr/service.py`)
  ```python
  def get_new_feature() -> List[Dict]:
      return repository.get_new_feature_data()
  ```

- [ ] **4. Router Endpoint بسازید** (`hr/router.py`)
  ```python
  @router.get("/new-feature", response_model=List[NewFeatureSchema])
  def get_new_feature(user: AuthenticatedUser = Depends(get_current_user)):
      return service.get_new_feature()
  ```

- [ ] **5. Test کنید**
  ```bash
  curl http://localhost:8000/api/hr/new-feature
  ```

---

### 🔄 جریان منطقی توسعه

```
تقاضا (Requirement)
        ↓
Schema (ساختار داده)
        ↓
Repository (SQL Query)
        ↓
Service (منطق تجاری)
        ↓
Router (Endpoint)
        ↓
Test
```

---

### 🚨 نکات مهم

#### 1. **هرگز منطق کسب‌وکار را در Router نشود بنویسید**
```python
# ❌ اشتباه
@router.get("/users")
def get_users():
    users = execute_query("SELECT ...")
    # منطق تجاری اینجا
    filtered = [u for u in users if u['Age'] > 20]
    return filtered

# ✅ درست
@router.get("/users")
def get_users():
    return service.get_adult_users()
```

#### 2. **هرگز SQL نشود در Service بنویسید**
```python
# ❌ اشتباه
def get_users():
    result = execute_query("SELECT ...")  # SQL اینجا
    return result

# ✅ درست
def get_users():
    return repository.get_users()
```

#### 3. **همیشه Type Hints استفاده کنید**
```python
# ❌ اشتباه
def get_user(code):
    return ...

# ✅ درست
def get_user(national_code: str) -> Optional[Dict]:
    return ...
```

#### 4. **همیشه Logging استفاده کنید**
```python
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("پیام معلومات")
logger.error("پیام خطا")
logger.warning("پیام هشدار")
```

#### 5. **احراز هویت را کنترل کنید**
```python
# الزامی بررسی کاربر:
def get_users(user: AuthenticatedUser = Depends(get_current_user)):
    # user فقط وارد شده‌ها می‌توانند اینجا بیایند
    pass
```

---

### 📊 جدول معادل‌ها با Django

| قسمت | Django | FastAPI Project |
|------|--------|-----------------|
| Entry Point | `manage.py` | `backend/run.py` |
| تنطیم های کلی | `settings.py` | `core/config.py` |
| URL ها | `urls.py` | `modules/*/router.py` |
| API | `APIView` / `viewsets` | `@router` decorator |
| منطق تجاری | `views.py` / `business.py` | `modules/*/service.py` |
| دسترسی داده‌ها | `models.py` / `ORM` | `modules/*/repository.py` |
| Validation | `serializers.py` | `schemas.py` |
| Authentication | `authentication.py` | `core/auth.py` |
| دیتابیس | `django.db` | `core/database.py` |
| Logging | `logging` | `core/logging.py` |

---

### 🎓 یادگیری مراحل

#### مرحله 1: درک ساختار
1. این فایل را مطالعه کنید
2. فایل‌های موجود را بازی کنید
3. جریان درخواست را ترسیم کنید

#### مرحله 2: اجرای سیستم
```bash
cd backend
python run.py
```

#### مرحله 3: تست API ها
```bash
# مثال: دریافت لیست کاربران
curl http://localhost:8000/api/hr/users
```

#### مرحله 4: افزودن Feature
1. شروع با Schema
2. Repository متد
3. Service متد
4. Router Endpoint

---

## 📞 سوالات متداول

### سوال 1: کجا باید منطق جدید اضافه کنم؟
**جواب:** اگر منطق تجاری است → Service | اگر SQL است → Repository | اگر HTTP است → Router

### سوال 2: چگونه Stored Procedure اجرا کنم؟
**جواب:** `execute_sp_with_result()` در Repository استفاده کنید

### سوال 3: چگونه از دیتابیس خطا handle کنم؟
**جواب:** Try/except و Logging استفاده کنید

### سوال 4: کاربر جاری را کجا بگیری؟
**جواب:** `Depends(get_current_user)` در Router استفاده کنید

### سوال 5: چگونه Custom Validation بسازم؟
**جواب:** Pydantic `validator` decorator در Schema استفاده کنید

---

## 🔗 روابط بین فایل‌ها

```
main.py (تنطیم app)
   ↑
   ├─→ config.py (تنظیمات)
   ├─→ auth.py (احراز هویت)
   ├─→ logging.py (Log کردن)
   └─→ router.py (endpoints)
         ↑
         ├─→ schemas.py (validation)
         └─→ service.py (منطق)
              ↑
              └─→ repository.py (SQL)
                   ↑
                   └─→ database.py (اتصال)
```

---

## نتیجه‌گیری

برای سالم ماندن پروژه باید:
1. هر لایه مسئول یک کار باشد
2. وابستگی‌ها یک سو باشند (Router → Service → Repository → Database)
3. کد تکراری نشود (Utilities میشود استفاده کنند)
4. Logging مداوم انجام شود
5. Type Hints استفاده شود

با رعایت این اصول می‌توان پروژه را بسادگی توسعه داد و مشکلات کمتر داشته باشد.

---

**آخرین ویرایش:** 1402/11/08
**نویسنده:** تیم توسعه
