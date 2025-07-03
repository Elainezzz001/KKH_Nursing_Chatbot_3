#!/bin/bash

echo "Starting KKH Nursing Chatbot..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip show streamlit &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Check if LM Studio is running
echo "Checking LM Studio connection..."
if ! curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "WARNING: LM Studio is not running at localhost:1234"
    echo "Please start LM Studio and load the OpenHermes-2.5-Mistral-7B model"
    echo "The application will run with basic responses only"
    echo
    read -p "Press Enter to continue..."
fi

echo "Starting Streamlit application..."
echo
echo "The application will open in your default web browser"
echo "Press Ctrl+C to stop the application"
echo

streamlit run app_clean.py
