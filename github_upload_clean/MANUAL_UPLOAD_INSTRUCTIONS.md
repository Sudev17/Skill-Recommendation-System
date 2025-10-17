# Manual GitHub Upload Instructions

This document provides step-by-step instructions for manually uploading your Skill Recommendation System to GitHub.

## 📁 Clean Directory Structure

You're now ready to upload these essential files only:

```
github_upload_clean/
├── .gitignore
├── README.md
├── config.py
├── streamlit_app.py
├── backend/
│   ├── app.py
│   ├── it_skill_questions.json
│   ├── requirements.txt
│   ├── resume_analyzer.py
│   └── app/
│       ├── __init__.py
│       └── utils/
│           ├── __init__.py
│           ├── resume_parser.py
│           └── skill_extractor.py
└── frontend/
    └── index.html
```

## ▶️ Manual Upload Steps

### Step 1: Navigate to Your Repository
1. Go to https://github.com/Sudev17/Skill-Recommendation-System
2. Make sure you're logged into your GitHub account

### Step 2: Upload Root Files
1. Click "Add file" → "Upload files"
2. Drag and drop these files from the `github_upload_clean` directory:
   - `.gitignore`
   - `README.md`
   - `config.py`
   - `streamlit_app.py`
3. Add a commit message: "Initial commit: Skill Recommendation System"
4. Click "Commit changes"

### Step 3: Create and Upload Backend Directory
1. Click "Add file" → "Create new file"
2. In the filename field, type `backend/.gitkeep`
3. Click "Commit new file"
4. Go back to the main repository page
5. Click on the `backend` directory
6. Click "Add file" → "Upload files"
7. Drag and drop all files from `github_upload_clean/backend/`:
   - `app.py`
   - `it_skill_questions.json`
   - `requirements.txt`
   - `resume_analyzer.py`
   - `app/` directory (with all its contents)
8. Add a commit message: "Add backend components"
9. Click "Commit changes"

### Step 4: Create and Upload Frontend Directory
1. Go back to the main repository page
2. Click "Add file" → "Create new file"
3. In the filename field, type `frontend/.gitkeep`
4. Click "Commit new file"
5. Go back to the main repository page
6. Click on the `frontend` directory
7. Click "Add file" → "Upload files"
8. Drag and drop `index.html` from `github_upload_clean/frontend/`
9. Add a commit message: "Add frontend interface"
10. Click "Commit changes"

## ✅ Verification

After uploading, your repository should contain only the essential files needed for your Skill Recommendation System to function properly.

## 🔐 Security Reminder

The `.gitignore` file ensures that sensitive files like API keys are not accidentally uploaded to GitHub.

## 🎉 Success!

Once you've completed these steps, your GitHub repository will showcase your complete Skill Recommendation System with a clean, professional structure.