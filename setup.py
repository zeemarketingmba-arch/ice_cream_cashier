"""
ملف إعداد لإنشاء ملف تنفيذي لبرنامج كاشير الآيس كريم
"""

from cx_Freeze import setup, Executable
import sys
import os

# إعدادات البناء
build_exe_options = {
    "packages": ["tkinter", "json", "os", "datetime", "pathlib"],
    "excludes": ["flask", "jinja2", "werkzeug"],  # استبعاد المكتبات غير المطلوبة
    "include_files": [
        ("ice_cream_cashier.html", "ice_cream_cashier.html"),
        ("كيفية_التشغيل.txt", "كيفية_التشغيل.txt"),
    ],
    "optimize": 2,
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

# إعدادات الملف التنفيذي
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # لإخفاء نافذة الأوامر

# معلومات التطبيق
executables = [
    Executable(
        "ice_cream_exe.py",
        base=base,
        target_name="كاشير_الآيس_كريم.exe",
        icon=None,  # يمكن إضافة أيقونة لاحقاً
        shortcut_name="كاشير الآيس كريم",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="كاشير الآيس كريم",
    version="1.0",
    description="برنامج كاشير متكامل لمحل الآيس كريم",
    author="Augment Agent",
    options={"build_exe": build_exe_options},
    executables=executables,
)
