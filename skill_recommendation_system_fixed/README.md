# Skill Recommendation System

A comprehensive skill assessment and resume analysis platform that helps users identify their strengths, weaknesses, and areas for improvement in various technical skills.

## Features

1. **Skill Assessment**: Interactive MCQ-based assessments in various Computer Science domains
2. **Resume Analysis**: AI-powered resume parsing and skill extraction
3. **Personalized Recommendations**: Tailored suggestions based on assessment performance and resume analysis

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Flask
- **AI APIs**: NVIDIA NIM, Google Gemini
- **Data Processing**: Python, scikit-learn, NLTK, spaCy
- **File Processing**: PyPDF2, python-docx

## Deployment Structure

This repository is structured for easy deployment on Streamlit Cloud:

```
skill_recommendation_system/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── config.py                 # Configuration settings
├── nvidia api key.py         # NVIDIA API key configuration
├── google api key.txt        # Google API key
├── backend/                  # Flask backend
│   ├── app.py                # Main Flask application
│   ├── resume_analyzer.py    # Resume analysis utilities
│   ├── it_skill_questions.json # IT skill questions database
│   └── app/                  # Backend application modules
│       └── utils/            # Utility functions
│           ├── resume_parser.py
│           └── skill_extractor.py
└── uploads/                  # Directory for uploaded files
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   - For NVIDIA API: Edit `nvidia api key.py` and replace `YOUR_NVIDIA_API_KEY_HERE` with your actual API key
   - For Google API: Edit `google api key.txt` and replace `YOUR_GOOGLE_API_KEY_HERE` with your actual API key

3. **Run the Application**:
   ```bash
   # Start the backend server
   python backend/app.py
   
   # In a new terminal, start the Streamlit frontend
   streamlit run streamlit_app.py
   ```

## Deployment on Streamlit Cloud

1. Push this repository to GitHub (ensure the folder name has no spaces)
2. Connect to Streamlit Cloud using the following settings:
   - **Main file path**: `streamlit_app.py`
   - **Requirements file**: Auto-detected from `requirements.txt`

## File Structure Explanation

- `streamlit_app.py`: Main frontend application with two modes - Skill Assessment and Resume Analysis
- `requirements.txt`: All necessary Python packages for the application
- `config.py`: Configuration settings for both frontend and backend
- `backend/app.py`: Flask backend server with API endpoints for AI integration
- `backend/app/utils/resume_parser.py`: Utility for parsing PDF and DOCX resumes
- `backend/app/utils/skill_extractor.py`: Utility for extracting skills from resume text
- `backend/it_skill_questions.json`: Database of technical questions for skill assessments

## API Integration

The system integrates with:
1. **NVIDIA NIM API**: For generating questions and analyzing responses
2. **Google Gemini API**: Alternative AI provider for question generation and analysis

## Usage

1. **Skill Assessment Mode**:
   - Select skills to test
   - Answer MCQ questions
   - Get personalized performance analysis and recommendations

2. **Resume Analysis Mode**:
   - Upload a PDF or DOCX resume
   - Answer interactive questions based on resume content
   - Receive AI-powered feedback and career recommendations

## Development Notes

- The application uses session state to maintain user progress
- Backend runs on port 5000 by default
- Frontend runs on port 8501 by default
- File uploads are temporarily stored in the `uploads/` directory