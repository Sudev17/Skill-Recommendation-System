import streamlit as st
import requests
import json
import os
import tempfile
from PIL import Image
import base64
import sys

# Add the backend directory to the Python path
# Handle different possible paths for deployment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, 'backend')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)
else:
    # Try alternative path for deployment
    alt_backend_path = os.path.join(current_dir, '..', 'backend')
    if os.path.exists(alt_backend_path):
        sys.path.insert(0, alt_backend_path)

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
    while len(questions) < 6:
        general_questions = [
            "What motivated you to pursue a career in technology?",
            "Describe a situation where you had to work in a team to solve a technical problem.",
            "What is your approach to debugging complex issues in code?",
            "How do you prioritize tasks when working on multiple projects?",
            "What tools or methodologies do you use for version control and collaboration?",
            "Can you explain a technical concept from your resume in simple terms?"
        ]
        # Add remaining questions from general pool
        remaining_needed = 6 - len(questions)
        questions.extend(general_questions[:remaining_needed])
        break
    
    # Ensure we have exactly 6 questions
    return questions[:6] if len(questions) >= 6 else questions + [
        "What are your career aspirations in the technology field?",
        "How do you handle feedback and criticism on your work?"
    ][:6-len(questions)]

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

# Function to analyze resume responses using backend API
def analyze_resume_responses_with_api(resume_text, questions_and_answers, api_provider='nvidia'):
    """
    Analyze resume responses using the backend API
    """
    try:
        # Prepare the data to send to the backend
        data = {
            'resume_text': resume_text,
            'questions_and_answers': questions_and_answers,
            'api_provider': api_provider
        }
        
        # Make API call to backend
        backend_url = "http://localhost:5000/api/analyze-resume-responses"
        response = requests.post(backend_url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            feedback = result.get('feedback', 'No feedback received from the analysis.')
            # Check if the feedback indicates an API key issue
            if "API key" in feedback and ("unable to access" in feedback or "configuration" in feedback):
                return {
                    'success': False,
                    'feedback': feedback,
                    'error_type': 'api_key'
                }
            return {
                'success': True,
                'feedback': feedback
            }
        else:
            return {
                'success': False,
                'feedback': f"Error: Received status code {response.status_code} from backend.",
                'error_type': 'http_error'
            }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'feedback': "Error: Request to backend timed out. Please try again.",
            'error_type': 'timeout'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'feedback': "Error: Could not connect to backend service. Please ensure the backend server is running.",
            'error_type': 'connection_error'
        }
    except Exception as e:
        return {
            'success': False,
            'feedback': f"Error: {str(e)}",
            'error_type': 'unknown'
        }

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
                
                # Function to generate skill-specific options (copied from backend)
                def generate_options_for_question(question_text, skill):
                    """Generate realistic options for a given question"""
                    # Generate skill-specific options based on the actual question content
                    if skill == 'Python':
                        if 'output' in question_text.lower() and 'print' in question_text.lower():
                            return [
                                "64 (exponentiation is right-associative)",
                                "512 (exponentiation is left-associative)",
                                "18 (multiplication is performed first)",
                                "Syntax Error"
                            ]
                        elif 'dictionary' in question_text.lower():
                            return [
                                "dict = {'a': 1, 'b': 2}",
                                "{'a': 1, 'b': 2}",
                                "dict('a' => 1, 'b' => 2)",
                                "dict(a=1, b=2)"
                            ]
                        elif 'time complexity' in question_text.lower() and 'binary search' in question_text.lower():
                            return [
                                "O(log n)",
                                "O(n)",
                                "O(n log n)",
                                "O(1)"
                            ]
                        elif 'global' in question_text.lower():
                            return [
                                "It allows modification of a global variable inside a function",
                                "It creates a new local variable with the same name",
                                "It deletes the global variable",
                                "It has no effect on variable scope"
                            ]
                        elif '==' in question_text.lower() and 'is' in question_text.lower():
                            return [
                                "'==' compares values, 'is' compares object identity",
                                "Both compare values but 'is' is faster",
                                "Both compare object identity but '==' is faster",
                                "'is' compares values, '==' compares object identity"
                            ]
                        elif 'append' in question_text.lower():
                            return [
                                "4",
                                "3",
                                "5",
                                "Error: append() returns None"
                            ]
                        elif 'garbage' in question_text.lower() and 'collection' in question_text.lower():
                            return [
                                "Python uses reference counting and cyclic garbage collection",
                                "Python doesn't have garbage collection",
                                "Python only uses reference counting",
                                "Python only uses cyclic garbage collection"
                            ]
                        elif '__init__' in question_text.lower():
                            return [
                                "To initialize the object's attributes when it's created",
                                "To destroy the object when it's no longer needed",
                                "To make the class inheritable",
                                "To define static methods"
                            ]
                        elif 'file opening mode' in question_text.lower():
                            return [
                                "'x' (exclusive creation)",
                                "'r+' (read and write)",
                                "'w+' (write and read)",
                                "'a+' (append and read)"
                            ]
                        elif 'type' in question_text.lower() and 'lambda' in question_text.lower():
                            return [
                                "<class 'function'>",
                                "<class 'method'>",
                                "<class 'lambda'>",
                                "Syntax Error"
                            ]
                        else:
                            # Generic but relevant options for other Python questions
                            return [
                                "It defines the behavior of objects in the language",
                                "It's a syntax rule with no practical impact",
                                "It's only relevant for object-oriented programming",
                                "It affects memory allocation but not program behavior"
                            ]
                    elif skill == 'Java':
                        if 'hashmap' in question_text.lower() and 'time complexity' in question_text.lower():
                            return [
                                "O(1) average case for get/put operations",
                                "O(log n) for all operations",
                                "O(n) for all operations",
                                "O(1) for all operations"
                            ]
                        elif 'interface' in question_text.lower():
                            return [
                                "Interfaces can contain only abstract methods and constants",
                                "Interfaces can contain both abstract and concrete methods",
                                "Interfaces can have instance variables",
                                "Interfaces don't support multiple inheritance"
                            ]
                        elif 'finally' in question_text.lower():
                            return [
                                "The finally block always executes whether an exception occurs or not",
                                "The finally block only executes when an exception is caught",
                                "The finally block prevents exceptions from being thrown",
                                "The finally block is optional in exception handling"
                            ]
                        elif '==' in question_text.lower() and 'equals' in question_text.lower():
                            return [
                                "'==' compares references, equals() compares content",
                                "'==' compares content, equals() compares references",
                                "Both compare content but '==' is faster",
                                "Both compare references but equals() is faster"
                            ]
                        elif 'static' in question_text.lower():
                            return [
                                "Static members belong to the class rather than instances",
                                "Static members are loaded when the class is instantiated",
                                "Static members cannot be accessed directly",
                                "Static members are unique for each object"
                            ]
                        elif 'inheritance' in question_text.lower():
                            return [
                                "The child class inherits fields and methods from the parent class",
                                "The parent class inherits fields and methods from the child class",
                                "Both classes share the same memory space",
                                "Inheritance is not supported in Java"
                            ]
                        elif 'access modifier' in question_text.lower():
                            return [
                                "private, default, protected, public",
                                "private, protected, public, global",
                                "internal, external, protected, public",
                                "final, abstract, static, volatile"
                            ]
                        elif 'garbage' in question_text.lower() and 'collection' in question_text.lower():
                            return [
                                "Java uses automatic garbage collection to reclaim memory",
                                "Java requires manual memory management",
                                "Java doesn't have garbage collection",
                                "Java only collects memory when the program exits"
                            ]
                        elif 'extern' in question_text.lower():
                            return [
                                "To declare a variable that is defined in another file",
                                "To make a variable accessible from multiple functions",
                                "To allocate memory for a global variable",
                                "To create a copy of a variable in another file"
                            ]
                        elif 'string' in question_text.lower() and '==' in question_text.lower():
                            return [
                                "false because s1 and s2 refer to different objects",
                                "true because s1 and s2 have the same content",
                                "true because string literals are interned",
                                "Compilation error due to invalid syntax"
                            ]
                        else:
                            # Generic but relevant options for other Java questions
                            return [
                                "It's a core concept that affects object behavior",
                                "It's a syntactic feature with minimal runtime impact",
                                "It's only relevant for enterprise applications",
                                "It primarily affects performance characteristics"
                            ]
                    elif skill == 'C Programming':
                        if 'output' in question_text.lower() and ('printf' in question_text.lower() or 'x++' in question_text.lower()):
                            return [
                                "5 7 6",
                                "6 7 5",
                                "5 6 7",
                                "Compilation Error"
                            ]
                        elif 'static' in question_text.lower():
                            return [
                                "Static variables retain their value between function calls",
                                "Static variables are allocated on the heap",
                                "Static variables are automatically initialized to zero",
                                "Static variables can only be accessed within the same file"
                            ]
                        elif 'const' in question_text.lower():
                            return [
                                "To declare a variable whose value cannot be changed",
                                "To allocate memory in the constant pool",
                                "To make a variable accessible from other files",
                                "To optimize the variable for faster access"
                            ]
                        elif 'malloc' in question_text.lower() and 'calloc' in question_text.lower():
                            return [
                                "malloc doesn't initialize memory, calloc initializes to zero",
                                "malloc is faster but less secure",
                                "calloc can allocate more memory than malloc",
                                "There is no difference, they are synonyms"
                            ]
                        elif 'pointer' in question_text.lower():
                            return [
                                "Pointers store memory addresses of variables",
                                "Pointers are only used for dynamic memory allocation",
                                "Pointers can only point to integer variables",
                                "Pointers automatically dereference when used"
                            ]
                        elif 'extern' in question_text.lower():
                            return [
                                "To declare a variable that is defined in another file",
                                "To make a variable accessible from multiple functions",
                                "To allocate memory for a global variable",
                                "To create a copy of a variable in another file"
                            ]
                        else:
                            # Generic but relevant options for other C questions
                            return [
                                "It's a fundamental concept that affects program execution",
                                "It's a syntactic feature with minimal impact",
                                "It's only relevant for advanced programming scenarios",
                                "It primarily affects memory usage patterns"
                            ]
                    elif skill == 'Data Structures & Algorithms':
                        if 'balanced binary search tree' in question_text.lower() and 'insertion' in question_text.lower():
                            return [
                                "O(log n)",
                                "O(n)",
                                "O(n log n)",
                                "O(1)"
                            ]
                        elif 'bfs' in question_text.lower():
                            return [
                                "Queue",
                                "Stack",
                                "Array",
                                "Linked List"
                            ]
                        elif 'merge sort' in question_text.lower() and 'space complexity' in question_text.lower():
                            return [
                                "O(n)",
                                "O(log n)",
                                "O(n log n)",
                                "O(1)"
                            ]
                        elif 'collision' in question_text.lower() and 'hash table' in question_text.lower():
                            return [
                                "When two keys map to the same index; handled by chaining or open addressing",
                                "When the hash table becomes full; handled by resizing",
                                "When two values are identical; handled by duplicate removal",
                                "When the hash function fails; handled by rehashing"
                            ]
                        elif 'stack' in question_text.lower() and 'queue' in question_text.lower():
                            return [
                                "Stack is LIFO, Queue is FIFO",
                                "Stack is FIFO, Queue is LIFO",
                                "Both are LIFO structures",
                                "Both are FIFO structures"
                            ]
                        elif 'sorting algorithm' in question_text.lower() and 'best average-case' in question_text.lower():
                            return [
                                "Merge Sort and Heap Sort: O(n log n)",
                                "Bubble Sort: O(n)",
                                "Quick Sort: O(n)",
                                "Insertion Sort: O(n log n)"
                            ]
                        elif "dijkstra" in question_text.lower() and 'binary heap' in question_text.lower():
                            return [
                                "O((V + E) log V)",
                                "O(V^2)",
                                "O(E)",
                                "O(V)"
                            ]
                        elif 'recursion' in question_text.lower():
                            return [
                                "Stack",
                                "Queue",
                                "Array",
                                "Tree"
                            ]
                        elif 'quicksort' in question_text.lower() and 'worst-case' in question_text.lower():
                            return [
                                "O(n^2)",
                                "O(n log n)",
                                "O(log n)",
                                "O(n)"
                            ]
                        elif 'traversal' in question_text.lower() and 'level-order' in question_text.lower():
                            return [
                                "Breadth-First Search (BFS)",
                                "Depth-First Search (DFS)",
                                "In-order traversal",
                                "Pre-order traversal"
                            ]
                        else:
                            # Generic but relevant options for other DSA questions
                            return [
                                "It's a fundamental concept that affects algorithm efficiency",
                                "It's a theoretical concept with minimal practical impact",
                                "It's only relevant for competitive programming",
                                "It primarily affects memory usage rather than time complexity"
                            ]
                    elif skill == 'SQL + DBMS':
                        if 'inner join' in question_text.lower() and 'left join' in question_text.lower():
                            return [
                                "INNER JOIN returns only matching rows, LEFT JOIN returns all left table rows",
                                "INNER JOIN returns all rows, LEFT JOIN returns only matching rows",
                                "Both return the same result set",
                                "INNER JOIN is faster but less accurate"
                            ]
                        elif 'normal form' in question_text.lower() and 'transitive dependency' in question_text.lower():
                            return [
                                "Third Normal Form (3NF)",
                                "First Normal Form (1NF)",
                                "Second Normal Form (2NF)",
                                "Boyce-Codd Normal Form (BCNF)"
                            ]
                        elif 'indexing' in question_text.lower():
                            return [
                                "To improve query performance by creating pointers to data",
                                "To encrypt sensitive data for security",
                                "To compress data for storage efficiency",
                                "To organize data in alphabetical order"
                            ]
                        elif 'acid' in question_text.lower():
                            return [
                                "Atomicity, Consistency, Isolation, Durability",
                                "Access, Control, Integrity, Durability",
                                "Accuracy, Consistency, Integrity, Durability",
                                "Atomicity, Concurrency, Isolation, Durability"
                            ]
                        elif 'optimize' in question_text.lower() and 'sql query' in question_text.lower():
                            return [
                                "Add indexes, rewrite queries, analyze execution plans",
                                "Increase server memory, upgrade hardware",
                                "Convert to stored procedures, use views",
                                "Normalize the database further, reduce table size"
                            ]
                        elif 'delete' in question_text.lower() and 'truncate' in question_text.lower():
                            return [
                                "DELETE can be rolled back, TRUNCATE cannot",
                                "DELETE is faster, TRUNCATE is slower",
                                "DELETE removes specific rows, TRUNCATE removes all rows",
                                "Both can be rolled back"
                            ]
                        elif 'primary key' in question_text.lower():
                            return [
                                "Uniquely identifies each record and cannot be NULL",
                                "Can have duplicate values but cannot be NULL",
                                "Uniquely identifies each record but can be NULL",
                                "Is optional and mainly for documentation"
                            ]
                        elif 'foreign key' in question_text.lower():
                            return [
                                "To maintain referential integrity between tables",
                                "To encrypt data between tables",
                                "To improve query performance",
                                "To create indexes automatically"
                            ]
                        elif 'char' in question_text.lower() and 'varchar' in question_text.lower():
                            return [
                                "CHAR is fixed-length, VARCHAR is variable-length",
                                "CHAR is variable-length, VARCHAR is fixed-length",
                                "Both are variable-length but CHAR is faster",
                                "Both are fixed-length but VARCHAR uses less memory"
                            ]
                        elif 'retrieve data' in question_text.lower():
                            return [
                                "SELECT",
                                "GET",
                                "FETCH",
                                "QUERY"
                            ]
                        else:
                            # Generic but relevant options for other SQL/DBMS questions
                            return [
                                "It's a critical concept for data integrity and performance",
                                "It's a syntactic feature with minimal database impact",
                                "It's only relevant for large-scale database systems",
                                "It primarily affects storage requirements rather than access speed"
                            ]
                    elif skill == 'Machine Learning':
                        if 'supervised' in question_text.lower() and 'unsupervised' in question_text.lower():
                            return [
                                "Supervised uses labeled data, unsupervised finds patterns in unlabeled data",
                                "Supervised is faster, unsupervised is more accurate",
                                "Supervised uses regression, unsupervised uses classification",
                                "Both require the same amount of data preprocessing"
                            ]
                        elif 'overfitting' in question_text.lower():
                            return [
                                "When a model learns training data too well and performs poorly on new data",
                                "When a model is too simple to capture data patterns",
                                "When training data is insufficient for model learning",
                                "When a model performs equally on training and test data"
                            ]
                        elif 'bias-variance' in question_text.lower():
                            return [
                                "Bias is error from assumptions, variance is sensitivity to training data",
                                "Bias is sensitivity to data, variance is error from assumptions",
                                "Both relate to model complexity but in opposite ways",
                                "Both are minimized by increasing training data size"
                            ]
                        elif 'cross-validation' in question_text.lower():
                            return [
                                "To assess model performance on unseen data",
                                "To speed up model training process",
                                "To reduce the size of training data",
                                "To eliminate outliers from the dataset"
                            ]
                        elif 'precision' in question_text.lower() and 'recall' in question_text.lower():
                            return [
                                "Precision is true positives over predicted positives, recall is true positives over actual positives",
                                "Precision is true positives over actual positives, recall is true positives over predicted positives",
                                "Both measure the same aspect but with different formulas",
                                "Precision is more important than recall for all applications"
                            ]
                        elif 'linearly separable' in question_text.lower():
                            return [
                                "Support Vector Machine (SVM)",
                                "K-Means Clustering",
                                "Decision Tree",
                                "Random Forest"
                            ]
                        elif 'regularization' in question_text.lower():
                            return [
                                "To prevent overfitting by adding penalty terms",
                                "To speed up model training by simplifying calculations",
                                "To normalize input features for better convergence",
                                "To increase model complexity for better accuracy"
                            ]
                        elif 'bagging' in question_text.lower() and 'boosting' in question_text.lower():
                            return [
                                "Bagging trains models in parallel, boosting trains sequentially",
                                "Bagging is for classification, boosting is for regression",
                                "Bagging reduces bias, boosting reduces variance",
                                "Both use the same training approach but different aggregation"
                            ]
                        elif 'imbalanced datasets' in question_text.lower():
                            return [
                                "F1-Score or AUC-ROC",
                                "Accuracy",
                                "Mean Squared Error",
                                "R-Squared"
                            ]
                        elif 'feature scaling' in question_text.lower():
                            return [
                                "To normalize feature ranges for equal contribution to the model",
                                "To reduce the number of features in the dataset",
                                "To eliminate outliers from the feature space",
                                "To convert categorical features to numerical"
                            ]
                        else:
                            # Generic but relevant options for other ML questions
                            return [
                                "It's a fundamental technique that affects model performance",
                                "It's a preprocessing step with minimal impact on results",
                                "It's only relevant for deep learning applications",
                                "It primarily affects training time rather than accuracy"
                            ]
                    elif skill == 'Operating System':
                        if 'process' in question_text.lower() and 'thread' in question_text.lower():
                            return [
                                "Process is a program in execution, thread is a lightweight process within a process",
                                "Process is single-threaded, thread is multi-threaded",
                                "Process uses more memory, thread uses less CPU",
                                "Both are identical but with different names"
                            ]
                        elif 'virtual memory' in question_text.lower():
                            return [
                                "A memory management technique that provides an illusion of large main memory",
                                "A hardware component that increases physical RAM",
                                "A software tool that compresses memory usage",
                                "A network protocol for remote memory access"
                            ]
                        elif 'deadlock' in question_text.lower():
                            return [
                                "Mutual exclusion, hold and wait, no preemption, circular wait",
                                "Race condition, starvation, livelock, priority inversion",
                                "Synchronization, serialization, isolation, atomicity",
                                "Blocking, sleeping, waiting, terminating"
                            ]
                        elif 'page table' in question_text.lower():
                            return [
                                "To map virtual addresses to physical addresses",
                                "To store frequently accessed pages for faster retrieval",
                                "To organize pages in chronological order",
                                "To encrypt pages for security purposes"
                            ]
                        elif 'preemptive' in question_text.lower() and 'non-preemptive' in question_text.lower():
                            return [
                                "Preemptive can interrupt processes, non-preemptive cannot",
                                "Preemptive is faster, non-preemptive is more secure",
                                "Preemptive uses priority, non-preemptive uses FIFO",
                                "Both provide the same level of control"
                            ]
                        elif 'semaphore' in question_text.lower():
                            return [
                                "To control access to shared resources by multiple processes",
                                "To encrypt communication between processes",
                                "To prioritize processes in the ready queue",
                                "To allocate memory dynamically to processes"
                            ]
                        elif 'paging' in question_text.lower() and 'segmentation' in question_text.lower():
                            return [
                                "Paging divides memory into fixed-size blocks, segmentation into variable-size blocks",
                                "Paging is faster, segmentation uses less memory",
                                "Paging is hardware-based, segmentation is software-based",
                                "Both provide the same memory organization approach"
                            ]
                        elif 'thrashing' in question_text.lower():
                            return [
                                "When a system spends more time swapping pages than executing processes",
                                "When CPU utilization is extremely high due to heavy processing",
                                "When multiple processes compete for the same resource",
                                "When memory fragmentation prevents efficient allocation"
                            ]
                        elif 'kernel' in question_text.lower():
                            return [
                                "Core component that manages system resources and hardware",
                                "User interface that allows interaction with the system",
                                "Application layer that provides utilities and services",
                                "Security module that protects system from malware"
                            ]
                        elif 'multitasking' in question_text.lower() and 'multiprocessing' in question_text.lower():
                            return [
                                "Multitasking runs multiple tasks on a single processor, multiprocessing uses multiple processors",
                                "Multitasking is software-based, multiprocessing is hardware-based",
                                "Multitasking is faster, multiprocessing is more secure",
                                "Both provide the same level of parallelism"
                            ]
                        else:
                            # Generic but relevant options for other OS questions
                            return [
                                "It's a core concept that affects system performance and resource management",
                                "It's a theoretical concept with minimal practical implementation",
                                "It's only relevant for server operating systems",
                                "It primarily affects user interface design rather than system efficiency"
                            ]
                    elif skill == 'Web Development (HTML/CSS/JS + Basics React)':
                        if 'let' in question_text.lower() and 'const' in question_text.lower() and 'var' in question_text.lower():
                            return [
                                "let is block-scoped, const is block-scoped and read-only, var is function-scoped",
                                "let is function-scoped, const is block-scoped, var is global-scoped",
                                "All have the same scope but different initialization rules",
                                "let and const are identical, var is deprecated"
                            ]
                        elif 'css box model' in question_text.lower():
                            return [
                                "Content, padding, border, margin",
                                "Header, body, footer, sidebar",
                                "Width, height, depth, opacity",
                                "Position, display, float, clear"
                            ]
                        elif 'virtual dom' in question_text.lower():
                            return [
                                "A lightweight representation of the actual DOM for performance optimization",
                                "A security feature that isolates components from the real DOM",
                                "A debugging tool that visualizes component hierarchy",
                                "A testing utility that simulates DOM events"
                            ]
                        elif 'useeffect' in question_text.lower():
                            return [
                                "To perform side effects in functional components",
                                "To manage component state in class components",
                                "To handle user events like clicks and inputs",
                                "To optimize rendering performance"
                            ]
                        elif 'session storage' in question_text.lower() and 'local storage' in question_text.lower():
                            return [
                                "Session storage is cleared when the page session ends, local storage persists",
                                "Session storage is faster, local storage is more secure",
                                "Session storage works only with HTTP, local storage works with HTTPS",
                                "Both have the same persistence but different APIs"
                            ]
                        elif 'css flexbox' in question_text.lower():
                            return [
                                "To create flexible layouts with alignment and distribution of space",
                                "To add animations and transitions to elements",
                                "To create responsive grids with fixed dimensions",
                                "To apply 3D transformations to elements"
                            ]
                        elif 'event bubbling' in question_text.lower():
                            return [
                                "When an event propagates from the target element up to its ancestors",
                                "When multiple events fire simultaneously on different elements",
                                "When an event handler creates an infinite loop of events",
                                "When event listeners are automatically removed after execution"
                            ]
                        elif '==' in question_text.lower() and '===' in question_text.lower():
                            return [
                                "'==' performs type coercion, '===' compares both value and type",
                                "'===' performs type coercion, '==' compares both value and type",
                                "Both perform type coercion but '===' is faster",
                                "Both compare value and type but '==' is more strict"
                            ]
                        elif 'react component' in question_text.lower():
                            return [
                                "Reusable, independent pieces of UI that manage their own state",
                                "Built-in HTML elements with enhanced functionality",
                                "CSS classes that define visual styles",
                                "JavaScript functions that always return HTML"
                            ]
                        elif 'transparent' in question_text.lower():
                            return [
                                "opacity",
                                "visibility",
                                "display",
                                "background"
                            ]
                        else:
                            # Generic but relevant options for other web development questions
                            return [
                                "It's a key concept that affects user experience and functionality",
                                "It's a syntactic feature with minimal impact on web performance",
                                "It's only relevant for modern frameworks and libraries",
                                "It primarily affects accessibility rather than visual design"
                            ]
                    else:
                        # For any other skills or if no specific pattern matches, generate relevant options
                        return [
                            "It's a fundamental concept that affects the domain's core functionality",
                            "It's a syntactic feature with minimal practical impact",
                            "It's an advanced topic that's only relevant in specific scenarios",
                            "It primarily affects performance or security characteristics"
                        ]
                
                for i, question_text in enumerate(selected_questions):
                    # Determine the skill for this question (use first selected skill as default)
                    skill = selected_skills[0] if selected_skills else "General"
                    
                    sample_questions.append({
                        "question_id": f"Q{i+1}",
                        "question": question_text,
                        "options": generate_options_for_question(question_text, skill),
                        "correct_answer": 0,
                        "skill": skill
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
                    from backend.app.utils.resume_parser import parse_resume
                    resume_text = parse_resume(tmp_file_path)
                    
                    # Extract skills using our utility
                    from backend.app.utils.skill_extractor import extract_skills
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
                        
                    add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 6 questions based on your resume.")
                    
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
                    add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 6 questions based on your resume.")
                    
                    # Generate sample questions
                    sample_questions = [
                        "What motivated you to pursue a career in technology?",
                        "Can you describe a challenging project you worked on and how you overcame obstacles?",
                        "What programming languages or technologies mentioned in your resume are you most proficient in?",
                        "How do you stay updated with the latest trends in technology?",
                        "Describe a situation where you had to work in a team to solve a technical problem.",
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
            add_chat_message("bot", "Let's start the interactive assessment. I'll ask you 6 questions based on your resume.")
            
            # Generate sample questions
            sample_questions = [
                "What motivated you to pursue a career in technology?",
                "Can you describe a challenging project you worked on and how you overcame obstacles?",
                "What programming languages or technologies mentioned in your resume are you most proficient in?",
                "How do you stay updated with the latest trends in technology?",
                "Describe a situation where you had to work in a team to solve a technical problem.",
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
                    
                    # Prepare questions and answers for API call
                    questions_and_answers = []
                    for i, question in enumerate(st.session_state.assessment_questions):
                        questions_and_answers.append({
                            'question': question,
                            'answer': st.session_state.assessment_answers[i]
                        })
                    
                    # Try to get AI-powered analysis from backend API
                    ai_result = analyze_resume_responses_with_api(
                        st.session_state.resume_text,
                        questions_and_answers
                    )
                    
                    if ai_result['success']:
                        # Use AI-powered feedback
                        add_chat_message("bot", ai_result['feedback'])
                    else:
                        # Handle different types of errors
                        if ai_result['error_type'] == 'api_key':
                            # API key issue - provide specific guidance
                            error_message = (
                                "I'm unable to access the AI API at the moment. "
                                "Please check your API key configuration.\n\n"
                                "To resolve this issue:\n"
                                "1. If using NVIDIA API:\n"
                                "   - Get your API key from https://build.nvidia.com/\n"
                                "   - Add it to the 'nvidia api key.py' file\n\n"
                                "2. If using Google API:\n"
                                "   - Get your API key from https://ai.google.dev/\n"
                                "   - Add it to the 'google api key.txt' file\n\n"
                                "3. Restart the application after updating the keys."
                            )
                            add_chat_message("bot", error_message)
                        else:
                            # Other errors - fall back to local generation
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