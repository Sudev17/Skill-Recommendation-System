# Deployment Guide for Skill Recommendation System

This guide provides instructions for deploying the Skill Recommendation System to various platforms.

## Streamlit Deployment

### Requirements for Streamlit Deployment

1. **File Structure**: The Streamlit app requires the following files in the root directory:
   - `streamlit_app.py` (main application file)
   - `requirements.txt` (dependencies for the Streamlit app)

2. **Dependencies**: The Streamlit app requires these packages:
   ```
   streamlit==1.22.0
   requests==2.31.0
   Pillow==9.5.0
   python-dotenv==1.0.0
   ```

### Deploying to Streamlit Cloud

1. **Repository Structure**: 
   - Ensure `streamlit_app.py` is in the root of your repository
   - Ensure `requirements.txt` is in the root of your repository
   - The backend files should be in a `backend/` subdirectory

2. **Dependencies**:
   - Streamlit Cloud will automatically install packages listed in `requirements.txt`
   - Make sure `requirements.txt` only contains packages needed for the Streamlit app

3. **Configuration**:
   - When setting up your Streamlit app, specify `streamlit_app.py` as the main file
   - The deployment system will automatically detect and install dependencies

### Troubleshooting Deployment Issues

1. **Path Issues**:
   - If you encounter path-related errors, ensure that the backend directory is properly referenced
   - The Streamlit app uses relative paths to import backend utilities

2. **Import Errors**:
   - If you see import errors for backend modules, check that:
     - The `backend/` directory exists in the correct location
     - The `__init__.py` files are present in all package directories
     - The sys.path is correctly modified in `streamlit_app.py`

3. **Dependency Installation Errors**:
   - If you see errors about requirements.txt parsing, check that:
     - The file is properly formatted with one package per line
     - There are no special characters or encoding issues
     - The file has a proper `.txt` extension

### Alternative Deployment Approach

If you continue to experience issues with the current structure, you can try this alternative approach:

1. **Create a separate deployment directory**:
   ```
   deployment/
   ├── streamlit_app.py
   ├── requirements.txt
   ├── backend/
   │   ├── app.py
   │   ├── app/
   │   │   ├── __init__.py
   │   │   └── utils/
   │   │       ├── __init__.py
   │   │       ├── resume_parser.py
   │   │       └── skill_extractor.py
   │   ├── it_skill_questions.json
   │   ├── requirements.txt
   │   └── uploads/
   └── frontend/
       └── index.html
   ```

2. **Update import paths** in `streamlit_app.py` to match the new structure

3. **Deploy from the deployment directory** instead of the root directory

## Backend Deployment

### Running the Backend Server

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**:
   ```bash
   python app.py
   ```

### Backend API Endpoints

The backend server provides the following API endpoints:
- `/api/skills` - Get available skills
- `/api/questions` - Get questions for selected skills
- `/api/evaluate` - Evaluate user answers
- `/api/upload-resume` - Upload and parse resume
- `/api/generate-resume-questions` - Generate questions based on resume
- `/api/analyze-resume-responses` - Analyze user responses to resume questions

## Dual Server Deployment

For full functionality, both the backend and Streamlit frontend need to be running:

1. **Start the backend server** on port 5000:
   ```bash
   cd backend
   python app.py
   ```

2. **Start the Streamlit app** on port 8501:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the applications**:
   - Backend API: http://localhost:5000
   - Streamlit app: http://localhost:8501

## Environment Configuration

### API Keys

1. **NVIDIA API Key**:
   - Required for AI-powered features
   - Create `nvidia api key.py` with your API key:
     ```python
     # NVIDIA API Key Configuration
     api_key = "Bearer YOUR_NVIDIA_API_KEY_HERE"
     ```

2. **Google API Key** (Optional):
   - Used as a fallback for AI features
   - Create `google api key.txt` with your API key:
     ```
     YOUR_GOOGLE_API_KEY_HERE
     ```

### Directory Structure

Ensure the following directory structure exists:
```
Skill Recommendation System/
├── backend/
│   └── uploads/          # For resume uploads
├── frontend/
└── streamlit_app.py
```

Create the uploads directory if it doesn't exist:
```bash
mkdir backend/uploads
```