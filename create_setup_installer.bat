@echo off
chcp 65001 >nul
cls

echo ================================================================
echo                Ice Cream Cashier - Omani Rial
echo                Create Professional Setup 1.0.0
echo ================================================================
echo.

echo This will create a professional Setup.exe installer
echo The installer will work on any Windows computer
echo.

echo ================================================================
echo Checking requirements...
echo ================================================================
echo.

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python first
    echo Use: install_python_correct.bat
    goto :error
)
echo OK: Python is available

REM Check PyInstaller
echo [2/3] Checking PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyInstaller not installed
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        echo Try: pip install --user pyinstaller
        goto :error
    )
)
echo OK: PyInstaller is available

REM Check NSIS
echo [3/3] Checking NSIS...
set NSIS_FOUND=0

if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set NSIS_PATH="C:\Program Files (x86)\NSIS\makensis.exe"
    set NSIS_FOUND=1
    echo OK: NSIS found in Program Files (x86)
) else if exist "C:\Program Files\NSIS\makensis.exe" (
    set NSIS_PATH="C:\Program Files\NSIS\makensis.exe"
    set NSIS_FOUND=1
    echo OK: NSIS found in Program Files
) else (
    makensis.exe /VERSION >nul 2>&1
    if not errorlevel 1 (
        set NSIS_PATH=makensis.exe
        set NSIS_FOUND=1
        echo OK: NSIS found in PATH
    )
)

if %NSIS_FOUND%==0 (
    echo WARNING: NSIS not installed
    echo.
    echo To create a professional Setup.exe, you need NSIS:
    echo Download from: https://nsis.sourceforge.io/Download
    echo Install NSIS and run this script again
    echo.
    echo Would you like to create a simple .exe instead?
    set /p choice="Choose (y for simple exe, n to exit): "
    if /i "%choice%"=="y" goto :simple_exe
    goto :error
)

echo.
echo ================================================================
echo Creating professional Setup 1.0.0.exe...
echo ================================================================
echo.

echo [1/5] Running setup installer creator...
python setup_installer.py
if errorlevel 1 (
    echo ERROR: Failed to create installer
    echo Falling back to simple exe creation...
    goto :simple_exe
)

echo.
echo ================================================================
echo SUCCESS: Setup 1.0.0.exe created successfully!
echo ================================================================
echo.

echo Installer file: Setup_Ice_Cream_Cashier_1.0.0.exe
echo Currency: Omani Rial (OMR)
echo.

echo Features:
echo - Professional installer interface
echo - Works on any Windows computer
echo - No Python installation needed
echo - Automatic shortcut creation
echo - Registers in Programs list
echo - Uninstaller included
echo - Arabic interface support
echo.

echo You can now:
echo 1. Distribute the Setup.exe file
echo 2. Users double-click to install
echo 3. Program appears in Start menu
echo 4. Easy uninstall from Control Panel
echo.

goto :end

:simple_exe
echo.
echo ================================================================
echo Creating simple .exe file instead...
echo ================================================================
echo.

echo [1/3] Creating spec file...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['كاشير_مستقل_تماما.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[('ice_cream_cashier.html', '.'), ('*.txt', '.')],
echo     hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox'],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=['flask', 'jinja2', 'werkzeug'],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo )
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='IceCream_Cashier_v1.0.0',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo )
) > ice_cream_simple.spec

echo OK: Spec file created

echo [2/3] Building executable...
pyinstaller --clean --noconfirm ice_cream_simple.spec
if errorlevel 1 (
    echo ERROR: Failed to build executable
    goto :error
)

echo OK: Executable built

echo [3/3] Creating distribution package...
if not exist "IceCream_Package_v1.0.0" mkdir "IceCream_Package_v1.0.0"
if exist "IceCream_Package_v1.0.0\*" del /q "IceCream_Package_v1.0.0\*"

if exist "dist\IceCream_Cashier_v1.0.0.exe" (
    copy "dist\IceCream_Cashier_v1.0.0.exe" "IceCream_Package_v1.0.0\"
    copy "ice_cream_cashier.html" "IceCream_Package_v1.0.0\"
    copy "*.txt" "IceCream_Package_v1.0.0\" 2>nul
    
    echo OK: Distribution package created
    echo.
    echo ================================================================
    echo SUCCESS: Simple executable created!
    echo ================================================================
    echo.
    echo Package folder: IceCream_Package_v1.0.0
    echo Main file: IceCream_Cashier_v1.0.0.exe
    echo Currency: Omani Rial (OMR)
    echo.
    echo Features:
    echo - Standalone executable
    echo - Works on any Windows computer
    echo - No Python installation needed
    echo - Optimized size
    echo.
) else (
    echo ERROR: Executable not found
    goto :error
)

goto :end

:error
echo.
echo ================================================================
echo ERROR: Failed to create installer
echo ================================================================
echo.
echo Alternative solutions:
echo.
echo 1. Use the HTML demo version:
echo    Double-click: ice_cream_cashier.html
echo.
echo 2. Use the standalone version:
echo    Double-click: run_standalone.bat
echo.
echo 3. Fix requirements and try again:
echo    Double-click: install_python_correct.bat
echo.
goto :end

:end
echo.
echo ================================================================
echo Thank you for using Ice Cream Cashier!
echo ================================================================
echo.
pause
