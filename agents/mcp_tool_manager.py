"""
MCP (Model Context Protocol) Style Tool Manager for EthIQ
Provides standardized tool calling and resource management for ethical deliberation agents
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable, Union, Type
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import inspect
import uuid
from functools import wraps

logger = logging.getLogger(__name__)


class ToolPermission(Enum):
    """Tool permission levels"""
    READ_ONLY = "read_only"
    WRITE = "write"
    ADMIN = "admin"
    SYSTEM = "system"


class ToolCategory(Enum):
    """Tool categories for organization"""
    ETHICAL_ANALYSIS = "ethical_analysis"
    CONTENT_MODERATION = "content_moderation"
    DATA_ACCESS = "data_access"
    COMMUNICATION = "communication"
    UTILITY = "utility"
    INTEGRATION = "integration"


@dataclass
class ToolParameter:
    """Tool parameter definition"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum_values: Optional[List[str]] = None


@dataclass
class ToolDefinition:
    """Tool definition for MCP-style tool calling"""
    name: str
    description: str
    category: ToolCategory
    parameters: List[ToolParameter] = field(default_factory=list)
    returns: str = "Any"
    permissions: List[ToolPermission] = field(default_factory=lambda: [ToolPermission.READ_ONLY])
    agent_access: List[str] = field(default_factory=list)  # Empty list means all agents
    is_async: bool = False
    tool_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ToolCall:
    """Tool call request"""
    tool_id: str
    agent_id: str
    parameters: Dict[str, Any]
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1


@dataclass
class ToolResult:
    """Tool call result"""
    call_id: str
    tool_id: str
    agent_id: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class MCPToolManager:
    """MCP-style tool manager for agent tool calling"""
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.tool_functions: Dict[str, Callable] = {}
        self.agent_permissions: Dict[str, List[ToolPermission]] = {}
        self.call_history: List[ToolCall] = []
        self.result_history: List[ToolResult] = []
        self.logger = logging.getLogger(__name__)
        
        # Register built-in tools
        self._register_builtin_tools()
    
    def register_tool(self, tool_def: ToolDefinition, tool_function: Callable) -> bool:
        """Register a tool with the MCP tool manager"""
        try:
            # Validate tool function
            if not callable(tool_function):
                raise ValueError("Tool function must be callable")
            
            # Store tool definition and function
            self.tools[tool_def.tool_id] = tool_def
            self.tool_functions[tool_def.tool_id] = tool_function
            
            self.logger.info(f"Registered tool: {tool_def.name} ({tool_def.tool_id})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register tool {tool_def.name}: {e}")
            return False
    
    def unregister_tool(self, tool_id: str) -> bool:
        """Unregister a tool from the MCP tool manager"""
        try:
            if tool_id in self.tools:
                tool_name = self.tools[tool_id].name
                del self.tools[tool_id]
                del self.tool_functions[tool_id]
                self.logger.info(f"Unregistered tool: {tool_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unregister tool {tool_id}: {e}")
            return False
    
    def register_agent_permissions(self, agent_id: str, permissions: List[ToolPermission]) -> bool:
        """Register permissions for an agent"""
        try:
            self.agent_permissions[agent_id] = permissions
            self.logger.info(f"Registered permissions for agent {agent_id}: {[p.value for p in permissions]}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register permissions for agent {agent_id}: {e}")
            return False
    
    async def call_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call"""
        start_time = datetime.now()
        
        try:
            # Validate tool exists
            if tool_call.tool_id not in self.tools:
                return ToolResult(
                    call_id=tool_call.call_id,
                    tool_id=tool_call.tool_id,
                    agent_id=tool_call.agent_id,
                    success=False,
                    result=None,
                    error=f"Tool {tool_call.tool_id} not found"
                )
            
            tool_def = self.tools[tool_call.tool_id]
            tool_function = self.tool_functions[tool_call.tool_id]
            
            # Check agent permissions
            if not self._check_agent_permissions(tool_call.agent_id, tool_def):
                return ToolResult(
                    call_id=tool_call.call_id,
                    tool_id=tool_call.tool_id,
                    agent_id=tool_call.agent_id,
                    success=False,
                    result=None,
                    error=f"Agent {tool_call.agent_id} lacks permission for tool {tool_def.name}"
                )
            
            # Validate parameters
            validation_error = self._validate_parameters(tool_def, tool_call.parameters)
            if validation_error:
                return ToolResult(
                    call_id=tool_call.call_id,
                    tool_id=tool_call.tool_id,
                    agent_id=tool_call.agent_id,
                    success=False,
                    result=None,
                    error=validation_error
                )
            
            # Execute tool
            if tool_def.is_async:
                result = await tool_function(**tool_call.parameters)
            else:
                result = tool_function(**tool_call.parameters)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Create successful result
            tool_result = ToolResult(
                call_id=tool_call.call_id,
                tool_id=tool_call.tool_id,
                agent_id=tool_call.agent_id,
                success=True,
                result=result,
                execution_time=execution_time
            )
            
            # Log call and result
            self.call_history.append(tool_call)
            self.result_history.append(tool_result)
            
            self.logger.info(f"Tool call successful: {tool_def.name} by {tool_call.agent_id} in {execution_time:.3f}s")
            return tool_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            tool_result = ToolResult(
                call_id=tool_call.call_id,
                tool_id=tool_call.tool_id,
                agent_id=tool_call.agent_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
            
            self.call_history.append(tool_call)
            self.result_history.append(tool_result)
            
            self.logger.error(f"Tool call failed: {tool_call.tool_id} by {tool_call.agent_id}: {e}")
            return tool_result
    
    def get_available_tools(self, agent_id: str) -> List[ToolDefinition]:
        """Get list of available tools for an agent"""
        available_tools = []
        
        for tool_def in self.tools.values():
            if self._check_agent_permissions(agent_id, tool_def):
                available_tools.append(tool_def)
        
        return available_tools
    
    def get_tool_definition(self, tool_id: str) -> Optional[ToolDefinition]:
        """Get tool definition by ID"""
        return self.tools.get(tool_id)
    
    def get_call_history(self, agent_id: Optional[str] = None, limit: int = 100) -> List[ToolCall]:
        """Get tool call history"""
        history = self.call_history
        if agent_id:
            history = [call for call in history if call.agent_id == agent_id]
        return history[-limit:]
    
    def get_result_history(self, agent_id: Optional[str] = None, limit: int = 100) -> List[ToolResult]:
        """Get tool result history"""
        history = self.result_history
        if agent_id:
            history = [result for result in history if result.agent_id == agent_id]
        return history[-limit:]
    
    def _check_agent_permissions(self, agent_id: str, tool_def: ToolDefinition) -> bool:
        """Check if agent has permission to use tool"""
        # If no specific agent access is defined, allow all agents
        if not tool_def.agent_access:
            return True
        
        # Check if agent is in allowed list
        if agent_id not in tool_def.agent_access:
            return False
        
        # Check permission levels
        agent_perms = self.agent_permissions.get(agent_id, [])
        for required_perm in tool_def.permissions:
            if required_perm not in agent_perms:
                return False
        
        return True
    
    def _validate_parameters(self, tool_def: ToolDefinition, parameters: Dict[str, Any]) -> Optional[str]:
        """Validate tool parameters"""
        for param in tool_def.parameters:
            if param.required and param.name not in parameters:
                return f"Required parameter '{param.name}' missing"
            
            if param.name in parameters:
                value = parameters[param.name]
                
                # Type validation
                if param.type == "string" and not isinstance(value, str):
                    return f"Parameter '{param.name}' must be a string"
                elif param.type == "integer" and not isinstance(value, int):
                    return f"Parameter '{param.name}' must be an integer"
                elif param.type == "boolean" and not isinstance(value, bool):
                    return f"Parameter '{param.name}' must be a boolean"
                
                # Enum validation
                if param.enum_values and value not in param.enum_values:
                    return f"Parameter '{param.name}' must be one of: {param.enum_values}"
        
        return None
    
    def _register_builtin_tools(self):
        """Register built-in tools for ethical deliberation"""
        
        # Content Analysis Tools
        content_analysis_tool = ToolDefinition(
            name="analyze_content_sentiment",
            description="Analyze content sentiment and emotional impact",
            category=ToolCategory.ETHICAL_ANALYSIS,
            parameters=[
                ToolParameter("content", "string", "Content to analyze", True),
                ToolParameter("context", "string", "Context information", False, "general")
            ],
            returns="Dict[str, Any]",
            permissions=[ToolPermission.READ_ONLY]
        )
        
        self.register_tool(content_analysis_tool, self._analyze_content_sentiment)
        
        # Cultural Context Tool
        cultural_context_tool = ToolDefinition(
            name="check_cultural_sensitivity",
            description="Check content for cultural sensitivity issues",
            category=ToolCategory.ETHICAL_ANALYSIS,
            parameters=[
                ToolParameter("content", "string", "Content to check", True),
                ToolParameter("target_cultures", "string", "Target cultures", False, "global")
            ],
            returns="Dict[str, Any]",
            permissions=[ToolPermission.READ_ONLY]
        )
        
        self.register_tool(cultural_context_tool, self._check_cultural_sensitivity)
        
        # Harm Assessment Tool
        harm_assessment_tool = ToolDefinition(
            name="assess_potential_harm",
            description="Assess potential harm from content",
            category=ToolCategory.ETHICAL_ANALYSIS,
            parameters=[
                ToolParameter("content", "string", "Content to assess", True),
                ToolParameter("audience_type", "string", "Type of audience", False, "general"),
                ToolParameter("vulnerable_groups", "string", "Vulnerable groups present", False, "none")
            ],
            returns="Dict[str, Any]",
            permissions=[ToolPermission.READ_ONLY]
        )
        
        self.register_tool(harm_assessment_tool, self._assess_potential_harm)
        
        # Communication Tools
        broadcast_tool = ToolDefinition(
            name="broadcast_to_agents",
            description="Broadcast message to all agents",
            category=ToolCategory.COMMUNICATION,
            parameters=[
                ToolParameter("message", "string", "Message to broadcast", True),
                ToolParameter("message_type", "string", "Type of message", False, "info")
            ],
            returns="bool",
            permissions=[ToolPermission.WRITE]
        )
        
        self.register_tool(broadcast_tool, self._broadcast_to_agents)
        
        # Data Access Tools
        get_audit_logs_tool = ToolDefinition(
            name="get_audit_logs",
            description="Get audit logs for analysis",
            category=ToolCategory.DATA_ACCESS,
            parameters=[
                ToolParameter("time_range", "string", "Time range for logs", False, "24h"),
                ToolParameter("agent_id", "string", "Filter by agent ID", False, "")
            ],
            returns="List[Dict[str, Any]]",
            permissions=[ToolPermission.READ_ONLY]
        )
        
        self.register_tool(get_audit_logs_tool, self._get_audit_logs)
    
    # Built-in tool implementations
    def _analyze_content_sentiment(self, content: str, context: str = "general") -> Dict[str, Any]:
        """Analyze content sentiment and emotional impact"""
        # Mock implementation - in real system, this would use NLP libraries
        sentiment_score = 0.0
        emotional_impact = "neutral"
        
        # Simple keyword-based analysis
        negative_words = ["hate", "kill", "hurt", "pain", "sad", "angry", "violent"]
        positive_words = ["love", "help", "happy", "joy", "peace", "kind", "good"]
        
        content_lower = content.lower()
        negative_count = sum(1 for word in negative_words if word in content_lower)
        positive_count = sum(1 for word in positive_words if word in content_lower)
        
        if negative_count > positive_count:
            sentiment_score = -0.5
            emotional_impact = "negative"
        elif positive_count > negative_count:
            sentiment_score = 0.5
            emotional_impact = "positive"
        
        return {
            "sentiment_score": sentiment_score,
            "emotional_impact": emotional_impact,
            "negative_keywords": negative_count,
            "positive_keywords": positive_count,
            "content_length": len(content),
            "context": context
        }
    
    def _check_cultural_sensitivity(self, content: str, target_cultures: str = "global") -> Dict[str, Any]:
        """Check content for cultural sensitivity issues"""
        # Mock implementation
        sensitivity_issues = []
        risk_level = "low"
        
        # Simple keyword checking
        sensitive_words = ["stereotype", "offensive", "inappropriate", "discriminatory"]
        content_lower = content.lower()
        
        for word in sensitive_words:
            if word in content_lower:
                sensitivity_issues.append(f"Contains potentially {word} language")
        
        if len(sensitivity_issues) > 2:
            risk_level = "high"
        elif len(sensitivity_issues) > 0:
            risk_level = "medium"
        
        return {
            "sensitivity_issues": sensitivity_issues,
            "risk_level": risk_level,
            "target_cultures": target_cultures,
            "recommendations": ["Review content for cultural appropriateness"] if sensitivity_issues else []
        }
    
    def _assess_potential_harm(self, content: str, audience_type: str = "general", vulnerable_groups: str = "none") -> Dict[str, Any]:
        """Assess potential harm from content"""
        # Mock implementation
        harm_indicators = []
        risk_level = "low"
        
        # Check for harmful content patterns
        harmful_patterns = ["self-harm", "violence", "harassment", "bullying"]
        content_lower = content.lower()
        
        for pattern in harmful_patterns:
            if pattern in content_lower:
                harm_indicators.append(f"Contains {pattern} content")
        
        if vulnerable_groups != "none":
            risk_level = "medium" if len(harm_indicators) > 0 else "low"
        
        if len(harm_indicators) > 2:
            risk_level = "high"
        
        return {
            "harm_indicators": harm_indicators,
            "risk_level": risk_level,
            "audience_type": audience_type,
            "vulnerable_groups": vulnerable_groups,
            "recommendations": ["Consider content warnings", "Review for vulnerable audiences"] if harm_indicators else []
        }
    
    def _broadcast_to_agents(self, message: str, message_type: str = "info") -> bool:
        """Broadcast message to all agents"""
        # This would integrate with the A2A protocol
        logger.info(f"Broadcasting {message_type} message: {message}")
        return True
    
    def _get_audit_logs(self, time_range: str = "24h", agent_id: str = "") -> List[Dict[str, Any]]:
        """Get audit logs for analysis"""
        # Mock implementation - would integrate with actual audit system
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id or "system",
                "action": "tool_call",
                "details": f"Retrieved logs for {time_range}"
            }
        ]


# Decorator for easy tool registration
def mcp_tool(tool_def: ToolDefinition):
    """Decorator to register a function as an MCP tool"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Register the tool with the global manager
        global_tool_manager.register_tool(tool_def, func)
        return wrapper
    return decorator


# Global MCP tool manager instance
global_tool_manager = MCPToolManager() 