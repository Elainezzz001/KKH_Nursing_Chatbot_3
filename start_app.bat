@echo off
echo Starting KKH Nursing Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if LM Studio is running
echo Checking LM Studio connection...
curl -s http://localhost:1234/v1/models >nul 2>&1
if errorlevel 1 (
    echo WARNING: LM Studio is not running at localhost:1234
    echo Please start LM Studio and load the OpenHermes-2.5-Mistral-7B model
    echo The application will run with basic responses only
    echo.
    pause
)

echo Starting Streamlit application...
echo.
echo The application will open in your default web browser
echo Press Ctrl+C to stop the application
echo.

streamlit run app_fixed.py

pause
