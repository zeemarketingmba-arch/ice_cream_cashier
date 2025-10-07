; IceCreamShopSetup.iss
[Setup]
AppName=نظام إدارة محل الآيس كريم | Ice Cream Shop Management System
AppVersion=1.0.0
DefaultDirName={pf}\IceCreamShop            ; مجلد التثبيت
DefaultGroupName=IceCreamShop
OutputBaseFilename=Setup_1.0.0              ; ينتج Setup_1.0.0.exe
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
; الأيقونة الرئيسـية للبرنامج والمثبت
SetupIconFile=icecream.ico
UninstallDisplayIcon={app}\app.exe
; لغات التثبيت (عربي + إنجليزي)
; يحتاج Inno Setup 6.2+ حيث يدعم العربية رسميًا
LanguageDetectionMethod=UILanguage
WizardStyle=modern
DefaultLanguage=en  ; يبدأ بالإنجليزية ويمكن للمستخدم التبديل
; ملفات اللغة
[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "ar"; MessagesFile: "compiler:Languages\Arabic.isl"

[Files]
; انسخ ملف البرنامج التنفيذي
Source: "dist\app.exe";    DestDir: "{app}"; Flags: ignoreversion
; إذا كان لديك مجلد templates/static مضمنًا بجوار exe ضمّه هكذا:
; Source: "dist\templates\*"; DestDir: "{app}\templates"; Flags: recursesubdirs
; Source: "dist\static\*";    DestDir: "{app}\static";    Flags: recursesubdirs

[Icons]
; اختصار في قائمة ابدأ
Name: "{group}\نظام إدارة محل الآيس كريم"; Filename: "{app}\app.exe"; WorkingDir: "{app}"
; اختصار على سطح المكتب
Name: "{userdesktop}\نظام إدارة محل الآيس كريم"; Filename: "{app}\app.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "إنشاء اختصار على سطح المكتب / Create a desktop shortcut"; Flags: unchecked

[Run]
; تشغيل البرنامج بعد انتهاء التثبيت (اختياري – مُعلَّق افتراضيًا)
Filename: "{app}\app.exe"; Description: "تشغيل البرنامج الآن / Run program"; Flags: nowait postinstall unchecked
