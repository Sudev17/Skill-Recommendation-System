import PyPDF2
import docx
import os

def parse_resume(file_path):
    """
    Parse resume from PDF, DOCX, or TXT file and extract text
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return parse_pdf_resume(file_path)
    elif file_extension == '.docx':
        # For testing purposes, if it's actually a text file with .docx extension, parse as text
        try:
            return parse_docx_resume(file_path)
        except:
            # If DOCX parsing fails, try as text
            return parse_txt_resume(file_path)
    elif file_extension == '.txt':
        return parse_txt_resume(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")

def parse_pdf_resume(file_path):
    """
    Parse PDF resume and extract text
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def parse_docx_resume(file_path):
    """
    Parse DOCX resume and extract text
    """
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error parsing DOCX: {str(e)}")

def parse_txt_resume(file_path):
    """
    Parse TXT resume and extract text
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error parsing TXT: {str(e)}")