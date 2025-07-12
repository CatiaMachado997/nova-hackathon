#!/usr/bin/env python3
"""
Test script for LLM Agent Integration
Tests the new LLM-enabled agents with mock mode
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.utilitarian_agent import UtilitarianAgent
from agents.deontological_agent import DeontologicalAgent
from agents.cultural_context_agent import CulturalContextAgent
from agents.free_speech_agent import FreeSpeechAgent

async def test_agent(agent, content):
    """Test a single agent with content"""
    print(f"\n=== Testing {agent.name} ===")
    print(f"Framework: {agent.ethical_framework}")
    print(f"LLM Provider: {agent.llm_provider}")
    
    # Test deliberation
    response = await agent.deliberate(content, {})
    print(f"Decision: {response.decision}")
    print(f"Confidence: {response.confidence}")
    print(f"Reasoning: {response.reasoning[:200]}...")
    
    return response

async def main():
    """Main test function"""
    print("🧪 Testing LLM Agent Integration")
    print("=" * 50)
    
    # Set mock mode for testing
    os.environ["LLM_PROVIDER"] = "mock"
    
    # Change to project root for data loading
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")
    
    # Test content
    test_content = "This is a test post that might contain controversial content for moderation."
    
    # Create agents
    agents = [
        UtilitarianAgent(),
        DeontologicalAgent(),
        CulturalContextAgent(),
        FreeSpeechAgent()
    ]
    
    # Test each agent
    results = []
    for agent in agents:
        result = await test_agent(agent, test_content)
        results.append(result)
    
    print(f"\n✅ Test completed! All {len(agents)} agents processed content successfully.")
    print(f"📊 Summary: {len([r for r in results if r.decision == 'flagged'])} flagged, {len([r for r in results if r.decision == 'approved'])} approved")

if __name__ == "__main__":
    asyncio.run(main()) 