@echo off
REM Build Windows executable for Pairwise Test Case Generator
REM
REM Prerequisites:
REM   python -m pip install -r requirements.txt
REM   python -m pip install pyinstaller
REM   Inno Setup (https://jrsoftware.org/isinfo.php) - for creating Setup.exe
REM
REM Usage:
REM   Double-click build_windows.bat  - builds .exe only
REM   Or run in cmd: build_windows.bat installer - builds .exe + runs Inno Setup
REM

setlocal enabledelayedexpansion

set APP_NAME=Pairwise
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo === Pairwise Windows Builder ===
echo.

REM Detect Python command
set PYTHON_CMD=
where python >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=python
    goto :python_found
)
where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=py
    goto :python_found
)
where python3 >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=python3
    goto :python_found
)

echo ERROR: Python not found!
echo.
echo Please install Python 3 from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:python_found
echo Python: !PYTHON_CMD!
!PYTHON_CMD! --version
echo.

REM Check PyInstaller
echo Checking PyInstaller...
!PYTHON_CMD! -m PyInstaller --version >nul 2>nul
if !errorlevel! neq 0 (
    echo PyInstaller not found. Installing...
    !PYTHON_CMD! -m pip install pyinstaller
    echo.
)

echo === Step 1: Clean previous builds ===
if exist "dist\%APP_NAME%" rmdir /s /q "dist\%APP_NAME%"
if exist "build" rmdir /s /q "build"
if exist "%APP_NAME%.spec" del "%APP_NAME%.spec"

echo === Step 2: Build .exe with PyInstaller (onedir) ===
echo.
!PYTHON_CMD! -m PyInstaller ^
    --onedir ^
    --windowed ^
    --name "%APP_NAME%" ^
    --icon "pairwise.ico" ^
    --add-data "pairwise.ico;." ^
    --hidden-import PySide6.QtWidgets ^
    --hidden-import PySide6.QtCore ^
    --hidden-import PySide6.QtGui ^
    --hidden-import PySide6.QtNetwork ^
    --hidden-import allpairspy ^
    main.py

echo.
if not exist "dist\%APP_NAME%\%APP_NAME%.exe" (
    echo ERROR: dist\%APP_NAME%\%APP_NAME%.exe was not created!
    echo Check the messages above for errors.
    echo.
    pause
    exit /b 1
)

echo === Step 3: Build complete! ===
echo Folder: dist\%APP_NAME%\
echo File:   dist\%APP_NAME%\%APP_NAME%.exe

if /i "%1"=="installer" (
    echo.
    echo === Step 4: Creating Inno Setup installer ===
    if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
        "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" "pairwise.iss"
    ) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
        "%ProgramFiles%\Inno Setup 6\ISCC.exe" "pairwise.iss"
    ) else (
        echo.
        echo Inno Setup not found. Please install it from https://jrsoftware.org/isinfo.php
        echo Then open pairwise.iss in Inno Setup Compiler and compile.
        pause
        exit /b 1
    )
    echo Installer created!
)

echo.
echo === Done! ===
echo.
pause