#!/usr/bin/env python3
"""
Debug test for EthicsCommander deliberation
"""

import asyncio
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import EthicsCommander

async def test_deliberation():
    """Test the deliberation process"""
    print("🧪 Testing EthicsCommander deliberation...")
    
    try:
        # Set mock mode for testing
        os.environ["LLM_PROVIDER"] = "mock"
        
        # Initialize commander
        commander = EthicsCommander()
        print("✅ Commander initialized")
        
        # Test deliberation
        content = "Test content for moderation"
        context = {
            "audience_size": 1000,
            "vulnerable_audience": False,
            "educational_value": False,
            "public_interest": False
        }
        
        print("🔄 Starting deliberation...")
        response = await commander.deliberate(content, context)
        
        print(f"✅ Deliberation completed!")
        print(f"   Decision: {response.decision}")
        print(f"   Confidence: {response.confidence}")
        print(f"   Reasoning: {response.reasoning[:100]}...")
        
        # Check deliberation history
        history = commander.get_deliberation_history()
        print(f"   History entries: {len(history)}")
        
        if history:
            latest = history[-1]
            print(f"   Latest task_id: {latest.get('task_id', 'unknown')}")
            print(f"   Has individual_responses: {'individual_responses' in latest}")
            
            if 'individual_responses' in latest:
                print("   Individual responses:")
                for agent_name, agent_response in latest['individual_responses'].items():
                    print(f"     • {agent_name}: {agent_response.decision} ({agent_response.confidence:.2%})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_deliberation())
    if success:
        print("\n🎉 Debug test passed!")
    else:
        print("\n❌ Debug test failed!")
        sys.exit(1) 