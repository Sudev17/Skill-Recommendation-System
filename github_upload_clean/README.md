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
8. [Running the Application](#running-the-application)
9. [Usage Guide](#usage-guide)
10. [API Endpoints](#api-endpoints)
11. [Development](#development)
12. [Testing](#testing)
13. [Deployment](#deployment)
14. [Troubleshooting](#troubleshooting)
15. [Contributing](#contributing)
16. [License](#license)

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
- Interactive chat interface for resume-based questions
- Personalized career recommendations

### UI/UX Features
- Royal space-themed dark mode interface
- Animated background with stars, asteroids, and meteors
- Responsive design for all device sizes
- Intuitive navigation and user-friendly interface

## Project Structure

```
Skill Recommendation System/
├── .gitignore
├── README.md
├── config.py
├── google api key.txt          # Google API key (optional)
├── nvidia api key.py           # NVIDIA API key
├── streamlit_app.py
├── test_resume.py
├── test_streamlit_upload.py
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── app/                    # Application package
│   │   ├── __init__.py
│   │   └── utils/              # Utility modules
│   │       ├── __init__.py
│   │       ├── resume_parser.py
│   │       └── skill_extractor.py
│   ├── it_skill_questions.json # Question bank (800 MCQs)
│   ├── requirements.txt        # Python dependencies
│   ├── resume_analyzer.py      # LLM API integration module
│   ├── test_api.py
│   └── uploads/                # Directory for uploaded resumes
└── frontend/
    └── index.html              # Main frontend file
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
- **Fetch API** - For HTTP requests

### AI/ML Integration
- **NVIDIA AI APIs** - Primary LLM provider
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
cd skill-recommendation-system
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
mkdir uploads
```

## Configuration

### API Keys Setup

1. **NVIDIA API Key**:
   - Obtain your NVIDIA API key from [NVIDIA API Catalog](https://build.nvidia.com/)
   - Update the `nvidia api key.py` file with your API key

2. **Google API Key** (Optional):
   - Obtain your Google API key from [Google AI Studio](https://aistudio.google.com/)
   - Create a `google api key.txt` file with your API key

### Environment Variables
No specific environment variables are required, but you can set:
- `FLASK_ENV=development` for development mode
- `FLASK_DEBUG=1` for debug mode

## Running the Application

### Using Startup Scripts

#### Windows
```bash
start.bat
```

#### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### Manual Startup
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### 1. Access the Application
Open your web browser and navigate to `http://localhost:5000`

### 2. Skill Assessment Mode
1. Click on "Skill Assessment" button
2. Select one or more skills using checkboxes
3. Choose the number of questions (5-25)
4. Click "Start Assessment"
5. Answer the MCQ questions
6. Click "Next" to proceed to the next question
7. Click "Submit" after answering all questions
8. View your score and personalized recommendations

### 3. Resume Analysis Mode
1. Click on "Resume Analysis" button
2. Upload your resume (PDF or DOCX format)
3. Wait for the AI analysis to complete
4. View extracted skills and initial recommendations
5. Ask questions about your resume using the chat interface
6. Receive personalized career guidance

## API Endpoints

### GET `/api/skills`
Retrieve all available skills for assessment

**Response:**
```json
{
  "skills": [
    "Python",
    "C Programming",
    "Java",
    "Data Structures & Algorithms",
    "SQL + DBMS",
    "Machine Learning",
    "Operating System",
    "Web Development (HTML/CSS/JS + Basics React)"
  ]
}
```

### POST `/api/questions`
Get questions for specific skills

**Request:**
```json
{
  "skill": "Python",
  "count": 10
}
```

**Response:**
```json
{
  "questions": [
    {
      "question_id": "PY001",
      "question": "What is the output of print(2**3)?",
      "options": [
        "6",
        "8",
        "9",
        "Error"
      ],
      "correct_answer": 1,
      "skill": "Python"
    }
  ],
  "skill": "Python"
}
```

### POST `/api/evaluate`
Evaluate user answers and provide recommendations

**Request:**
```json
{
  "answers": [
    {
      "questionId": "PY001",
      "question": "What is the output of print(2**3)?",
      "selectedOption": 1,
      "correct": true,
      "skill": "Python"
    }
  ],
  "skill": "Python",
  "api_provider": "nvidia"
}
```

**Response:**
```json
{
  "score": 100.0,
  "correct_answers": 1,
  "total_questions": 1,
  "recommendation": "Excellent performance in Python! Continue challenging yourself with advanced topics."
}
```

### POST `/api/upload-resume`
Upload and analyze resume

**Request:**
- Form data with `resume` file field

**Response:**
```json
{
  "message": "Resume uploaded successfully",
  "skills": [
    {
      "name": "Python",
      "confidence": 0.9
    }
  ],
  "resume_text": "Extracted resume content..."
}
```

### POST `/api/generate-resume-questions`
Generate questions based on resume analysis

**Request:**
```json
{
  "resume_text": "Extracted resume content...",
  "api_provider": "nvidia"
}
```

**Response:**
```json
{
  "questions": [
    "What motivated you to pursue a career in technology?",
    "Can you describe a challenging project you worked on?"
  ]
}
```

## Development

### Project Components

#### 1. Main Application (`app.py`)
- Flask web server with RESTful API endpoints
- CORS configuration for frontend communication
- Question bank loading and management
- Skill assessment logic
- Resume upload handling

#### 2. Resume Analyzer (`resume_analyzer.py`)
- LLM API integration (NVIDIA and Google)
- Recommendation generation
- Response formatting and cleaning

#### 3. Utility Modules (`app/utils/`)
- `resume_parser.py`: PDF and DOCX parsing
- `skill_extractor.py`: Skill identification from text

#### 4. Frontend (`frontend/src/index.html`)
- Single-page application with dual-mode interface
- Space-themed UI with animations
- Interactive MCQ assessment
- Resume analysis chat interface

### Code Structure

#### Backend Routes
1. `/api/skills` - GET skills list
2. `/api/questions` - POST get questions for skills
3. `/api/evaluate` - POST evaluate answers
4. `/api/upload-resume` - POST upload and parse resume
5. `/api/generate-resume-questions` - POST generate resume questions
6. `/` - Serve frontend
7. `/<path:path>` - Serve static files

#### Frontend Components
1. Mode Selection Interface
2. Skill Assessment Module
3. Resume Analysis Module
4. Chat Interface
5. Animation System

## Testing

### Backend Testing
Run the provided test scripts:
```bash
python test_questions.py
python test_resume_api.py
python test_resume_parsing.py
```

### Manual Testing
1. Test skill assessment with different skill combinations
2. Test resume upload with various file formats
3. Verify chat functionality
4. Check responsive design on different screen sizes
5. Test navigation between questions

### API Testing
Use tools like Postman or curl to test API endpoints directly.

## Deployment

### Production Considerations
1. Use a production WSGI server (Gunicorn, uWSGI) instead of Flask's development server
2. Set up a reverse proxy (Nginx, Apache) for static files
3. Configure proper logging and error handling
4. Set up SSL/TLS for secure connections
5. Use environment variables for configuration
6. Implement proper authentication if needed

### Cloud Deployment Options
1. **Heroku**: Simple deployment with free tier available
2. **AWS**: EC2 instances or Elastic Beanstalk
3. **Google Cloud**: App Engine or Compute Engine
4. **Azure**: App Service or Virtual Machines

### Docker Deployment
Create a Dockerfile for containerized deployment:
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

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
- Ensure `uploads` directory exists
- Check file size limits
- Verify file format support (PDF, DOCX)

#### 4. Frontend not loading
- Check if Flask server is running
- Verify port 5000 is not blocked
- Check browser console for errors

### Debugging Steps
1. Check terminal output for error messages
2. Verify all required files exist in correct locations
3. Test API endpoints individually
4. Check browser developer tools for frontend errors

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Commit with descriptive messages
6. Push to your fork
7. Create a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Write docstrings for modules and functions

### Reporting Issues
1. Check existing issues before creating new ones
2. Provide detailed description of the problem
3. Include steps to reproduce
4. Add screenshots if applicable
5. Specify your environment (OS, Python version, etc.)

## Deployment

### GitHub Deployment

To deploy this project to GitHub, you have several options:

#### Option 1: Using Git (Recommended)

1. **If Git is not installed**:
   - Follow instructions in `GIT_INSTALLATION_INSTRUCTIONS.md`
   - Or run `INSTALL_AND_INIT_GIT.bat` for guided installation

2. **Initialize repository** (if not already done):
   ```bash
   cd "H:\Skill Recommendation System"
   git init
   git branch -M main
   ```

3. **Push to GitHub**:
   - **Automated method**: Run `git_push.bat` (Windows) or `git_push.sh` (Linux/Mac)
   - **Manual method**: Follow instructions in `GITHUB_PUSH_INSTRUCTIONS.md`

4. **Check status**: See `GIT_INITIALIZATION_STATUS.md` for current status and next steps

#### Option 2: Using GitHub API (Alternative)

If Git is not available or you prefer not to install it:

1. **Create a GitHub Personal Access Token**:
   - Visit https://github.com/settings/tokens
   - Generate a new token with `repo` permissions
   - Copy the token

2. **Configure the upload script**:
   - Open `upload_to_github.py`
   - Add your token to the `GITHUB_TOKEN` variable
   - Save the file

3. **Run the upload**:
   - Double-click `upload_to_github.bat`
   - Or run `python upload_to_github.py` from the command line

4. **Follow the instructions** in `GITHUB_UPLOAD_VIA_API.md` for detailed steps

## License

This project is proprietary and intended for educational purposes. All rights reserved.

---

*Developed by Sudev Basti*