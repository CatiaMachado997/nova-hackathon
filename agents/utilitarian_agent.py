import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

class UtilitarianAgent(BaseAgent):
    """Real GenAI AgentOS Utilitarian Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="UtilitarianAgent",
            description="Agent applying utilitarian ethical reasoning (maximizing overall good).",
            ethical_framework="Utilitarianism"
        )
        
    async def initialize(self):
        """Initialize AgentOS connection"""
        await self.initialize_agentos()
        
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using utilitarian ethical reasoning"""
        try:
            # Try AgentOS first
            agentos_response = await self.analyze_with_agentos(content, context)
            if agentos_response:
                return agentos_response
            
            # Fallback to local analysis
            return await self._analyze_locally(content, context)
            
        except Exception as e:
            logger.error(f"UtilitarianAgent analysis error: {e}")
            return self._create_error_response(str(e))

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content using utilitarian reasoning"""
        return await self.analyze_content(content, context)

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a task using utilitarian reasoning"""
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
        """Analyze content using local utilitarian reasoning"""
        # Health misinformation detection
        health_keywords = [
            "vaccine", "covid", "coronavirus", "autism", "dangerous", "harmful",
            "government", "trust", "conspiracy", "fake", "hoax", "cure", "treatment"
        ]
        
        content_lower = content.lower()
        health_score = sum(1 for keyword in health_keywords if keyword in content_lower)
        
        # Utilitarian analysis: maximize overall good
        if health_score >= 3:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.8,
                reasoning="High potential for health misinformation - may cause harm to public health",
                supporting_evidence=[f"Detected {health_score} health-related keywords"],
                timestamp=datetime.now()
            )
        elif health_score >= 1:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.6,
                reasoning="Some health content detected but insufficient evidence for flagging",
                supporting_evidence=[f"Detected {health_score} health-related keywords"],
                timestamp=datetime.now()
            )
        else:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.9,
                reasoning="No concerning health content detected",
                supporting_evidence=["No health misinformation patterns found"],
                timestamp=datetime.now()
            )
    
    async def shutdown(self):
        """Cleanup AgentOS connection"""
        await super().shutdown() 