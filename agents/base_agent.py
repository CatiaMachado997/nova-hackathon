"""
Base Agent Class for AutoEthos Ethical Deliberation System
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

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