#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EthIQ Startup Script
Interactive startup for the EthIQ ethical deliberation system
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print the EthIQ banner"""
    print("=" * 80)
    print("EthIQ - Ethical Intelligence Platform")
    print("=" * 80)
    print("GenAI Hackathon 2025 - Team Nova")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'flask', 'flask_socketio', 
        'openai', 'anthropic', 'google.generativeai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("   Core dependencies found")
        return True

def run_test():
    """Run system test"""
    print("Running system test...")
    try:
        result = subprocess.run([sys.executable, "debug_test.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("   System test passed")
        else:
            print("   System test failed")
            print(result.stderr)
    except Exception as e:
        print(f"   Error running test: {e}")

def run_demo():
    """Run demo scenarios"""
    print("Running demo scenarios...")
    try:
        subprocess.run([sys.executable, "demo.py"], cwd=os.getcwd())
    except Exception as e:
        print(f"   Error running demo: {e}")

def start_api():
    """Start the API server"""
    print("Starting API server...")
    print("   API: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    
    # Change to the project root directory
    project_root = os.getcwd()
    
    try:
        # Start uvicorn from the project root, not from api directory
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ]
        
        # Set PYTHONPATH to include the project root
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{project_root}:{env.get('PYTHONPATH', '')}"
        
        subprocess.run(cmd, cwd=project_root, env=env)
    except KeyboardInterrupt:
        print("\n   API server stopped")
    except Exception as e:
        print(f"   Error starting API server: {e}")

def start_dashboard():
    """Start the web dashboard"""
    print("Starting web dashboard...")
    print("   Dashboard: http://localhost:8080")
    
    try:
        subprocess.run([sys.executable, "dashboard.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n   Dashboard stopped")
    except Exception as e:
        print(f"   Error starting dashboard: {e}")

def start_both():
    """Start both API server and dashboard"""
    print("Starting EthIQ system...")
    print("   API: http://localhost:8000")
    print("   Dashboard: http://localhost:8080")
    print("   Press Ctrl+C to stop both")
    print()
    
    project_root = os.getcwd()
    
    # Start API server in background
    api_env = os.environ.copy()
    api_env['PYTHONPATH'] = f"{project_root}:{api_env.get('PYTHONPATH', '')}"
    
    api_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], cwd=project_root, env=api_env)
    
    # Wait a moment for API to start
    time.sleep(3)
    
    # Start dashboard
    try:
        dashboard_process = subprocess.Popen([
            sys.executable, "dashboard.py"
        ], cwd=project_root)
        
        # Wait for either process to finish
        while True:
            if api_process.poll() is not None:
                print("   API server stopped unexpectedly")
                dashboard_process.terminate()
                break
            if dashboard_process.poll() is not None:
                print("   Dashboard stopped unexpectedly")
                api_process.terminate()
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n   Stopping both services...")
        api_process.terminate()
        dashboard_process.terminate()
        api_process.wait()
        dashboard_process.wait()
        print("   Both services stopped")

def show_menu():
    """Show the main menu"""
    print("Available options:")
    print("1. Run system test")
    print("2. Run demo scenarios")
    print("3. Start API server")
    print("4. Start web dashboard")
    print("5. Start API + Dashboard (recommended)")
    print("6. Exit")

def main():
    """Main function"""
    print_banner()
    
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return
    
    while True:
        print()
        show_menu()
        print()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                run_test()
            elif choice == "2":
                run_demo()
            elif choice == "3":
                start_api()
            elif choice == "4":
                start_dashboard()
            elif choice == "5":
                start_both()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 