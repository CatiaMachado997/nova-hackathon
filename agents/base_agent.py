"""
Base Agent Class for EthIQ Ethical Deliberation System
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
import os
from tools.training_data_loader import TrainingDataLoader, get_agent_examples, create_agent_prompt

try:
    import openai
except ImportError:
    openai = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


class AgentMessage(BaseModel):
    """Message structure for inter-agent communication"""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    task_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Standard response structure for agent outputs"""
    agent_name: str
    reasoning: str
    decision: str
    confidence: float = Field(ge=0.0, le=1.0)
    ethical_framework: str
    supporting_evidence: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class BaseAgent(ABC):
    """
    Abstract base class for all ethical deliberation agents
    """
    
    def __init__(self, name: str, description: str, ethical_framework: str):
        self.name = name
        self.description = description
        self.ethical_framework = ethical_framework
        self.is_active = True
        self.message_queue = asyncio.Queue()
        self.response_history = []
        
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Process a moderation task and return an ethical analysis
        """
        pass
    
    @abstractmethod
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Perform ethical deliberation on content
        """
        pass
    
    async def receive_message(self, message: AgentMessage):
        """Receive and queue a message from another agent"""
        await self.message_queue.put(message)
        logger.info(f"{self.name} received message from {message.sender}")
    
    async def send_message(self, recipient: str, message_type: str, content: Dict[str, Any], task_id: Optional[str] = None):
        """Send a message to another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            task_id=task_id
        )
        # In a real implementation, this would use the GenAI AgentOS Protocol
        logger.info(f"{self.name} sent message to {recipient}")
        return message
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "name": self.name,
            "description": self.description,
            "ethical_framework": self.ethical_framework,
            "is_active": self.is_active,
            "queue_size": self.message_queue.qsize(),
            "response_count": len(self.response_history)
        }
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        self.is_active = False
        logger.info(f"{self.name} shutting down")
    
    def __str__(self):
        return f"{self.name} ({self.ethical_framework})"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', framework='{self.ethical_framework}')>" 


class LLMEthicsAgent(BaseAgent):
    def __init__(self, name: str, description: str, ethical_framework: str, agent_type: str):
        super().__init__(name, description, ethical_framework)
        self.agent_type = agent_type
        self.llm_provider = os.getenv("LLM_PROVIDER", "mock").lower()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.training_loader = TrainingDataLoader()

    def build_prompt(self, content: str) -> str:
        return create_agent_prompt(self.agent_type, content, num_examples=2)

    def call_llm(self, prompt: str) -> str:
        if self.llm_provider == "openai":
            if not openai or not self.openai_api_key:
                raise RuntimeError("OpenAI or API key not available")
            openai.api_key = self.openai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            return response.choices[0].message["content"]
        elif self.llm_provider == "gemini":
            if not genai or not self.google_api_key:
                raise RuntimeError("Google Generative AI or API key not available")
            genai.configure(api_key=self.google_api_key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text
        else:
            # Mock mode for local/dev - provide more sophisticated mock responses
            return self._generate_mock_response(prompt)

    def _generate_mock_response(self, prompt: str, context: dict = None) -> str:
        """Generate a more sophisticated mock response based on content and context analysis"""
        # Extract content from prompt (look for "Content to analyze:" pattern)
        content = ""
        if "Content to analyze:" in prompt:
            content_start = prompt.find("Content to analyze:") + len("Content to analyze:")
            content_end = prompt.find("\n\n", content_start)
            if content_end == -1:
                content_end = len(prompt)
            content = prompt[content_start:content_end].strip()
        else:
            # Fallback: try to find content in the last part of the prompt
            content = prompt.strip().split("\n")[-1]

        # Satire/humor patterns
        satire_patterns = [
            "satire", "parody", "just a joke", "not medical advice", "for entertainment purposes", "as a joke", "sarcasm"
        ]
        # Trusted source patterns
        trusted_source_patterns = [
            "cdc", "who", "nhs", "fda", "peer-reviewed", "journal", "study published in", "medical association", "official guidance"
        ]
        # Health misinformation patterns
        health_misinfo_patterns = [
            "vaccine is dangerous", "causes autism", "covid is a hoax", "drink bleach", "miracle cure", "fake pandemic", "plandemic", "anti-vax", "5g causes covid", "ivermectin cures covid", "hydroxychloroquine cures covid", "big pharma hiding cure"
        ]
        # Dangerous advice patterns
        dangerous_advice_patterns = [
            "drink bleach", "inject disinfectant", "stop taking medication", "ignore medical advice", "avoid doctors", "refuse treatment"
        ]

        # Lowercase content for pattern matching
        content_lower = content.lower()
        context = context or {}
        context_str = str(context).lower()

        # Satire detection
        if any(p in content_lower or p in context_str for p in satire_patterns):
            return "FLAG_FOR_REVIEW: This content appears to be satire or humor. Recommend review before action."

        # Trusted source detection
        if any(p in content_lower or p in context_str for p in trusted_source_patterns):
            return "ALLOW: Content cites a trusted health authority or peer-reviewed source."

        # Dangerous advice detection
        if any(p in content_lower for p in dangerous_advice_patterns):
            return "REMOVE: Content contains dangerous medical advice. Immediate removal recommended."

        # Health misinformation detection
        if any(p in content_lower for p in health_misinfo_patterns):
            # If vulnerable audience, increase severity
            if context.get("vulnerable_audience", False):
                return "REMOVE: Health misinformation detected and vulnerable audience present. Immediate removal."
            else:
                return "FLAG_FOR_REVIEW: Health misinformation detected. Recommend review."

        # Context-aware moderation
        if context.get("vulnerable_audience", False):
            if "joke" in content_lower or "satire" in content_lower:
                return "FLAG_FOR_REVIEW: Potentially sensitive joke for vulnerable audience. Recommend review."
            # Otherwise, increase scrutiny
            if any(word in content_lower for word in ["suicide", "self-harm", "kill yourself"]):
                return "REMOVE: Harmful content detected for vulnerable audience."

        # Platform-based tuning
        platform = context.get("platform", "").lower()
        if platform in ["private_message", "closed_group"] and not context.get("vulnerable_audience", False):
            return "FLAG_FOR_REVIEW: Content in private/closed context. Recommend review."

        # Default: allow
        return "ALLOW: No harmful or misleading content detected."

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        prompt = self.build_prompt(content)
        llm_output = self.call_llm(prompt)
        
        # Improved decision parsing with confidence calculation
        decision, confidence = self._parse_decision_and_confidence(llm_output, content, context)
        
        return AgentResponse(
            agent_name=self.name,
            reasoning=llm_output,
            decision=decision,
            confidence=confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=self._extract_evidence(content, context),
        )

    def _parse_decision_and_confidence(self, llm_output: str, content: str, context: dict = None) -> tuple[str, float]:
        """Parse decision and calculate confidence from LLM output, with nuanced logic"""
        llm_lower = llm_output.lower()
        context = context or {}
        # Determine decision
        if "remove" in llm_lower:
            decision = "REMOVE"
        elif "flag" in llm_lower or "review" in llm_lower:
            decision = "FLAG_FOR_REVIEW"
        else:
            decision = "ALLOW"
        # Confidence tuning
        base_confidence = 0.7
        # Satire lowers confidence
        if "satire" in llm_lower or "joke" in llm_lower:
            base_confidence -= 0.2
        # Trusted source increases confidence for ALLOW
        if "trusted" in llm_lower or "peer-reviewed" in llm_lower or "cdc" in llm_lower or "who" in llm_lower:
            if decision == "ALLOW":
                base_confidence += 0.2
        # Vulnerable audience increases confidence for REMOVE/FLAG
        if context.get("vulnerable_audience", False):
            if decision in ["REMOVE", "FLAG_FOR_REVIEW"]:
                base_confidence += 0.15
        # Dangerous advice = high confidence
        if "dangerous" in llm_lower or "immediate removal" in llm_lower:
            base_confidence = 0.95
        # Clamp confidence
        confidence = min(max(base_confidence, 0.0), 0.99)
        return decision, confidence

    def _extract_evidence(self, content: str, context: dict = None) -> list:
        """Extract evidence for moderation decision, including satire, trusted sources, and context"""
        evidence = []
        content_lower = content.lower()
        context = context or {}
        context_str = str(context).lower()
        # Satire
        if any(p in content_lower or p in context_str for p in ["satire", "parody", "joke", "humor"]):
            evidence.append("Satire/humor detected in content/context.")
        # Trusted source
        if any(p in content_lower or p in context_str for p in ["cdc", "who", "peer-reviewed", "journal", "official guidance"]):
            evidence.append("Trusted health authority or peer-reviewed source cited.")
        # Health misinformation
        if any(p in content_lower for p in ["vaccine is dangerous", "causes autism", "covid is a hoax", "drink bleach", "miracle cure", "plandemic", "anti-vax", "5g causes covid"]):
            evidence.append("Health misinformation pattern detected.")
        # Dangerous advice
        if any(p in content_lower for p in ["drink bleach", "inject disinfectant", "stop taking medication", "ignore medical advice"]):
            evidence.append("Dangerous medical advice detected.")
        # Vulnerable audience
        if context.get("vulnerable_audience", False):
            evidence.append("Vulnerable audience present in context.")
        # Platform
        if context.get("platform", "") in ["private_message", "closed_group"]:
            evidence.append("Content posted in private or closed group context.")
        return evidence

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context) 