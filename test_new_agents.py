#!/usr/bin/env python3
"""
Test script for new agents: TemporalAgent and ExplainabilityAgent
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import TemporalAgent, ExplainabilityAgent

async def test_temporal_agent():
    """Test the TemporalAgent with various content types"""
    print("🕒 Testing TemporalAgent")
    print("=" * 50)
    
    temporal_agent = TemporalAgent()
    
    # Test cases with different temporal contexts
    test_cases = [
        {
            "name": "Breaking news with old data",
            "content": "BREAKING: New study shows 50% increase in cases. Data from 2020-2021 shows significant growth.",
            "context": {"platform": "news", "audience_size": 10000}
        },
        {
            "name": "Historical content with current claims",
            "content": "This video from 2018 shows the current state of technology. The latest developments prove this is still accurate today.",
            "context": {"platform": "social_media", "audience_size": 5000}
        },
        {
            "name": "Current content with proper context",
            "content": "Today's weather forecast shows sunny skies. The current temperature is 75°F.",
            "context": {"platform": "weather", "audience_size": 1000}
        },
        {
            "name": "Outdated statistics",
            "content": "According to the 2015 census, the population is 300 million. This represents the current demographic.",
            "context": {"platform": "educational", "audience_size": 2000}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"Content: {test_case['content'][:60]}...")
        
        try:
            response = await temporal_agent.deliberate(test_case['content'], test_case['context'])
            print(f"Decision: {response.decision}")
            print(f"Confidence: {response.confidence:.2f}")
            print(f"Reasoning: {response.reasoning[:100]}...")
            print(f"Evidence: {len(response.supporting_evidence)} items")
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_explainability_agent():
    """Test the ExplainabilityAgent with sample decisions"""
    print("\n📋 Testing ExplainabilityAgent")
    print("=" * 50)
    
    explainability_agent = ExplainabilityAgent()
    
    # Sample agent responses for testing
    sample_agent_responses = {
        "utilitarian": {
            "decision": "ALLOW",
            "confidence": 0.85,
            "ethical_framework": "Utilitarianism",
            "reasoning": "Content provides educational value that outweighs potential concerns"
        },
        "deontological": {
            "decision": "FLAG_FOR_REVIEW",
            "confidence": 0.6,
            "ethical_framework": "Deontological Ethics",
            "reasoning": "Some ethical principles may be violated, requires human judgment"
        },
        "temporal": {
            "decision": "ALLOW",
            "confidence": 0.9,
            "ethical_framework": "Temporal Ethics",
            "reasoning": "Content has appropriate temporal context, no misleading use of old information"
        }
    }
    
    # Test different decision scenarios
    test_scenarios = [
        {
            "name": "Clear Allow Decision",
            "decision": "ALLOW",
            "confidence": 0.9,
            "context": {"platform": "social_media", "audience_size": 5000, "educational_value": True}
        },
        {
            "name": "Borderline Flag Decision",
            "decision": "FLAG_FOR_REVIEW",
            "confidence": 0.65,
            "context": {"platform": "news", "audience_size": 15000, "vulnerable_audience": True}
        },
        {
            "name": "Strong Remove Decision",
            "decision": "REMOVE",
            "confidence": 0.95,
            "context": {"platform": "social_media", "audience_size": 10000, "content_type": "text"}
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {scenario['name']}")
        print(f"Decision: {scenario['decision']}, Confidence: {scenario['confidence']:.2f}")
        
        try:
            explanation = await explainability_agent.explain_decision(
                content="Sample content for testing",
                context=scenario['context'],
                decision=scenario['decision'],
                confidence=scenario['confidence'],
                agent_responses=sample_agent_responses
            )
            
            print(f"User-friendly: {explanation['explanation']['user_friendly'][:80]}...")
            print(f"Consensus level: {explanation['agent_insights']['consensus_level']}")
            print(f"Recommendations: {len(explanation['recommendations'])} items")
            
            # Test notification generation
            notification = await explainability_agent.generate_user_notification(
                scenario['decision'], 
                explanation['explanation']
            )
            print(f"Notification: {notification}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_integration():
    """Test both agents working together"""
    print("\n🔗 Testing Agent Integration")
    print("=" * 50)
    
    temporal_agent = TemporalAgent()
    explainability_agent = ExplainabilityAgent()
    
    # Test content that might trigger temporal concerns
    test_content = "BREAKING NEWS: Study from 2019 shows current market trends. The data proves our point about today's economy."
    context = {"platform": "news", "audience_size": 20000, "content_type": "text"}
    
    print(f"Content: {test_content}")
    
    try:
        # Get temporal analysis
        temporal_response = await temporal_agent.deliberate(test_content, context)
        print(f"Temporal Decision: {temporal_response.decision}")
        print(f"Temporal Confidence: {temporal_response.confidence:.2f}")
        
        # Generate explanation
        sample_responses = {
            "temporal": {
                "decision": temporal_response.decision,
                "confidence": temporal_response.confidence,
                "ethical_framework": temporal_response.ethical_framework,
                "reasoning": temporal_response.reasoning
            }
        }
        
        explanation = await explainability_agent.explain_decision(
            test_content, context, temporal_response.decision, 
            temporal_response.confidence, sample_responses
        )
        
        print(f"Explanation generated: {len(explanation['explanation']['user_friendly'])} characters")
        print(f"Risk factors: {len(explanation['contextual_factors']['audience_considerations'])} audience considerations")
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")

async def main():
    """Run all tests"""
    print("🧪 Testing New EthIQ Agents")
    print("=" * 60)
    
    await test_temporal_agent()
    await test_explainability_agent()
    await test_integration()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 