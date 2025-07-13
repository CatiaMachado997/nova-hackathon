#!/usr/bin/env python3
"""
AgentMaker Setup Script
Installs and configures AgentMaker for EthIQ
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing AgentMaker dependencies...")
    
    dependencies = [
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.1.0",
        "click>=8.0.0"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating AgentMaker directories...")
    
    base_dir = Path(__file__).parent
    directories = [
        "agentmaker/templates",
        "agentmaker/projects",
        "agentmaker/agents",
        "agentmaker/configs"
    ]
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {dir_path}")

def create_symlink():
    """Create symlink for agentmaker command"""
    print("🔗 Creating agentmaker command...")
    
    try:
        # Create symlink in tools directory
        tools_dir = Path(__file__).parent
        agentmaker_cli = tools_dir / "agentmaker_cli.py"
        
        if agentmaker_cli.exists():
            # Make executable
            os.chmod(agentmaker_cli, 0o755)
            print("✅ Made agentmaker_cli.py executable")
            
            # Create alias
            alias_script = tools_dir / "agentmaker"
            with open(alias_script, "w") as f:
                f.write(f"#!/bin/bash\npython3 {agentmaker_cli.absolute()} \"$@\"\n")
            
            os.chmod(alias_script, 0o755)
            print("✅ Created agentmaker command")
        else:
            print("❌ agentmaker_cli.py not found")
            
    except Exception as e:
        print(f"❌ Failed to create symlink: {e}")

def main():
    """Main setup function"""
    print("🚀 AgentMaker Setup for EthIQ")
    print("=" * 40)
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Create symlink
    create_symlink()
    
    print("\n✅ AgentMaker setup complete!")
    print("\n📖 Usage:")
    print("  python tools/agentmaker_cli.py build     # Build all EthIQ agents")
    print("  python tools/agentmaker_cli.py create    # Create a new agent")
    print("  python tools/agentmaker_cli.py list      # List all agents")
    print("  python tools/agentmaker_cli.py deploy    # Deploy agents")
    
    print("\n🎯 Next steps:")
    print("  1. Run: python tools/agentmaker_cli.py build")
    print("  2. Start your EthIQ system")
    print("  3. Use the dashboard to test agents")

if __name__ == "__main__":
    main() 