"""
GenAI AgentOS Protocol Integration for EthIQ
Enables agent orchestration, messaging, and lifecycle management through the protocol
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)

class RealAgentOSIntegration:
    """Real GenAI AgentOS Integration for EthIQ"""
    
    def __init__(self, agentos_url: str = "ws://4b262edbb4ce.ngrok-free.app/ws"):
        self.agentos_url = agentos_url
        self.jwt_token = None
        self.registered_agents = {}
        self.session = None
        
    async def initialize(self):
        """Initialize connection to real AgentOS"""
        try:
            self.session = aiohttp.ClientSession()
            
            # Authenticate with AgentOS
            auth_response = await self.session.post(
                f"{self.agentos_url}/auth/login",
                json={
                    "username": "ethiq_user",
                    "password": "ethiq_password"
                }
            )
            
            if auth_response.status == 200:
                auth_data = await auth_response.json()
                self.jwt_token = auth_data.get("access_token")
                logger.info("✅ Authenticated with real AgentOS")
            else:
                logger.warning("⚠️ Could not authenticate with AgentOS, using mock mode")
                self.jwt_token = None
                
        except Exception as e:
            logger.warning(f"⚠️ AgentOS connection failed: {e}, using mock mode")
            self.jwt_token = None
            
    async def register_agent(self, agent_id: str, agent_config: Dict[str, Any]) -> bool:
        """Register an agent with real AgentOS"""
        if not self.jwt_token or not self.session:
            logger.warning("No JWT token or session, skipping AgentOS registration")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            register_data = {
                "agent_id": agent_id,
                "name": agent_config.get("name", agent_id),
                "description": agent_config.get("description", ""),
                "capabilities": agent_config.get("capabilities", []),
                "endpoint": agent_config.get("endpoint", ""),
                "metadata": agent_config.get("metadata", {})
            }
            
            response = await self.session.post(
                f"{self.agentos_url}/agents/register",
                headers=headers,
                json=register_data
            )
            
            if response.status == 200:
                self.registered_agents[agent_id] = agent_config
                logger.info(f"✅ Registered {agent_id} with AgentOS")
                return True
            else:
                logger.warning(f"⚠️ Failed to register {agent_id} with AgentOS")
                return False
                
        except Exception as e:
            logger.error(f"Error registering {agent_id}: {e}")
            return False
            
    async def send_analysis_request(self, agent_id: str, content: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send analysis request to real AgentOS agent"""
        if not self.jwt_token or agent_id not in self.registered_agents or not self.session:
            return None
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            request_data = {
                "content": content,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.session.post(
                f"{self.agentos_url}/agents/{agent_id}/analyze",
                headers=headers,
                json=request_data
            )
            
            if response.status == 200:
                result = await response.json()
                logger.info(f"✅ Received analysis from {agent_id}")
                return result
            else:
                logger.warning(f"⚠️ Analysis request failed for {agent_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error in analysis request to {agent_id}: {e}")
            return None
            
    async def broadcast_event(self, event_type: str, event_data: Dict[str, Any]):
        """Broadcast event to all registered agents"""
        if not self.jwt_token or not self.session:
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            event_payload = {
                "event_type": event_type,
                "data": event_data,
                "timestamp": datetime.now().isoformat(),
                "source": "ethiq_system"
            }
            
            response = await self.session.post(
                f"{self.agentos_url}/events/broadcast",
                headers=headers,
                json=event_payload
            )
            
            if response.status == 200:
                logger.info(f"✅ Broadcasted {event_type} event to AgentOS")
            else:
                logger.warning(f"⚠️ Failed to broadcast {event_type} event")
                
        except Exception as e:
            logger.error(f"Error broadcasting event: {e}")
            
    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of registered agent"""
        if not self.jwt_token or not self.session:
            return None
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            response = await self.session.get(
                f"{self.agentos_url}/agents/{agent_id}/status",
                headers=headers
            )
            
            if response.status == 200:
                return await response.json()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting status for {agent_id}: {e}")
            return None
            
    async def shutdown(self):
        """Cleanup AgentOS connections"""
        if self.jwt_token and self.session:
            try:
                # Shutdown all registered agents
                for agent_id in self.registered_agents:
                    headers = {"Authorization": f"Bearer {self.jwt_token}"}
                    await self.session.post(
                        f"{self.agentos_url}/agents/{agent_id}/shutdown",
                        headers=headers
                    )
                    
                logger.info("✅ Shutdown all AgentOS agents")
                
            except Exception as e:
                logger.warning(f"Error during AgentOS shutdown: {e}")
                
        if self.session:
            await self.session.close()
            
        logger.info("AgentOS integration shutdown complete")

    async def close(self):
        """Close AgentOS connection"""
        if self.session:
            await self.session.close()
            self.session = None
        self.jwt_token = None

    async def orchestrate_moderation(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate content moderation with AgentOS agents"""
        try:
            if not self.session:
                await self.initialize()
            
            # Send moderation request to AgentOS
            headers = {"Authorization": f"Bearer {self.jwt_token}"} if self.jwt_token else {}
            
            moderation_data = {
                "content": content,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            if self.session:
                response = await self.session.post(
                    f"{self.agentos_url}/moderate",
                    json=moderation_data,
                    headers=headers
                )
                
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"AgentOS moderation failed: {response.status}")
                    return {"error": "AgentOS moderation failed"}
            else:
                return {"error": "AgentOS session not available"}
                
        except Exception as e:
            logger.error(f"AgentOS orchestration error: {e}")
            return {"error": str(e)}

    async def get_status(self) -> Dict[str, Any]:
        """Get AgentOS integration status"""
        try:
            if not self.session:
                await self.initialize()
            
            headers = {"Authorization": f"Bearer {self.jwt_token}"} if self.jwt_token else {}
            
            if self.session:
                response = await self.session.get(
                    f"{self.agentos_url}/status",
                    headers=headers
                )
                
                if response.status == 200:
                    return await response.json()
                else:
                    return {"status": "disconnected", "error": f"HTTP {response.status}"}
            else:
                return {"status": "error", "error": "Session not available"}
                
        except Exception as e:
            logger.error(f"Failed to get AgentOS status: {e}")
            return {"status": "error", "error": str(e)}

# Global instance
agentos_integration = RealAgentOSIntegration("ws://4b262edbb4ce.ngrok-free.app/ws") 

async def initialize_agentos_protocol(agents: Dict[str, Any]) -> bool:
    """Initialize AgentOS Protocol integration"""
    try:
        integration = RealAgentOSIntegration("ws://4b262edbb4ce.ngrok-free.app/ws")
        await integration.initialize()
        return True
    except Exception as e:
        logger.error(f"Failed to initialize AgentOS Protocol: {e}")
        return False

async def orchestrate_with_agentos(content: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Orchestrate content moderation with AgentOS"""
    try:
        integration = RealAgentOSIntegration("ws://4b262edbb4ce.ngrok-free.app/ws")
        await integration.initialize()
        return await integration.orchestrate_moderation(content, context)
    except Exception as e:
        logger.error(f"AgentOS orchestration failed: {e}")
        return {"error": str(e)}

async def get_agentos_status() -> Dict[str, Any]:
    """Get AgentOS integration status"""
    try:
        integration = RealAgentOSIntegration("ws://4b262edbb4ce.ngrok-free.app/ws")
        return await integration.get_status()
    except Exception as e:
        logger.error(f"Failed to get AgentOS status: {e}")
        return {"status": "error", "error": str(e)} 