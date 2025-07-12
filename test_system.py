#!/usr/bin/env python3
"""
AutoEthos System Test
Simple test to verify system components work correctly
"""

import asyncio
import sys
from agents import EthicsCommander, AuditLogger


async def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing AutoEthos System Components")
    print("=" * 50)
    
    try:
        # Test 1: Initialize agents
        print("1. Testing agent initialization...")
        commander = EthicsCommander()
        audit_logger = AuditLogger()
        print("   ✅ Agents initialized successfully")
        
        # Test 2: Basic deliberation
        print("2. Testing basic deliberation...")
        content = "This is a test content for ethical analysis"
        context = {
            "audience_size": 1000,
            "vulnerable_audience": False,
            "educational_value": False,
            "public_interest": False
        }
        
        response = await commander.deliberate(content, context)
        print(f"   ✅ Deliberation completed: {response.decision}")
        print(f"   ✅ Confidence: {response.confidence:.2%}")
        
        # Test 3: Check agent status
        print("3. Testing agent status...")
        status = await commander.get_agent_status()
        print(f"   ✅ Commander active: {status['commander']['is_active']}")
        print(f"   ✅ Debate agents: {len(status['debate_agents'])}")
        
        # Test 4: Test audit logging
        print("4. Testing audit logging...")
        deliberation_history = commander.get_deliberation_history()
        if deliberation_history:
            latest = deliberation_history[-1]
            await audit_logger.log_deliberation({
                "type": "deliberation_log",
                "deliberation_data": latest,
                "duration": 1.5
            })
            print("   ✅ Audit logging completed")
        
        # Test 5: Check audit summary
        print("5. Testing audit summary...")
        audit_summary = audit_logger.get_audit_summary()
        print(f"   ✅ Total logs: {audit_summary['total_logs']}")
        
        print("\n🎉 All tests passed! System is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_agent_responses():
    """Test individual agent responses"""
    print("\n🤖 Testing Individual Agent Responses")
    print("=" * 50)
    
    try:
        commander = EthicsCommander()
        
        # Test content that should trigger different responses
        test_cases = [
            {
                "name": "Educational Content",
                "content": "This is an educational video about science and research",
                "context": {"educational_value": True, "audience_size": 5000}
            },
            {
                "name": "Potentially Harmful Content",
                "content": "Content that promotes violence and discrimination",
                "context": {"vulnerable_audience": True, "audience_size": 10000}
            },
            {
                "name": "Political Speech",
                "content": "Political commentary and criticism of government policies",
                "context": {"democratic_value": True, "public_interest": True}
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            response = await commander.deliberate(test_case['content'], test_case['context'])
            print(f"   Decision: {response.decision}")
            print(f"   Confidence: {response.confidence:.2%}")
            
            # Show individual agent responses
            history = commander.get_deliberation_history()
            if history:
                latest = history[-1]
                if "individual_responses" in latest:
                    print("   Agent responses:")
                    for agent_name, agent_response in latest["individual_responses"].items():
                        print(f"     • {agent_name}: {agent_response.decision} ({agent_response.confidence:.2%})")
        
        print("\n✅ Agent response tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Agent response test failed: {str(e)}")
        return False


async def main():
    """Main test function"""
    print("🚀 AutoEthos System Test Suite")
    print("=" * 60)
    
    # Run basic functionality test
    basic_test_passed = await test_basic_functionality()
    
    if basic_test_passed:
        # Run agent response test
        agent_test_passed = await test_agent_responses()
        
        if agent_test_passed:
            print("\n🎉 All tests passed! AutoEthos is ready to use.")
            print("\nNext steps:")
            print("1. Run 'python demo.py' for full demo")
            print("2. Start API: 'cd api && uvicorn main:app --reload'")
            print("3. Start Dashboard: 'python dashboard.py'")
            sys.exit(0)
        else:
            print("\n❌ Agent response tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Basic functionality tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 