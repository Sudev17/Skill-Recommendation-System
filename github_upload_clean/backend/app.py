from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import json
import random
import os
import requests
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from resume_analyzer import analyze_resume_with_google_api, analyze_resume_with_nvidia_api, generate_skill_recommendations

# Import the resume parsing and skill extraction utilities
from app.utils.resume_parser import parse_resume
from app.utils.skill_extractor import extract_skills

# Import configuration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

app = Flask(__name__)
app.config.from_object(config.config['default'])
CORS(app)

# Load the question data
with open(os.path.join(os.path.dirname(__file__), 'it_skill_questions.json'), 'r') as f:
    questions_data = json.load(f)

# Group questions by skill
skills_questions = {}
for question in questions_data:
    skill = question['skill']
    if skill not in skills_questions:
        skills_questions[skill] = []
    skills_questions[skill].append(question)

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all available skills"""
    return jsonify({
        'skills': list(skills_questions.keys())
    })

@app.route('/api/questions', methods=['POST'])
def get_questions():
    """Get questions for a specific skill"""
    data = request.get_json()
    skill = data.get('skill')
    count = data.get('count', 10)
    
    if skill not in skills_questions:
        return jsonify({'error': 'Skill not found'}), 404
    
    # Get random questions for the skill
    questions = random.sample(skills_questions[skill], min(count, len(skills_questions[skill])))
    
    # Enhance questions with proper options
    enhanced_questions = []
    for question in questions:
        # Add options to each question
        enhanced_question = question.copy()
        
        # Check if this is a placeholder question
        clean_question = re.sub(r'Q\d+ for [^:]+: ', '', question['question'])
        if "Explain a key concept or solve a coding/logical scenario" in clean_question:
            # Generate a better question based on the skill
            better_question = generate_better_question(skill)
            enhanced_question['question'] = better_question
            enhanced_question['options'] = generate_options_for_question(better_question, skill)
        else:
            # Use the existing question as is
            enhanced_question['options'] = generate_options_for_question(question['question'], skill)
            
        enhanced_question['correct_answer'] = 0  # For demo, first option is correct
        enhanced_questions.append(enhanced_question)
    
    return jsonify({
        'questions': enhanced_questions,
        'skill': skill
    })

def generate_better_question(skill):
    """Generate a better question for a given skill"""
    skill_specific_questions = {
        "Python": [
            "What is the output of the following Python code: print(2 ** 3 ** 2)?",
            "Which of the following is NOT a valid way to create a dictionary in Python?",
            "What is the time complexity of binary search in a sorted list?",
            "In Python, what does the 'global' keyword do?",
            "What is the difference between '==' and 'is' operators in Python?",
            "What will be the output of: x = [1, 2, 3]; y = x; y.append(4); print(len(x))?",
            "Which of the following is true about Python's garbage collection?",
            "What is the purpose of the __init__ method in a Python class?",
            "Which of the following is NOT a valid file opening mode in Python?",
            "What is the output of: print(type(lambda: None))?"
        ],
        "C Programming": [
            "What is the output of the following C code: int x=5; printf('%d %d %d', x++, ++x, x--);?",
            "Which of the following is true about static variables in C?",
            "What is the purpose of the 'const' keyword in C?",
            "In C, what is the difference between 'malloc' and 'calloc'?",
            "What will be the output of: int a[5] = {1,2,3,4,5}; printf('%d', *(a+2));?",
            "Which of the following is true about pointers in C?",
            "What is the size of a pointer variable in a 64-bit system?",
            "Which of the following is NOT a valid storage class in C?",
            "What is the output of: int x = 10; printf('%d %d %d', x, ++x, x++);?",
            "What is the purpose of the 'extern' keyword in C?"
        ],
        "Java": [
            "What is the output of the following Java code involving inheritance?",
            "Which of the following is true about Java interfaces?",
            "What is the purpose of the 'finally' block in Java exception handling?",
            "In Java, what is the difference between '==' and '.equals()' methods?",
            "What is the time complexity of HashMap operations in Java?",
            "Which of the following is true about Java's garbage collection?",
            "What is the purpose of the 'static' keyword in Java?",
            "Which of the following is NOT a valid access modifier in Java?",
            "What is the output of: String s1 = 'Hello'; String s2 = 'Hello'; System.out.println(s1 == s2);?",
            "What is the purpose of the 'super' keyword in Java?"
        ],
        "Data Structures & Algorithms": [
            "What is the time complexity of insertion in a balanced binary search tree?",
            "Which data structure is most appropriate for implementing BFS?",
            "What is the space complexity of merge sort algorithm?",
            "In a hash table, what is collision and how is it handled?",
            "What is the difference between stack and queue data structures?",
            "Which sorting algorithm has the best average-case time complexity?",
            "What is the time complexity of Dijkstra's algorithm using a binary heap?",
            "Which data structure is used to implement recursion?",
            "What is the worst-case time complexity of quicksort?",
            "Which traversal method is used for level-order traversal of a tree?"
        ],
        "SQL + DBMS": [
            "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
            "Which normal form eliminates transitive dependency?",
            "What is the purpose of indexing in a database?",
            "What is the ACID property in database transactions?",
            "How would you optimize a slow-running SQL query?",
            "What is the difference between DELETE and TRUNCATE commands?",
            "Which of the following is true about primary keys?",
            "What is the purpose of a foreign key constraint?",
            "What is the difference between CHAR and VARCHAR data types?",
            "Which SQL command is used to retrieve data from a database?"
        ],
        "Machine Learning": [
            "What is the difference between supervised and unsupervised learning?",
            "What is overfitting and how can it be prevented?",
            "Explain the bias-variance tradeoff in machine learning.",
            "What is the purpose of cross-validation in model evaluation?",
            "What is the difference between precision and recall metrics?",
            "Which algorithm is best suited for linearly separable data?",
            "What is the purpose of regularization in machine learning?",
            "What is the difference between bagging and boosting?",
            "Which metric is most appropriate for imbalanced datasets?",
            "What is the purpose of feature scaling in machine learning?"
        ],
        "Operating System": [
            "What is the difference between process and thread?",
            "Explain the concept of virtual memory in operating systems.",
            "What is a deadlock and what are the necessary conditions for it to occur?",
            "What is the purpose of a page table in memory management?",
            "What is the difference between preemptive and non-preemptive scheduling?",
            "What is the purpose of semaphores in process synchronization?",
            "What is the difference between paging and segmentation?",
            "What is thrashing in the context of virtual memory?",
            "What is the purpose of the kernel in an operating system?",
            "What is the difference between multitasking and multiprocessing?"
        ],
        "Web Development (HTML/CSS/JS + Basics React)": [
            "What is the difference between 'let', 'const', and 'var' in JavaScript?",
            "Explain the CSS box model and its components.",
            "What is the virtual DOM in React and how does it improve performance?",
            "What is the purpose of useEffect hook in React?",
            "What is the difference between session storage and local storage?",
            "What is the purpose of CSS flexbox?",
            "What is event bubbling in JavaScript?",
            "What is the difference between == and === in JavaScript?",
            "What is the purpose of React components?",
            "What is the CSS property used to make an element transparent?"
        ]
    }
    
    # Return a random question for the skill if available, otherwise a generic question
    if skill in skill_specific_questions:
        return random.choice(skill_specific_questions[skill])
    else:
        return "Explain a key concept or solve a coding/logical scenario related to " + skill + "."

def generate_options_for_question(question_text, skill):
    """Generate realistic options for a given question"""
    # Remove the prefix from the question text for option generation
    clean_question = re.sub(r'Q\d+ for [^:]+: ', '', question_text)
    
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
                "'is' compares values, '==' compares object identity",
                "Both compare object identity but '==' is faster"
            ]
        else:
            # Generic options for other Python questions
            return [
                "This is the correct approach for the given scenario",
                "This approach has a logical error in implementation",
                "This solution is inefficient for the given problem",
                "This method is not applicable to the problem"
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
                "Static variables can be accessed from other files",
                "Static variables are automatically initialized to zero every time"
            ]
        elif 'const' in question_text.lower():
            return [
                "It declares a variable whose value cannot be changed",
                "It makes a variable accessible from other files",
                "It allocates memory in the read-only section",
                "It initializes a variable at compile time"
            ]
        elif 'malloc' in question_text.lower() and 'calloc' in question_text.lower():
            return [
                "malloc doesn't initialize memory, calloc initializes to zero",
                "malloc is faster, calloc is slower",
                "malloc allocates stack memory, calloc allocates heap memory",
                "There is no difference between malloc and calloc"
            ]
        elif 'a[5]' in question_text.lower() and '*(a+2)' in question_text.lower():
            return [
                "3",
                "2",
                "Address of a[2]",
                "Compilation Error"
            ]
        else:
            # Generic options for other C questions
            return [
                "The code will compile and run correctly",
                "There is a syntax error in the code",
                "The program will produce unexpected output",
                "This approach uses incorrect data types"
            ]
    elif skill == 'Java':
        if 'inheritance' in question_text.lower():
            return [
                "Depends on the specific code implementation",
                "Will always result in a compilation error",
                "Will always print the parent class method",
                "Will always print the child class method"
            ]
        elif 'interface' in question_text.lower():
            return [
                "Interfaces can contain abstract methods and default methods",
                "Interfaces can have private methods but not public methods",
                "Interfaces can contain instance variables",
                "Interfaces cannot be implemented by a class"
            ]
        elif 'finally' in question_text.lower():
            return [
                "It is always executed, regardless of exceptions",
                "It is only executed when an exception is thrown",
                "It is only executed when no exception is thrown",
                "It is optional and rarely used"
            ]
        elif '==' in question_text.lower() and '.equals()' in question_text.lower():
            return [
                "'==' compares references, '.equals()' compares content",
                "Both compare object content but '.equals()' is faster",
                "'==' compares content, '.equals()' compares references",
                "Both compare references but '==' is faster"
            ]
        elif 'hashmap' in question_text.lower() and 'complexity' in question_text.lower():
            return [
                "O(1) average case, O(n) worst case",
                "O(log n) for all operations",
                "O(n) for all operations",
                "O(1) for all operations"
            ]
        else:
            # Generic options for other Java questions
            return [
                "This implementation follows Java best practices",
                "The code violates object-oriented principles",
                "This solution has memory management issues",
                "The method signature is incorrect"
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
                "When the hash table is full; handled by resizing",
                "When a key is not found; handled by linear probing",
                "When two values are equal; handled by separate chaining"
            ]
        elif 'stack' in question_text.lower() and 'queue' in question_text.lower():
            return [
                "Stack is LIFO, Queue is FIFO",
                "Stack is FIFO, Queue is LIFO",
                "Both are LIFO structures",
                "Both are FIFO structures"
            ]
        else:
            # Generic options for other DSA questions
            return [
                "This algorithm has optimal time complexity",
                "The solution uses an inappropriate data structure",
                "This approach will cause stack overflow",
                "The algorithm does not handle edge cases"
            ]
    elif skill == 'SQL + DBMS':
        if 'inner join' in question_text.lower() and 'left join' in question_text.lower():
            return [
                "INNER JOIN returns only matching rows, LEFT JOIN returns all left table rows",
                "INNER JOIN returns all rows, LEFT JOIN returns only matching rows",
                "Both return the same result set",
                "INNER JOIN is faster than LEFT JOIN"
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
                "To encrypt sensitive data in the database",
                "To compress data and save storage space",
                "To backup data for disaster recovery"
            ]
        elif 'acid' in question_text.lower():
            return [
                "Atomicity, Consistency, Isolation, Durability",
                "Availability, Consistency, Isolation, Durability",
                "Atomicity, Concurrency, Isolation, Durability",
                "Atomicity, Consistency, Integrity, Durability"
            ]
        elif 'optimize' in question_text.lower() and 'sql query' in question_text.lower():
            return [
                "Add appropriate indexes, rewrite queries, analyze execution plan",
                "Increase database server memory and CPU",
                "Convert all queries to stored procedures",
                "Use SELECT * in all queries to retrieve all data"
            ]
        else:
            # Generic options for other SQL questions
            return [
                "This query will return the expected results",
                "The SQL statement has a syntax error",
                "This query will cause performance issues",
                "The join condition is logically incorrect"
            ]
    elif skill == 'Machine Learning':
        if 'supervised' in question_text.lower() and 'unsupervised' in question_text.lower():
            return [
                "Supervised uses labeled data, unsupervised finds patterns in unlabeled data",
                "Supervised is faster, unsupervised is slower",
                "Supervised uses regression, unsupervised uses classification",
                "There is no difference between supervised and unsupervised learning"
            ]
        elif 'overfitting' in question_text.lower():
            return [
                "When model performs well on training data but poorly on new data; prevented by regularization",
                "When model performs poorly on both training and test data; prevented by more data",
                "When model is too simple; prevented by adding more features",
                "When model training takes too long; prevented by early stopping"
            ]
        elif 'bias-variance' in question_text.lower():
            return [
                "Bias is underfitting, variance is overfitting; tradeoff in model complexity",
                "Bias is overfitting, variance is underfitting; tradeoff in model complexity",
                "Both bias and variance indicate good model performance",
                "Both bias and variance indicate poor model performance"
            ]
        elif 'cross-validation' in question_text.lower():
            return [
                "To evaluate model performance on multiple data splits and reduce overfitting",
                "To speed up model training by using parallel processing",
                "To combine multiple models for better performance",
                "To reduce the size of training data for faster processing"
            ]
        elif 'precision' in question_text.lower() and 'recall' in question_text.lower():
            return [
                "Precision is TP/(TP+FP), Recall is TP/(TP+FN)",
                "Precision is TP/(TP+FN), Recall is TP/(TP+FP)",
                "Both measure the same aspect of model performance",
                "Precision is about speed, Recall is about accuracy"
            ]
        else:
            # Generic options for other ML questions
            return [
                "This model selection is appropriate for the dataset",
                "The algorithm is not suitable for this type of data",
                "The hyperparameters are not optimized",
                "This approach will lead to overfitting"
            ]
    elif skill == 'Operating System':
        if 'process' in question_text.lower() and 'thread' in question_text.lower():
            return [
                "Process is independent with separate memory, Thread shares memory within a process",
                "Process shares memory, Thread is independent with separate memory",
                "Both are identical in terms of memory management",
                "Process is lighter weight than Thread"
            ]
        elif 'virtual memory' in question_text.lower():
            return [
                "Technique that allows system to use disk storage as an extension of physical RAM",
                "Method to encrypt data stored in RAM for security",
                "Way to compress memory to fit more data in RAM",
                "Technique to share memory between multiple processes"
            ]
        elif 'deadlock' in question_text.lower():
            return [
                "Mutual exclusion, Hold and wait, No preemption, Circular wait",
                "Race condition, Starvation, Priority inversion, Thrashing",
                "Segmentation, Paging, Swapping, Caching",
                "Synchronization, Mutex, Semaphore, Monitor"
            ]
        elif 'page table' in question_text.lower():
            return [
                "Maps virtual addresses to physical addresses in memory",
                "Stores frequently accessed data for faster retrieval",
                "Organizes memory into fixed-size blocks for allocation",
                "Tracks which processes are using which memory segments"
            ]
        elif 'preemptive' in question_text.lower() and 'non-preemptive' in question_text.lower():
            return [
                "Preemptive can interrupt processes, Non-preemptive runs to completion",
                "Preemptive is slower, Non-preemptive is faster",
                "Preemptive uses more memory, Non-preemptive uses less memory",
                "Both have identical behavior in modern operating systems"
            ]
        else:
            # Generic options for other OS questions
            return [
                "This process scheduling approach is efficient",
                "The memory management technique is flawed",
                "This solution creates a deadlock scenario",
                "The synchronization mechanism is incorrect"
            ]
    elif skill == 'Web Development (HTML/CSS/JS + Basics React)':
        if 'let' in question_text.lower() and 'const' in question_text.lower() and 'var' in question_text.lower():
            return [
                "let/const are block-scoped, var is function-scoped; const cannot be reassigned",
                "let/const are function-scoped, var is block-scoped; const can be reassigned",
                "All three have identical scoping behavior but different performance",
                "let is for numbers, const is for strings, var is for objects"
            ]
        elif 'css box model' in question_text.lower():
            return [
                "Content, Padding, Border, Margin",
                "Padding, Content, Margin, Border",
                "Border, Margin, Content, Padding",
                "Content, Border, Margin, Padding"
            ]
        elif 'virtual dom' in question_text.lower():
            return [
                "Lightweight representation of UI that enables efficient updates",
                "Security feature that isolates web components",
                "Storage mechanism for offline web applications",
                "Protocol for real-time communication between client and server"
            ]
        elif 'useeffect' in question_text.lower():
            return [
                "To handle side effects like data fetching, subscriptions, or DOM manipulation",
                "To define the component's initial state and props",
                "To optimize rendering performance by memoizing values",
                "To create context providers for global state management"
            ]
        elif 'session storage' in question_text.lower() and 'local storage' in question_text.lower():
            return [
                "Session storage is cleared when tab closes, Local storage persists until deleted",
                "Session storage persists until deleted, Local storage is cleared when tab closes",
                "Both have identical behavior and storage capacity",
                "Session storage is for sensitive data, Local storage is for public data"
            ]
        else:
            # Generic options for other Web Dev questions
            return [
                "This implementation follows web development best practices",
                "The code has accessibility issues",
                "This approach will not work in all browsers",
                "The component structure is not properly organized"
            ]
    else:
        # Generic options for unknown skills
        return [
            "Option A - Correct approach",
            "Option B - Contains errors",
            "Option C - Inefficient solution",
            "Option D - Not applicable"
        ]

@app.route('/api/evaluate', methods=['POST'])
def evaluate_answers():
    """Evaluate user answers and provide recommendations"""
    data = request.get_json()
    answers = data.get('answers', [])
    skill = data.get('skill', 'this area')
    api_provider = data.get('api_provider', 'google')
    
    # Simple evaluation - in a real system, this would be more complex
    correct_count = sum(1 for answer in answers if answer.get('correct', False))
    total_questions = len(answers)
    
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Use LLM for detailed recommendations if API key is available
    try:
        if api_provider == 'google':
            with open('google api key.txt', 'r') as f:
                api_key = f.read().strip()
        elif api_provider == 'nvidia':
            with open('nvidia api key.py', 'r') as f:
                content = f.read()
                import re
                match = re.search(r'Bearer ([^"]+)', content)
                if match:
                    api_key = match.group(1)
                else:
                    api_key = None
        else:
            api_key = None
        
        if api_key:
            detailed_recommendation = generate_skill_recommendations(answers, api_key, api_provider)
            # Clean up the recommendation to ensure it's plain text
            if detailed_recommendation:
                lines = detailed_recommendation.split('\n')
                # Take only first 5 lines
                detailed_recommendation = '\n'.join(lines[:5])
            else:
                # Fallback to simple recommendations
                if score_percentage < 60:
                    detailed_recommendation = f"You need to improve in {skill}. Focus on fundamental concepts."
                elif score_percentage < 80:
                    detailed_recommendation = f"Good performance in {skill}, but there's room for improvement. Practice more problems."
                else:
                    detailed_recommendation = f"Excellent performance in {skill}! Continue challenging yourself with advanced topics."
        else:
            # Fallback to simple recommendations
            if score_percentage < 60:
                detailed_recommendation = f"To strengthen your {skill} skills, focus on core concepts and practice foundational problems regularly. Consider reviewing basic syntax and data structures."
            elif score_percentage < 80:
                detailed_recommendation = f"Your {skill} knowledge is solid but can be enhanced. Target specific weak areas and tackle more complex challenges to improve."
            else:
                detailed_recommendation = f"Excellent work in {skill}! To maintain your proficiency, explore advanced topics and real-world applications."
    except Exception as e:
        # Fallback to simple recommendations if LLM fails
        if score_percentage < 60:
            detailed_recommendation = f"To strengthen your {skill} skills, focus on core concepts and practice foundational problems regularly. Consider reviewing basic syntax and data structures."
        elif score_percentage < 80:
            detailed_recommendation = f"Your {skill} knowledge is solid but can be enhanced. Target specific weak areas and tackle more complex challenges to improve."
        else:
            detailed_recommendation = f"Excellent work in {skill}! To maintain your proficiency, explore advanced topics and real-world applications."
    
    return jsonify({
        'score': score_percentage,
        'correct_answers': correct_count,
        'total_questions': total_questions,
        'recommendation': detailed_recommendation
    })

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Analyze resume and generate questions"""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    api_provider = data.get('api_provider', 'nvidia')  # 'google' or 'nvidia'
    
    if not resume_text:
        return jsonify({'error': 'Resume text is required'}), 400
    
    # Read API key
    try:
        if api_provider == 'google':
            with open('google api key.txt', 'r') as f:
                api_key = f.read().strip()
            result = analyze_resume_with_google_api(resume_text, api_key)
        elif api_provider == 'nvidia':
            # For NVIDIA, we'll use the key from the Python file
            # In a real implementation, you'd want to store this more securely
            with open('nvidia api key.py', 'r') as f:
                content = f.read()
                # Extract the API key from the file
                import re
                match = re.search(r'Bearer ([^"]+)', content)
                if match:
                    api_key = match.group(1)
                    result = analyze_resume_with_nvidia_api(resume_text, api_key)
                else:
                    return jsonify({'error': 'Could not extract NVIDIA API key'}), 500
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
            
        return jsonify(result)
    except FileNotFoundError:
        return jsonify({'error': 'API key file not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload and initial skill extraction"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    filename = file.filename
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    
    try:
        # Parse resume
        resume_text = parse_resume(file_path)
        
        # Extract skills
        skills = extract_skills(resume_text)
        
        # Store both full resume text and truncated version for display
        return jsonify({
            'message': 'Resume uploaded successfully',
            'skills': skills,
            'resume_text': resume_text,  # Full resume text
            'resume_preview': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-resume-questions', methods=['POST'])
def generate_resume_questions():
    """Generate questions based on resume analysis"""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    api_provider = data.get('api_provider', 'nvidia')
    
    if not resume_text:
        return jsonify({'error': 'Resume text is required'}), 400
    
    try:
        # Generate 10 questions based on resume using LLM
        if api_provider == 'google':
            with open('google api key.txt', 'r') as f:
                api_key = f.read().strip()
            questions = generate_questions_with_google_api(resume_text, api_key)
        elif api_provider == 'nvidia':
            with open('nvidia api key.py', 'r') as f:
                content = f.read()
                import re
                match = re.search(r'Bearer\s+([^\s"]+)', content)
                if match:
                    api_key = match.group(1)
                    questions = generate_questions_with_nvidia_api(resume_text, api_key)
                else:
                    return jsonify({'error': 'Could not extract NVIDIA API key'}), 500
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
            
        return jsonify({
            'questions': questions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-resume-responses', methods=['POST'])
def analyze_resume_responses():
    """Analyze user responses to resume-based questions and provide feedback"""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    questions_and_answers = data.get('questions_and_answers', [])
    api_provider = data.get('api_provider', 'nvidia')
    
    if not resume_text or not questions_and_answers:
        return jsonify({'error': 'Resume text and questions with answers are required'}), 400
    
    try:
        # Analyze responses using LLM
        if api_provider == 'google':
            with open('google api key.txt', 'r') as f:
                api_key = f.read().strip()
            feedback = analyze_responses_with_google_api(resume_text, questions_and_answers, api_key)
        elif api_provider == 'nvidia':
            with open('nvidia api key.py', 'r') as f:
                content = f.read()
                import re
                match = re.search(r'Bearer\s+([^\s"]+)', content)
                if match:
                    api_key = match.group(1)
                    feedback = analyze_responses_with_nvidia_api(resume_text, questions_and_answers, api_key)
                else:
                    return jsonify({'error': 'Could not extract NVIDIA API key'}), 500
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
            
        return jsonify({'feedback': feedback})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_questions_with_google_api(resume_text, api_key):
    """Generate questions based on resume using Google's Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
    Based on the following resume, please generate exactly 10 thoughtful questions that would help assess the candidate's skills, experience, and potential areas for improvement.
    
    Resume:
    {resume_text}
    
    Please provide the questions as a numbered list (1 to 10) without any markdown formatting.
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.5,
            "topP": 0.8
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            # Extract questions from numbered list
            import re
            questions = re.findall(r'\d+\.\s*(.+)', content)
            return questions[:10]  # Ensure exactly 10 questions
        
        return [
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
    except Exception as e:
        # Fallback questions
        return [
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

def generate_questions_with_nvidia_api(resume_text, api_key):
    """Generate questions based on resume using NVIDIA's API"""
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Based on the following resume, please generate exactly 10 thoughtful questions that would help assess the candidate's skills, experience, and potential areas for improvement.
    
    Resume:
    {resume_text}
    
    Please provide the questions as a numbered list (1 to 10) without any markdown formatting.
    """
    
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.5,
        "top_p": 0.8,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            # Extract questions from numbered list
            import re
            questions = re.findall(r'\d+\.\s*(.+)', content)
            return questions[:10]  # Ensure exactly 10 questions
        
        return [
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
    except Exception as e:
        # Fallback questions
        return [
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

def analyze_responses_with_google_api(resume_text, questions_and_answers, api_key):
    """Analyze user responses and provide feedback using Google's Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    # Format questions and answers for the prompt
    qa_text = "\n".join([f"Question {i+1}: {qa['question']}\nAnswer {i+1}: {qa['answer']}" 
                         for i, qa in enumerate(questions_and_answers)])
    
    prompt = f"""
    Based on the following resume and the candidate's responses to questions about their experience, please provide a comprehensive analysis with:
    1. Overall assessment of the candidate's self-awareness and communication skills
    2. Key strengths demonstrated through their responses
    3. Areas for improvement in their answers
    4. Specific recommendations for skill development
    
    Resume:
    {resume_text}
    
    Questions and Answers:
    {qa_text}
    
    Please provide your analysis in exactly 4-6 lines of plain text without any markdown formatting.
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.3,
            "topP": 0.8
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            # Clean up the response to ensure it's plain text
            lines = content.split('\n')
            # Take only first 6 lines
            clean_content = '\n'.join(lines[:6])
            return clean_content
        
        return "Based on your responses, I recommend focusing on clearly articulating your technical skills and experiences. Practice explaining complex concepts in simple terms and provide specific examples from your projects to demonstrate your capabilities."
    except Exception as e:
        return "Based on your responses, I recommend focusing on clearly articulating your technical skills and experiences. Practice explaining complex concepts in simple terms and provide specific examples from your projects to demonstrate your capabilities."

def analyze_responses_with_nvidia_api(resume_text, questions_and_answers, api_key):
    """Analyze user responses and provide feedback using NVIDIA's API"""
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Format questions and answers for the prompt
    qa_text = "\n".join([f"Question {i+1}: {qa['question']}\nAnswer {i+1}: {qa['answer']}" 
                         for i, qa in enumerate(questions_and_answers)])
    
    prompt = f"""
    Based on the following resume and the candidate's responses to questions about their experience, please provide a comprehensive analysis with:
    1. Overall assessment of the candidate's self-awareness and communication skills
    2. Key strengths demonstrated through their responses
    3. Areas for improvement in their answers
    4. Specific recommendations for skill development
    
    Resume:
    {resume_text}
    
    Questions and Answers:
    {qa_text}
    
    Please provide your analysis in exactly 4-6 lines of plain text without any markdown formatting.
    """
    
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
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
            # Take only first 6 lines
            clean_content = '\n'.join(lines[:6])
            return clean_content
        
        return "Based on your responses, I recommend focusing on clearly articulating your technical skills and experiences. Practice explaining complex concepts in simple terms and provide specific examples from your projects to demonstrate your capabilities."
    except Exception as e:
        return "Based on your responses, I recommend focusing on clearly articulating your technical skills and experiences. Practice explaining complex concepts in simple terms and provide specific examples from your projects to demonstrate your capabilities."

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file"""
    return send_file(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html'))

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from frontend"""
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), path)
    except FileNotFoundError:
        # If file not found, serve the main index.html (for SPA routing)
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)