"""
A2A (Agent-to-Agent) Protocol for EthIQ
Enhanced communication and orchestration for ethical deliberation agents
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable, Set
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of A2A messages"""
    DELIBERATION_REQUEST = "deliberation_request"
    DELIBERATION_RESPONSE = "deliberation_response"
    CROSS_EXAMINATION = "cross_examination"
    CONSENSUS_BUILDING = "consensus_building"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class A2AMessage:
    """Enhanced A2A message structure"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    recipients: List[str] = field(default_factory=list)
    message_type: MessageType = MessageType.BROADCAST
    priority: MessagePriority = MessagePriority.NORMAL
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    task_id: Optional[str] = None
    correlation_id: Optional[str] = None
    ttl: Optional[int] = None  # Time to live in seconds


class A2AProtocol:
    """Enhanced A2A protocol for agent communication"""
    
    def __init__(self):
        self.agents: Dict[str, 'A2AAgent'] = {}
        self.topics: Dict[str, Set[str]] = {}  # topic -> set of agent_ids
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.broadcast_queue: asyncio.Queue = asyncio.Queue()
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
    async def register_agent(self, agent: 'A2AAgent') -> bool:
        """Register an agent with the A2A protocol"""
        try:
            self.agents[agent.agent_id] = agent
            self.logger.info(f"Registered agent: {agent.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent.agent_id}: {e}")
            return False
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the A2A protocol"""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                # Remove from all topics
                for topic_agents in self.topics.values():
                    topic_agents.discard(agent_id)
                self.logger.info(f"Unregistered agent: {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    async def subscribe_to_topic(self, topic: str, agent_id: str) -> bool:
        """Subscribe an agent to a topic"""
        try:
            if topic not in self.topics:
                self.topics[topic] = set()
            self.topics[topic].add(agent_id)
            self.logger.info(f"Agent {agent_id} subscribed to topic: {topic}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to subscribe {agent_id} to topic {topic}: {e}")
            return False
    
    async def unsubscribe_from_topic(self, topic: str, agent_id: str) -> bool:
        """Unsubscribe an agent from a topic"""
        try:
            if topic in self.topics:
                self.topics[topic].discard(agent_id)
                self.logger.info(f"Agent {agent_id} unsubscribed from topic: {topic}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unsubscribe {agent_id} from topic {topic}: {e}")
            return False
    
    async def publish_to_topic(self, topic: str, message: A2AMessage) -> bool:
        """Publish a message to a topic"""
        try:
            if topic not in self.topics:
                self.logger.warning(f"Topic {topic} has no subscribers")
                return False
            
            # Send to all subscribers
            for agent_id in self.topics[topic]:
                if agent_id in self.agents:
                    await self.agents[agent_id].receive_message(message)
            
            self.logger.info(f"Published message to topic {topic} for {len(self.topics[topic])} subscribers")
            return True
        except Exception as e:
            self.logger.error(f"Failed to publish to topic {topic}: {e}")
            return False
    
    async def send_direct_message(self, message: A2AMessage) -> bool:
        """Send a direct message to specific recipients"""
        try:
            sent_count = 0
            for recipient in message.recipients:
                if recipient in self.agents:
                    await self.agents[recipient].receive_message(message)
                    sent_count += 1
            
            self.logger.info(f"Sent direct message to {sent_count}/{len(message.recipients)} recipients")
            return sent_count > 0
        except Exception as e:
            self.logger.error(f"Failed to send direct message: {e}")
            return False
    
    async def broadcast_message(self, message: A2AMessage) -> bool:
        """Broadcast a message to all agents"""
        try:
            message.recipients = list(self.agents.keys())
            for agent in self.agents.values():
                await agent.receive_message(message)
            
            self.logger.info(f"Broadcasted message to {len(self.agents)} agents")
            return True
        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {e}")
            return False
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                "is_active": agent.is_active,
                "last_heartbeat": agent.last_heartbeat.isoformat(),
                "subscribed_topics": [topic for topic, agents in self.topics.items() if agent_id in agents],
                "message_count": agent.message_count
            }
        return status
    
    async def start(self):
        """Start the A2A protocol"""
        self.is_running = True
        self.logger.info("A2A Protocol started")
        
        # Start message processing
        asyncio.create_task(self._process_messages())
        asyncio.create_task(self._process_broadcasts())
        asyncio.create_task(self._heartbeat_monitor())
    
    async def stop(self):
        """Stop the A2A protocol"""
        self.is_running = False
        self.logger.info("A2A Protocol stopped")
    
    async def _process_messages(self):
        """Process queued messages"""
        while self.is_running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
    
    async def _process_broadcasts(self):
        """Process broadcast messages"""
        while self.is_running:
            try:
                message = await asyncio.wait_for(self.broadcast_queue.get(), timeout=1.0)
                await self.broadcast_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing broadcast: {e}")
    
    async def _handle_message(self, message: A2AMessage):
        """Handle a specific message"""
        try:
            if message.message_type == MessageType.HEARTBEAT:
                # Update agent heartbeat
                if message.sender in self.agents:
                    self.agents[message.sender].last_heartbeat = datetime.now()
            elif message.message_type == MessageType.ERROR:
                self.logger.error(f"Agent {message.sender} reported error: {message.content}")
            else:
                # Route to appropriate handler
                await self._route_message(message)
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
    
    async def _route_message(self, message: A2AMessage):
        """Route message to appropriate handler"""
        # This can be extended with more sophisticated routing logic
        if message.recipients:
            await self.send_direct_message(message)
        else:
            await self.broadcast_message(message)
    
    async def _heartbeat_monitor(self):
        """Monitor agent heartbeats"""
        while self.is_running:
            try:
                current_time = datetime.now()
                inactive_agents = []
                
                for agent_id, agent in self.agents.items():
                    if (current_time - agent.last_heartbeat).seconds > 30:  # 30 second timeout
                        inactive_agents.append(agent_id)
                
                for agent_id in inactive_agents:
                    self.logger.warning(f"Agent {agent_id} appears inactive, removing from registry")
                    await self.unregister_agent(agent_id)
                
                await asyncio.sleep(10)  # Check every 10 seconds
            except Exception as e:
                self.logger.error(f"Error in heartbeat monitor: {e}")


class A2AAgent:
    """Base class for agents using A2A protocol"""
    
    def __init__(self, agent_id: str, agent_type: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.is_active = True
        self.last_heartbeat = datetime.now()
        self.message_count = 0
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.logger = logging.getLogger(f"{__name__}.{agent_id}")
        
        # Register default handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers"""
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat
        self.message_handlers[MessageType.ERROR] = self._handle_error
    
    async def receive_message(self, message: A2AMessage):
        """Receive a message from the A2A protocol"""
        try:
            self.message_count += 1
            
            # Check if we have a handler for this message type
            if message.message_type in self.message_handlers:
                await self.message_handlers[message.message_type](message)
            else:
                self.logger.warning(f"No handler for message type: {message.message_type}")
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
    
    async def send_message(self, message: A2AMessage) -> bool:
        """Send a message through the A2A protocol"""
        try:
            # This would be called by the A2A protocol
            self.logger.info(f"Sending message: {message.message_type.value}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False
    
    async def _handle_heartbeat(self, message: A2AMessage):
        """Handle heartbeat message"""
        self.last_heartbeat = datetime.now()
    
    async def _handle_error(self, message: A2AMessage):
        """Handle error message"""
        self.logger.error(f"Received error message: {message.content}")
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a custom message handler"""
        self.message_handlers[message_type] = handler
    
    async def start_heartbeat(self, protocol: A2AProtocol):
        """Start sending heartbeat messages"""
        while self.is_active:
            try:
                heartbeat_message = A2AMessage(
                    sender=self.agent_id,
                    message_type=MessageType.HEARTBEAT,
                    content={"status": "active"},
                    timestamp=datetime.now()
                )
                await protocol.broadcast_message(heartbeat_message)
                await asyncio.sleep(15)  # Send heartbeat every 15 seconds
            except Exception as e:
                self.logger.error(f"Error sending heartbeat: {e}")
                await asyncio.sleep(5)


# Global A2A protocol instance
a2a_protocol = A2AProtocol() 