#!/usr/bin/env python3
"""
Single Python script to run both FastAPI (uvicorn) and Streamlit servers simultaneously.
Usage: python run_app.py
"""

import subprocess
import sys
import time
import multiprocessing
from pathlib import Path


def run_uvicorn():
    """Run the FastAPI server with uvicorn"""
    print("🚀 Starting FastAPI server on http://localhost:8000")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  FastAPI server stopped")
    except Exception as e:
        print(f"❌ Error running FastAPI server: {e}")


def run_streamlit():
    """Run the Streamlit app"""
    print("🎨 Starting Streamlit app on http://localhost:8501")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", 
            "src/streamlit_app.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Streamlit app stopped")
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")


def main():
    """Main function to run both servers"""
    print("🤖 Starting APMT Analytics Chatbot...")
    print("📁 Current directory:", Path.cwd())
    print()
    
    # Check if required files exist
    main_file = Path("src/main.py")
    streamlit_file = Path("src/streamlit_app.py")
    
    if not main_file.exists():
        print(f"❌ Error: {main_file} not found!")
        sys.exit(1)
    
    if not streamlit_file.exists():
        print(f"❌ Error: {streamlit_file} not found!")
        sys.exit(1)
    
    # Create processes for both servers
    uvicorn_process = multiprocessing.Process(target=run_uvicorn)
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    
    try:
        # Start FastAPI server
        uvicorn_process.start()
        
        # Wait a moment for FastAPI to start
        time.sleep(3)
        
        # Start Streamlit app
        streamlit_process.start()
        
        print("\n✅ Both servers are running!")
        print("📊 FastAPI: http://localhost:8000")
        print("🎨 Streamlit: http://localhost:8501")
        print("\nPress Ctrl+C to stop both servers")
        
        # Wait for both processes
        uvicorn_process.join()
        streamlit_process.join()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down servers...")
        
        # Terminate processes
        if uvicorn_process.is_alive():
            uvicorn_process.terminate()
            uvicorn_process.join(timeout=5)
        
        if streamlit_process.is_alive():
            streamlit_process.terminate()
            streamlit_process.join(timeout=5)
        
        print("✅ All servers stopped successfully!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Ensure we're running in the correct directory
    script_dir = Path(__file__).parent
    if script_dir != Path.cwd():
        print(f"📁 Changing directory to: {script_dir}")
        import os
        os.chdir(script_dir)
    
    main()
