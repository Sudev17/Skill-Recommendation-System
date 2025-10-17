# Skill Recommendation System - Deployment Package

This is a deployment-ready package for the Skill Recommendation System.

## Project Structure

```
skill-recommendation-system/
├── streamlit_app.py            # Streamlit frontend application
├── requirements.txt            # Dependencies for Streamlit app
├── config.py                   # Application configuration
├── nvidia api key.py           # NVIDIA API key (add your key)
├── google api key.txt          # Google API key (optional)
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── app/                    # Application package
│   │   ├── __init__.py
│   │   └── utils/              # Utility modules
│   │       ├── __init__.py
│   │       ├── resume_parser.py
│   │       └── skill_extractor.py
│   ├── it_skill_questions.json # Question bank (800 MCQs)
│   ├── requirements.txt        # Python dependencies for backend
│   ├── resume_analyzer.py      # LLM API integration module
│   └── uploads/                # Directory for uploaded resumes
└── frontend/
    └── index.html              # Main frontend file
```

## Deployment Instructions

### For Streamlit Cloud Deployment

1. **Repository Setup**:
   - Push this entire directory to your GitHub repository
   - Make sure `streamlit_app.py` is in the root directory
   - Make sure `requirements.txt` is in the root directory

2. **Streamlit App Configuration**:
   - When setting up your Streamlit app on Streamlit Cloud:
     - Set the main file to `streamlit_app.py`
     - The deployment system will automatically detect and install dependencies from `requirements.txt`

3. **API Keys**:
   - Add your NVIDIA API key to `nvidia api key.py`:
     ```python
     # NVIDIA API Key Configuration
     api_key = "Bearer YOUR_NVIDIA_API_KEY_HERE"
     ```
   - (Optional) Add your Google API key to `google api key.txt`

### For Local Deployment

1. **Backend Server**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   The backend will start on `http://localhost:5000`

2. **Streamlit App**:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
   The Streamlit app will start on `http://localhost:8501`

## Requirements

- Python 3.8+
- NVIDIA API key (required for AI features)
- Google API key (optional, for fallback)

## Environment Setup

1. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Uploads Directory**:
   ```bash
   mkdir backend/uploads
   ```

## API Endpoints

The backend provides the following API endpoints:
- `/api/skills` - Get available skills
- `/api/questions` - Get questions for selected skills
- `/api/evaluate` - Evaluate user answers
- `/api/upload-resume` - Upload and parse resume
- `/api/generate-resume-questions` - Generate questions based on resume
- `/api/analyze-resume-responses` - Analyze user responses to resume questions

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Make sure the backend directory is in the correct location relative to streamlit_app.py
   - The sys.path is modified in streamlit_app.py to include the backend directory

2. **API Key Issues**:
   - Verify that your NVIDIA API key is correctly set in `nvidia api key.py`
   - Check that you have internet connectivity
   - Confirm that your API key has not expired

3. **File Upload Issues**:
   - Ensure the `backend/uploads` directory exists
   - Check file size limits
   - Verify file format support (PDF, DOCX)

---

*Developed by Sudev Basti*