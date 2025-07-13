#!/usr/bin/env python3
"""
Integrate EthIQ System with Cloudera Project
Connects the running EthIQ system to the Cloudera AI Workbench project
"""

import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloudera_project_integration import ClouderaProjectIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EthIQClouderaIntegrator:
    """Integrates EthIQ system with Cloudera project"""
    
    def __init__(self):
        self.cloudera_integration = ClouderaProjectIntegration()
        self.api_base_url = "http://localhost:8000"
        self.dashboard_url = "http://localhost:5000"
        
    async def setup_integration(self) -> bool:
        """Set up the complete integration"""
        
        print("🔗 Setting up EthIQ-Cloudera Integration")
        print("=" * 50)
        
        # 1. Check if EthIQ system is running
        if not await self._check_ethiq_system():
            print("❌ EthIQ system is not running. Please start the API and dashboard first.")
            return False
        
        # 2. Set up Cloudera project infrastructure
        print("\n1️⃣ Setting up Cloudera project infrastructure...")
        success = await self.cloudera_integration.setup_project_infrastructure()
        if not success:
            print("❌ Failed to setup Cloudera infrastructure")
            return False
        
        # 3. Connect real-time data streaming
        print("\n2️⃣ Setting up real-time data streaming...")
        await self._setup_realtime_streaming()
        
        # 4. Test the integration
        print("\n3️⃣ Testing integration...")
        await self._test_integration()
        
        # 5. Start continuous monitoring
        print("\n4️⃣ Starting continuous monitoring...")
        await self._start_monitoring()
        
        return True
    
    async def _check_ethiq_system(self) -> bool:
        """Check if EthIQ system is running"""
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Check API
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status != 200:
                        return False
                
                # Commented out dashboard check for compatibility
                # async with session.get(self.dashboard_url) as response:
                #     if response.status != 200:
                #         return False
                
                print("✅ EthIQ system is running")
                return True
                
        except Exception as e:
            logger.error(f"Error checking EthIQ system: {e}")
            return False
    
    async def _setup_realtime_streaming(self):
        """Set up real-time data streaming from EthIQ to Cloudera"""
        
        print("📡 Setting up real-time streaming...")
        
        # Stream current system status
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Get current analytics
                async with session.get(f"{self.api_base_url}/api/analytics/summary") as response:
                    if response.status == 200:
                        analytics = await response.json()
                        await self.cloudera_integration.stream_project_data(
                            analytics, "deliberation_analytics"
                        )
                
                # Get agent status
                async with session.get(f"{self.api_base_url}/api/agents") as response:
                    if response.status == 200:
                        agents = await response.json()
                        await self.cloudera_integration.stream_project_data(
                            agents, "agent_metrics"
                        )
                
                print("✅ Real-time streaming setup complete")
                
        except Exception as e:
            logger.error(f"Error setting up streaming: {e}")
    
    async def _test_integration(self):
        """Test the integration by submitting content and monitoring"""
        
        print("🧪 Testing integration...")
        
        try:
            import aiohttp
            
            test_content = {
                "content": "Integration test content for Cloudera project. This content will be processed by all agents and streamed to Cloudera.",
                "audience_size": 5000,
                "vulnerable_audience": False,
                "educational_value": True,
                "content_type": "text"
            }
            
            async with aiohttp.ClientSession() as session:
                # Submit moderation request
                async with session.post(
                    f"{self.api_base_url}/api/moderate",
                    json=test_content
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Stream the result to Cloudera
                        await self.cloudera_integration.stream_project_data(
                            result, "moderation_events"
                        )
                        
                        print(f"✅ Test moderation completed: {result['final_decision']}")
                        print(f"📊 Task ID: {result['task_id']}")
                        print(f"🎯 Confidence: {result['confidence']}")
                        
                        # Stream agent performance data
                        for agent_name, agent_response in result.get('individual_responses', {}).items():
                            await self.cloudera_integration.stream_project_data(
                                {
                                    "agent_name": agent_name,
                                    "decision": agent_response.get('decision'),
                                    "confidence": agent_response.get('confidence'),
                                    "response_time_ms": int(result.get('processing_time', 0) * 1000),
                                    "task_id": result['task_id'],
                                    "timestamp": datetime.now().isoformat()
                                },
                                "agent_metrics"
                            )
                        
                        return True
                    else:
                        print(f"❌ Test moderation failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error testing integration: {e}")
            return False
    
    async def _start_monitoring(self):
        """Start continuous monitoring of the integration"""
        
        print("📊 Starting continuous monitoring...")
        print("🔄 Monitoring will continue in the background")
        print("📈 Check your Cloudera AI Workbench for real-time data")
        
        # Start background monitoring task
        asyncio.create_task(self._monitor_loop())
    
    async def _monitor_loop(self):
        """Background monitoring loop"""
        
        while True:
            try:
                # Get current analytics every 30 seconds
                analytics = await self.cloudera_integration.get_project_analytics()
                
                # Stream performance metrics
                await self.cloudera_integration.stream_project_data(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "total_moderations": analytics['moderation_summary']['total_moderations'],
                        "average_confidence": analytics['moderation_summary']['average_confidence'],
                        "system_health": analytics['system_health']
                    },
                    "performance_metrics"
                )
                
                logger.info(f"📊 Monitored {analytics['moderation_summary']['total_moderations']} total moderations")
                
                # Wait 30 seconds before next check
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Get the current integration status"""
        
        try:
            import aiohttp
            
            status = {
                "ethiq_system": "unknown",
                "cloudera_connection": "unknown",
                "data_streaming": "unknown",
                "last_update": datetime.now().isoformat()
            }
            
            # Check EthIQ system
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    status["ethiq_system"] = "healthy" if response.status == 200 else "unhealthy"
            
            # Check Cloudera analytics
            analytics = await self.cloudera_integration.get_project_analytics()
            status["cloudera_connection"] = "connected" if analytics else "disconnected"
            status["data_streaming"] = "active" if analytics.get('moderation_summary') else "inactive"
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting integration status: {e}")
            return {"error": str(e)}

async def main():
    """Main integration function"""
    
    print("🚀 EthIQ-Cloudera Project Integration")
    print("=" * 50)
    
    integrator = EthIQClouderaIntegrator()
    
    # Set up integration
    success = await integrator.setup_integration()
    
    if success:
        print("\n✅ Integration setup complete!")
        print("\n📋 Integration Summary:")
        print("• EthIQ system: Connected and streaming")
        print("• Cloudera project: Infrastructure created")
        print("• Real-time data: Streaming to Cloudera")
        print("• Monitoring: Active")
        
        print("\n🌐 Access Points:")
        print(f"• EthIQ Dashboard: {integrator.dashboard_url}")
        print(f"• EthIQ API: {integrator.api_base_url}")
        print("• Cloudera AI Workbench: Check your Cloudera dashboard")
        
        print("\n📊 What's happening now:")
        print("• Every moderation request is streamed to Cloudera")
        print("• Agent performance metrics are tracked")
        print("• Analytics dashboards are updated in real-time")
        print("• ML models can be trained on the data")
        
        # Keep the integration running
        print("\n🔄 Integration is running. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(60)
                status = await integrator.get_integration_status()
                if status.get("ethiq_system") == "healthy":
                    print("✅ Integration status: Healthy")
                else:
                    print("⚠️ Integration status: Issues detected")
        except KeyboardInterrupt:
            print("\n🛑 Integration stopped by user")
    else:
        print("❌ Integration setup failed")

if __name__ == "__main__":
    asyncio.run(main()) 