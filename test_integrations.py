#!/usr/bin/env python3
"""
Test script to verify Notion and Cloudera integrations
"""

import os
import asyncio
from dotenv import load_dotenv
from agents.audit_logger import AuditLogger
from agents.cloudera_integration import initialize_cloudera_integration

# Load environment variables
load_dotenv()

async def test_integrations():
    """Test Notion and Cloudera integrations"""
    print("🔧 Testing EthIQ Integrations")
    print("=" * 50)
    
    # Test environment variables
    print("📋 Environment Variables:")
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db = os.getenv("NOTION_DATABASE_ID")
    cloudera_host = os.getenv("CLOUDERA_HOST")
    
    print(f"   NOTION_TOKEN: {'✅ Set' if notion_token else '❌ Not set'}")
    print(f"   NOTION_DATABASE_ID: {'✅ Set' if notion_db else '❌ Not set'}")
    print(f"   CLOUDERA_HOST: {'✅ Set' if cloudera_host else '❌ Not set'}")
    
    # Test Audit Logger
    print("\n📝 Testing Audit Logger:")
    try:
        audit_logger = AuditLogger()
        print(f"   ✅ Audit Logger initialized")
        print(f"   Notion logging: {'✅ Enabled' if audit_logger.notion_token else '❌ Disabled'}")
        print(f"   Cloudera streaming: {'✅ Enabled' if audit_logger.cloudera_config else '❌ Disabled'}")
    except Exception as e:
        print(f"   ❌ Audit Logger failed: {e}")
    
    # Test Cloudera Integration
    print("\n☁️ Testing Cloudera Integration:")
    try:
        cloudera_initialized = await initialize_cloudera_integration()
        print(f"   Cloudera initialization: {'✅ Success' if cloudera_initialized else '❌ Failed'}")
    except Exception as e:
        print(f"   ❌ Cloudera test failed: {e}")
    
    # Test sample logging
    print("\n🧪 Testing Sample Logging:")
    try:
        sample_task = {
            "type": "deliberation_log",
            "deliberation_data": {
                "task_id": "test_001",
                "content_preview": "Test content for integration verification",
                "individual_responses": {
                    "utilitarian": {"decision": "ALLOW", "confidence": 0.9},
                    "deontological": {"decision": "ALLOW", "confidence": 0.8}
                },
                "final_decision": {"decision": "ALLOW", "confidence": 0.85}
            },
            "duration": 1.5
        }
        
        response = await audit_logger.log_deliberation(sample_task)
        print(f"   ✅ Sample logging successful: {response.decision}")
        print(f"   Confidence: {response.confidence}")
        
    except Exception as e:
        print(f"   ❌ Sample logging failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_integrations()) 