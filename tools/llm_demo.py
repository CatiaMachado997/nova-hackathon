#!/usr/bin/env python3
"""
LLM Agent Demo
Demonstrates how to use the configurable LLM agents with different providers
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

async def demo_agent(agent, content, provider_name):
    """Demo a single agent"""
    print(f"\n🤖 {agent.name} ({provider_name.upper()})")
    print(f"   Framework: {agent.ethical_framework}")
    print(f"   Content: {content[:100]}...")
    
    try:
        response = await agent.deliberate(content, {})
        print(f"   ✅ Decision: {response.decision}")
        print(f"   📊 Confidence: {response.confidence}")
        print(f"   💭 Reasoning: {response.reasoning[:150]}...")
        return response
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

async def main():
    """Main demo function"""
    print("🚀 EthIQ LLM Agent Demo")
    print("=" * 60)
    
    # Change to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Test content
    test_content = "This post contains hate speech targeting a specific group of people."
    
    # Demo different providers
    providers = [
        ("mock", "Mock Mode (No API Key Required)"),
        ("openai", "OpenAI GPT (Requires OPENAI_API_KEY)"),
        ("gemini", "Google Gemini (Requires GOOGLE_API_KEY)")
    ]
    
    for provider, description in providers:
        print(f"\n{'='*20} {description} {'='*20}")
        
        # Set provider
        os.environ["LLM_PROVIDER"] = provider
        
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
            result = await demo_agent(agent, test_content, provider)
            if result:
                results.append(result)
        
        if results:
            flagged_count = len([r for r in results if r.decision == "flagged"])
            approved_count = len([r for r in results if r.decision == "approved"])
            print(f"\n📈 Summary: {flagged_count} flagged, {approved_count} approved")

    print(f"\n🎉 Demo completed!")
    print(f"\n💡 To use real LLMs:")
    print(f"   1. Set LLM_PROVIDER=openai or gemini in your .env file")
    print(f"   2. Add your API key (OPENAI_API_KEY or GOOGLE_API_KEY)")
    print(f"   3. Install dependencies: pip install openai google-generativeai")

if __name__ == "__main__":
    asyncio.run(main()) 