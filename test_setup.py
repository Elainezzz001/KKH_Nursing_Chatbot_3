"""
Test script for KKH Nursing Chatbot
Run this to verify that all components are working correctly
"""

import os
import sys

def test_dependencies():
    """Test if all required packages are installed"""
    print("Testing dependencies...")
    
    required_packages = [
        'streamlit', 'pdfplumber', 'sentence_transformers', 
        'numpy', 'pandas', 'sklearn', 'requests', 
        'PIL', 'torch', 'transformers'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("All dependencies are installed!")
    return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "app.py",
        "utils.py", 
        "config.py",
        "requirements.txt",
        "data/KKH Information file.pdf"
    ]
    
    optional_files = [
        "logo/photo_2025-06-16_15-57-21.jpg",
        "embedded_knowledge.json"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing_files.append(file)
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✓ {file} (optional)")
        else:
            print(f"- {file} (optional, will be created/not used)")
    
    if missing_files:
        print(f"\nMissing required files: {', '.join(missing_files)}")
        return False
    
    print("All required files are present!")
    return True

def test_configuration():
    """Test if configuration loads correctly"""
    print("\nTesting configuration...")
    
    try:
        import config
        print("✓ Configuration loaded successfully")
        print(f"  - LLM API URL: {config.LLM_API_URL}")
        print(f"  - Embedding Model: {config.EMBEDDING_MODEL}")
        print(f"  - PDF Path: {config.PDF_PATH}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing functionality"""
    print("\nTesting PDF processing...")
    
    try:
        from utils import load_and_process_pdf
        import config
        
        if not os.path.exists(config.PDF_PATH):
            print(f"✗ PDF file not found: {config.PDF_PATH}")
            return False
        
        chunks = load_and_process_pdf(config.PDF_PATH)
        if chunks:
            print(f"✓ PDF processed successfully ({len(chunks)} chunks extracted)")
            return True
        else:
            print("✗ No content extracted from PDF")
            return False
    
    except Exception as e:
        print(f"✗ PDF processing error: {e}")
        return False

def test_llm_connection():
    """Test LLM connection (optional)"""
    print("\nTesting LLM connection...")
    
    try:
        import requests
        import config
        
        # Try to ping the LLM server
        response = requests.get(config.LLM_API_URL.replace('/v1/chat/completions', '/health'), timeout=5)
        print("✓ LLM server is reachable")
        return True
    
    except requests.exceptions.ConnectionError:
        print("- LLM server not running (start LM Studio)")
        return True  # This is optional for basic functionality
    
    except Exception as e:
        print(f"- LLM connection test failed: {e}")
        return True  # This is optional for basic functionality

def main():
    """Run all tests"""
    print("KKH Nursing Chatbot - System Test")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_files,
        test_configuration,
        test_pdf_processing,
        test_llm_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready to run.")
        print("\nTo start the application:")
        print("1. Ensure LM Studio is running with OpenHermes-2.5-Mistral-7B")
        print("2. Run: streamlit run app.py")
        print("3. Or double-click: start_app.bat")
    else:
        print(f"⚠️  {passed}/{total} tests passed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
