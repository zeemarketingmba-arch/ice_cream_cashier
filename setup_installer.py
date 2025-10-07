#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء ملف تثبيت احترافي لبرنامج كاشير الآيس كريم
Setup 1.0.0.exe - الريال العماني
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class IceCreamSetupBuilder:
    def __init__(self):
        self.app_name = "كاشير الآيس كريم"
        self.app_version = "1.0.0"
        self.app_description = "برنامج كاشير متكامل لمحلات الآيس كريم - الريال العماني"
        self.company_name = "Augment Code"
        self.copyright = "© 2024 Augment Code. جميع الحقوق محفوظة."
        
        self.build_dir = "build_setup"
        self.dist_dir = "dist_setup"
        self.installer_dir = "installer"
        
    def create_directories(self):
        """إنشاء المجلدات المطلوبة"""
        print("📁 إنشاء مجلدات البناء...")
        
        for directory in [self.build_dir, self.dist_dir, self.installer_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
        
        print("✅ تم إنشاء المجلدات")
    
    def create_main_executable(self):
        """إنشاء الملف التنفيذي الرئيسي"""
        print("🔨 إنشاء الملف التنفيذي الرئيسي...")
        
        # إنشاء ملف spec محسن لـ PyInstaller
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['كاشير_مستقل_تماما.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ice_cream_cashier.html', '.'),
        ('templates', 'templates'),
        ('static', 'static'),
        ('*.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'flask',
        'jinja2',
        'werkzeug',
        'matplotlib',
        'numpy',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='app_icon.ico',
)
'''
        
        with open('ice_cream_setup.spec', 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print("✅ تم إنشاء ملف spec")
    
    def create_version_info(self):
        """إنشاء معلومات الإصدار"""
        print("📋 إنشاء معلومات الإصدار...")
        
        version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.company_name}'),
        StringStruct(u'FileDescription', u'{self.app_description}'),
        StringStruct(u'FileVersion', u'{self.app_version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'{self.copyright}'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'{self.app_name}'),
        StringStruct(u'ProductVersion', u'{self.app_version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        with open('version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        
        print("✅ تم إنشاء معلومات الإصدار")
    
    def create_app_icon(self):
        """إنشاء أيقونة التطبيق"""
        print("🎨 إنشاء أيقونة التطبيق...")
        
        # إنشاء أيقونة بسيطة باستخدام PIL إذا كانت متاحة
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # إنشاء صورة 256x256
            img = Image.new('RGBA', (256, 256), (70, 130, 180, 255))
            draw = ImageDraw.Draw(img)
            
            # رسم دائرة للآيس كريم
            draw.ellipse([50, 50, 206, 206], fill=(255, 255, 255, 255))
            draw.ellipse([60, 60, 196, 196], fill=(255, 182, 193, 255))
            
            # رسم مخروط
            draw.polygon([(128, 180), (100, 240), (156, 240)], fill=(222, 184, 135, 255))
            
            # حفظ كـ ICO
            img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print("✅ تم إنشاء أيقونة مخصصة")
            
        except ImportError:
            # إنشاء ملف أيقونة فارغ
            with open('app_icon.ico', 'wb') as f:
                f.write(b'')
            print("ℹ️ تم إنشاء ملف أيقونة فارغ (PIL غير متاح)")
    
    def build_executable(self):
        """بناء الملف التنفيذي"""
        print("🔨 بناء الملف التنفيذي...")
        
        try:
            # تشغيل PyInstaller
            cmd = ['pyinstaller', '--clean', '--noconfirm', 'ice_cream_setup.spec']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم بناء الملف التنفيذي بنجاح")
                return True
            else:
                print(f"❌ فشل في بناء الملف التنفيذي: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("❌ PyInstaller غير مثبت")
            return False
    
    def create_installer_script(self):
        """إنشاء سكريبت NSIS للتثبيت"""
        print("📦 إنشاء سكريبت التثبيت...")
        
        nsis_script = f'''# برنامج كاشير الآيس كريم - سكريبت التثبيت
# الإصدار {self.app_version} - الريال العماني

!define APP_NAME "{self.app_name}"
!define APP_VERSION "{self.app_version}"
!define APP_PUBLISHER "{self.company_name}"
!define APP_URL "https://augmentcode.com"
!define APP_DESCRIPTION "{self.app_description}"

# إعدادات عامة
Name "${{APP_NAME}} ${{APP_VERSION}}"
OutFile "Setup_${{APP_NAME}}_${{APP_VERSION}}.exe"
InstallDir "$PROGRAMFILES\\${{APP_NAME}}"
InstallDirRegKey HKLM "Software\\${{APP_NAME}}" "InstallDir"
RequestExecutionLevel admin

# واجهة التثبيت
!include "MUI2.nsh"

# الصفحات
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# اللغات
!insertmacro MUI_LANGUAGE "Arabic"
!insertmacro MUI_LANGUAGE "English"

# قسم التثبيت
Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    SetOverwrite ifnewer
    
    # نسخ الملفات
    File /r "dist\\{self.app_name}\\*.*"
    
    # إنشاء اختصارات
    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\{self.app_name}.exe"
    CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\{self.app_name}.exe"
    
    # تسجيل في النظام
    WriteRegStr HKLM "Software\\${{APP_NAME}}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayVersion" "${{APP_VERSION}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "Publisher" "${{APP_PUBLISHER}}"
    
    # إنشاء أداة إلغاء التثبيت
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

# قسم إلغاء التثبيت
Section "Uninstall"
    # حذف الملفات
    RMDir /r "$INSTDIR"
    
    # حذف الاختصارات
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
    RMDir /r "$SMPROGRAMS\\${{APP_NAME}}"
    
    # حذف التسجيل
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
    DeleteRegKey HKLM "Software\\${{APP_NAME}}"
SectionEnd
'''
        
        with open(os.path.join(self.installer_dir, 'installer.nsi'), 'w', encoding='utf-8') as f:
            f.write(nsis_script)
        
        print("✅ تم إنشاء سكريپت التثبيت")
    
    def create_license_file(self):
        """إنشاء ملف الترخيص"""
        print("📄 إنشاء ملف الترخيص...")
        
        license_text = f"""اتفاقية ترخيص برنامج كاشير الآيس كريم
الإصدار {self.app_version} - الريال العماني

{self.copyright}

شروط الاستخدام:
================

1. يُسمح باستخدام هذا البرنامج للأغراض التجارية والشخصية.

2. يُسمح بتوزيع البرنامج مع الاحتفاظ بحقوق الطبع والنشر.

3. لا يُسمح بتعديل الكود المصدري بدون إذن مكتوب.

4. البرنامج مقدم "كما هو" بدون أي ضمانات.

5. المطور غير مسؤول عن أي أضرار قد تنتج عن استخدام البرنامج.

المميزات:
=========

✅ نظام كاشير متكامل
✅ إدارة المنتجات والأسعار
✅ تقارير مالية مفصلة
✅ حساب الأرباح والخسائر
✅ نسخ احتياطية آمنة
✅ واجهة عربية سهلة الاستخدام
✅ العملة بالريال العماني

الدعم الفني:
============

للحصول على الدعم الفني أو الإبلاغ عن مشاكل:
- البريد الإلكتروني: support@augmentcode.com
- الموقع الإلكتروني: https://augmentcode.com

شكراً لاختيارك برنامج كاشير الآيس كريم!
"""
        
        with open(os.path.join(self.installer_dir, 'license.txt'), 'w', encoding='utf-8') as f:
            f.write(license_text)
        
        print("✅ تم إنشاء ملف الترخيص")
    
    def build_installer(self):
        """بناء ملف التثبيت"""
        print("📦 بناء ملف التثبيت...")
        
        try:
            # البحث عن NSIS
            nsis_paths = [
                r"C:\Program Files (x86)\NSIS\makensis.exe",
                r"C:\Program Files\NSIS\makensis.exe",
                "makensis.exe"
            ]
            
            nsis_exe = None
            for path in nsis_paths:
                if os.path.exists(path) or shutil.which(path):
                    nsis_exe = path
                    break
            
            if not nsis_exe:
                print("❌ NSIS غير مثبت")
                print("💡 حمل NSIS من: https://nsis.sourceforge.io/Download")
                return False
            
            # تشغيل NSIS
            cmd = [nsis_exe, os.path.join(self.installer_dir, 'installer.nsi')]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم إنشاء ملف التثبيت بنجاح")
                return True
            else:
                print(f"❌ فشل في إنشاء ملف التثبيت: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في بناء ملف التثبيت: {str(e)}")
            return False
    
    def build_complete_setup(self):
        """بناء حزمة التثبيت الكاملة"""
        print("🚀 بدء بناء حزمة التثبيت الكاملة...")
        print("=" * 60)
        
        try:
            # الخطوة 1: إنشاء المجلدات
            self.create_directories()
            
            # الخطوة 2: إنشاء الملفات المطلوبة
            self.create_version_info()
            self.create_app_icon()
            self.create_main_executable()
            
            # الخطوة 3: بناء الملف التنفيذي
            if not self.build_executable():
                return False
            
            # الخطوة 4: إنشاء ملفات التثبيت
            self.create_license_file()
            self.create_installer_script()
            
            # الخطوة 5: بناء ملف التثبيت
            if self.build_installer():
                print("=" * 60)
                print("🎉 تم إنشاء ملف التثبيت بنجاح!")
                print(f"📁 الملف: Setup_{self.app_name}_{self.app_version}.exe")
                print("=" * 60)
                return True
            else:
                print("❌ فشل في إنشاء ملف التثبيت")
                return False
                
        except Exception as e:
            print(f"❌ خطأ عام: {str(e)}")
            return False

def main():
    """الدالة الرئيسية"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    🍦 كاشير الآيس كريم 🍦                    ║")
    print("║                   إنشاء ملف التثبيت 1.0.0                   ║")
    print("║                   الريال العماني (ر.ع)                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    builder = IceCreamSetupBuilder()
    success = builder.build_complete_setup()
    
    if success:
        print("\n🎊 تم إنشاء ملف التثبيت الاحترافي بنجاح!")
        print("📦 يمكنك الآن توزيع البرنامج على أي جهاز Windows")
    else:
        print("\n❌ فشل في إنشاء ملف التثبيت")
        print("💡 تحقق من تثبيت PyInstaller و NSIS")
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
