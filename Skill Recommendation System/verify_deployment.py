#!/usr/bin/env python3
"""
Verification script for the deployment structure
"""

import os

def verify_structure():
    """Verify that all required files exist in the correct locations"""
    print("Verifying deployment structure...")
    
    # Change to the deployment directory
    deployment_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Deployment directory: {deployment_dir}")
    
    # List of required files at root level
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'config.py'
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
        if os.path.exists(file_name):
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            return False
    
    # Check directories
    print("\nChecking directories:")
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
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
        if os.path.exists(file_path):
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
        if os.path.exists(file_path):
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

if __name__ == "__main__":
    success = verify_structure()
    if not success:
        print("\n❌ Deployment verification failed!")
        exit(1)
    else:
        print("\n✅ Deployment verification passed!")
        exit(0)