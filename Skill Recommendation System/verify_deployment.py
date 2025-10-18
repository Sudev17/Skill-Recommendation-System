#!/usr/bin/env python3
"""
Verification script for the deployment structure
"""

import os

def verify_structure():
    """Verify that all required files exist in the correct locations"""
    print("Verifying deployment structure...")
    
    # Get the current directory (should be the project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Project root: {project_root}")
    
    # List of required files at root level
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'config.py',
        'nvidia api key.py',
        'google api key.txt'
    ]
    
    # List of required directories
    required_dirs = [
        'backend',
        'frontend',
        'backend/app',
        'backend/app/utils',
        'backend/uploads'
    ]
    
    # Check root level files
    print("\nChecking root level files:")
    for file_name in required_files:
        if os.path.exists(os.path.join(project_root, file_name)):
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            return False
    
    # Check directories
    print("\nChecking directories:")
    for dir_name in required_dirs:
        full_path = os.path.join(project_root, dir_name)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            print(f"  ✓ {dir_name}")
        else:
            print(f"  ✗ {dir_name} - MISSING")
            return False
    
    # Check key backend files
    backend_files = [
        'backend/app.py',
        'backend/it_skill_questions.json',
        'backend/app/utils/resume_parser.py',
        'backend/app/utils/skill_extractor.py'
    ]
    
    print("\nChecking backend files:")
    for file_path in backend_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            return False
    
    # Check frontend files
    frontend_files = [
        'frontend/index.html'
    ]
    
    print("\nChecking frontend files:")
    for file_path in frontend_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            return False
    
    print("\n🎉 All files and directories are in the correct locations!")
    print("\nFor Streamlit Cloud deployment:")
    print("  - Main file path: streamlit_app.py")
    print("  - Requirements: requirements.txt (automatically detected)")
    print("  - Backend utilities: backend/app/utils/")
    return True

def check_api_keys():
    """Check if API key files exist and have content"""
    print("\nChecking API key files:")
    
    # Check NVIDIA API key file
    try:
        with open('nvidia api key.py', 'r') as f:
            content = f.read()
            if 'YOUR_NVIDIA_API_KEY_HERE' in content:
                print("  ⚠️  NVIDIA API key needs to be configured")
            else:
                print("  ✓ NVIDIA API key file exists")
    except FileNotFoundError:
        print("  ✗ NVIDIA API key file missing")
    
    # Check Google API key file
    try:
        with open('google api key.txt', 'r') as f:
            content = f.read().strip()
            if not content or 'YOUR_GOOGLE_API_KEY_HERE' in content:
                print("  ⚠️  Google API key needs to be configured (optional)")
            else:
                print("  ✓ Google API key file exists")
    except FileNotFoundError:
        print("  ✗ Google API key file missing")

if __name__ == "__main__":
    success = verify_structure()
    check_api_keys()
    
    if not success:
        print("\n❌ Deployment verification failed!")
        exit(1)
    else:
        print("\n✅ Deployment verification passed!")
        print("\nNext steps:")
        print("1. Push this repository to GitHub")
        print("2. Deploy to Streamlit Cloud using streamlit_app.py as the main file")
        print("3. Configure your API keys in the Streamlit Cloud environment")
        exit(0)