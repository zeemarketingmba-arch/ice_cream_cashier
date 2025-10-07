@echo off
chcp 65001 >nul
cls

echo ================================================================
echo                Ice Cream Cashier - Omani Rial
echo                   Create Simple EXE File
echo ================================================================
echo.

echo Creating a standalone executable file...
echo Currency: Omani Rial (OMR)
echo.

echo ================================================================
echo Checking requirements...
echo ================================================================
echo.

REM Check Python
echo [1/2] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python first
    echo Use: install_python_correct.bat
    pause
    exit /b 1
)
echo OK: Python is available

REM Check PyInstaller
echo [2/2] Checking PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyInstaller not installed
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        echo Try: pip install --user pyinstaller
        pause
        exit /b 1
    )
    echo OK: PyInstaller installed
) else (
    echo OK: PyInstaller is available
)

echo.
echo ================================================================
echo Building executable file...
echo ================================================================
echo.

echo [1/3] Cleaning old files...
if exist "dist" rmdir /s /q "dist" >nul 2>&1
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "*.spec" del /q "*.spec" >nul 2>&1
echo OK: Old files cleaned

echo [2/3] Creating executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "IceCream_Cashier_v1.0.0" ^
    --add-data "ice_cream_cashier.html;." ^
    --add-data "*.txt;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.simpledialog ^
    --hidden-import tkinter.filedialog ^
    --exclude-module flask ^
    --exclude-module jinja2 ^
    --exclude-module werkzeug ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --clean ^
    --noconfirm ^
    كاشير_مستقل_تماما.py

if errorlevel 1 (
    echo ERROR: Failed to create executable
    echo.
    echo Possible solutions:
    echo 1. Make sure the Python file exists
    echo 2. Try running the program first: python كاشير_مستقل_تماما.py
    echo 3. Check tkinter: python -m tkinter
    echo.
    pause
    exit /b 1
)

echo OK: Executable created

echo [3/3] Creating distribution package...
set PACKAGE_NAME=IceCream_Package_v1.0.0
if exist "%PACKAGE_NAME%" rmdir /s /q "%PACKAGE_NAME%" >nul 2>&1
mkdir "%PACKAGE_NAME%"

REM Copy executable
if exist "dist\IceCream_Cashier_v1.0.0.exe" (
    copy "dist\IceCream_Cashier_v1.0.0.exe" "%PACKAGE_NAME%\"
    echo OK: Executable copied
) else (
    echo ERROR: Executable not found
    pause
    exit /b 1
)

REM Copy additional files
if exist "ice_cream_cashier.html" copy "ice_cream_cashier.html" "%PACKAGE_NAME%\" >nul
if exist "دليل_المستخدم_الشامل.txt" copy "دليل_المستخدم_الشامل.txt" "%PACKAGE_NAME%\" >nul
if exist "README_النهائي.txt" copy "README_النهائي.txt" "%PACKAGE_NAME%\" >nul
if exist "إصلاحات_Flask.txt" copy "إصلاحات_Flask.txt" "%PACKAGE_NAME%\" >nul

REM Create run script
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo.
echo Ice Cream Cashier - Omani Rial
echo Starting application...
echo.
echo Please wait...
echo.
echo If antivirus blocks the file, please allow it.
echo.
echo Starting in 3 seconds...
echo.
timeout /t 3 /nobreak ^>nul
echo.
echo Starting Ice Cream Cashier...
echo.
start "" "IceCream_Cashier_v1.0.0.exe"
echo.
echo Application started!
echo You can close this window now.
echo.
pause
) > "%PACKAGE_NAME%\RUN_APP.bat"

REM Create info file
(
echo ================================================================
echo                Ice Cream Cashier v1.0.0
echo                Distribution Package
echo                Omani Rial Currency
echo ================================================================
echo.
echo Package Contents:
echo ================
echo.
echo IceCream_Cashier_v1.0.0.exe  - Main application
echo ice_cream_cashier.html       - HTML demo version
echo RUN_APP.bat                  - Quick launcher
echo Documentation files          - User guides
echo.
echo How to Run:
echo ===========
echo.
echo Method 1: Double-click on IceCream_Cashier_v1.0.0.exe
echo Method 2: Double-click on RUN_APP.bat
echo Method 3: For demo, open ice_cream_cashier.html in browser
echo.
echo Features:
echo =========
echo.
echo - Complete cashier system for ice cream shops
echo - Omani Rial currency support
echo - Arabic interface
echo - Sales tracking and reporting
echo - Expense management
echo - Profit/loss calculations
echo - Backup and restore functionality
echo - Works on any Windows computer
echo - No Python installation required
echo.
echo System Requirements:
echo ===================
echo.
echo - Windows 7/8/10/11
echo - 50 MB free disk space
echo - No additional software needed
echo.
echo Troubleshooting:
echo ===============
echo.
echo If the program doesn't start:
echo 1. Right-click and "Run as administrator"
echo 2. Add exception in antivirus software
echo 3. Make sure Windows is up to date
echo 4. Try the HTML demo version instead
echo.
echo Support:
echo ========
echo.
echo For technical support or questions:
echo Email: support@augmentcode.com
echo Website: https://augmentcode.com
echo.
echo Thank you for using Ice Cream Cashier!
echo.
echo ================================================================
) > "%PACKAGE_NAME%\README.txt"

echo OK: Distribution package created

echo.
echo ================================================================
echo SUCCESS: Executable file created successfully!
echo ================================================================
echo.

echo Package folder: %PACKAGE_NAME%
echo Main file: IceCream_Cashier_v1.0.0.exe
echo Size: Approximately 15-25 MB
echo Currency: Omani Rial (OMR)
echo.

echo Features:
echo - Standalone executable file
echo - Works on any Windows computer
echo - No Python installation needed
echo - Full Arabic interface
echo - All features included
echo.

echo How to use:
echo 1. Double-click on the executable file
echo 2. Use RUN_APP.bat for guided startup
echo 3. For demo: open ice_cream_cashier.html
echo.

echo Distribution:
echo - Copy the folder to USB drive
echo - Send via email (zip the folder first)
echo - Upload to your website
echo - Share with customers
echo.

REM Open package folder
echo Opening package folder...
start "" "%PACKAGE_NAME%"

echo.
echo ================================================================
echo Thank you for using Ice Cream Cashier!
echo ================================================================
echo.
pause
