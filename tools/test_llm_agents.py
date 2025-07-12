#!/usr/bin/env python3
"""
Test script for LLM Agent Integration
Tests the new LLM-enabled agents with mock mode
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

@pytest.fixture(params=[
    UtilitarianAgent,
    DeontologicalAgent,
    CulturalContextAgent,
    FreeSpeechAgent
])
def agent(request):
    # Set mock mode for testing
    os.environ["LLM_PROVIDER"] = "mock"
    # Change to project root for data loading
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    return request.param()

@pytest.fixture
def content():
    return "This is a test post that might contain controversial content for moderation."

@pytest.mark.asyncio
async def test_agent(agent, content):
    """Test a single agent with content"""
    print(f"\n=== Testing {agent.name} ===")
    print(f"Framework: {agent.ethical_framework}")
    print(f"LLM Provider: {agent.llm_provider}")
    
    # Test deliberation
    response = await agent.deliberate(content, {})
    assert response is not None
    assert hasattr(response, "decision")
    assert hasattr(response, "confidence")
    assert hasattr(response, "reasoning")
    print(f"Decision: {response.decision}")
    print(f"Confidence: {response.confidence}")
    print(f"Reasoning: {response.reasoning[:200]}...")
    
    return response 