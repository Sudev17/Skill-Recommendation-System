# Deployment Instructions

This document provides instructions for deploying the Skill Recommendation System to Streamlit Cloud.

## Current Deployment Structure

The repository now has the correct structure for deployment:

```
Skill Recommendation System/
├── streamlit_app.py
├── requirements.txt
├── config.py
├── nvidia api key.py
├── google api key.txt
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
│   ├── resume_analyzer.py
│   └── uploads/
└── frontend/
    └── index.html
```

## Streamlit Cloud Deployment

To deploy to Streamlit Cloud:

1. **Push this repository to GitHub**
   - Make sure all files are committed and pushed to your repository

2. **Configure Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy!"

3. **Add Your API Keys**
   - After deployment, edit the `nvidia api key.py` file in your Streamlit Cloud environment:
     ```python
     # NVIDIA API Key Configuration
     api_key = "Bearer YOUR_NVIDIA_API_KEY_HERE"
     ```
   - (Optional) Add your Google API key to `google api key.txt`

## Local Development

To run the application locally:

1. **Start the backend server**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   The backend will be available at http://localhost:5000

2. **Start the Streamlit app**:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
   The Streamlit app will be available at http://localhost:8501

## Directory Structure Explanation

The key to successful deployment is having the correct file structure:

- `streamlit_app.py` and `requirements.txt` are at the repository root
- Backend utilities are in the `backend/app/utils/` directory
- The Streamlit app can import backend utilities using the sys.path modification in `streamlit_app.py`

This structure ensures that:
1. Streamlit Cloud can automatically detect and install dependencies from `requirements.txt`
2. The Streamlit app can import backend utilities correctly
3. All necessary files are available for both local development and cloud deployment

## Troubleshooting

If you encounter deployment issues:

1. **Check file paths**: Ensure `streamlit_app.py` and `requirements.txt` are at the repository root
2. **Verify imports**: Make sure backend utilities can be imported by the Streamlit app
3. **Check API keys**: Ensure your NVIDIA API key is properly configured
4. **Verify directory structure**: Run `verify_deployment.py` to check if all files are in the correct locations

---

*Developed by Sudev Basti*