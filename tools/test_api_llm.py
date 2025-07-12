#!/usr/bin/env python3
"""
Test LLM Integration through API
Tests the moderation endpoint with LLM-enabled agents
"""

import requests
import json
import time

def test_moderation_api():
    """Test the moderation API endpoint"""
    api_url = "http://localhost:8000/api/moderate"
    
    # Test content
    test_content = "This post contains hate speech targeting a specific group of people."
    
    payload = {
        "content": test_content,
        "context": {
            "user_id": "test_user_123",
            "platform": "social_media",
            "content_type": "post"
        }
    }
    
    print("🧪 Testing LLM Integration through API")
    print("=" * 50)
    print(f"API URL: {api_url}")
    print(f"Content: {test_content}")
    print()
    
    try:
        # Make the request
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Decision: {result.get('decision', 'unknown')}")
            print(f"   Confidence: {result.get('confidence', 'unknown')}")
            
            # Show agent responses
            if 'agent_responses' in result:
                print(f"\n🤖 Agent Responses ({len(result['agent_responses'])} agents):")
                for agent_resp in result['agent_responses']:
                    print(f"   {agent_resp.get('agent_name', 'Unknown')}: {agent_resp.get('decision', 'unknown')} ({agent_resp.get('confidence', 'unknown')})")
            
            # Show reasoning
            if 'reasoning' in result:
                print(f"\n💭 Reasoning: {result['reasoning'][:200]}...")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout: The request took too long")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except:
        print("❌ API is not running")
        return False

if __name__ == "__main__":
    if test_health_check():
        test_moderation_api()
    else:
        print("\n💡 To start the API server:")
        print("   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000") 