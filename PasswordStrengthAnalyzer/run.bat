@echo off
title Password Strength Analyzer GUI Launcher
cls

echo ========================================================
echo       Password Strength Analyzer - Java Swing GUI
echo ========================================================
echo.

:: Check if Java compiler javac is available in PATH
where javac >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] JDK javac was not found on your system PATH!
    echo Please install JDK 21 and ensure it is added to your environment PATH.
    echo.
    pause
    exit /b 1
)

:: Create out directory if it does not exist
if not exist out (
    mkdir out
)

:: Compile the Java program
echo [INFO] Compiling PasswordStrengthAnalyzer.java ...
javac -d out src\PasswordStrengthAnalyzer.java
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Compilation failed.
    echo.
    pause
    exit /b 1
)

echo [INFO] Launching Java Swing Desktop GUI window...
start javaw -cp out PasswordStrengthAnalyzer
exit
