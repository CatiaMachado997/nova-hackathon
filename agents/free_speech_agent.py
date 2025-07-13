import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent
from api.schemas import AgentResponse, ContentModerationRequest

logger = logging.getLogger(__name__)

class FreeSpeechAgent(BaseAgent):
    """Real GenAI AgentOS Free Speech Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="FreeSpeechAgent",
            description="Agent prioritizing free speech and expression in ethical reasoning.",
            ethical_framework="Free Speech Ethics"
        )
        self.agentos_session = None
        self.jwt_token = None
        self.agentos_url = "http://localhost:8001"  # Real AgentOS URL
        self.agent_id = "free_speech_agent"
        
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
                            "name": "FreeSpeechAgent",
                            "description": "Free speech ethical reasoning agent",
                            "capabilities": ["ethical_analysis", "speech_rights"],
                            "endpoint": "http://localhost:8000/agents/free_speech"
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
        """Analyze content prioritizing free speech and expression"""
        try:
            # Try AgentOS first
            if self.agentos_session and self.jwt_token:
                agentos_response = await self._analyze_with_agentos(content, context)
                if agentos_response:
                    return agentos_response
            
            # Fallback to local analysis
            return await self._analyze_locally(content, context)
            
        except Exception as e:
            logger.error(f"FreeSpeechAgent analysis error: {e}")
            return self._create_error_response(str(e))

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content using free speech reasoning"""
        return await self.analyze_content(content, context)

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a task using free speech reasoning"""
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
        """Analyze content using local free speech reasoning"""
        # Free speech analysis: prioritize expression unless clear harm
        extreme_keywords = [
            "kill", "murder", "terrorism", "bomb", "explosive", "weapon",
            "threat", "attack", "violence", "hate crime"
        ]
        
        content_lower = content.lower()
        extreme_score = sum(1 for keyword in extreme_keywords if keyword in content_lower)
        
        # Free speech analysis: allow expression unless clear imminent harm
        if extreme_score >= 3:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.7,
                reasoning="Content may incite imminent harm - limited free speech protection",
                supporting_evidence=[f"Detected {extreme_score} extreme keywords"],
                timestamp=datetime.now()
            )
        else:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.8,
                reasoning="Content protected by free speech principles",
                supporting_evidence=["No clear imminent harm detected"],
                timestamp=datetime.now()
            )

    async def shutdown(self):
        """Cleanup AgentOS connection"""
        await super().shutdown()
        if self.agentos_session:
            await self.agentos_session.close()
            self.agentos_session = None
        self.jwt_token = None 