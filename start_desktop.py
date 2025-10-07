#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل مباشر لتطبيق سطح المكتب
"""

import sys
import os

# إضافة المجلد الحالي للمسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🍦 مرحباً بك في برنامج كاشير الآيس كريم!")
    print("🚀 جاري تشغيل تطبيق سطح المكتب...")
    print()
    
    # تجربة تشغيل النسخة المستقلة
    try:
        from ice_cream_standalone import SimpleIceCreamCashier
        print("✅ تم تحميل النسخة المستقلة")
        app = SimpleIceCreamCashier()
        app.run()
    except ImportError as e:
        print(f"❌ خطأ في تحميل النسخة المستقلة: {e}")
        
        # تجربة النسخة المتقدمة
        try:
            from desktop_app import IceCreamCashier
            print("✅ تم تحميل النسخة المتقدمة")
            app = IceCreamCashier()
            app.run()
        except ImportError as e2:
            print(f"❌ خطأ في تحميل النسخة المتقدمة: {e2}")
            print()
            print("💡 جاري تشغيل النسخة البديلة...")
            
            # تشغيل نسخة مبسطة جداً
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.title("🍦 كاشير الآيس كريم")
            root.geometry("800x600")
            
            # رسالة ترحيب
            welcome_label = tk.Label(root, 
                                   text="🍦 مرحباً بك في كاشير الآيس كريم!", 
                                   font=('Arial', 20, 'bold'))
            welcome_label.pack(pady=50)
            
            info_label = tk.Label(root, 
                                text="هذه نسخة تجريبية مبسطة\nللحصول على النسخة الكاملة، تأكد من وجود جميع الملفات", 
                                font=('Arial', 12))
            info_label.pack(pady=20)
            
            def show_message():
                messagebox.showinfo("معلومات", "مرحباً! هذا برنامج كاشير الآيس كريم\nالنسخة التجريبية")
            
            test_button = tk.Button(root, 
                                  text="اختبار البرنامج", 
                                  font=('Arial', 14, 'bold'),
                                  bg='#3498db', 
                                  fg='white',
                                  command=show_message)
            test_button.pack(pady=20)
            
            instructions_text = """
تعليمات التشغيل:

1. تأكد من وجود ملف ice_cream_standalone.py
2. أو استخدم النسخة التجريبية في المتصفح
3. أو ثبت المكتبات المطلوبة للنسخة الكاملة

الملفات المطلوبة:
• ice_cream_standalone.py (النسخة المستقلة)
• desktop_app.py (النسخة المتقدمة)
• ice_cream_cashier.html (النسخة التجريبية)
            """
            
            instructions_label = tk.Label(root, 
                                        text=instructions_text, 
                                        font=('Arial', 10),
                                        justify='right')
            instructions_label.pack(pady=20)
            
            root.mainloop()

except Exception as e:
    print(f"❌ خطأ عام: {e}")
    print()
    print("💡 الحلول البديلة:")
    print("1. افتح ملف ice_cream_cashier.html في المتصفح")
    print("2. تأكد من وجود جميع ملفات البرنامج")
    print("3. جرب تشغيل: python ice_cream_standalone.py")
    
    input("\nاضغط Enter للخروج...")
