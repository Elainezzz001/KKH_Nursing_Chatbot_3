#!/usr/bin/env python3
"""
Test script for KKH Nursing Chatbot
This script verifies that all dependencies are installed and working correctly.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pdfplumber
        print("✅ pdfplumber imported successfully")
    except ImportError as e:
        print(f"❌ pdfplumber import failed: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers imported successfully")
    except ImportError as e:
        print(f"❌ sentence-transformers import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "data/KKH Information file.pdf",
        "logo/photo_2025-06-16_15-57-21.jpg",
        "utils/__init__.py",
        "utils/pdf_processor.py",
        "utils/fluid_calculator.py",
        "utils/quiz_generator.py",
        "utils/llm_interface.py",
        "config.py",
        "requirements.txt"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} not found")
            all_files_exist = False
    
    return all_files_exist

def test_utils_import():
    """Test if utils modules can be imported"""
    print("\nTesting utils imports...")
    
    try:
        from utils import pdf_processor, fluid_calculator, quiz_generator, llm_interface
        print("✅ All utils modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return False

def test_lm_studio_connection():
    """Test connection to LM Studio"""
    print("\nTesting LM Studio connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ LM Studio is running and accessible")
            return True
        else:
            print(f"❌ LM Studio returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ LM Studio connection failed: {e}")
        print("Note: This is normal if LM Studio is not running")
        return False

def test_embedding_model():
    """Test if embedding model can be loaded"""
    print("\nTesting embedding model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')
        print("✅ Embedding model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Embedding model failed to load: {e}")
        print("Note: This may take time on first run to download the model")
        return False

def main():
    """Run all tests"""
    print("KKH Nursing Chatbot - System Test")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("File Structure Tests", test_file_structure),
        ("Utils Import Tests", test_utils_import),
        ("LM Studio Connection", test_lm_studio_connection),
        ("Embedding Model Test", test_embedding_model)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        if passed >= 3:
            print("💡 The application may still work with limited functionality.")

if __name__ == "__main__":
    main()
