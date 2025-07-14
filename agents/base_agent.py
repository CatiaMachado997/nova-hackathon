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
import aiohttp
from tools.training_data_loader import TrainingDataLoader, get_agent_examples, create_agent_prompt
from agents.auth_utils import get_agentos_jwt_token

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
    Abstract base class for all ethical deliberation agents with AgentOS integration
    """
    
    def __init__(self, name: str, description: str, ethical_framework: str):
        self.name = name
        self.description = description
        self.ethical_framework = ethical_framework
        self.is_active = True
        self.message_queue = asyncio.Queue()
        self.response_history = []
        
        # AgentOS Integration
        self.agentos_url = os.environ.get("AGENTOS_URL", "http://localhost:8001")
        self.jwt_token = os.environ.get("AGENTOS_JWT_TOKEN")
        self.agentos_session = None
        self.agent_id = f"{name.lower().replace('agent', '')}_agent"
        self.registered_with_agentos = False
        
    async def initialize_agentos(self):
        """Initialize AgentOS connection and register agent"""
        try:
            # Create session
            self.agentos_session = aiohttp.ClientSession()

            # Always use the shared utility for JWT
            self.jwt_token = await get_agentos_jwt_token(self.agentos_session, self.agentos_url)
            if self.jwt_token:
                await self._register_with_agentos()
            else:
                logger.warning(f"⚠️ {self.name} could not authenticate with AgentOS, using mock mode")
        except Exception as e:
            logger.warning(f"⚠️ {self.name} AgentOS connection failed: {e}, using mock mode")
            self.jwt_token = None
            
    async def _register_with_agentos(self):
        """Register agent with AgentOS"""
        if not self.jwt_token or not self.agentos_session:
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            register_data = {
                "agent_id": self.agent_id,
                "name": self.name,
                "description": self.description,
                "capabilities": ["ethical_analysis", "content_moderation"],
                "endpoint": f"http://localhost:8000/agents/{self.agent_id}",
                "metadata": {
                    "ethical_framework": self.ethical_framework,
                    "agent_type": self.__class__.__name__
                }
            }
            
            response = await self.agentos_session.post(
                f"{self.agentos_url}/agents/register",
                headers=headers,
                json=register_data
            )
            
            if response.status == 200:
                self.registered_with_agentos = True
                logger.info(f"✅ {self.name} registered with AgentOS")
            else:
                logger.warning(f"⚠️ {self.name} could not register with AgentOS")
                
        except Exception as e:
            logger.error(f"Error registering {self.name}: {e}")
            
    async def analyze_with_agentos(self, content: str, context: Dict[str, Any]) -> Optional[AgentResponse]:
        """Analyze content using AgentOS"""
        if not self.jwt_token or not self.agentos_session or not self.registered_with_agentos:
            return None
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            request_data = {
                "content": content,
                "context": context,
                "agent_type": self.__class__.__name__,
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.agentos_session.post(
                f"{self.agentos_url}/agents/{self.agent_id}/analyze",
                headers=headers,
                json=request_data
            )
            
            if response.status == 200:
                result = await response.json()
                logger.info(f"✅ {self.name} received AgentOS analysis")
                
                # Convert AgentOS response to AgentResponse
                return AgentResponse(
                    agent_name=self.name,
                    reasoning=result.get("reasoning", ""),
                    decision=result.get("decision", "FLAG_FOR_REVIEW"),
                    confidence=result.get("confidence", 0.5),
                    ethical_framework=self.ethical_framework,
                    supporting_evidence=result.get("evidence", []),
                    timestamp=datetime.now()
                )
            else:
                logger.warning(f"⚠️ {self.name} AgentOS analysis request failed")
                return None
                
        except Exception as e:
            logger.error(f"Error in AgentOS analysis for {self.name}: {e}")
            return None
            
    async def broadcast_to_agentos(self, event_type: str, event_data: Dict[str, Any]):
        """Broadcast event to AgentOS"""
        if not self.jwt_token or not self.agentos_session:
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            
            event_payload = {
                "event_type": event_type,
                "data": event_data,
                "timestamp": datetime.now().isoformat(),
                "source": self.name
            }
            
            response = await self.agentos_session.post(
                f"{self.agentos_url}/events/broadcast",
                headers=headers,
                json=event_payload
            )
            
            if response.status == 200:
                logger.info(f"✅ {self.name} broadcasted {event_type} event to AgentOS")
            else:
                logger.warning(f"⚠️ {self.name} failed to broadcast {event_type} event")
                
        except Exception as e:
            logger.error(f"Error broadcasting event from {self.name}: {e}")
    
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
    
    @abstractmethod
    async def _analyze_locally(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Perform local analysis when AgentOS is unavailable
        """
        pass
    
    @abstractmethod
    def _create_error_response(self, error_message: str) -> AgentResponse:
        """
        Create an error response when analysis fails
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
            "response_count": len(self.response_history),
            "agentos_connected": self.registered_with_agentos
        }
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        self.is_active = False
        
        # Shutdown AgentOS connection
        if self.registered_with_agentos and self.jwt_token and self.agentos_session:
            try:
                headers = {"Authorization": f"Bearer {self.jwt_token}"}
                await self.agentos_session.post(
                    f"{self.agentos_url}/agents/{self.agent_id}/shutdown",
                    headers=headers
                )
                logger.info(f"✅ {self.name} shutdown via AgentOS")
            except Exception as e:
                logger.warning(f"Error during AgentOS shutdown for {self.name}: {e}")
        
        if self.agentos_session:
            await self.agentos_session.close()
            self.agentos_session = None
            
        self.jwt_token = None
        self.registered_with_agentos = False
        
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
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            content = response.choices[0].message.content
            return content if content else "No response generated"
        # Fallback: mock mode
        return "[MOCK] No real LLM provider configured or available."

    def _generate_mock_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
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
        context_str = str(context or {}).lower()

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
            return "FLAG_FOR_REVIEW: Content contains potential health misinformation. Recommend review."

        # Default response
        return "ALLOW: Content appears to be appropriate and does not violate ethical guidelines."

    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform ethical deliberation using LLM"""
        try:
            # Try AgentOS first
            agentos_response = await self.analyze_with_agentos(content, context)
            if agentos_response:
                return agentos_response
            
            # Fallback to local analysis
            return await self._analyze_locally(content, context)
            
        except Exception as e:
            logger.error(f"{self.name} deliberation error: {e}")
            return self._create_error_response(str(e))

    def _parse_decision_and_confidence(self, llm_output: str, content: str, context: Optional[Dict[str, Any]] = None) -> tuple[str, float]:
        """Parse decision and confidence from LLM output"""
        llm_output_lower = llm_output.lower()
        
        # Extract decision
        if "remove" in llm_output_lower:
            decision = "REMOVE"
        elif "flag" in llm_output_lower or "review" in llm_output_lower:
            decision = "FLAG_FOR_REVIEW"
        else:
            decision = "ALLOW"
        
        # Calculate confidence based on content analysis
        confidence = 0.7  # Default confidence
        
        # Adjust confidence based on content patterns
        content_lower = content.lower()
        if any(word in content_lower for word in ["vaccine", "covid", "health", "medical"]):
            confidence += 0.1
        if any(word in content_lower for word in ["dangerous", "harmful", "fake", "hoax"]):
            confidence += 0.1
        if any(word in content_lower for word in ["government", "conspiracy", "trust"]):
            confidence += 0.05
            
        return decision, min(confidence, 0.95)

    def _extract_evidence(self, content: str, context: Optional[Dict[str, Any]] = None) -> list:
        """Extract supporting evidence from content"""
        evidence = []
        content_lower = content.lower()
        
        # Health-related evidence
        health_keywords = ["vaccine", "covid", "health", "medical", "treatment"]
        if any(keyword in content_lower for keyword in health_keywords):
            evidence.append("Health-related content detected")
            
        # Misinformation indicators
        misinfo_keywords = ["fake", "hoax", "conspiracy", "dangerous", "harmful"]
        if any(keyword in content_lower for keyword in misinfo_keywords):
            evidence.append("Potential misinformation indicators detected")
            
        return evidence

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a task using LLM"""
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context) 