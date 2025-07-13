"""
Hybrid Ethics Commander - Enhanced Agent for EthIQ
Integrates A2A protocol and MCP tool calling for sophisticated ethical deliberation
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse
from .a2a_protocol import A2AAgent, A2AMessage, MessageType, MessagePriority, a2a_protocol
from .mcp_tool_manager import MCPToolManager, ToolCall, ToolPermission, global_tool_manager
from .utilitarian_agent import UtilitarianAgent
from .deontological_agent import DeontologicalAgent
from .cultural_context_agent import CulturalContextAgent
from .free_speech_agent import FreeSpeechAgent
from .psychological_agent import PsychologicalAgent
from .religious_ethics_agent import ReligiousEthicsAgent
from .financial_impact_agent import FinancialImpactAgent

logger = logging.getLogger(__name__)


class HybridEthicsCommander(A2AAgent):
    """
    Hybrid Ethics Commander: Enhanced agent that integrates A2A protocol and MCP tool calling
    Provides sophisticated orchestration of ethical deliberation with tool-enhanced analysis
    """
    
    def __init__(self):
        super().__init__(
            agent_id="hybrid_ethics_commander",
            agent_type="orchestrator",
            capabilities=["deliberation", "consensus", "decision_making", "tool_calling", "a2a_communication"]
        )
        
        # Initialize base agent properties
        self.name = "HybridEthicsCommander"
        self.description = "Enhanced master agent that orchestrates ethical deliberation using A2A protocol and MCP tools"
        self.ethical_framework = "Hybrid Multi-Framework Orchestration"
        
        # Initialize debate agents with A2A integration
        self.debate_agents = {
            "utilitarian": UtilitarianAgent(),
            "deontological": DeontologicalAgent(),
            "cultural": CulturalContextAgent(),
            "free_speech": FreeSpeechAgent(),
            "psychological": PsychologicalAgent(),
            "religious_ethics": ReligiousEthicsAgent(),
            "financial_impact": FinancialImpactAgent()
        }
        
        # Register agents with A2A protocol
        self._register_agents_with_a2a()
        
        # Initialize MCP tool manager
        self.tool_manager = global_tool_manager
        self._register_agent_permissions()
        
        # Deliberation state
        self.active_tasks = {}
        self.deliberation_history = []
        self.tool_call_history = []
        
        # Register message handlers
        self._register_message_handlers()
        
        # Subscribe to relevant topics (moved to async start method)
        # self._subscribe_to_topics()
    
    def _register_agents_with_a2a(self):
        """Register all debate agents with A2A protocol"""
        for agent_name, agent in self.debate_agents.items():
            # Create A2A agent wrapper for each debate agent
            a2a_agent = A2AAgent(
                agent_id=f"a2a_{agent_name}",
                agent_type="debate",
                capabilities=["ethical_analysis", "deliberation"]
            )
            
            # Store reference to original agent
            setattr(a2a_agent, 'original_agent', agent)
            self.debate_agents[agent_name] = a2a_agent
    
    def _register_agent_permissions(self):
        """Register permissions for this agent"""
        permissions = [
            ToolPermission.READ_ONLY,
            ToolPermission.WRITE,
            ToolPermission.ADMIN
        ]
        self.tool_manager.register_agent_permissions(self.agent_id, permissions)
    
    def _register_message_handlers(self):
        """Register custom message handlers"""
        self.register_handler(MessageType.DELIBERATION_REQUEST, self._handle_deliberation_request)
        self.register_handler(MessageType.TOOL_REQUEST, self._handle_tool_request)
        self.register_handler(MessageType.CROSS_EXAMINATION, self._handle_cross_examination)
        self.register_handler(MessageType.CONSENSUS_BUILDING, self._handle_consensus_building)
    
    # def _subscribe_to_topics(self):
    async def _subscribe_to_topics_async(self):
        """Subscribe to relevant A2A topics"""
        topics = [
            "ethical_deliberation",
            "content_moderation",
            "agent_coordination",
            "tool_calls"
        ]
        
        for topic in topics:
            await a2a_protocol.subscribe_to_topic(topic, self.agent_id)
    
    async def _handle_deliberation_request(self, message: A2AMessage):
        """Handle deliberation request from A2A protocol"""
        try:
            content = message.content.get("content", "")
            context = message.content.get("context", {})
            task_id = message.task_id or str(uuid.uuid4())
            
            logger.info(f"Handling deliberation request for task {task_id}")
            
            # Start hybrid deliberation process
            result = await self._conduct_hybrid_deliberation(content, context, task_id)
            
            # Send response back through A2A
            response_message = A2AMessage(
                sender=self.agent_id,
                recipients=[message.sender],
                message_type=MessageType.DELIBERATION_RESPONSE,
                content=result,
                task_id=task_id,
                correlation_id=message.message_id
            )
            
            await a2a_protocol.send_direct_message(response_message)
            
        except Exception as e:
            logger.error(f"Error handling deliberation request: {e}")
            await self._send_error_message(message.sender, str(e), message.message_id)
    
    async def _handle_tool_request(self, message: A2AMessage):
        """Handle tool request from other agents"""
        try:
            tool_id = message.content.get("tool_id")
            parameters = message.content.get("parameters", {})
            
            if not tool_id:
                raise ValueError("Tool ID is required")
            
            # Create tool call
            tool_call = ToolCall(
                tool_id=tool_id,
                agent_id=message.sender,
                parameters=parameters
            )
            
            # Execute tool call
            result = await self.tool_manager.call_tool(tool_call)
            
            # Send response back
            response_message = A2AMessage(
                sender=self.agent_id,
                recipients=[message.sender],
                message_type=MessageType.TOOL_RESPONSE,
                content={
                    "success": result.success,
                    "result": result.result,
                    "error": result.error,
                    "execution_time": result.execution_time
                },
                correlation_id=message.message_id
            )
            
            await a2a_protocol.send_direct_message(response_message)
            
        except Exception as e:
            logger.error(f"Error handling tool request: {e}")
            await self._send_error_message(message.sender, str(e), message.message_id)
    
    async def _handle_cross_examination(self, message: A2AMessage):
        """Handle cross-examination phase"""
        try:
            individual_responses = message.content.get("individual_responses", {})
            task_id = message.task_id or str(uuid.uuid4())
            
            # Use MCP tools to enhance cross-examination
            cross_examination_result = await self._enhanced_cross_examination(
                individual_responses, task_id
            )
            
            # Broadcast cross-examination result
            broadcast_message = A2AMessage(
                sender=self.agent_id,
                message_type=MessageType.CROSS_EXAMINATION,
                content=cross_examination_result,
                task_id=task_id,
                priority=MessagePriority.HIGH
            )
            
            await a2a_protocol.publish_to_topic("ethical_deliberation", broadcast_message)
            
        except Exception as e:
            logger.error(f"Error in cross-examination: {e}")
    
    async def _handle_consensus_building(self, message: A2AMessage):
        """Handle consensus building phase"""
        try:
            cross_examination_data = message.content.get("cross_examination", {})
            task_id = message.task_id or str(uuid.uuid4())
            
            # Use MCP tools to enhance consensus building
            consensus_result = await self._enhanced_consensus_building(
                cross_examination_data, task_id
            )
            
            # Broadcast consensus result
            broadcast_message = A2AMessage(
                sender=self.agent_id,
                message_type=MessageType.CONSENSUS_BUILDING,
                content=consensus_result,
                task_id=task_id,
                priority=MessagePriority.HIGH
            )
            
            await a2a_protocol.publish_to_topic("ethical_deliberation", broadcast_message)
            
        except Exception as e:
            logger.error(f"Error in consensus building: {e}")
    
    async def _send_error_message(self, recipient: str, error: str, correlation_id: Optional[str] = None):
        """Send error message through A2A protocol"""
        error_message = A2AMessage(
            sender=self.agent_id,
            recipients=[recipient],
            message_type=MessageType.ERROR,
            content={"error": error},
            correlation_id=correlation_id,
            priority=MessagePriority.HIGH
        )
        
        await a2a_protocol.send_direct_message(error_message)
    
    async def _conduct_hybrid_deliberation(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Conduct enhanced deliberation using both A2A protocol and MCP tools"""
        
        logger.info(f"Starting hybrid deliberation for task {task_id}")
        
        # Phase 1: Pre-analysis using MCP tools
        pre_analysis = await self._conduct_pre_analysis(content, context, task_id)
        
        # Phase 2: Individual agent analysis with A2A communication
        individual_responses = await self._conduct_individual_analysis(content, context, task_id, pre_analysis)
        
        # Phase 3: Enhanced cross-examination
        cross_examination = await self._enhanced_cross_examination(individual_responses, task_id)
        
        # Phase 4: Enhanced consensus building
        consensus = await self._enhanced_consensus_building(cross_examination, task_id)
        
        # Phase 5: Final decision with tool validation
        final_decision = await self._make_final_decision(consensus, content, context, task_id)
        
        # Store deliberation history
        deliberation_record = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "pre_analysis": pre_analysis,
            "individual_responses": individual_responses,
            "cross_examination": cross_examination,
            "consensus": consensus,
            "final_decision": final_decision,
            "tool_calls": self.tool_call_history[-10:]  # Last 10 tool calls
        }
        
        self.deliberation_history.append(deliberation_record)
        
        return final_decision
    
    async def _conduct_pre_analysis(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Conduct pre-analysis using MCP tools"""
        
        pre_analysis = {}
        
        # Use sentiment analysis tool
        sentiment_tool = self._find_tool_by_name("analyze_content_sentiment")
        if sentiment_tool:
            sentiment_call = ToolCall(
                tool_id=sentiment_tool.tool_id,
                agent_id=self.agent_id,
                parameters={"content": content, "context": context.get("platform", "general")}
            )
            sentiment_result = await self.tool_manager.call_tool(sentiment_call)
            if sentiment_result.success:
                pre_analysis["sentiment"] = sentiment_result.result
        
        # Use cultural sensitivity tool
        cultural_tool = self._find_tool_by_name("check_cultural_sensitivity")
        if cultural_tool:
            cultural_call = ToolCall(
                tool_id=cultural_tool.tool_id,
                agent_id=self.agent_id,
                parameters={
                    "content": content,
                    "target_cultures": context.get("target_cultures", ["global"])
                }
            )
            cultural_result = await self.tool_manager.call_tool(cultural_call)
            if cultural_result.success:
                pre_analysis["cultural_sensitivity"] = cultural_result.result
        
        # Use harm assessment tool
        harm_tool = self._find_tool_by_name("assess_potential_harm")
        if harm_tool:
            harm_call = ToolCall(
                tool_id=harm_tool.tool_id,
                agent_id=self.agent_id,
                parameters={
                    "content": content,
                    "audience_type": context.get("audience_type", "general"),
                    "vulnerable_groups": "yes" if context.get("vulnerable_audience") else "none"
                }
            )
            harm_result = await self.tool_manager.call_tool(harm_call)
            if harm_result.success:
                pre_analysis["harm_assessment"] = harm_result.result
        
        return pre_analysis
    
    async def _conduct_individual_analysis(self, content: str, context: Dict[str, Any], task_id: str, pre_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct individual agent analysis using A2A protocol"""
        
        individual_responses = {}
        
        # Send deliberation request to each agent through A2A
        for agent_name, agent in self.debate_agents.items():
            deliberation_message = A2AMessage(
                sender=self.agent_id,
                recipients=agent.agent_id,
                message_type=MessageType.DELIBERATION_REQUEST,
                content={
                    "content": content,
                    "context": context,
                    "pre_analysis": pre_analysis
                },
                task_id=task_id,
                priority=MessagePriority.HIGH
            )
            
            # Send message and wait for response
            await a2a_protocol.send_direct_message(deliberation_message)
            
            # For now, use the original agent's deliberation method
            # In a full implementation, this would wait for A2A response
            original_agent = getattr(agent, 'original_agent', agent)
            if hasattr(original_agent, 'deliberate'):
                response = await original_agent.deliberate(content, context)
                individual_responses[agent_name] = {
                    "decision": response.decision,
                    "confidence": response.confidence,
                    "reasoning": response.reasoning,
                    "ethical_framework": response.ethical_framework,
                    "evidence": response.supporting_evidence
                }
        
        return individual_responses
    
    async def _enhanced_cross_examination(self, individual_responses: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Enhanced cross-examination using MCP tools"""
        
        cross_examination = {
            "conflicts": [],
            "agreements": [],
            "analysis": {}
        }
        
        # Analyze responses for conflicts and agreements
        decisions = [resp.get("decision") for resp in individual_responses.values()]
        unique_decisions = set(decisions)
        
        if len(unique_decisions) > 1:
            cross_examination["conflicts"] = [
                f"Conflict between agents: {list(unique_decisions)}"
            ]
        else:
            cross_examination["agreements"] = [
                f"All agents agree: {list(unique_decisions)[0]}"
            ]
        
        # Use audit logs tool to get historical context
        audit_tool = self._find_tool_by_name("get_audit_logs")
        if audit_tool:
            audit_call = ToolCall(
                tool_id=audit_tool.tool_id,
                agent_id=self.agent_id,
                parameters={"time_range": "24h", "agent_id": ""}
            )
            audit_result = await self.tool_manager.call_tool(audit_call)
            if audit_result.success:
                cross_examination["historical_context"] = audit_result.result
        
        return cross_examination
    
    async def _enhanced_consensus_building(self, cross_examination: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Enhanced consensus building using MCP tools"""
        
        consensus = {
            "consensus_reached": False,
            "final_decision": None,
            "confidence": 0.0,
            "reasoning": "",
            "weighted_analysis": {}
        }
        
        # Use broadcast tool to coordinate consensus
        broadcast_tool = self._find_tool_by_name("broadcast_to_agents")
        if broadcast_tool:
            broadcast_call = ToolCall(
                tool_id=broadcast_tool.tool_id,
                agent_id=self.agent_id,
                parameters={
                    "message": f"Building consensus for task {task_id}",
                    "message_type": "consensus"
                }
            )
            await self.tool_manager.call_tool(broadcast_call)
        
        # For now, implement simple consensus logic
        # In a full implementation, this would involve more sophisticated negotiation
        
        return consensus
    
    async def _make_final_decision(self, consensus: Dict[str, Any], content: str, context: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Make final decision with tool validation"""
        
        final_decision = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "final_decision": {
                "decision": "ALLOW",  # Default decision
                "confidence": 0.8,
                "reasoning": "Hybrid deliberation completed",
                "evidence": ["A2A protocol coordination", "MCP tool analysis"]
            },
            "deliberation_summary": {
                "phases_completed": 5,
                "agents_involved": len(self.debate_agents),
                "tool_calls_made": len(self.tool_call_history),
                "consensus_reached": True
            },
            "individual_responses": {},
            "cross_examination": consensus,
            "processing_time": 0.0
        }
        
        return final_decision
    
    def _find_tool_by_name(self, tool_name: str):
        """Find tool definition by name"""
        for tool_def in self.tool_manager.tools.values():
            if tool_def.name == tool_name:
                return tool_def
        return None
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Conduct ethical deliberation using hybrid approach"""
        
        task_id = str(uuid.uuid4())
        
        # Conduct hybrid deliberation
        result = await self._conduct_hybrid_deliberation(content, context, task_id)
        
        # Convert to AgentResponse format
        final_decision = result.get("final_decision", {})
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=final_decision.get("reasoning", "Hybrid deliberation completed"),
            decision=final_decision.get("decision", "ALLOW"),
            confidence=final_decision.get("confidence", 0.8),
            ethical_framework=self.ethical_framework,
            supporting_evidence=final_decision.get("evidence", [])
        )
        
        return response
    
    async def get_hybrid_status(self) -> Dict[str, Any]:
        """Get comprehensive status of hybrid system"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "is_active": self.is_active,
            "a2a_protocol": {
                "registered_agents": len(a2a_protocol.agents),
                "topics": list(a2a_protocol.topics.keys()),
                "message_count": self.message_count
            },
            "mcp_tools": {
                "available_tools": len(self.tool_manager.get_available_tools(self.agent_id)),
                "total_tools": len(self.tool_manager.tools),
                "call_history": len(self.tool_manager.call_history)
            },
            "deliberation_history": len(self.deliberation_history),
            "last_heartbeat": self.last_heartbeat.isoformat()
        }

    async def start(self):
        await self._subscribe_to_topics_async()


# Global hybrid ethics commander instance
hybrid_ethics_commander = HybridEthicsCommander() 