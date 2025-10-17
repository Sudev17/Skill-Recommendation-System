#!/usr/bin/env python3
"""
Test script to verify the deployment package structure and imports
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    # Test Streamlit imports
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    # Test backend imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_path = os.path.join(current_dir, 'backend')
    if os.path.exists(backend_path):
        sys.path.insert(0, backend_path)
    
    try:
        from app.utils.resume_parser import parse_resume
        print("✓ Resume parser import successful")
    except ImportError as e:
        print(f"✗ Resume parser import failed: {e}")
        return False
    
    try:
        from app.utils.skill_extractor import extract_skills
        print("✓ Skill extractor import successful")
    except ImportError as e:
        print(f"✗ Skill extractor import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'config.py',
        'backend/app.py',
        'backend/app/utils/resume_parser.py',
        'backend/app/utils/skill_extractor.py',
        'backend/it_skill_questions.json',
        'frontend/index.html'
    ]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True

def main():
    """Main test function"""
    print("=== Skill Recommendation System Deployment Test ===\n")
    
    # Test file structure
    if not test_file_structure():
        print("\n✗ File structure test failed")
        return False
    
    # Test imports
    if not test_imports():
        print("\n✗ Import test failed")
        return False
    
    print("\n=== All tests passed! ===")
    print("The deployment package is ready for use.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)