#!/usr/bin/env python3
"""
AutoEthos Startup Script
Easy way to start different components of the system
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path


def print_banner():
    """Print startup banner"""
    print("=" * 80)
    print("🤖 AutoEthos - Ethical Intelligence Platform")
    print("=" * 80)
    print("GenAI Hackathon 2025 - Team Nova")
    print()


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import flask
        import pydantic
        print("   ✅ Core dependencies found")
    except ImportError as e:
        print(f"   ❌ Missing dependency: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    return True


def run_test():
    """Run system test"""
    print("🧪 Running system test...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ System test passed")
            return True
        else:
            print("   ❌ System test failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def run_demo():
    """Run the demo"""
    print("🎮 Running AutoEthos demo...")
    try:
        subprocess.run([sys.executable, "demo.py"])
    except KeyboardInterrupt:
        print("\n   Demo interrupted by user")
    except Exception as e:
        print(f"   ❌ Demo failed: {e}")


def start_api():
    """Start the API server"""
    print("🚀 Starting API server...")
    print("   API will be available at: http://localhost:8000")
    print("   API docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        os.chdir("api")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", 
                       "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n   API server stopped")
    except Exception as e:
        print(f"   ❌ API server failed: {e}")
    finally:
        os.chdir("..")


def start_dashboard():
    """Start the web dashboard"""
    print("🌐 Starting web dashboard...")
    print("   Dashboard will be available at: http://localhost:8080")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run([sys.executable, "dashboard.py"])
    except KeyboardInterrupt:
        print("\n   Dashboard stopped")
    except Exception as e:
        print(f"   ❌ Dashboard failed: {e}")


def show_menu():
    """Show the main menu"""
    print("📋 Available options:")
    print("1. Run system test")
    print("2. Run demo scenarios")
    print("3. Start API server")
    print("4. Start web dashboard")
    print("5. Start API + Dashboard (recommended)")
    print("6. Exit")
    print()


def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                print()
                if run_test():
                    print("\n✅ System is ready!")
                else:
                    print("\n❌ System has issues. Please check the errors above.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                print()
                run_demo()
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                print()
                start_api()
                
            elif choice == "4":
                print()
                start_dashboard()
                
            elif choice == "5":
                print()
                print("🚀 Starting AutoEthos system...")
                print("   API: http://localhost:8000")
                print("   Dashboard: http://localhost:8080")
                print("   Press Ctrl+C to stop both")
                print()
                
                try:
                    # Start API in background
                    api_process = subprocess.Popen(
                        [sys.executable, "-m", "uvicorn", "main:app", 
                         "--host", "0.0.0.0", "--port", "8000"],
                        cwd="api"
                    )
                    
                    # Wait a moment for API to start
                    import time
                    time.sleep(3)
                    
                    # Start dashboard
                    dashboard_process = subprocess.Popen(
                        [sys.executable, "dashboard.py"]
                    )
                    
                    # Wait for either process to finish
                    try:
                        api_process.wait()
                    except KeyboardInterrupt:
                        print("\n🛑 Stopping AutoEthos system...")
                        api_process.terminate()
                        dashboard_process.terminate()
                        print("✅ System stopped")
                        
                except Exception as e:
                    print(f"❌ Failed to start system: {e}")
                
            elif choice == "6":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 