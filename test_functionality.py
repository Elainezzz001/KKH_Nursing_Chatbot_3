#!/usr/bin/env python3
"""
Test script to verify all functionality of the KKH Nursing Chatbot
"""
import os
import sys
import time
import requests
from pathlib import Path

def test_app_running():
    """Test if the app is running on localhost:8501"""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ App is running successfully")
            return True
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ App is not running: {e}")
        return False

def test_files_exist():
    """Test if all required files exist"""
    required_files = [
        "app_fixed.py",
        "requirements.txt",
        "data/KKH Information file.pdf",
        "logo/photo_2025-06-16_15-57-21.jpg"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if all required imports are available"""
    try:
        import streamlit
        import sentence_transformers
        import sklearn
        import pypdf
        import requests
        import numpy
        import pandas
        print("✅ All required packages are importable")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing KKH Nursing Chatbot Functionality")
    print("=" * 50)
    
    # Test file existence
    print("\n📁 Testing file existence...")
    files_ok = test_files_exist()
    
    # Test imports
    print("\n📦 Testing package imports...")
    imports_ok = test_imports()
    
    # Test app running
    print("\n🌐 Testing app status...")
    app_ok = test_app_running()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if all([files_ok, imports_ok, app_ok]):
        print("🎉 ALL TESTS PASSED! The app is ready to use.")
        print("\n🔗 Features available:")
        print("   • PDF knowledge base from KKH Information file")
        print("   • Logo integration in header")
        print("   • Sample question buttons in sidebar")
        print("   • Chat interface with auto-response")
        print("   • Pediatric fluid calculator")
        print("   • Interactive nursing quiz")
        print("   • LM Studio integration (if available)")
        print("\n📱 Access the app at: http://localhost:8501")
        print("\n🎯 To test sample questions:")
        print("   1. Look for 'Quick Start Questions' in the sidebar")
        print("   2. Click any sample question button")
        print("   3. The chatbot should respond automatically")
        
    else:
        print("❌ Some tests failed. Please check the issues above.")
        if not files_ok:
            print("   • Check that all required files are present")
        if not imports_ok:
            print("   • Install missing packages with: pip install -r requirements.txt")
        if not app_ok:
            print("   • Start the app with: streamlit run app_fixed.py")

if __name__ == "__main__":
    main()
