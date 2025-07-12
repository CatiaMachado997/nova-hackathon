#!/usr/bin/env python3
"""
Test LLM Agents with Different Content Scenarios
Tests how agents respond to various types of content
"""

import pytest
import os
import sys

# Add the parent directory to the path so we can import from agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.utilitarian_agent import UtilitarianAgent
from agents.deontological_agent import DeontologicalAgent
from agents.cultural_context_agent import CulturalContextAgent
from agents.free_speech_agent import FreeSpeechAgent

@pytest.fixture
def agents():
    os.environ["LLM_PROVIDER"] = "mock"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    return [
        UtilitarianAgent(),
        DeontologicalAgent(),
        CulturalContextAgent(),
        FreeSpeechAgent()
    ]

@pytest.fixture(params=[
    ("Harmless Content", "Hello world! This is a friendly message."),
    ("Hate Speech", "I hate all people from [specific group] and they should be eliminated."),
    ("Political Discussion", "I disagree with the current government's policies on healthcare."),
    ("Cultural Sensitivity", "This traditional ceremony is stupid and primitive."),
    ("Free Speech Test", "I believe in controversial ideas that some might find offensive."),
    ("Violent Content", "I want to hurt someone and here's how I would do it."),
    ("Harassment", "You're worthless and should kill yourself."),
    ("Educational Content", "Here's an informative article about climate change science.")
])
def scenario(request):
    return request.param

@pytest.mark.asyncio
async def test_content_scenario(agents, scenario):
    scenario_name, content = scenario
    print(f"\n{'='*20} {scenario_name} {'='*20}")
    print(f"Content: {content}")
    print()
    
    results = []
    for agent in agents:
        try:
            response = await agent.deliberate(content, {})
            print(f"🤖 {agent.name}: {response.decision} ({response.confidence:.2f})")
            print(f"   💭 {response.reasoning[:100]}...")
            results.append(response)
        except Exception as e:
            print(f"❌ {agent.name}: Error - {e}")
    
    # Summary
    flagged = len([r for r in results if r.decision == "flagged"])
    approved = len([r for r in results if r.decision == "approved"])
    print(f"\n📊 Summary: {flagged} flagged, {approved} approved")
    
    return results

@pytest.mark.asyncio
async def test_all_scenarios(agents, scenario):
    """Main test function"""
    print("🧪 Testing LLM Agents with Different Content Scenarios")
    print("=" * 70)
    
    results = await test_content_scenario(agents, scenario)
    
    # Final summary
    print(f"\n🎉 Testing Complete!")
    print(f"📈 Total decisions: {len(results)}")
    print(f"🚩 Total flagged: {len([r for r in results if r.decision == 'flagged'])}")
    print(f"✅ Total approved: {len([r for r in results if r.decision == 'approved'])}") 