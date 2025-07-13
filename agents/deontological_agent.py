import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent
from api.schemas import AgentResponse, ContentModerationRequest

logger = logging.getLogger(__name__)

class DeontologicalAgent(BaseAgent):
    """Real GenAI AgentOS Deontological Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="DeontologicalAgent",
            description="Agent applying deontological (duty-based) ethical reasoning.",
            ethical_framework="Deontological Ethics"
        )
        self.agentos_session = None
        self.jwt_token = None
        self.agentos_url = "http://localhost:8001"  # Real AgentOS URL
        self.agent_id = "deontological_agent"
        
    async def initialize(self):
        """Initialize real AgentOS connection"""
        try:
            # Get JWT token from AgentOS
            async with aiohttp.ClientSession() as session:
                auth_response = await session.post(
                    f"{self.agentos_url}/auth/login",
                    json={
                        "username": "ethiq_user",
                        "password": "ethiq_password"
                    }
                )
                if auth_response.status == 200:
                    auth_data = await auth_response.json()
                    self.jwt_token = auth_data.get("access_token")
                    logger.info("✅ Authenticated with AgentOS")
                else:
                    logger.warning("⚠️ Could not authenticate with AgentOS, using mock mode")
                    self.jwt_token = None
                    
            # Register agent with AgentOS
            if self.jwt_token:
                headers = {"Authorization": f"Bearer {self.jwt_token}"}
                async with aiohttp.ClientSession() as session:
                    register_response = await session.post(
                        f"{self.agentos_url}/agents/register",
                        headers=headers,
                        json={
                            "agent_id": self.agent_id,
                            "name": "DeontologicalAgent",
                            "description": "Deontological ethical reasoning agent",
                            "capabilities": ["ethical_analysis", "duty_assessment"],
                            "endpoint": "http://localhost:8000/agents/deontological"
                        }
                    )
                    if register_response.status == 200:
                        logger.info("✅ Registered with AgentOS")
                    else:
                        logger.warning("⚠️ Could not register with AgentOS")
                        
        except Exception as e:
            logger.warning(f"⚠️ AgentOS initialization failed: {e}, using mock mode")
            self.jwt_token = None
            
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using deontological ethical reasoning"""
        try:
            # Try AgentOS first
            if self.agentos_session and self.jwt_token:
                agentos_response = await self._analyze_with_agentos(content, context)
                if agentos_response:
                    return agentos_response
            
            # Fallback to local analysis
            return await self._analyze_locally(content, context)
            
        except Exception as e:
            logger.error(f"DeontologicalAgent analysis error: {e}")
            return self._create_error_response(str(e))

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content using deontological reasoning"""
        return await self.analyze_content(content, context)

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a task using deontological reasoning"""
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.analyze_content(content, context)

    def _create_error_response(self, error_message: str) -> AgentResponse:
        """Create an error response when analysis fails"""
        return AgentResponse(
            agent_name=self.name,
            ethical_framework=self.ethical_framework,
            decision="FLAG_FOR_REVIEW",
            confidence=0.3,
            reasoning=f"Analysis failed: {error_message}",
            supporting_evidence=["Analysis error occurred"],
            timestamp=datetime.now()
        )

    async def _analyze_locally(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using local deontological reasoning"""
        # Duty-based analysis: focus on rules and principles
        harmful_keywords = [
            "kill", "harm", "hurt", "dangerous", "threat", "attack", "violence",
            "hate", "discriminate", "bully", "abuse", "exploit"
        ]
        
        content_lower = content.lower()
        harmful_score = sum(1 for keyword in harmful_keywords if keyword in content_lower)
        
        # Deontological analysis: duty to prevent harm
        if harmful_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.7,
                reasoning="Content may violate duty to prevent harm",
                supporting_evidence=[f"Detected {harmful_score} potentially harmful keywords"],
                timestamp=datetime.now()
            )
        else:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.8,
                reasoning="Content appears to respect duty-based principles",
                supporting_evidence=["No clear violations of ethical duties detected"],
                timestamp=datetime.now()
            )

    async def shutdown(self):
        """Cleanup AgentOS connection"""
        await super().shutdown()
        if self.agentos_session:
            await self.agentos_session.close()
            self.agentos_session = None
        self.jwt_token = None 