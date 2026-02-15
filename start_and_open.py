"""
Script to start Django server and open browser with correct HTTP URL
"""

import subprocess
import webbrowser
import time
import sys
import os

def start_server():
    """Start Django development server on port 8080"""
    print("="*60)
    print("  Starting Dental Management System")
    print("="*60)
    print()
    print("Server will start on port 8080")
    print("Opening browser in 3 seconds...")
    print()
    
    # Start Django server in background
    try:
        # Start server process
        server_process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', '8080'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Open browser with HTTP URL using localhost (not 127.0.0.1)
        # This avoids Chrome's HSTS cache for 127.0.0.1
        url = 'http://localhost:8080'
        print(f"Opening browser: {url}")
        print("Note: Using 'localhost' instead of '127.0.0.1' to avoid HTTPS issues")
        webbrowser.open(url)
        
        print()
        print("="*60)
        print(f"  Server is running on {url}")
        print("  Press Ctrl+C to stop the server")
        print("="*60)
        print()
        
        # Keep script running and show server output
        try:
            while True:
                output = server_process.stdout.readline()
                if output:
                    print(output.strip())
                error = server_process.stderr.readline()
                if error:
                    # Filter out HTTPS errors
                    if 'HTTPS' not in error and 'Bad request' not in error:
                        print(error.strip())
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")
            
    except Exception as e:
        print(f"Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()
