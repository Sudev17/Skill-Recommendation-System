# Skill Recommendation System

A comprehensive skill assessment and recommendation platform that helps Computer Science Engineering students identify their strengths and areas for improvement through MCQ assessments and resume analysis.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Technology Stack](#technology-stack)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Running the Application Locally](#running-the-application-locally)
9. [Deployment to Streamlit Cloud](#deployment-to-streamlit-cloud)
10. [API Endpoints](#api-endpoints)
11. [Troubleshooting](#troubleshooting)

## Project Overview

The Skill Recommendation System is a full-stack web application that provides two main functionalities:

1. **Skill Assessment**: Users can select multiple Computer Science Engineering skills and take MCQ assessments to evaluate their knowledge
2. **Resume Analysis**: Users can upload their resumes for AI-powered analysis and personalized skill recommendations

The system uses a comprehensive question bank of 800 MCQs across 8 CSE subjects and integrates with NVIDIA AI APIs for intelligent recommendations.

## Features

### Skill Assessment
- Multiple skill selection (Python, C Programming, Java, etc.)
- Configurable question count (5-25 questions per test)
- Interactive MCQ interface with visual feedback
- Instant scoring and detailed performance analysis
- Personalized skill improvement recommendations

### Resume Analysis
- Resume upload support for PDF and DOCX formats
- AI-powered skill extraction from resume content
- Interactive assessment with exactly 6 professional technical interview questions
- AI-powered analysis of user responses with personalized feedback
- Career recommendations based on resume content and user responses

### UI/UX Features
- Royal space-themed dark mode interface
- Animated background with stars, asteroids, and meteors
- Responsive design for all device sizes
- Intuitive navigation and user-friendly interface

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
│   ├── it_skill_questions.json # Question bank (800 MCQs)
│   ├── requirements.txt        # Backend dependencies
│   ├── resume_analyzer.py      # LLM API integration module
│   └── uploads/                # Directory for uploaded resumes
└── frontend/
    └── index.html              # HTML frontend
```

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing

### Frontend
- **HTML5**
- **CSS3** - With animations and gradients
- **Vanilla JavaScript** - No external frameworks
- **Streamlit** - Python-based frontend

### AI/ML Integration
- **NVIDIA AI APIs** - Primary LLM provider (Mistral Small)
- **Google Gemini APIs** - Secondary LLM provider (optional)

### Data
- **JSON** - Question bank storage
- **RESTful APIs** - Communication between frontend and backend

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)
- NVIDIA API key (required for AI features)
- Google API key (optional, for fallback)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Skill Recommendation System"
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Uploads Directory
```bash
mkdir backend/uploads
```

## Configuration

### API Keys Setup

1. **NVIDIA API Key**:
   - Obtain your NVIDIA API key from [NVIDIA API Catalog](https://build.nvidia.com/)
   - Update the `nvidia api key.py` file with your API key

2. **Google API Key** (Optional):
   - Obtain your Google API key from [Google AI Studio](https://aistudio.google.com/)
   - Update the `google api key.txt` file with your API key

## Running the Application Locally

### Start Backend Server
```bash
cd backend
python app.py
```
The backend will start on `http://localhost:5000`

### Start Streamlit App
```bash
streamlit run streamlit_app.py
```
The Streamlit app will start on `http://localhost:8501`

## Deployment to Streamlit Cloud

### Steps to Deploy:

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push this folder to your GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Skill Recommendation System"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [https://share.streamlit.io/](https://share.streamlit.io/)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the following configuration:
     - **Branch**: main
     - **Main file path**: streamlit_app.py
   - Click "Deploy!"

3. **Configure API Keys in Streamlit Cloud**
   - After deployment, go to your app's settings
   - Edit the `nvidia api key.py` file directly in the Streamlit Cloud environment
   - Replace the placeholder with your actual NVIDIA API key:
   ```python
   # NVIDIA API Key Configuration
   api_key = "Bearer YOUR_ACTUAL_NVIDIA_API_KEY_HERE"
   ```

4. **Restart the App**
   - After adding your API key, restart the app from the Streamlit Cloud dashboard

## API Endpoints

### GET `/api/skills`
Retrieve all available skills for assessment

### POST `/api/questions`
Get questions for specific skills

### POST `/api/evaluate`
Evaluate user answers and provide recommendations

### POST `/api/upload-resume`
Upload and analyze resume

### POST `/api/generate-resume-questions`
Generate exactly 6 professional technical interview questions based on resume analysis

### POST `/api/analyze-resume-responses`
Analyze user responses to resume questions and provide personalized feedback

## Troubleshooting

### Common Issues

#### 1. "Module not found" errors
Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

#### 2. API key issues
- Verify NVIDIA API key is correctly set in `nvidia api key.py`
- Check internet connectivity
- Confirm API key has not expired

#### 3. Resume upload failures
- Ensure `backend/uploads` directory exists
- Check file size limits
- Verify file format support (PDF, DOCX)

#### 4. Frontend not loading
- Check if Flask server is running
- Verify port 5000 is not blocked
- Check browser console for errors

#### 5. AI analysis not working
- Check API key configuration
- Verify backend server is running
- Check network connectivity

---

*Developed by Sudev Basti*