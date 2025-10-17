import streamlit as st
import requests
import json
import os
import tempfile
from PIL import Image
import base64

# Set page config
st.set_page_config(
    page_title="Skill Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for space theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #0D0D0D 100%);
        color: #E5E5E5;
    }
    .main-header {
        color: #A0D8F1;
        text-align: center;
        text-shadow: 0 0 12px rgba(160, 216, 241, 0.6);
        font-weight: 600;
    }
    .stButton>button {
        background: rgba(20, 20, 20, 0.8);
        color: #E5E5E5;
        border: 1px solid #A0D8F1;
        border-radius: 50px;
        padding: 14px 30px;
        font-weight: 600;
        transition: all 0.4s ease;
    }
    .stButton>button:hover {
        background: rgba(30, 30, 30, 0.9);
        color: #FFD700;
        border-color: #FFD700;
        box-shadow: 0 0 18px rgba(160, 216, 241, 0.4);
    }
    .skill-button {
        background: rgba(20, 20, 20, 0.8);
        color: #E5E5E5;
        border: 1px solid #A0D8F1;
        padding: 16px 30px;
        margin: 15px;
        border-radius: 50px;
        cursor: pointer;
        font-size: 17px;
        font-weight: 600;
        transition: all 0.4s ease;
        box-shadow: 0 0 15px rgba(160, 216, 241, 0.2);
    }
    .chat-message {
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .user-message {
        background: rgba(245, 245, 220, 0.15);
        color: #f5f5dc;
        text-align: right;
        border: 1px solid rgba(245, 245, 220, 0.3);
    }
    .bot-message {
        background: rgba(30, 30, 30, 0.8);
        color: #f5f5dc;
        border: 1px solid rgba(245, 245, 220, 0.2);
    }
    .stProgress > div > div > div {
        background-color: #A0D8F1;
    }
    .stSelectbox > div > div {
        background: rgba(25, 25, 25, 0.8);
        border: 1px solid rgba(160, 216, 241, 0.2);
        color: #E5E5E5;
    }
    .stTextInput > div > input {
        background: rgba(25, 25, 25, 0.8);
        border: 1px solid rgba(160, 216, 241, 0.2);
        color: #E5E5E5;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>🎓 Skill Recommendation System</h1>", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 'home'
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ''
if 'assessment_questions' not in st.session_state:
    st.session_state.assessment_questions = []
if 'assessment_answers' not in st.session_state:
    st.session_state.assessment_answers = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_skills' not in st.session_state:
    st.session_state.selected_skills = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# Function to add message to chat history
def add_chat_message(role, message):
    st.session_state.chat_history.append({"role": role, "message": message})

# Function to reset session state
def reset_session():
    st.session_state.resume_text = ''
    st.session_state.assessment_questions = []
    st.session_state.assessment_answers = []
    st.session_state.current_question_index = 0
    st.session_state.assessment_complete = False
    st.session_state.chat_history = []
    st.session_state.selected_skills = []
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.answers = []
    if 'extracted_skills' in st.session_state:
        del st.session_state.extracted_skills

# Function to generate personalized questions based on extracted skills
def generate_personalized_questions(extracted_skills):
    """
    Generate personalized questions based on extracted skills
    """
    questions = []
    
    # If we have extracted skills, create skill-specific questions
    if extracted_skills:
        for i, skill in enumerate(extracted_skills[:5]):  # Limit to top 5 skills
            skill_name = skill['name']
            questions.append(f"Can you describe a challenging project you worked on using {skill_name} and how you overcame obstacles?")
            questions.append(f"What are your strengths and areas for improvement in {skill_name}?")
            questions.append(f"How do you stay updated with the latest trends and best practices in {skill_name}?")
    
    # Add some general career questions if we don't have enough
    while len(questions) < 10:
        general_questions = [
            "What motivated you to pursue a career in technology?",
            "Describe a situation where you had to work in a team to solve a technical problem.",
            "What is your approach to debugging complex issues in code?",
            "How do you prioritize tasks when working on multiple projects?",
            "What tools or methodologies do you use for version control and collaboration?",
            "Can you explain a technical concept from your resume in simple terms?",
            "What are your short-term and long-term career goals in the technology field?",
            "How do you handle tight deadlines and high-pressure situations?",
            "What's the most challenging technical problem you've solved, and what did you learn from it?",
            "How do you approach learning new technologies and programming languages?"
        ]
        # Add remaining questions from general pool
        remaining_needed = 10 - len(questions)
        questions.extend(general_questions[:remaining_needed])
        break
    
    # Ensure we have exactly 10 questions
    return questions[:10] if len(questions) >= 10 else questions + [
        "What are your career aspirations in the technology field?",
        "How do you handle feedback and criticism on your work?",
        "What makes you stand out from other candidates in your field?"
    ][:10-len(questions)]

# Function to generate personalized recommendations
def generate_personalized_recommendations(questions, answers, extracted_skills):
    """
    Generate personalized recommendations based on user responses and extracted skills
    """
    # Create a summary of skills
    skill_names = [skill['name'] for skill in extracted_skills[:5]] if extracted_skills else []
    skills_text = f" (skills: {', '.join(skill_names)})" if skill_names else ""
    
    # Analyze answers for keywords to provide better recommendations
    answer_text = " ".join([ans for ans in answers if ans])
    technical_terms = ["project", "team", "debug", "solution", "implement", "design", "develop"]
    behavioral_terms = ["communicate", "collaborate", "lead", "manage", "organize", "prioritize"]
    
    has_technical_detail = any(term in answer_text.lower() for term in technical_terms)
    has_behavioral_detail = any(term in answer_text.lower() for term in behavioral_terms)
    
    # Generate personalized recommendations
    recommendations = "Based on your resume analysis and responses, here are my recommendations:\n\n"
    
    if skill_names:
        recommendations += f"• You have experience in {', '.join(skill_names[:3])}. "
        recommendations += "Focus on highlighting specific projects and achievements with these technologies in your job applications.\n"
    
    if has_technical_detail:
        recommendations += "• You demonstrate strong technical communication skills. Continue developing this by contributing to technical blogs or documentation.\n"
    else:
        recommendations += "• Work on providing more specific technical details when describing your projects and experiences.\n"
    
    if has_behavioral_detail:
        recommendations += "• You show good awareness of teamwork and collaboration. Emphasize leadership experiences in your interviews.\n"
    else:
        recommendations += "• Practice articulating your teamwork and leadership experiences more clearly.\n"
    
    # General recommendations
    recommendations += "\nGeneral improvement areas:\n"
    recommendations += "• Practice explaining complex technical concepts in simple terms\n"
    recommendations += "• Prepare specific examples from your projects to demonstrate your capabilities\n"
    recommendations += "• Research the companies you're applying to and tailor your responses accordingly\n"
    recommendations += "• Continue learning and staying updated with industry trends\n"
    
    return recommendations

# Function to generate assessment recommendations
def generate_assessment_recommendations(score_percentage, skill_performance, selected_skills):
    """
    Generate personalized recommendations based on assessment performance
    """
    recommendations = ""
    
    # Overall performance feedback
    if score_percentage < 60:
        recommendations += "You need to improve in the selected skills. "
        recommendations += "Focus on fundamental concepts and practice more problems.\n\n"
    elif score_percentage < 80:
        recommendations += "Good performance, but there's room for improvement. "
        recommendations += "Practice more problems and review advanced topics.\n\n"
    else:
        recommendations += "Excellent performance! Continue challenging yourself with advanced topics and real-world projects.\n\n"
    
    # Skill-specific recommendations
    if skill_performance:
        recommendations += "Skill-specific recommendations:\n"
        for skill, data in skill_performance.items():
            skill_percentage = (data['correct'] / data['total']) * 100
            if skill_percentage < 60:
                recommendations += f"• {skill}: Focus on fundamental concepts. Review basics and practice more problems.\n"
            elif skill_percentage < 80:
                recommendations += f"• {skill}: Good understanding but needs improvement. Practice advanced problems.\n"
            else:
                recommendations += f"• {skill}: Strong understanding. Challenge yourself with complex problems.\n"
    
    # Study resources recommendations
    recommendations += "\nRecommended study resources:\n"
    for skill in selected_skills[:3]:  # Limit to top 3 skills
        if "Python" in skill:
            recommendations += "• Python: Complete Python documentation, Automate the Boring Stuff with Python\n"
        elif "Java" in skill:
            recommendations += "• Java: Oracle's Java Tutorials, Effective Java by Joshua Bloch\n"
        elif "C" in skill:
            recommendations += "• C Programming: The C Programming Language by Kernighan and Ritchie\n"
        elif "Data Structures" in skill:
            recommendations += "• Data Structures: Introduction to Algorithms by Cormen et al.\n"
        elif "SQL" in skill:
            recommendations += "• SQL: SQL Cookbook by Anthony Molinaro\n"
        elif "Machine Learning" in skill:
            recommendations += "• Machine Learning: Hands-On Machine Learning by Aurélien Géron\n"
        elif "Operating System" in skill:
            recommendations += "• Operating Systems: Operating System Concepts by Silberschatz et al.\n"
        elif "Web Development" in skill:
            recommendations += "• Web Development: MDN Web Docs, freeCodeCamp tutorials\n"
        else:
            recommendations += f"• {skill}: Search for online courses and tutorials on {skill}\n"
    
    return recommendations

# Home page
if st.session_state.mode == 'home':
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 Skill Assessment")
        st.write("Test your knowledge in various Computer Science skills through adaptive MCQ assessments.")
        if st.button("Start Skill Assessment", key="skill_assessment_btn"):
            st.session_state.mode = 'skill_assessment'
            reset_session()
            st.experimental_rerun()
    
    with col2:
        st.markdown("### 📄 Resume Analysis")
        st.write("Upload your resume for AI-powered skill extraction and personalized recommendations.")
        if st.button("Start Resume Analysis", key="resume_analysis_btn"):
            st.session_state.mode = 'resume_analysis'
            reset_session()
            st.experimental_rerun()

# Skill Assessment Mode
elif st.session_state.mode == 'skill_assessment':
    st.markdown("### 🧠 Skill Assessment")
    
    # Show skill selection if we haven't started the assessment yet
    if not st.session_state.selected_skills or len(st.session_state.questions) == 0:
        # Skill selection
        st.markdown("#### Select Skills to Test")
        
        # Available skills (hardcoded for now, in a real app this would come from the backend)
        available_skills = [
            "Python", "C Programming", "Java", "Data Structures & Algorithms",
            "SQL + DBMS", "Machine Learning", "Operating System",
            "Web Development (HTML/CSS/JS + Basics React)"
        ]
        
        # Create checkboxes for each skill
        selected_skills = []
        cols = st.columns(2)
        for i, skill in enumerate(available_skills):
            with cols[i % 2]:
                if st.checkbox(skill, key=f"skill_{skill}"):
                    selected_skills.append(skill)
        
        st.session_state.selected_skills = selected_skills
        
        # Question count selection
        question_count = st.slider("Number of Questions", min_value=5, max_value=25, value=10)
        
        # Single Start assessment button with proper logic
        if st.button("Start Assessment", key="start_assessment_btn"):
            if selected_skills:
                # In a real implementation, we would fetch questions from the backend
                # For this demo, we'll generate more meaningful sample questions
                sample_questions = []
                
                # Generate skill-specific questions
                skill_specific_questions = {
                    "Python": [
                        "What is the output of the following Python code: print(2 ** 3 ** 2)?",
                        "Which of the following is NOT a valid way to create a dictionary in Python?",
                        "What is the time complexity of binary search in a sorted list?",
                        "In Python, what does the 'global' keyword do?",
                        "What is the difference between '==' and 'is' operators in Python?"
                    ],
                    "C Programming": [
                        "What is the output of the following C code: int x=5; printf('%%d %%d %%d', x++, ++x, x--);?",
                        "Which of the following is true about static variables in C?",
                        "What is the purpose of the 'const' keyword in C?",
                        "In C, what is the difference between 'malloc' and 'calloc'?",
                        "What will be the output of: int a[5] = {1,2,3,4,5}; printf('%%d', *(a+2));?"
                    ],
                    "Java": [
                        "What is the output of the following Java code involving inheritance?",
                        "Which of the following is true about Java interfaces?",
                        "What is the purpose of the 'finally' block in Java exception handling?",
                        "In Java, what is the difference between '==' and '.equals()' methods?",
                        "What is the time complexity of HashMap operations in Java?"
                    ],
                    "Data Structures & Algorithms": [
                        "What is the time complexity of insertion in a balanced binary search tree?",
                        "Which data structure is most appropriate for implementing BFS?",
                        "What is the space complexity of merge sort algorithm?",
                        "In a hash table, what is collision and how is it handled?",
                        "What is the difference between stack and queue data structures?"
                    ],
                    "SQL + DBMS": [
                        "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
                        "Which normal form eliminates transitive dependency?",
                        "What is the purpose of indexing in a database?",
                        "What is the ACID property in database transactions?",
                        "How would you optimize a slow-running SQL query?"
                    ],
                    "Machine Learning": [
                        "What is the difference between supervised and unsupervised learning?",
                        "What is overfitting and how can it be prevented?",
                        "Explain the bias-variance tradeoff in machine learning.",
                        "What is the purpose of cross-validation in model evaluation?",
                        "What is the difference between precision and recall metrics?"
                    ],
                    "Operating System": [
                        "What is the difference between process and thread?",
                        "Explain the concept of virtual memory in operating systems.",
                        "What is a deadlock and what are the necessary conditions for it to occur?",
                        "What is the purpose of a page table in memory management?",
                        "What is the difference between preemptive and non-preemptive scheduling?"
                    ],
                    "Web Development (HTML/CSS/JS + Basics React)": [
                        "What is the difference between 'let', 'const', and 'var' in JavaScript?",
                        "Explain the CSS box model and its components.",
                        "What is the virtual DOM in React and how does it improve performance?",
                        "What is the purpose of useEffect hook in React?",
                        "What is the difference between session storage and local storage?"
                    ]
                }
                
                # Get questions for selected skills
                all_questions = []
                for skill in selected_skills:
                    if skill in skill_specific_questions:
                        all_questions.extend(skill_specific_questions[skill])
                    else:
                        # Fallback to generic questions
                        all_questions.extend([
                            "What is the time complexity of this algorithm?",
                            "Identify the bug in this code snippet.",
                            "What is the output of this code execution?",
                            "Which design pattern is being used here?",
                            "How would you optimize this solution?"
                        ])
                
                # Select the requested number of questions
                import random
                selected_questions = random.sample(all_questions, min(question_count, len(all_questions)))
                
                for i, question_text in enumerate(selected_questions):
                    sample_questions.append({
                        "question_id": f"Q{i+1}",
                        "question": question_text,
                        "options": [
                            "This is the correct approach for the given scenario",
                            "This approach has a logical error in implementation",
                            "This solution is inefficient for the given problem",
                            "This method is not applicable to the problem"
                        ],
                        "correct_answer": 0,
                        "skill": selected_skills[0] if selected_skills else "General"
                    })
                
                st.session_state.questions = sample_questions
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.experimental_rerun()
            else:
                st.warning("Please select at least one skill to test.")
    
    # Display questions if we have them
    elif (st.session_state.selected_skills and 
          st.session_state.questions and 
          len(st.session_state.questions) > 0 and 
          st.session_state.current_question < len(st.session_state.questions)):
        # Display current question
        question = st.session_state.questions[st.session_state.current_question]
        
        st.markdown(f"**Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}**")
        st.markdown(f"### {question['question']}")
        
        # Display options
        selected_option = st.radio("Select your answer:", question['options'], key=f"question_{st.session_state.current_question}")
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Previous", key="prev_btn") and st.session_state.current_question > 0:
                st.session_state.current_question -= 1
                st.experimental_rerun()
        
        with col2:
            if st.button("Next", key="next_btn") and st.session_state.current_question < len(st.session_state.questions) - 1:
                # Save answer
                st.session_state.answers.append({
                    "questionId": question["question_id"],
                    "question": question["question"],
                    "selectedOption": question['options'].index(selected_option) if selected_option in question['options'] else 0,
                    "correct": question['options'].index(selected_option) == question['correct_answer'] if selected_option in question['options'] else False,
                    "skill": question["skill"]
                })
                st.session_state.current_question += 1
                st.experimental_rerun()
        
        with col3:
            if st.button("Submit", key="submit_btn") and st.session_state.current_question == len(st.session_state.questions) - 1:
                # Save last answer
                st.session_state.answers.append({
                    "questionId": question["question_id"],
                    "question": question["question"],
                    "selectedOption": question['options'].index(selected_option) if selected_option in question['options'] else 0,
                    "correct": question['options'].index(selected_option) == question['correct_answer'] if selected_option in question['options'] else False,
                    "skill": question["skill"]
                })
                # In a real implementation, we would send answers to backend for evaluation
                # For this demo, we'll just show results
                st.session_state.mode = 'assessment_results'
                st.experimental_rerun()
    
    # Back to home button
    if st.button("Back to Home", key="back_to_home_assessment"):
        st.session_state.mode = 'home'
        reset_session()
        st.experimental_rerun()

# Assessment Results
elif st.session_state.mode == 'assessment_results':
    st.markdown("### 📊 Assessment Results")
    
    # Calculate score
    correct_count = sum(1 for answer in st.session_state.answers if answer.get('correct', False))
    total_questions = len(st.session_state.answers)
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Display score
    st.markdown(f"#### Your Score: {score_percentage:.1f}%")
    st.progress(score_percentage / 100)
    st.markdown(f"**Correct Answers:** {correct_count} / {total_questions}")
    
    # Group results by skill
    skill_performance = {}
    for answer in st.session_state.answers:
        skill = answer.get('skill', 'General')
        if skill not in skill_performance:
            skill_performance[skill] = {'correct': 0, 'total': 0}
        skill_performance[skill]['total'] += 1
        if answer.get('correct', False):
            skill_performance[skill]['correct'] += 1
    
    # Display skill-wise performance
    if skill_performance:
        st.markdown("#### Skill-wise Performance:")
        for skill, data in skill_performance.items():
            skill_percentage = (data['correct'] / data['total']) * 100
            st.markdown(f"- **{skill}**: {data['correct']}/{data['total']} ({skill_percentage:.1f}%)")
    
    # Display personalized recommendations
    st.markdown("#### Personalized Recommendations:")
    
    # Generate recommendations based on performance
    recommendations = generate_assessment_recommendations(score_percentage, skill_performance, st.session_state.selected_skills)
    st.write(recommendations)
    
    # Back to home button
    if st.button("Back to Home", key="back_to_home_assessment_results"):
        st.session_state.mode = 'home'
        reset_session()
        st.experimental_rerun()

# Resume Analysis Mode
elif st.session_state.mode == 'resume_analysis':
    st.markdown("### 📄 Resume Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None and not st.session_state.resume_text:
        try:
            # Show processing message
            with st.spinner("Processing your resume..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Parse the resume using our utility
                try:
                    from app.utils.resume_parser import parse_resume
                    resume_text = parse_resume(tmp_file_path)
                    
                    # Extract skills using our utility
                    from app.utils.skill_extractor import extract_skills
                    extracted_skills = extract_skills(resume_text)
                    
                    # Store resume text and extracted skills
                    st.session_state.resume_text = resume_text
                    st.session_state.extracted_skills = extracted_skills
                    
                    # Add initial bot messages
                    skill_names = [skill['name'] for skill in extracted_skills[:5]]  # Show top 5 skills
                    if skill_names:
                        add_chat_message("bot", f"I've analyzed your resume and found the following skills: {', '.join(skill_names)}")
                    else:
                        add_chat_message("bot", "I've analyzed your resume. I'll ask you some general questions about your experience.")
                    
                    add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 10 questions based on your resume.")
                    
                    # Generate personalized questions based on extracted skills
                    sample_questions = generate_personalized_questions(extracted_skills)
                    st.session_state.assessment_questions = sample_questions
                    st.session_state.assessment_answers = [""] * len(sample_questions)
                    st.session_state.current_question_index = 0
                    st.session_state.assessment_complete = False
                    
                except Exception as e:
                    # If there's an error with the utilities, fall back to simulation
                    st.warning(f"Could not process resume with utilities: {str(e)}. Using simulation mode.")
                    st.session_state.resume_text = "This is a sample resume text extracted from the uploaded file. In a real implementation, this would contain the actual resume content."
                    add_chat_message("bot", "I've analyzed your resume. I found the following skills: Python, Java, Machine Learning, SQL.")
                    add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 10 questions based on your resume.")
                    
                    # Generate sample questions
                    sample_questions = [
                        "What motivated you to pursue a career in technology?",
                        "Can you describe a challenging project you worked on and how you overcame obstacles?",
                        "What programming languages or technologies mentioned in your resume are you most proficient in?",
                        "How do you stay updated with the latest trends in technology?",
                        "Describe a situation where you had to work in a team to solve a technical problem.",
                        "What is your approach to debugging complex issues in code?",
                        "How do you prioritize tasks when working on multiple projects?",
                        "What tools or methodologies do you use for version control and collaboration?",
                        "Can you explain a technical concept from your resume in simple terms?",
                        "What are your career goals in the technology field?"
                    ]
                    st.session_state.assessment_questions = sample_questions
                    st.session_state.assessment_answers = [""] * len(sample_questions)
                    st.session_state.current_question_index = 0
                    st.session_state.assessment_complete = False
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass  # Ignore cleanup errors
                        
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
            # Fallback to simulation
            st.session_state.resume_text = "This is a sample resume text extracted from the uploaded file. In a real implementation, this would contain the actual resume content."
            add_chat_message("bot", "I've analyzed your resume. I found the following skills: Python, Java, Machine Learning, SQL.")
            add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 10 questions based on your resume.")
            
            # Generate sample questions
            sample_questions = [
                "What motivated you to pursue a career in technology?",
                "Can you describe a challenging project you worked on and how you overcame obstacles?",
                "What programming languages or technologies mentioned in your resume are you most proficient in?",
                "How do you stay updated with the latest trends in technology?",
                "Describe a situation where you had to work in a team to solve a technical problem.",
                "What is your approach to debugging complex issues in code?",
                "How do you prioritize tasks when working on multiple projects?",
                "What tools or methodologies do you use for version control and collaboration?",
                "Can you explain a technical concept from your resume in simple terms?",
                "What are your career goals in the technology field?"
            ]
            st.session_state.assessment_questions = sample_questions
            st.session_state.assessment_answers = [""] * len(sample_questions)
            st.session_state.current_question_index = 0
            st.session_state.assessment_complete = False
    
    # Display chat history
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-message user-message'><strong>You:</strong><br>{msg['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message bot-message'><strong>Assistant:</strong><br>{msg['message']}</div>", unsafe_allow_html=True)
    
    # Display current assessment question
    if st.session_state.assessment_questions and st.session_state.current_question_index < len(st.session_state.assessment_questions):
        current_question = st.session_state.assessment_questions[st.session_state.current_question_index]
        st.markdown(f"**Question {st.session_state.current_question_index + 1}:** {current_question}")
        
        # Answer input
        answer = st.text_area("Your answer:", key=f"answer_{st.session_state.current_question_index}", height=100)
        
        # Submit answer button
        if st.button("Submit Answer", key="submit_answer_btn"):
            if answer.strip():
                st.session_state.assessment_answers[st.session_state.current_question_index] = answer
                st.session_state.current_question_index += 1
                
                if st.session_state.current_question_index >= len(st.session_state.assessment_questions):
                    # Assessment complete
                    st.session_state.assessment_complete = True
                    add_chat_message("user", answer)
                    add_chat_message("bot", "Thank you for completing the assessment! Analyzing your responses...")
                    
                    # Generate personalized recommendations
                    recommendations = generate_personalized_recommendations(
                        st.session_state.assessment_questions, 
                        st.session_state.assessment_answers,
                        st.session_state.extracted_skills if 'extracted_skills' in st.session_state else []
                    )
                    add_chat_message("bot", recommendations)
                    st.experimental_rerun()
                else:
                    add_chat_message("user", answer)
                    st.experimental_rerun()
            else:
                st.warning("Please provide an answer before submitting.")
    
    # Back to home button
    if st.button("Back to Home", key="back_to_home_resume_analysis"):
        st.session_state.mode = 'home'
        reset_session()
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #E5E5E5;'>Developed by Sudev Basti</div>", unsafe_allow_html=True)