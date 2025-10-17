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

# Configure CORS to allow requests from any origin
CORS(app, origins=["http://localhost:8504", "http://127.0.0.1:5000", "http://localhost:8501", "http://localhost:8502", "http://localhost:8503"], 
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

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
    elif skill == 'Java':
        if 'inheritance' in question_text.lower():
            return [
                "The child class inherits fields and methods from the parent class",
                "The parent class inherits fields and methods from the child class",
                "Both classes share the same memory space",
                "Inheritance is not supported in Java"
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
        elif 'hashmap' in question_text.lower():
            return [
                "O(1) average case for get/put operations",
                "O(log n) for all operations",
                "O(n) for all operations",
                "O(1) for all operations"
            ]
        elif 'garbage' in question_text.lower() and 'collection' in question_text.lower():
            return [
                "Java uses automatic garbage collection to reclaim memory",
                "Java requires manual memory management",
                "Java doesn't have garbage collection",
                "Java only collects memory when the program exits"
            ]
        elif 'static' in question_text.lower():
            return [
                "Static members belong to the class rather than instances",
                "Static members are loaded when the class is instantiated",
                "Static members cannot be accessed directly",
                "Static members are unique for each object"
            ]
        elif 'access modifier' in question_text.lower():
            return [
                "private, default, protected, public",
                "private, protected, public, global",
                "internal, external, protected, public",
                "final, abstract, static, volatile"
            ]
        elif 'string' in question_text.lower() and '==' in question_text.lower():
            return [
                "false because s1 and s2 refer to different objects",
                "true because s1 and s2 have the same content",
                "true because string literals are interned",
                "Compilation error due to invalid syntax"
            ]
        elif 'super' in question_text.lower():
            return [
                "To access the parent class's members",
                "To call a method in the current class",
                "To create an instance of the parent class",
                "To define a superclass method"
            ]
        else:
            # Generic but relevant options for other Java questions
            return [
                "It's a core concept that affects object behavior",
                "It's a syntactic feature with minimal runtime impact",
                "It's only relevant for enterprise applications",
                "It primarily affects performance characteristics"
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
    """Upload and parse resume"""
    try:
        # Check if resume file is present in request
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed.'}), 400
        
        # Create uploads directory if it doesn't exist
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Parse resume
        try:
            resume_text = parse_resume(file_path)
        except Exception as e:
            # If parsing fails, try to read as text
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    resume_text = f.read()
            except:
                resume_text = "Could not extract text from resume"
        
        # Extract skills
        try:
            extracted_skills = extract_skills(resume_text)
        except Exception as e:
            extracted_skills = []
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume_text': resume_text,
            'skills': extracted_skills
        })
    except Exception as e:
        return jsonify({'error': f'Failed to process resume: {str(e)}'}), 500

@app.route('/api/generate-resume-questions', methods=['POST'])
def generate_resume_questions():
    """Generate questions based on resume analysis"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        api_provider = data.get('api_provider', 'nvidia')
        
        if not resume_text:
            return jsonify({'error': 'No resume text provided'}), 400
        
        # Try to get API key from config
        if api_provider == 'google':
            api_key = app.config.get('GOOGLE_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('google api key.txt', 'r') as f:
                        api_key = f.read().strip()
                except:
                    pass
        elif api_provider == 'nvidia':
            api_key = app.config.get('NVIDIA_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('nvidia api key.py', 'r') as f:
                        content = f.read()
                        import re
                        match = re.search(r'Bearer\s+([^\s"]+)', content)
                        if match:
                            api_key = match.group(1)
                except:
                    pass
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
        
        if not api_key:
            # Generate fallback questions
            questions = [
                "What motivated you to pursue a career in technology?",
                "Can you describe a challenging project you worked on and how you overcame obstacles?",
                "What programming languages or technologies mentioned in your resume are you most proficient in?",
                "How do you stay updated with the latest trends in technology?",
                "Describe a situation where you had to work in a team to solve a technical problem.",
                "What are your career goals in the technology field?"
            ]
            return jsonify({'questions': questions})
        
        # Generate questions using API
        if api_provider == 'google':
            questions = generate_questions_with_google_api(resume_text, api_key)
        else:
            questions = generate_questions_with_nvidia_api(resume_text, api_key)
        
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': f'Failed to generate questions: {str(e)}'}), 500

@app.route('/api/answer-resume-question', methods=['POST'])
def answer_resume_question():
    """Answer a question based on resume content"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        question = data.get('question', '')
        api_provider = data.get('api_provider', 'nvidia')
        
        if not resume_text or not question:
            return jsonify({'error': 'Missing resume text or question'}), 400
        
        # Try to get API key from config
        if api_provider == 'google':
            api_key = app.config.get('GOOGLE_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('google api key.txt', 'r') as f:
                        api_key = f.read().strip()
                except:
                    pass
        elif api_provider == 'nvidia':
            api_key = app.config.get('NVIDIA_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('nvidia api key.py', 'r') as f:
                        content = f.read()
                        import re
                        match = re.search(r'Bearer\s+([^\s"]+)', content)
                        if match:
                            api_key = match.group(1)
                except:
                    pass
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
        
        if not api_key:
            return jsonify({'answer': 'I\'m unable to access the AI API at the moment. Please check your API key configuration.'})
        
        # Generate answer using API
        if api_provider == 'google':
            answer = answer_question_with_google_api(resume_text, question, api_key)
        else:
            answer = answer_question_with_nvidia_api(resume_text, question, api_key)
        
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f'Failed to generate answer: {str(e)}'}), 500

@app.route('/api/analyze-resume-responses', methods=['POST'])
def analyze_resume_responses():
    """Analyze user responses to resume-based questions"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        questions_and_answers = data.get('questions_and_answers', [])
        api_provider = data.get('api_provider', 'nvidia')
        
        if not resume_text or not questions_and_answers:
            return jsonify({'error': 'Missing resume text or questions and answers'}), 400
        
        # Try to get API key from config
        if api_provider == 'google':
            api_key = app.config.get('GOOGLE_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('google api key.txt', 'r') as f:
                        api_key = f.read().strip()
                except:
                    pass
        elif api_provider == 'nvidia':
            api_key = app.config.get('NVIDIA_API_KEY', '')
            if not api_key:
                # Try to read from file
                try:
                    with open('nvidia api key.py', 'r') as f:
                        content = f.read()
                        import re
                        match = re.search(r'Bearer\s+([^\s"]+)', content)
                        if match:
                            api_key = match.group(1)
                except:
                    pass
        else:
            return jsonify({'error': 'Invalid API provider'}), 400
        
        if not api_key:
            return jsonify({'feedback': 'I\'m unable to access the AI API at the moment. Please check your API key configuration.'})
        
        # Analyze responses using API
        if api_provider == 'google':
            feedback = analyze_responses_with_google_api(resume_text, questions_and_answers, api_key)
        else:
            feedback = analyze_responses_with_nvidia_api(resume_text, questions_and_answers, api_key)
        
        return jsonify({'feedback': feedback})
    except Exception as e:
        return jsonify({'error': f'Failed to analyze responses: {str(e)}'}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx'})

def secure_filename(filename):
    """Secure filename by removing special characters"""
    import re
    # Remove any characters that aren't alphanumeric, dots, underscores, or hyphens
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    return filename

def generate_questions_with_google_api(resume_text, api_key):
    """Generate questions based on resume using Google's Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
    Based on the following resume, please generate exactly 6 thoughtful, professional questions that would help assess the candidate's technical skills, experience, and potential areas for improvement in a job interview context.
    
    Resume:
    {resume_text}
    
    Please provide the questions as a numbered list (1 to 6) without any markdown formatting. 
    Each question should be specific, relevant to the candidate's background, and designed to elicit detailed technical responses.
    Focus on areas such as technical expertise, problem-solving approaches, project experiences, and career development.
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
            "temperature": 0.4,
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
            return questions[:6]  # Ensure exactly 6 questions
        
        return [
            "Based on your experience with [specific technology from resume], can you describe a particularly challenging technical problem you solved and the approach you took?",
            "Can you walk me through a significant project you've worked on, highlighting your role, the technologies used, and the business impact?",
            "How do you ensure code quality and maintainability in your projects? Can you provide specific examples of your practices?",
            "Tell me about a time when you had to collaborate with a cross-functional team. What was your role and how did you contribute to the team's success?",
            "Describe an instance where you had to make a critical technical decision with limited information. What was the outcome?",
            "Where do you see your technical skills and career heading in the next 3-5 years, and how are you preparing for that journey?"
        ]
    except Exception as e:
        # Fallback questions
        return [
            "Based on your experience with [specific technology from resume], can you describe a particularly challenging technical problem you solved and the approach you took?",
            "Can you walk me through a significant project you've worked on, highlighting your role, the technologies used, and the business impact?",
            "How do you ensure code quality and maintainability in your projects? Can you provide specific examples of your practices?",
            "Tell me about a time when you had to collaborate with a cross-functional team. What was your role and how did you contribute to the team's success?",
            "Describe an instance where you had to make a critical technical decision with limited information. What was the outcome?",
            "Where do you see your technical skills and career heading in the next 3-5 years, and how are you preparing for that journey?"
        ]

def generate_questions_with_nvidia_api(resume_text, api_key):
    """Generate questions based on resume using NVIDIA's API"""
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Based on the following resume, please generate exactly 6 thoughtful, professional questions that would help assess the candidate's technical skills, experience, and potential areas for improvement in a job interview context.
    
    Resume:
    {resume_text}
    
    Please provide the questions as a numbered list (1 to 6) without any markdown formatting. 
    Each question should be specific, relevant to the candidate's background, and designed to elicit detailed technical responses.
    Focus on areas such as technical expertise, problem-solving approaches, project experiences, and career development.
    """
    
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.4,
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
            return questions[:6]  # Ensure exactly 6 questions
        
        return [
            "Based on your experience with [specific technology from resume], can you describe a particularly challenging technical problem you solved and the approach you took?",
            "Can you walk me through a significant project you've worked on, highlighting your role, the technologies used, and the business impact?",
            "How do you ensure code quality and maintainability in your projects? Can you provide specific examples of your practices?",
            "Tell me about a time when you had to collaborate with a cross-functional team. What was your role and how did you contribute to the team's success?",
            "Describe an instance where you had to make a critical technical decision with limited information. What was the outcome?",
            "Where do you see your technical skills and career heading in the next 3-5 years, and how are you preparing for that journey?"
        ]
    except Exception as e:
        # Fallback questions
        return [
            "Based on your experience with [specific technology from resume], can you describe a particularly challenging technical problem you solved and the approach you took?",
            "Can you walk me through a significant project you've worked on, highlighting your role, the technologies used, and the business impact?",
            "How do you ensure code quality and maintainability in your projects? Can you provide specific examples of your practices?",
            "Tell me about a time when you had to collaborate with a cross-functional team. What was your role and how did you contribute to the team's success?",
            "Describe an instance where you had to make a critical technical decision with limited information. What was the outcome?",
            "Where do you see your technical skills and career heading in the next 3-5 years, and how are you preparing for that journey?"
        ]


def answer_question_with_google_api(resume_text, question, api_key):
    """Answer a question based on resume content using Google's Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
    Based on the following resume, please provide a thoughtful answer to the question.
    
    Resume:
    {resume_text}
    
    Question:
    {question}
    
    Please provide your answer in plain text without any markdown formatting.
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
            # Take only first 3 lines
            clean_content = '\n'.join(lines[:3])
            return clean_content
        
        return "I don't have enough information in the resume to provide a specific answer to that question."
    except Exception as e:
        return "I don't have enough information in the resume to provide a specific answer to that question."

def answer_question_with_nvidia_api(resume_text, question, api_key):
    """Answer a question based on resume content using NVIDIA's API"""
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Based on the following resume, please provide a thoughtful answer to the question.
    
    Resume:
    {resume_text}
    
    Question:
    {question}
    
    Please provide your answer in plain text without any markdown formatting.
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
            # Take only first 3 lines
            clean_content = '\n'.join(lines[:3])
            return clean_content
        
        return "I don't have enough information in the resume to provide a specific answer to that question."
    except Exception as e:
        return "I don't have enough information in the resume to provide a specific answer to that question."

def analyze_responses_with_google_api(resume_text, questions_and_answers, api_key):
    """Analyze user responses and provide feedback using Google's Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    # Format questions and answers for the prompt
    qa_text = "\n".join([f"Question {i+1}: {qa['question']}\nAnswer {i+1}: {qa['answer']}" 
                         for i, qa in enumerate(questions_and_answers)])
    
    prompt = f"""
    Based on the following resume and the candidate's responses to technical interview questions, please provide a comprehensive, professional analysis with:
    1. Overall assessment of the candidate's technical communication skills and self-awareness
    2. Key strengths demonstrated through their responses with specific examples
    3. Areas for improvement in their technical explanations and problem-solving approaches
    4. Detailed, actionable recommendations for professional skill development
    5. Suggestions for how to better articulate technical experiences and achievements
    
    Resume:
    {resume_text}
    
    Questions and Answers:
    {qa_text}
    
    Please structure your response in exactly 6-8 lines of plain text without any markdown formatting.
    Focus on providing specific, actionable feedback that would be valuable in a professional development context.
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
            "maxOutputTokens": 1200,
            "temperature": 0.3,
            "topP": 0.85
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
            # Take only first 8 lines for more detailed feedback
            clean_content = '\n'.join(lines[:8])
            return clean_content
        
        return """Your technical communication shows good foundational knowledge. To enhance your interview performance, focus on providing more specific examples from your projects, quantifying your achievements with metrics where possible, and clearly explaining your problem-solving approach. Practice the STAR method (Situation, Task, Action, Result) to structure your responses. Consider deepening your expertise in [relevant technologies] through hands-on projects and stay current with industry best practices. Work on articulating complex technical concepts to both technical and non-technical audiences."""
    except Exception as e:
        return """Your technical communication shows good foundational knowledge. To enhance your interview performance, focus on providing more specific examples from your projects, quantifying your achievements with metrics where possible, and clearly explaining your problem-solving approach. Practice the STAR method (Situation, Task, Action, Result) to structure your responses. Consider deepening your expertise in [relevant technologies] through hands-on projects and stay current with industry best practices. Work on articulating complex technical concepts to both technical and non-technical audiences."""

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
    Based on the following resume and the candidate's responses to technical interview questions, please provide a comprehensive, professional analysis with:
    1. Overall assessment of the candidate's technical communication skills and self-awareness
    2. Key strengths demonstrated through their responses with specific examples
    3. Areas for improvement in their technical explanations and problem-solving approaches
    4. Detailed, actionable recommendations for professional skill development
    5. Suggestions for how to better articulate technical experiences and achievements
    
    Resume:
    {resume_text}
    
    Questions and Answers:
    {qa_text}
    
    Please structure your response in exactly 6-8 lines of plain text without any markdown formatting.
    Focus on providing specific, actionable feedback that would be valuable in a professional development context.
    """
    
    data = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1200,
        "temperature": 0.3,
        "top_p": 0.85,
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
            # Take only first 8 lines for more detailed feedback
            clean_content = '\n'.join(lines[:8])
            return clean_content
        
        return """Your technical communication shows good foundational knowledge. To enhance your interview performance, focus on providing more specific examples from your projects, quantifying your achievements with metrics where possible, and clearly explaining your problem-solving approach. Practice the STAR method (Situation, Task, Action, Result) to structure your responses. Consider deepening your expertise in [relevant technologies] through hands-on projects and stay current with industry best practices. Work on articulating complex technical concepts to both technical and non-technical audiences."""
    except Exception as e:
        return """Your technical communication shows good foundational knowledge. To enhance your interview performance, focus on providing more specific examples from your projects, quantifying your achievements with metrics where possible, and clearly explaining your problem-solving approach. Practice the STAR method (Situation, Task, Action, Result) to structure your responses. Consider deepening your expertise in [relevant technologies] through hands-on projects and stay current with industry best practices. Work on articulating complex technical concepts to both technical and non-technical audiences."""

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