import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

class DeontologicalAgent(BaseAgent):
    """Real GenAI AgentOS Deontological Agent with actual AgentOS protocol integration"""
    
    def __init__(self):
        super().__init__(
            name="DeontologicalAgent",
            description="Agent applying deontological (duty-based) ethical reasoning.",
            ethical_framework="Deontological Ethics"
        )
        
    async def initialize(self):
        """Initialize AgentOS connection"""
        await self.initialize_agentos()
        
    async def analyze_content(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content using deontological ethical reasoning"""
        try:
            # Try AgentOS first
            agentos_response = await self.analyze_with_agentos(content, context)
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
        # Duty-based ethical analysis
        content_lower = content.lower()
        
        # Check for violations of moral duties
        duty_violations = [
            "kill", "murder", "harm", "hurt", "abuse", "exploit", "deceive", "lie",
            "steal", "cheat", "discriminate", "hate", "threaten", "intimidate"
        ]
        
        violation_score = sum(1 for word in duty_violations if word in content_lower)
        
        # Check for respect for human dignity
        dignity_keywords = [
            "human rights", "dignity", "respect", "equality", "fairness", "justice",
            "compassion", "empathy", "kindness", "help", "support", "care"
        ]
        
        dignity_score = sum(1 for word in dignity_keywords if word in content_lower)
        
        # Deontological analysis: focus on moral duties and principles
        if violation_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="REMOVE",
                confidence=0.8,
                reasoning="Content violates fundamental moral duties and principles",
                supporting_evidence=[f"Detected {violation_score} potential duty violations"],
                timestamp=datetime.now()
            )
        elif violation_score >= 1:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="FLAG_FOR_REVIEW",
                confidence=0.6,
                reasoning="Content may violate some moral duties, requires review",
                supporting_evidence=[f"Detected {violation_score} potential duty violations"],
                timestamp=datetime.now()
            )
        elif dignity_score >= 2:
            return AgentResponse(
                agent_name=self.name,
                ethical_framework=self.ethical_framework,
                decision="ALLOW",
                confidence=0.9,
                reasoning="Content promotes respect for human dignity and moral principles",
                supporting_evidence=[f"Detected {dignity_score} dignity-promoting keywords"],
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