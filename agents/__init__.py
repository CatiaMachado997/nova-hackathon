"""
EthIQ - The Ethical Arbiter
Multi-agent system for ethical content moderation deliberation
"""

from .base_agent import BaseAgent, LLMEthicsAgent
from .ethics_commander import EthicsCommander
from .utilitarian_agent import UtilitarianAgent
from .deontological_agent import DeontologicalAgent
from .cultural_context_agent import CulturalContextAgent
from .free_speech_agent import FreeSpeechAgent
from .psychological_agent import PsychologicalAgent
from .religious_ethics_agent import ReligiousEthicsAgent
from .financial_impact_agent import FinancialImpactAgent
from .consensus_agent import ConsensusAgent
from .audit_logger import AuditLogger

# A2A Protocol and MCP Tool Manager
from .a2a_protocol import A2AProtocol, A2AAgent, A2AMessage, MessageType, MessagePriority, a2a_protocol
from .mcp_tool_manager import MCPToolManager, ToolCall, ToolResult, ToolDefinition, ToolPermission, global_tool_manager
from .hybrid_ethics_commander import HybridEthicsCommander, hybrid_ethics_commander

__all__ = [
    'BaseAgent',
    'LLMEthicsAgent',
    'EthicsCommander',
    'UtilitarianAgent',
    'DeontologicalAgent',
    'CulturalContextAgent',
    'FreeSpeechAgent',
    'PsychologicalAgent',
    'ReligiousEthicsAgent',
    'FinancialImpactAgent',
    'ConsensusAgent',
    'AuditLogger',
    # A2A Protocol
    'A2AProtocol',
    'A2AAgent',
    'A2AMessage',
    'MessageType',
    'MessagePriority',
    'a2a_protocol',
    # MCP Tool Manager
    'MCPToolManager',
    'ToolCall',
    'ToolResult',
    'ToolDefinition',
    'ToolPermission',
    'global_tool_manager',
    # Hybrid System
    'HybridEthicsCommander',
    'hybrid_ethics_commander'
]
