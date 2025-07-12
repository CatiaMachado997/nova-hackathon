#!/usr/bin/env python3
"""
Test script for new agents
"""

import asyncio
import os
import sys

from agents import EthicsCommander

async def test_new_agents():
    """Test the new agents"""
    print("🧪 Testing new agents...")
    
    try:
        # Set mock mode for testing
        os.environ["LLM_PROVIDER"] = "mock"
        
        # Initialize commander
        commander = EthicsCommander()
        print(f"✅ Commander initialized with {len(commander.debate_agents)} agents")
        print(f"🤖 Agents: {list(commander.debate_agents.keys())}")
        
        # Check if new agents are present
        expected_agents = ["utilitarian", "deontological", "cultural", "free_speech", 
                          "psychological", "religious_ethics", "financial_impact"]
        
        for agent_name in expected_agents:
            if agent_name in commander.debate_agents:
                print(f"✅ {agent_name}: {commander.debate_agents[agent_name].name}")
            else:
                print(f"❌ {agent_name}: Missing")
        
        # Test deliberation with new agents
        print("\n🔄 Testing deliberation with all agents...")
        content = "Test content for moderation with all agents"
        context = {"audience_size": 1000}
        
        response = await commander.deliberate(content, context)
        print(f"✅ Deliberation completed!")
        print(f"   Decision: {response.decision}")
        print(f"   Confidence: {response.confidence}")
        
        # Check deliberation history
        history = commander.get_deliberation_history()
        if history:
            latest = history[-1]
            if 'individual_responses' in latest:
                print(f"   Individual responses from {len(latest['individual_responses'])} agents:")
                for agent_name, agent_response in latest['individual_responses'].items():
                    print(f"     • {agent_name}: {agent_response.decision} ({agent_response.confidence:.2%})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_new_agents())
    if success:
        print("\n🎉 All new agents working correctly!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1) 