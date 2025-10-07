@echo off
chcp 65001 >nul
cls

:start
echo ================================================================
echo                Ice Cream Cashier - Omani Rial
echo                    Main Launcher v1.0.0
echo ================================================================
echo.

echo Welcome to Ice Cream Cashier!
echo Complete cashier system for ice cream shops
echo Currency: Omani Rial (OMR)
echo.

echo ================================================================
echo Choose your option:
echo ================================================================
echo.

echo 1. HTML Demo Version (Instant)
echo    File: ice_cream_cashier.html
echo    Works in any web browser
echo    No installation needed
echo.

echo 2. Standalone Desktop App (Python)
echo    File: standalone_app.py
echo    Full desktop application
echo    Requires Python
echo.

echo 3. Enhanced Desktop App (Python)
echo    File: enhanced_app.py
echo    Advanced features
echo    Requires Python
echo.

echo 4. Backup Manager
echo    File: backup_manager.py
echo    Manage data backups
echo.

echo 5. Advanced Settings
echo    File: advanced_settings.py
echo    Customize products and prices
echo.

echo 6. Create Simple EXE File
echo    Creates standalone executable
echo    No Python needed for end users
echo.

echo 7. Create Professional Setup Installer
echo    Creates Setup.exe with installer
echo    Professional distribution
echo.

echo 8. Install Python (Fix Issues)
echo    Comprehensive Python installation guide
echo    Fixes common problems
echo.

echo 9. Show All Files
echo    Display all available files
echo.

echo 0. Exit
echo.

echo ================================================================
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto :html_version
if "%choice%"=="2" goto :standalone_version
if "%choice%"=="3" goto :enhanced_version
if "%choice%"=="4" goto :backup_manager
if "%choice%"=="5" goto :advanced_settings
if "%choice%"=="6" goto :create_exe
if "%choice%"=="7" goto :create_setup
if "%choice%"=="8" goto :install_python
if "%choice%"=="9" goto :show_files
if "%choice%"=="0" goto :exit

echo ERROR: Invalid choice!
pause
goto :start

:html_version
echo.
echo Starting HTML Demo Version...
echo.
if exist "ice_cream_cashier.html" (
    start "" "ice_cream_cashier.html"
    echo HTML demo opened in your default browser
) else (
    echo ERROR: ice_cream_cashier.html not found
)
goto :end

:standalone_version
echo.
echo Starting Standalone Desktop App...
echo.
if exist "كاشير_مستقل_تماما.py" (
    python "كاشير_مستقل_تماما.py"
) else if exist "standalone_app.py" (
    python "standalone_app.py"
) else (
    echo ERROR: Standalone app file not found
)
goto :end

:enhanced_version
echo.
echo Starting Enhanced Desktop App...
echo.
if exist "ice_cream_exe.py" (
    python "ice_cream_exe.py"
) else if exist "enhanced_app.py" (
    python "enhanced_app.py"
) else (
    echo ERROR: Enhanced app file not found
)
goto :end

:backup_manager
echo.
echo Starting Backup Manager...
echo.
if exist "نسخة_احتياطية.py" (
    python "نسخة_احتياطية.py"
) else if exist "backup_manager.py" (
    python "backup_manager.py"
) else (
    echo ERROR: Backup manager file not found
)
goto :end

:advanced_settings
echo.
echo Starting Advanced Settings...
echo.
if exist "إعدادات_متقدمة.py" (
    python "إعدادات_متقدمة.py"
) else if exist "advanced_settings.py" (
    python "advanced_settings.py"
) else (
    echo ERROR: Advanced settings file not found
)
goto :end

:create_exe
echo.
echo Creating Simple EXE File...
echo.
if exist "create_exe_simple.bat" (
    call "create_exe_simple.bat"
) else if exist "إنشاء_exe_سريع.bat" (
    call "إنشاء_exe_سريع.bat"
) else (
    echo ERROR: EXE creation script not found
)
goto :end

:create_setup
echo.
echo Creating Professional Setup Installer...
echo.
if exist "create_setup_installer.bat" (
    call "create_setup_installer.bat"
) else if exist "إنشاء_Setup_1.0.0.bat" (
    call "إنشاء_Setup_1.0.0.bat"
) else (
    echo ERROR: Setup creation script not found
)
goto :end

:install_python
echo.
echo Python Installation Guide...
echo.
if exist "تثبيت_Python_الصحيح.bat" (
    call "تثبيت_Python_الصحيح.bat"
) else if exist "install_python_correct.bat" (
    call "install_python_correct.bat"
) else (
    echo ERROR: Python installation guide not found
)
goto :end

:show_files
echo.
echo Available Files:
echo ================================================================
echo.

echo Web Versions:
if exist "ice_cream_cashier.html" (echo OK: ice_cream_cashier.html - HTML demo) else (echo MISSING: ice_cream_cashier.html)
echo.

echo Desktop Applications:
if exist "كاشير_مستقل_تماما.py" (echo OK: Standalone app - Arabic filename) else (echo MISSING: Standalone app)
if exist "ice_cream_exe.py" (echo OK: ice_cream_exe.py - Enhanced version) else (echo MISSING: ice_cream_exe.py)
if exist "desktop_app.py" (echo OK: desktop_app.py - Advanced version) else (echo MISSING: desktop_app.py)
if exist "app.py" (echo OK: app.py - Flask web version) else (echo MISSING: app.py)
echo.

echo Tools:
if exist "نسخة_احتياطية.py" (echo OK: Backup manager - Arabic filename) else (echo MISSING: Backup manager)
if exist "إعدادات_متقدمة.py" (echo OK: Advanced settings - Arabic filename) else (echo MISSING: Advanced settings)
echo.

echo Launchers:
if exist "مشغل_شامل.bat" (echo OK: Main launcher - Arabic filename) else (echo MISSING: Main launcher)
if exist "launcher_main.bat" (echo OK: launcher_main.bat - This file) else (echo MISSING: launcher_main.bat)
if exist "create_exe_simple.bat" (echo OK: create_exe_simple.bat - EXE creator) else (echo MISSING: EXE creator)
if exist "create_setup_installer.bat" (echo OK: create_setup_installer.bat - Setup creator) else (echo MISSING: Setup creator)
echo.

echo Documentation:
if exist "README_النهائي.txt" (echo OK: Final README - Arabic filename) else (echo MISSING: Final README)
if exist "دليل_المستخدم_الشامل.txt" (echo OK: User guide - Arabic filename) else (echo MISSING: User guide)
if exist "README_Setup_والتوزيع.txt" (echo OK: Setup guide - Arabic filename) else (echo MISSING: Setup guide)
echo.

goto :end

:exit
echo.
echo Thank you for using Ice Cream Cashier!
echo Goodbye!
echo.
exit /b 0

:end
echo.
echo ================================================================
echo Operation completed!
echo ================================================================
echo.
echo Press any key to return to main menu, or close this window
pause >nul
goto :start
