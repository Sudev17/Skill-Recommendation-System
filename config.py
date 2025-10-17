import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # NVIDIA API Configuration
    NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
    
    # Google API Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # Upload directory
    UPLOAD_FOLDER = 'uploads'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    
    # Maximum file size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}