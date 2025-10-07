#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشغل برنامج كاشير الآيس كريم
يبحث عن Python ويشغل التطبيق المناسب
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def find_python():
    """البحث عن Python في النظام"""
    # قائمة المواقع الشائعة
    common_paths = [
        r"C:\Python39\python.exe",
        r"C:\Python38\python.exe", 
        r"C:\Python37\python.exe",
        r"C:\Python310\python.exe",
        r"C:\Python311\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Users\{}\AppData\Local\Programs\Python\Python39\python.exe".format(os.getenv('USERNAME', '')),
        r"C:\Users\{}\AppData\Local\Programs\Python\Python38\python.exe".format(os.getenv('USERNAME', '')),
        r"C:\Users\{}\AppData\Local\Programs\Python\Python310\python.exe".format(os.getenv('USERNAME', '')),
        r"C:\Users\{}\AppData\Local\Programs\Python\Python311\python.exe".format(os.getenv('USERNAME', '')),
        r"C:\Users\{}\AppData\Local\Programs\Python\Python312\python.exe".format(os.getenv('USERNAME', '')),
        r"C:\Program Files\Python39\python.exe",
        r"C:\Program Files\Python38\python.exe",
        r"C:\Program Files (x86)\Python39\python.exe",
        r"C:\Program Files (x86)\Python38\python.exe",
    ]
    
    # البحث في المواقع الشائعة
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # البحث في PATH
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'python'
    except:
        pass
    
    try:
        result = subprocess.run(['py', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'py'
    except:
        pass
    
    return None

def run_desktop_app(python_path):
    """تشغيل تطبيق سطح المكتب"""
    try:
        print("🚀 جاري تشغيل تطبيق سطح المكتب...")
        
        # تجربة النسخة المستقلة أولاً
        if os.path.exists('ice_cream_standalone.py'):
            result = subprocess.run([python_path, 'ice_cream_standalone.py'])
            if result.returncode == 0:
                return True
        
        # تجربة النسخة المتقدمة
        if os.path.exists('desktop_app.py'):
            result = subprocess.run([python_path, 'desktop_app.py'])
            if result.returncode == 0:
                return True
                
        return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        return False

def run_web_app(python_path):
    """تشغيل تطبيق الويب"""
    try:
        print("🌐 جاري تشغيل تطبيق الويب...")
        
        # تجربة النسخة المبسطة
        if os.path.exists('simple_app.py'):
            print("تشغيل النسخة المبسطة...")
            subprocess.Popen([python_path, 'simple_app.py'])
            return True
            
        # تجربة النسخة الكاملة
        if os.path.exists('app.py'):
            print("تشغيل النسخة الكاملة...")
            subprocess.Popen([python_path, 'app.py'])
            return True
            
        return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل تطبيق الويب: {e}")
        return False

def run_html_version():
    """تشغيل النسخة التجريبية HTML"""
    try:
        html_file = Path('ice_cream_cashier.html')
        if html_file.exists():
            print("🌐 فتح النسخة التجريبية في المتصفح...")
            webbrowser.open(html_file.absolute().as_uri())
            return True
        return False
    except Exception as e:
        print(f"❌ خطأ في فتح النسخة التجريبية: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    🍦 كاشير الآيس كريم 🍦                    ║")
    print("║                      مشغل البرنامج الذكي                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # البحث عن Python
    print("🔍 جاري البحث عن Python...")
    python_path = find_python()
    
    if python_path:
        print(f"✅ تم العثور على Python: {python_path}")
        print()
        
        # عرض الخيارات
        print("اختر نوع التطبيق:")
        print("1️⃣  تطبيق سطح المكتب (مستقل)")
        print("2️⃣  تطبيق ويب (متصفح)")
        print("3️⃣  النسخة التجريبية (HTML)")
        print("4️⃣  خروج")
        print()
        
        try:
            choice = input("اختر رقم (1-4): ").strip()
            
            if choice == '1':
                if not run_desktop_app(python_path):
                    print("❌ فشل في تشغيل تطبيق سطح المكتب")
                    print("🔄 جاري تجربة تطبيق الويب...")
                    run_web_app(python_path)
                    
            elif choice == '2':
                if run_web_app(python_path):
                    print("✅ تم تشغيل تطبيق الويب!")
                    print("🌐 افتح المتصفح على: http://localhost:8000")
                else:
                    print("❌ فشل في تشغيل تطبيق الويب")
                    
            elif choice == '3':
                if not run_html_version():
                    print("❌ لم يتم العثور على النسخة التجريبية")
                    
            elif choice == '4':
                print("👋 وداعاً!")
                return
                
            else:
                print("❌ اختيار غير صحيح")
                
        except KeyboardInterrupt:
            print("\n👋 تم الإلغاء")
            
    else:
        print("❌ لم يتم العثور على Python!")
        print()
        print("🔄 جاري تشغيل النسخة التجريبية...")
        if not run_html_version():
            print("❌ لم يتم العثور على أي نسخة قابلة للتشغيل")
            print()
            print("💡 الحلول:")
            print("• ثبت Python من: https://www.python.org/downloads/")
            print("• تأكد من تحديد 'Add Python to PATH' أثناء التثبيت")
    
    print()
    input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
