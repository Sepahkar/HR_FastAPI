# *********************************** HR System – راهنمای راه‌اندازی (مرحله ۴)
# راه‌اندازی کامل سایت در IIS (گام‌به‌گام برای فرد مبتدی)

در این مرحله فرض می‌کنیم که:
- مراحل ۱، ۲ و ۳ را با موفقیت انجام داده‌اید
- Backend به‌صورت تستی با دستور `python run.py` اجرا شده و سالم است
- Frontend به‌صورت محلی (index.html) درست نمایش داده می‌شود
- هیچ تجربه قبلی جدی با IIS ندارید

هدف این مرحله:
- تعریف سایت Frontend در IIS
- فعال‌سازی Windows Authentication
- اتصال Frontend به Backend از طریق Reverse Proxy
- باز کردن سایت از طریق IIS در مرورگر

در پایان این مرحله:
- سایت را از طریق یک URL (مثلاً http://localhost:8080) باز می‌کنید
- نام کاربر ویندوزی نمایش داده می‌شود
- لیست کاربران نمایش داده می‌شود

---

## 1️⃣ آشنایی خیلی کوتاه با IIS (برای شروع)

IIS یک وب‌سرور ویندوزی است.
در این پروژه:
- IIS فایل‌های Frontend (HTML, CSS, JS) را سرو می‌کند
- IIS کار احراز هویت ویندوز (Active Directory) را انجام می‌دهد
- درخواست‌های `/api/*` را به Backend (FastAPI) هدایت می‌کند

به زبان ساده:
- Frontend ← IIS
- Backend ← FastAPI (روی پورت 8000)
- IIS بین این دو واسطه است

---

## 2️⃣ باز کردن IIS Manager

1. دکمه Start ویندوز را بزنید
2. عبارت `IIS` را تایپ کنید
3. روی **Internet Information Services (IIS) Manager** کلیک کنید

اگر پنجره IIS Manager باز شد، یعنی IIS روی سیستم شما نصب است.

---

## 3️⃣ ساخت سایت جدید برای Frontend

### مرحله 3-1: انتخاب Sites

در پنل سمت چپ IIS Manager:
- روی نام کامپیوتر کلیک کنید
- سپس روی پوشه **Sites** کلیک کنید

---

### مرحله 3-2: افزودن سایت جدید

1. روی **Sites** راست‌کلیک کنید
2. گزینه **Add Website…** را انتخاب کنید

پنجره‌ای باز می‌شود.

---

### مرحله 3-3: پر کردن اطلاعات سایت

در پنجره Add Website این مقادیر را وارد کنید:

- Site name:
  HR-Frontend

- Physical path:
  مسیر فولدر frontend پروژه، مثلاً:
  C:\Projects\HR\frontend

- Binding:
  - Type: http
  - IP address: All Unassigned
  - Port: 8080
  - Host name: (خالی بگذارید)

سپس روی **OK** کلیک کنید.

---

## 4️⃣ تست اولیه سایت Frontend در IIS

مرورگر را باز کنید و آدرس زیر را وارد کنید:

http://localhost:8080

اگر همه‌چیز درست باشد:
- صفحه سامانه منابع انسانی باز می‌شود
- ممکن است هنوز داده‌ها نیایند (طبیعی است)

اگر صفحه باز نشد:
- IIS Manager → Sites → HR-Frontend
- وضعیت سایت باید **Started** باشد
- اگر Stopped بود، راست‌کلیک → Start

---

## 5️⃣ فعال‌سازی Windows Authentication

### مرحله 5-1: ورود به تنظیمات Authentication

1. در IIS Manager روی سایت **HR-Frontend** کلیک کنید
2. در وسط صفحه روی **Authentication** دوبار کلیک کنید

---

### مرحله 5-2: تنظیم Authentication

در لیست Authentication:

- **Windows Authentication**
  - Right Click → Enable

- **Anonymous Authentication**
  - Right Click → Disable

این مرحله بسیار مهم است، چون:
- نام کاربر ویندوزی از اینجا به Backend منتقل می‌شود

---

## 6️⃣ نصب و فعال‌سازی Reverse Proxy (ARR)

برای اینکه IIS درخواست‌های API را به FastAPI بفرستد، نیاز به Reverse Proxy داریم.

### مرحله 6-1: نصب ARR (اگر نصب نیست)

اگر گزینه‌های ARR را ندارید:
- باید **Application Request Routing** نصب شود
- این کار معمولاً توسط مدیر سیستم انجام می‌شود

---

### مرحله 6-2: فعال‌سازی Proxy

1. در IIS Manager روی نام کامپیوتر (بالای Sites) کلیک کنید
2. در وسط صفحه روی **Application Request Routing Cache** کلیک کنید
3. در پنل سمت راست روی **Server Proxy Settings** کلیک کنید
4. گزینه **Enable Proxy** را تیک بزنید
5. روی **Apply** کلیک کنید

---

## 7️⃣ ساخت Rule برای هدایت API به FastAPI

### مرحله 7-1: ورود به URL Rewrite

1. روی سایت **HR-Frontend** کلیک کنید
2. در وسط صفحه روی **URL Rewrite** دوبار کلیک کنید
3. روی **Add Rule(s)…** کلیک کنید
4. گزینه **Reverse Proxy** را انتخاب کنید

---

### مرحله 7-2: تنظیم Reverse Proxy

در پنجره بازشده:

- Inbound Rules:
  - Enter the URL of the server:  
    http://127.0.0.1:8000

- تیک گزینه:
  - Enable SSL Offloading (اگر وجود داشت)

روی **OK** کلیک کنید.

---

### مرحله 7-3: محدود کردن به مسیر /api

پس از ساخت Rule:
- Rule ساخته‌شده را باز کنید
- شرط (Condition) را طوری تنظیم کنید که:
  فقط درخواست‌هایی که با `/api/` شروع می‌شوند هدایت شوند

به این معنا:
- http://localhost:8080/api/... → FastAPI
- بقیه مسیرها → Frontend

---

## 8️⃣ اجرای Backend در کنار IIS

در این مرحله:
- IIS فقط Frontend را اجرا می‌کند
- Backend باید جداگانه اجرا شود

در Command Prompt:

cd C:\Projects\HR\backend
venv\Scripts\activate
python run.py

این پنجره باید باز بماند.

---

## 9️⃣ تست نهایی از طریق IIS

مرورگر را باز کنید و آدرس زیر را وارد کنید:

http://localhost:8080

انتظار داریم:
- صفحه Frontend باز شود
- نام کاربر ویندوزی نمایش داده شود
- لیست کاربران نمایش داده شود

همچنین این آدرس را تست کنید:

http://localhost:8080/api/hr/me

اگر JSON کاربر را دیدید:
- Reverse Proxy درست کار می‌کند
- Authentication درست انجام شده است

---

## 10️⃣ جمع‌بندی مرحله چهارم

در پایان این مرحله:

- سایت Frontend در IIS تعریف شده است
- Windows Authentication فعال است
- درخواست‌های API به FastAPI هدایت می‌شوند
- سایت از طریق IIS در مرورگر باز می‌شود

اگر هر کدام از این موارد درست کار نکرد:
- به مرحله بعد (خطاها) مراجعه کنید
- یا از مسئول پروژه کمک بگیرید

---

