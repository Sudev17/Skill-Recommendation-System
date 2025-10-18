"""
Script to run both the backend and frontend of the Skill Recommendation System
"""
import subprocess
import sys
import time
import threading

def run_backend():
    """Run the Flask backend server"""
    print("Starting Flask backend server...")
    try:
        subprocess.run([sys.executable, "backend/app.py"])
    except Exception as e:
        print(f"Error starting backend: {e}")

def run_frontend():
    """Run the Streamlit frontend"""
    print("Starting Streamlit frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except Exception as e:
        print(f"Error starting frontend: {e}")

if __name__ == "__main__":
    print("Starting Skill Recommendation System...")
    print("Make sure you have configured your API keys in nvidia api key.py and google api key.txt")
    
    # Run backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    # Run frontend in main thread
    run_frontend()