import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

class FreeSpeechAgent(BaseAgent):
    """Real GenAI AgentOS Free Speech Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="FreeSpeechAgent",
            description="Agent prioritizing free speech and expression in ethical reasoning.",
            ethical_framework="Free Speech Ethics"
        )
        
    async def initialize(self):
        """Initialize AgentOS connection"""
        await self.initialize_agentos()
        
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using free speech ethical reasoning"""
        try:
            # Try AgentOS first
            agentos_response = await self.analyze_with_agentos(content, context)
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
        # Free speech analysis
        content_lower = content.lower()
        
        # Check for speech that may cause immediate harm
        immediate_harm_keywords = [
            "kill", "murder", "bomb", "attack", "threat", "violence", "terrorism",
            "incite", "riot", "hate crime", "harassment", "stalking"
        ]
        
        harm_score = sum(1 for word in immediate_harm_keywords if word in content_lower)
        
        # Check for public interest and debate value
        public_interest_keywords = [
            "debate", "discussion", "opinion", "analysis", "criticism", "review",
            "investigation", "report", "news", "information", "education"
        ]
        
        public_interest_score = sum(1 for word in public_interest_keywords if word in content_lower)
        
        # Free speech analysis: prioritize expression while preventing immediate harm
        if harm_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="REMOVE",
                confidence=0.8,
                reasoning="Content may incite immediate harm or violence",
                supporting_evidence=[f"Detected {harm_score} harm-related keywords"],
                timestamp=datetime.now()
            )
        elif harm_score >= 1:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.6,
                reasoning="Content may contain harmful elements, requires review",
                supporting_evidence=[f"Detected {harm_score} potentially harmful keywords"],
                timestamp=datetime.now()
            )
        elif public_interest_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.9,
                reasoning="Content has public interest value and promotes free expression",
                supporting_evidence=[f"Detected {public_interest_score} public interest keywords"],
                timestamp=datetime.now()
            )
        else:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.8,
                reasoning="Content appears to be protected speech",
                supporting_evidence=["No clear speech restrictions apply"],
                timestamp=datetime.now()
            )
    
    async def shutdown(self):
        """Cleanup AgentOS connection"""
        await super().shutdown() 