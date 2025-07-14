import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

class CulturalContextAgent(BaseAgent):
    """Real GenAI AgentOS Cultural Context Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="CulturalContextAgent",
            description="Agent considering cultural context and norms in ethical reasoning.",
            ethical_framework="Cultural Context Ethics"
        )
        
    async def initialize(self):
        """Initialize AgentOS connection"""
        await self.initialize_agentos()
        
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using cultural context ethical reasoning"""
        try:
            # Try AgentOS first
            agentos_response = await self.analyze_with_agentos(content, context)
            if agentos_response:
                return agentos_response
            
            # Fallback to local analysis
            return await self._analyze_locally(content, context)
            
        except Exception as e:
            logger.error(f"CulturalContextAgent analysis error: {e}")
            return self._create_error_response(str(e))

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content using cultural context reasoning"""
        return await self.analyze_content(content, context)

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a task using cultural context reasoning"""
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
        """Analyze content using local cultural context reasoning"""
        # Cultural sensitivity analysis
        content_lower = content.lower()
        
        # Check for cultural insensitivity
        insensitive_keywords = [
            "racist", "racism", "discriminatory", "stereotype", "offensive", "insult",
            "hate speech", "bigotry", "prejudice", "xenophobic", "ethnocentric"
        ]
        
        insensitive_score = sum(1 for word in insensitive_keywords if word in content_lower)
        
        # Check for cultural respect
        respectful_keywords = [
            "diversity", "inclusion", "respect", "understanding", "tolerance",
            "multicultural", "cultural exchange", "heritage", "tradition"
        ]
        
        respectful_score = sum(1 for word in respectful_keywords if word in content_lower)
        
        # Cultural context analysis: balance cultural expression with sensitivity
        if insensitive_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="REMOVE",
                confidence=0.8,
                reasoning="Content contains culturally insensitive or discriminatory language",
                supporting_evidence=[f"Detected {insensitive_score} insensitive keywords"],
                timestamp=datetime.now()
            )
        elif insensitive_score >= 1:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.6,
                reasoning="Content may contain culturally insensitive elements, requires review",
                supporting_evidence=[f"Detected {insensitive_score} potentially insensitive keywords"],
                timestamp=datetime.now()
            )
        elif respectful_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.9,
                reasoning="Content promotes cultural understanding and respect",
                supporting_evidence=[f"Detected {respectful_score} culturally respectful keywords"],
                timestamp=datetime.now()
            )
        else:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.8,
                reasoning="Content appears culturally appropriate",
                supporting_evidence=["No clear cultural sensitivity issues detected"],
                timestamp=datetime.now()
            )
    
    async def shutdown(self):
        """Cleanup AgentOS connection"""
        await super().shutdown() 