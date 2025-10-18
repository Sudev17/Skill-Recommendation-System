#!/usr/bin/env python3
"""
Project initialization script
"""

import os
import sys

def create_uploads_directory():
    """Create the uploads directory if it doesn't exist"""
    uploads_dir = os.path.join('backend', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✓ Created uploads directory: {uploads_dir}")
    else:
        print(f"✓ Uploads directory already exists: {uploads_dir}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8 or higher is recommended")
        return False
    else:
        print(f"✓ Python version is compatible: {sys.version}")
        return True

def check_requirements_file():
    """Check if requirements.txt exists"""
    if os.path.exists('requirements.txt'):
        print("✓ requirements.txt found")
        return True
    else:
        print("✗ requirements.txt not found")
        return False

def main():
    """Main initialization function"""
    print("Initializing Skill Recommendation System...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check requirements file
    check_requirements_file()
    
    # Create uploads directory
    create_uploads_directory()
    
    print("\n" + "=" * 50)
    print("Initialization complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure your API keys in nvidia api key.py and google api key.txt")
    print("3. Run the backend: cd backend && python app.py")
    print("4. Run the Streamlit app: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()