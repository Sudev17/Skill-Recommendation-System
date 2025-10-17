import requests
import json

def analyze_resume_with_google_api(resume_text, api_key):
    """
    Analyze resume using Google's Gemini API
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
    Analyze the following resume and identify the technical skills mentioned:
    
    {resume_text}
    
    Please provide:
    1. A list of technical skills found in the resume
    2. A brief assessment of the candidate's technical profile
    3. 5-10 technical questions that would be relevant for an interview based on the skills mentioned
    
    Format your response as JSON with the following structure:
    {{
        "skills": ["skill1", "skill2", ...],
        "assessment": "brief assessment",
        "questions": ["question1", "question2", ...]
    }}
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract the text response
        if "candidates" in result and len(result["candidates"]) > 0:
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            # Try to parse as JSON
            try:
                return json.loads(text_response)
            except:
                # If not JSON, return as text
                return {"analysis": text_response}
        
        return {"error": "No response from API"}
    except Exception as e:
        return {"error": str(e)}

def analyze_resume_with_nvidia_api(resume_text, api_key):
    """
    Analyze resume using NVIDIA's API
    """
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analyze the following resume and identify the technical skills mentioned:
    
    {resume_text}
    
    Please provide:
    1. A list of technical skills found in the resume
    2. A brief assessment of the candidate's technical profile
    3. 5-10 technical questions that would be relevant for an interview based on the skills mentioned
    
    Format your response as JSON with the following structure:
    {{
        "skills": ["skill1", "skill2", ...],
        "assessment": "brief assessment",
        "questions": ["question1", "question2", ...]
    }}
    """
    
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.7,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract the text response
        if "choices" in result and len(result["choices"]) > 0:
            text_response = result["choices"][0]["message"]["content"]
            # Try to parse as JSON
            try:
                return json.loads(text_response)
            except:
                # If not JSON, return as text
                return {"analysis": text_response}
        
        return {"error": "No response from API"}
    except Exception as e:
        return {"error": str(e)}

def generate_skill_recommendations(answers, api_key, api_provider='google'):
    """
    Generate personalized skill recommendations using LLM APIs based on user answers
    """
    # Prepare assessment summary
    correct_count = sum(1 for answer in answers if answer.get('correct', False))
    total_questions = len(answers)
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Group answers by skill
    skill_performance = {}
    for answer in answers:
        skill = answer.get('skill', 'Unknown')
        if skill not in skill_performance:
            skill_performance[skill] = {'correct': 0, 'total': 0, 'questions': []}
        skill_performance[skill]['total'] += 1
        if answer.get('correct', False):
            skill_performance[skill]['correct'] += 1
        skill_performance[skill]['questions'].append({
            'question': answer.get('question', ''),
            'correct': answer.get('correct', False)
        })
    
    # Create performance summary
    performance_summary = ""
    for skill, data in skill_performance.items():
        skill_percentage = (data['correct'] / data['total']) * 100
        performance_summary += f"{skill}: {data['correct']}/{data['total']} ({skill_percentage:.1f}%)\n"
    
    if api_provider == 'google':
        # Try different Gemini models
        models = ["gemini-pro", "gemini-1.5-pro-latest", "gemini-1.5-flash-latest"]
        headers = {"Content-Type": "application/json"}
        
        prompt = f"""
        Based on the following skill assessment performance, provide personalized recommendations for improvement in exactly 5 lines of plain text without any markdown formatting:
        
        Overall Score: {score_percentage:.1f}% ({correct_count}/{total_questions})
        
        Performance by Skill:
        {performance_summary}
        
        Please provide exactly 5 lines of plain text recommendations without any markdown, bullet points, or special formatting. Keep recommendations concise and actionable.
        """
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 512
            }
        }
        
        # Try each model until one works
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 404:
                    continue  # Try next model
                response.raise_for_status()
                result = response.json()
                
                if "candidates" in result and len(result["candidates"]) > 0:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                
                return "No detailed recommendations available."
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    continue  # Try next model
                else:
                    return f"Error generating recommendations: {str(e)}"
            except Exception as e:
                return f"Error generating recommendations: {str(e)}"
        
        return "Error: None of the Gemini models are available. Please check the API key and try again."
    
    elif api_provider == 'nvidia':
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Based on the following skill assessment performance, provide personalized recommendations for improvement in exactly 5 lines of plain text without any markdown formatting:
        
        Overall Score: {score_percentage:.1f}% ({correct_count}/{total_questions})
        
        Performance by Skill:
        {performance_summary}
        
        Please provide exactly 5 lines of plain text recommendations without any markdown, bullet points, or special formatting. Keep recommendations concise and actionable.
        """
        
        data = {
            "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,  # Reduced for faster response
            "temperature": 0.3,
            "top_p": 0.8,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                # Clean up the response to ensure it's plain text
                lines = content.split('\n')
                # Take only first 5 lines
                clean_content = '\n'.join(lines[:5])
                return clean_content
            
            return "Focus on improving weak areas with targeted practice. Review fundamental concepts regularly. Use online resources for additional learning. Practice coding problems daily. Seek feedback from mentors or peers."
        except Exception as e:
            return f"Focus on improving weak areas with targeted practice. Review fundamental concepts regularly. Use online resources for additional learning. Practice coding problems daily. Seek feedback from mentors or peers."
    
    return "Invalid API provider specified."