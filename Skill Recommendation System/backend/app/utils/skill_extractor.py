import re

def extract_skills(resume_text):
    """
    Extract technical skills from resume text
    """
    # Common technical skills keywords
    technical_skills = [
        # Programming Languages
        'Python', 'Java', 'C++', 'C#', 'JavaScript', 'TypeScript', 'PHP', 'Ruby', 'Go', 'Rust',
        'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS', 'C',
        
        # Web Development
        'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring',
        'ASP.NET', 'Ruby on Rails', 'Laravel', 'Bootstrap', 'jQuery', 'Ajax',
        
        # Databases
        'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'SQL Server', 'Redis', 'Firebase',
        'Elasticsearch', 'Cassandra', 'DynamoDB',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
        'GitHub', 'GitLab', 'CI/CD', 'Terraform', 'Ansible', 'Puppet',
        
        # Machine Learning & Data Science
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib',
        'Seaborn', 'Jupyter', 'Spark', 'Hadoop', 'Tableau', 'Power BI',
        
        # Mobile Development
        'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin', 'Ionic',
        
        # Operating Systems
        'Linux', 'Unix', 'Windows', 'macOS',
        
        # Other Technologies
        'Blockchain', 'IoT', 'Cybersecurity', 'DevOps', 'Agile', 'Scrum'
    ]
    
    # Normalize resume text
    normalized_text = resume_text.lower()
    
    # Extract skills found in resume
    found_skills = []
    for skill in technical_skills:
        if skill.lower() in normalized_text:
            found_skills.append({
                'name': skill,
                'confidence': 0.9  # Default confidence
            })
    
    # Also extract skills from a "Skills" section if present
    skills_section = extract_skills_section(resume_text)
    if skills_section:
        additional_skills = extract_skills_from_section(skills_section, technical_skills)
        for skill in additional_skills:
            # Avoid duplicates
            if not any(s['name'].lower() == skill['name'].lower() for s in found_skills):
                found_skills.append(skill)
    
    return found_skills

def extract_skills_section(resume_text):
    """
    Extract the skills section from resume text
    """
    # Look for common section headers
    section_patterns = [
        r'skills\s*[:\-]?(.*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
        r'technical skills\s*[:\-]?(.*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
        r'competencies\s*[:\-]?(.*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
        r'proficiencies\s*[:\-]?(.*?)(?=\n\n|\n[A-Z][a-z]+:|$)'
    ]
    
    for pattern in section_patterns:
        match = re.search(pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return None

def extract_skills_from_section(skills_section, known_skills):
    """
    Extract skills from a skills section
    """
    found_skills = []
    
    # Split section into lines or phrases
    lines = re.split(r'[\n,;]', skills_section)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if any known skill is in this line
        for skill in known_skills:
            if skill.lower() in line.lower():
                found_skills.append({
                    'name': skill,
                    'confidence': 0.8
                })
                break  # Move to next line after finding a match
    
    return found_skills