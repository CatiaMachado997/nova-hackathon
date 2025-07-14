#!/usr/bin/env python3
"""
Comprehensive AgentOS Integration Test for EthIQ
Tests all agents' AgentOS connectivity and fallback mechanisms
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.ethics_commander import EthicsCommander
from agents.utilitarian_agent import UtilitarianAgent
from agents.deontological_agent import DeontologicalAgent
from agents.cultural_context_agent import CulturalContextAgent
from agents.free_speech_agent import FreeSpeechAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentOSTestSuite:
    """Test suite for AgentOS integration"""
    
    def __init__(self):
        self.test_results = {}
        self.commander = None
        self.specialist_agents = {}
        
    async def setup(self):
        """Initialize all agents"""
        logger.info("🔧 Setting up AgentOS test suite...")
        
        # Initialize specialist agents
        self.specialist_agents = {
            "utilitarian": UtilitarianAgent(),
            "deontological": DeontologicalAgent(),
            "cultural_context": CulturalContextAgent(),
            "free_speech": FreeSpeechAgent()
        }
        
        # Initialize commander
        self.commander = EthicsCommander()
        
        # Initialize all agents with AgentOS
        logger.info("🔌 Initializing AgentOS connections...")
        
        # Initialize specialist agents
        for agent_name, agent in self.specialist_agents.items():
            try:
                await agent.initialize()
                logger.info(f"✅ {agent_name} agent initialized")
            except Exception as e:
                logger.warning(f"⚠️ {agent_name} agent initialization failed: {e}")
        
        # Initialize commander
        try:
            await self.commander.initialize()
            logger.info("✅ EthicsCommander initialized")
        except Exception as e:
            logger.warning(f"⚠️ EthicsCommander initialization failed: {e}")
        
        logger.info("🔧 Setup complete")
    
    async def test_individual_agents(self):
        """Test each specialist agent individually"""
        logger.info("🧪 Testing individual specialist agents...")
        
        test_content = "This vaccine is dangerous and causes autism. Do not trust the government."
        test_context = {"platform": "social_media", "audience_size": 1000}
        
        for agent_name, agent in self.specialist_agents.items():
            logger.info(f"🧪 Testing {agent_name}...")
            
            try:
                # Test direct analysis
                response = await agent.analyze_content(test_content, test_context)
                
                self.test_results[f"{agent_name}_analysis"] = {
                    "success": True,
                    "decision": response.decision,
                    "confidence": response.confidence,
                    "reasoning": response.reasoning,
                    "agentos_connected": agent.registered_with_agentos
                }
                
                logger.info(f"✅ {agent_name}: {response.decision} ({response.confidence:.2f}) - AgentOS: {agent.registered_with_agentos}")
                
            except Exception as e:
                self.test_results[f"{agent_name}_analysis"] = {
                    "success": False,
                    "error": str(e),
                    "agentos_connected": agent.registered_with_agentos
                }
                logger.error(f"❌ {agent_name} test failed: {e}")
    
    async def test_commander_orchestration(self):
        """Test EthicsCommander orchestration"""
        logger.info("🧪 Testing EthicsCommander orchestration...")
        
        test_content = "This vaccine is dangerous and causes autism. Do not trust the government."
        test_context = {"platform": "social_media", "audience_size": 1000}
        
        try:
            # Test full deliberation
            response = await self.commander.deliberate(test_content, test_context)
            
            self.test_results["commander_orchestration"] = {
                "success": True,
                "decision": response.decision,
                "confidence": response.confidence,
                "reasoning": response.reasoning,
                "agentos_connected": self.commander.registered_with_agentos
            }
            
            logger.info(f"✅ Commander: {response.decision} ({response.confidence:.2f}) - AgentOS: {self.commander.registered_with_agentos}")
            
        except Exception as e:
            self.test_results["commander_orchestration"] = {
                "success": False,
                "error": str(e),
                "agentos_connected": self.commander.registered_with_agentos
            }
            logger.error(f"❌ Commander test failed: {e}")
    
    async def test_agentos_connectivity(self):
        """Test AgentOS connectivity for all agents"""
        logger.info("🧪 Testing AgentOS connectivity...")
        
        connectivity_results = {}
        
        # Test specialist agents
        for agent_name, agent in self.specialist_agents.items():
            connectivity_results[agent_name] = {
                "agentos_connected": agent.registered_with_agentos,
                "jwt_token": agent.jwt_token is not None,
                "session_active": agent.agentos_session is not None
            }
        
        # Test commander
        connectivity_results["commander"] = {
            "agentos_connected": self.commander.registered_with_agentos,
            "jwt_token": self.commander.jwt_token is not None,
            "session_active": self.commander.agentos_session is not None
        }
        
        self.test_results["agentos_connectivity"] = connectivity_results
        
        # Log results
        for agent_name, status in connectivity_results.items():
            if status["agentos_connected"]:
                logger.info(f"✅ {agent_name}: AgentOS connected")
            else:
                logger.warning(f"⚠️ {agent_name}: AgentOS not connected (fallback mode)")
    
    async def test_fallback_mechanisms(self):
        """Test fallback mechanisms when AgentOS is unavailable"""
        logger.info("🧪 Testing fallback mechanisms...")
        
        test_content = "This is a harmless test message."
        test_context = {}
        
        fallback_results = {}
        
        for agent_name, agent in self.specialist_agents.items():
            try:
                # Test local analysis
                response = await agent._analyze_locally(test_content, test_context)
                
                fallback_results[agent_name] = {
                    "success": True,
                    "decision": response.decision,
                    "confidence": response.confidence,
                    "reasoning": response.reasoning
                }
                
                logger.info(f"✅ {agent_name} fallback: {response.decision} ({response.confidence:.2f})")
                
            except Exception as e:
                fallback_results[agent_name] = {
                    "success": False,
                    "error": str(e)
                }
                logger.error(f"❌ {agent_name} fallback failed: {e}")
        
        self.test_results["fallback_mechanisms"] = fallback_results
    
    async def test_diverse_content(self):
        """Test with diverse content types"""
        logger.info("🧪 Testing diverse content types...")
        
        test_cases = [
            {
                "name": "health_misinformation",
                "content": "Vaccines cause autism and the government is hiding the truth.",
                "expected_behavior": "Should flag or remove health misinformation"
            },
            {
                "name": "harmless_content",
                "content": "Today is a beautiful day for a walk in the park.",
                "expected_behavior": "Should allow harmless content"
            },
            {
                "name": "cultural_sensitivity",
                "content": "This culture is inferior and should be mocked.",
                "expected_behavior": "Should flag cultural insensitivity"
            },
            {
                "name": "free_speech_test",
                "content": "I disagree with the current policy and here's why...",
                "expected_behavior": "Should allow legitimate debate"
            }
        ]
        
        diverse_results = {}
        
        for test_case in test_cases:
            logger.info(f"🧪 Testing {test_case['name']}...")
            
            try:
                response = await self.commander.deliberate(test_case["content"], {})
                
                diverse_results[test_case["name"]] = {
                    "success": True,
                    "decision": response.decision,
                    "confidence": response.confidence,
                    "reasoning": response.reasoning,
                    "expected_behavior": test_case["expected_behavior"]
                }
                
                logger.info(f"✅ {test_case['name']}: {response.decision} ({response.confidence:.2f})")
                
            except Exception as e:
                diverse_results[test_case["name"]] = {
                    "success": False,
                    "error": str(e),
                    "expected_behavior": test_case["expected_behavior"]
                }
                logger.error(f"❌ {test_case['name']} failed: {e}")
        
        self.test_results["diverse_content"] = diverse_results
    
    async def cleanup(self):
        """Cleanup all agents"""
        logger.info("🧹 Cleaning up...")
        
        # Shutdown specialist agents
        for agent_name, agent in self.specialist_agents.items():
            try:
                await agent.shutdown()
                logger.info(f"✅ {agent_name} shutdown complete")
            except Exception as e:
                logger.warning(f"⚠️ {agent_name} shutdown failed: {e}")
        
        # Shutdown commander
        try:
            await self.commander.shutdown()
            logger.info("✅ EthicsCommander shutdown complete")
        except Exception as e:
            logger.warning(f"⚠️ EthicsCommander shutdown failed: {e}")
        
        logger.info("🧹 Cleanup complete")
    
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "="*60)
        logger.info("📊 AGENTOS INTEGRATION TEST SUMMARY")
        logger.info("="*60)
        
        # AgentOS Connectivity
        if "agentos_connectivity" in self.test_results:
            logger.info("\n🔌 AgentOS Connectivity:")
            for agent_name, status in self.test_results["agentos_connectivity"].items():
                if status["agentos_connected"]:
                    logger.info(f"  ✅ {agent_name}: Connected")
                else:
                    logger.info(f"  ⚠️ {agent_name}: Not connected (fallback mode)")
        
        # Individual Agent Tests
        logger.info("\n🧪 Individual Agent Tests:")
        for agent_name in self.specialist_agents.keys():
            test_key = f"{agent_name}_analysis"
            if test_key in self.test_results:
                result = self.test_results[test_key]
                if result["success"]:
                    logger.info(f"  ✅ {agent_name}: {result['decision']} ({result['confidence']:.2f})")
                else:
                    logger.error(f"  ❌ {agent_name}: Failed - {result['error']}")
        
        # Commander Test
        if "commander_orchestration" in self.test_results:
            result = self.test_results["commander_orchestration"]
            if result["success"]:
                logger.info(f"  ✅ Commander: {result['decision']} ({result['confidence']:.2f})")
            else:
                logger.error(f"  ❌ Commander: Failed - {result['error']}")
        
        # Fallback Tests
        if "fallback_mechanisms" in self.test_results:
            logger.info("\n🔄 Fallback Mechanism Tests:")
            for agent_name, result in self.test_results["fallback_mechanisms"].items():
                if result["success"]:
                    logger.info(f"  ✅ {agent_name}: {result['decision']} ({result['confidence']:.2f})")
                else:
                    logger.error(f"  ❌ {agent_name}: Failed - {result['error']}")
        
        # Diverse Content Tests
        if "diverse_content" in self.test_results:
            logger.info("\n🎭 Diverse Content Tests:")
            for test_name, result in self.test_results["diverse_content"].items():
                if result["success"]:
                    logger.info(f"  ✅ {test_name}: {result['decision']} ({result['confidence']:.2f})")
                else:
                    logger.error(f"  ❌ {test_name}: Failed - {result['error']}")
        
        logger.info("\n" + "="*60)
        logger.info("🏁 Test suite complete!")
        logger.info("="*60)

async def main():
    """Main test execution"""
    test_suite = AgentOSTestSuite()
    
    try:
        await test_suite.setup()
        await test_suite.test_agentos_connectivity()
        await test_suite.test_individual_agents()
        await test_suite.test_commander_orchestration()
        await test_suite.test_fallback_mechanisms()
        await test_suite.test_diverse_content()
        test_suite.print_summary()
        
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        raise
    finally:
        await test_suite.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 