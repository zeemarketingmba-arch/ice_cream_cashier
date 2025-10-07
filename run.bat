@echo off
chcp 65001 >nul
echo ========================================
echo       برنامج كاشير الآيس كريم 🍦
echo ========================================
echo.

echo جاري التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    echo يمكنك تحميله من: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python متاح
echo.

echo جاري تثبيت المتطلبات...
pip install Flask Flask-SQLAlchemy Werkzeug Jinja2 python-dateutil
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    echo جرب تشغيل الأمر التالي يدوياً:
    echo pip install Flask Flask-SQLAlchemy Werkzeug Jinja2 python-dateutil
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات بنجاح
echo.

echo جاري إنشاء البيانات التجريبية...
python init_data.py
echo.

echo جاري تشغيل البرنامج...
echo ستفتح نافذة المتصفح تلقائياً على العنوان:
echo http://127.0.0.1:5000
echo.
echo لإيقاف البرنامج اضغط Ctrl+C
echo.

timeout /t 3 >nul
start http://127.0.0.1:5000
python app.py

pause
