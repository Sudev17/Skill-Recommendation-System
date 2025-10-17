# Skill Recommendation System

This is the deployment package for the Skill Recommendation System.

## Project Structure

```
Skill Recommendation System/
├── streamlit_app.py            # Main Streamlit application file
├── requirements.txt            # Streamlit app dependencies
├── config.py                   # Application configuration
├── nvidia api key.py           # NVIDIA API key (add your key here)
├── google api key.txt          # Google API key (optional)
├── backend/
│   ├── app.py                  # Flask backend application
│   ├── app/                    # Backend utilities
│   │   ├── __init__.py
│   │   └── utils/              # Resume processing utilities
│   │       ├── __init__.py
│   │       ├── resume_parser.py
│   │       └── skill_extractor.py
│   ├── it_skill_questions.json # Question bank
│   ├── requirements.txt        # Backend dependencies
│   ├── resume_analyzer.py      # AI integration module
│   └── uploads/                # Resume upload directory
└── frontend/
    └── index.html              # HTML frontend
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

---

*Developed by Sudev Basti*