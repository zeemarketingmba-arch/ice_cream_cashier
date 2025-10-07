#!/bin/bash

echo "========================================"
echo "       برنامج كاشير الآيس كريم 🍦"
echo "========================================"
echo

echo "جاري التحقق من Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python غير مثبت! يرجى تثبيت Python أولاً"
    exit 1
fi

echo "✅ Python متاح"
echo

echo "جاري تثبيت المتطلبات..."
pip3 install Flask Flask-SQLAlchemy Werkzeug Jinja2 python-dateutil
if [ $? -ne 0 ]; then
    echo "❌ فشل في تثبيت المتطلبات"
    echo "جرب تشغيل الأمر التالي يدوياً:"
    echo "pip3 install Flask Flask-SQLAlchemy Werkzeug Jinja2 python-dateutil"
    exit 1
fi

echo "✅ تم تثبيت المتطلبات بنجاح"
echo

echo "جاري إنشاء البيانات التجريبية..."
python3 init_data.py
echo

echo "جاري تشغيل البرنامج..."
echo "ستحتاج لفتح المتصفح على العنوان:"
echo "http://127.0.0.1:5000"
echo
echo "لإيقاف البرنامج اضغط Ctrl+C"
echo

sleep 3
python3 app.py
