# Deployment Instructions for Skill Recommendation System

## Problem Summary

The previous deployment was failing because:
1. Folder name had spaces: `Skill Recommendation System` → Streamlit Cloud was reading it as `System`
2. Multiple requirements.txt files in different directories
3. Incorrect path structure for Streamlit Cloud

## Solution Implemented

### 1. Renamed Folder Structure
- **Before**: `Skill Recommendation System/` (with spaces)
- **After**: `skill_recommendation_system_fixed/` (no spaces, lowercase)

### 2. Consolidated Requirements
- **Before**: Two requirements.txt files (one in root, one in backend)
- **After**: Single requirements.txt in root with cleaned dependencies (no version numbers for better compatibility)

### 3. Corrected File Structure
```
skill_recommendation_system_fixed/          # ✅ No spaces in folder name
├── streamlit_app.py                       # ✅ Main application file
├── requirements.txt                       # ✅ Single requirements file in root
├── config.py                             # ✅ Configuration file
├── nvidia api key.py                     # ✅ API key configuration
├── google api key.txt                    # ✅ API key configuration
├── README.md                             # ✅ Documentation
├── .gitignore                            # ✅ Git ignore file
├── run_app.py                            # ✅ Convenience script to run both services
├── DEPLOYMENT_INSTRUCTIONS.md            # ✅ This file
└── backend/                              # ✅ Backend directory
    ├── app.py                            # ✅ Flask backend application
    ├── resume_analyzer.py                # ✅ Resume analysis utilities
    ├── it_skill_questions.json           # ✅ Question database
    └── app/                              # ✅ Backend application modules
        └── utils/                        # ✅ Utility functions
            ├── resume_parser.py
            └── skill_extractor.py
```

## Streamlit Cloud Deployment Settings

When deploying to Streamlit Cloud, use these settings:

| Field | Value |
|-------|-------|
| **Repository** | Your GitHub repository with this structure |
| **Branch** | main (or your default branch) |
| **Main file path** | `streamlit_app.py` |
| **Requirements file** | Auto-detected from `requirements.txt` |

## Steps to Deploy

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Fixed deployment structure"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Connect to Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository
   - Set the configuration as shown above
   - Click "Deploy!"

3. **Configure API Keys**:
   - After deployment, go to your app settings in Streamlit Cloud
   - Add environment variables:
     - `NVIDIA_API_KEY` = your NVIDIA API key
     - `GOOGLE_API_KEY` = your Google API key

## Local Development

To run the application locally:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   - Edit `nvidia api key.py` and replace `YOUR_NVIDIA_API_KEY_HERE` with your actual key
   - Edit `google api key.txt` and replace `YOUR_GOOGLE_API_KEY_HERE` with your actual key

3. **Run the application**:
   ```bash
   # Option 1: Run both services separately
   # Terminal 1: python backend/app.py
   # Terminal 2: streamlit run streamlit_app.py
   
   # Option 2: Use the convenience script
   python run_app.py
   ```

## Key Improvements

1. **✅ No Spaces**: Folder name now has no spaces
2. **✅ Flat Structure**: All necessary files at root level
3. **✅ Single Requirements**: One requirements.txt file in root
4. **✅ Clear Documentation**: README.md and DEPLOYMENT_INSTRUCTIONS.md
5. **✅ Proper Paths**: All imports and paths corrected
6. **✅ Streamlit Cloud Ready**: Structure meets Streamlit Cloud requirements

## Troubleshooting

If you still encounter deployment issues:

1. **Check folder name**: Ensure no spaces in repository folder name
2. **Verify requirements.txt**: Should be in root directory only
3. **Check main file path**: Should be exactly `streamlit_app.py`
4. **API Keys**: Configure as environment variables in Streamlit Cloud settings
5. **Dependencies**: If issues persist, try removing version numbers from requirements.txt

This structure should deploy successfully to Streamlit Cloud without the path resolution errors you were experiencing.