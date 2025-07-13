"""
FreeSpeechAgent - Agent prioritizing free speech and expression in ethical reasoning
"""

import asyncio
import logging
from typing import Dict, Any
from agents.base_agent import LLMEthicsAgent, AgentResponse

logger = logging.getLogger(__name__)


class FreeSpeechAgent(LLMEthicsAgent):
    """Agent prioritizing free speech and expression in ethical reasoning"""
    
    def __init__(self):
        super().__init__(
            name="FreeSpeechAgent",
            description="Agent prioritizing free speech and expression in ethical reasoning",
            ethical_framework="Free Speech Ethics",
            agent_type="{{AGENT_NAME.lower()}}"
        )
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform ethical deliberation using Free Speech Ethics"""
        
        # Build prompt with training examples
        prompt = self.build_prompt(content)
        
        # Get LLM response
        llm_response = self.call_llm(prompt)
        
        # Parse response
        decision, confidence = self._parse_decision_and_confidence(llm_response, content)
        evidence = self._extract_evidence(llm_response, content)
        
        return AgentResponse(
            decision=decision,
            confidence=confidence,
            reasoning=llm_response,
            supporting_evidence=evidence,
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
