#!/usr/bin/env python3
"""
Setup script for Cloudera AI Workbench integration
Helps configure environment variables for Cloudera API key and SSH key
"""

import os
import sys

def create_env_file():
    """Create or update .env file with Cloudera configuration"""
    
    print("🔧 Setting up Cloudera AI Workbench Integration")
    print("=" * 50)
    
    # Get user input
    print("\nPlease provide your Cloudera AI Workbench details:")
    
    api_key = input("Enter your Cloudera API Key: ").strip()
    if not api_key:
        print("❌ API Key is required!")
        return False
    
    ssh_key_path = input("Enter path to your SSH key (optional, press Enter to skip): ").strip()
    if not ssh_key_path:
        ssh_key_path = ""
    
    host = input("Enter Cloudera host URL (default: https://cloudera-cluster.example.com): ").strip()
    if not host:
        host = "https://cloudera-cluster.example.com"
    
    port = input("Enter port (default: 9092): ").strip()
    if not port:
        port = "9092"
    
    topic = input("Enter Kafka topic name (default: ethiq-moderation-events): ").strip()
    if not topic:
        topic = "ethiq-moderation-events"
    
    username = input("Enter username (optional): ").strip()
    password = input("Enter password (optional): ").strip()
    
    # Create .env content
    env_content = f"""# Cloudera AI Workbench Configuration
CLOUDERA_API_KEY={api_key}
CLOUDERA_SSH_KEY_PATH={ssh_key_path}
CLOUDERA_HOST={host}
CLOUDERA_PORT={port}
CLOUDERA_TOPIC={topic}
CLOUDERA_USERNAME={username}
CLOUDERA_PASSWORD={password}

# Notion Configuration (if you have it)
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_notion_database_id

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        
        print("\n🔍 Configuration Summary:")
        print(f"   API Key: {api_key[:8]}...")
        print(f"   SSH Key: {ssh_key_path if ssh_key_path else 'Not configured'}")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Topic: {topic}")
        
        print("\n🚀 Next steps:")
        print("1. Restart your API server to load the new configuration")
        print("2. Test the integration with: python test_cloudera_integration.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_cloudera_connection():
    """Test the Cloudera connection"""
    print("\n🧪 Testing Cloudera Connection")
    print("=" * 30)
    
    try:
        # Import and test the integration
        from agents.cloudera_integration import cloudera_client, initialize_cloudera_integration
        
        print("Connecting to Cloudera...")
        success = initialize_cloudera_integration()
        
        if success:
            print("✅ Cloudera connection successful!")
            return True
        else:
            print("❌ Cloudera connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_cloudera_connection()
    else:
        create_env_file() 