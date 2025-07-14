"""
API Schemas for EthIQ Ethical Deliberation System
Pydantic models for request/response validation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class ContentModerationRequest(BaseModel):
    """Request schema for content moderation"""
    
    content: str = Field(..., description="Content to be moderated", min_length=1, max_length=10000)
    content_type: str = Field(default="text", description="Type of content (text, video, image, etc.)")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for moderation")
    platform: str = Field(default="general", description="Platform where content will be posted")
    audience_size: int = Field(default=1000, description="Expected audience size", ge=1)
    vulnerable_audience: bool = Field(default=False, description="Whether audience includes vulnerable groups")
    educational_value: bool = Field(default=False, description="Whether content has educational value")
    public_interest: bool = Field(default=False, description="Whether content serves public interest")
    democratic_value: bool = Field(default=False, description="Whether content has democratic value")
    target_cultures: List[str] = Field(default=["global"], description="Target cultural contexts")
    audience_diversity: str = Field(default="high", description="Audience diversity level")
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['text', 'video', 'image', 'audio', 'mixed']
        if v not in allowed_types:
            raise ValueError(f'content_type must be one of {allowed_types}')
        return v
    
    @validator('audience_diversity')
    def validate_audience_diversity(cls, v):
        allowed_levels = ['low', 'medium', 'high']
        if v not in allowed_levels:
            raise ValueError(f'audience_diversity must be one of {allowed_levels}')
        return v


class AgentResponse(BaseModel):
    """Response from an individual ethical agent"""
    
    agent_name: str = Field(..., description="Name of the ethical agent")
    ethical_framework: str = Field(..., description="Ethical framework used")
    decision: str = Field(..., description="Decision made by the agent")
    confidence: float = Field(..., description="Confidence level (0-1)", ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Detailed reasoning for the decision")
    supporting_evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the decision was made")


class CrossExaminationResult(BaseModel):
    """Results from cross-examination phase"""
    
    conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Conflicts identified")
    agreements: List[Dict[str, Any]] = Field(default_factory=list, description="Agreements found")
    questions: List[Dict[str, Any]] = Field(default_factory=list, description="Questions for clarification")
    clarifications: List[Dict[str, Any]] = Field(default_factory=list, description="Clarifications provided")


class ConsensusResult(BaseModel):
    """Results from consensus building phase"""
    
    decision: str = Field(..., description="Consensus decision")
    confidence: float = Field(..., description="Consensus confidence level", ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Consensus reasoning")
    evidence: List[str] = Field(default_factory=list, description="All supporting evidence")
    individual_contributions: Dict[str, Dict[str, Any]] = Field(..., description="Individual agent contributions")
    cross_examination_results: CrossExaminationResult = Field(..., description="Cross-examination results")


class DeliberationSummary(BaseModel):
    """Summary of the deliberation process"""
    
    agents_consulted: int = Field(..., description="Number of agents consulted")
    consensus_reached: bool = Field(..., description="Whether consensus was reached")
    conflicts_resolved: int = Field(..., description="Number of conflicts resolved")
    deliberation_quality: str = Field(..., description="Quality of deliberation (high/medium/low)")


class ContentModerationResponse(BaseModel):
    """Response schema for content moderation"""
    
    task_id: str = Field(..., description="Unique task identifier")
    final_decision: str = Field(..., description="Final moderation decision")
    confidence: float = Field(..., description="Overall confidence level", ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Comprehensive reasoning for the decision")
    evidence: List[str] = Field(default_factory=list, description="All supporting evidence")
    deliberation_summary: DeliberationSummary = Field(..., description="Summary of deliberation process")
    individual_responses: Dict[str, AgentResponse] = Field(..., description="Individual agent responses")
    cross_examination: CrossExaminationResult = Field(..., description="Cross-examination results")
    consensus: ConsensusResult = Field(..., description="Consensus building results")
    processing_time: float = Field(..., description="Time taken for deliberation in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the decision was made")


class AgentStatus(BaseModel):
    """Status information for an agent"""
    
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    ethical_framework: str = Field(..., description="Ethical framework")
    is_active: bool = Field(..., description="Whether agent is active")
    queue_size: int = Field(..., description="Number of messages in queue")
    response_count: int = Field(..., description="Number of responses made")


class SystemStatus(BaseModel):
    """Overall system status"""
    
    commander: AgentStatus = Field(..., description="Ethics Commander status")
    debate_agents: Dict[str, AgentStatus] = Field(..., description="Debate agents status")
    total_agents: int = Field(..., description="Total number of agents")
    active_agents: int = Field(..., description="Number of active agents")
    system_health: str = Field(..., description="Overall system health")


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    
    task_id: str = Field(..., description="Task identifier")
    timestamp: datetime = Field(..., description="When the log was created")
    content_preview: str = Field(..., description="Preview of moderated content")
    final_decision: str = Field(..., description="Final decision made")
    agents_involved: int = Field(..., description="Number of agents involved")
    deliberation_duration: float = Field(..., description="Duration of deliberation")
    platform: str = Field(..., description="Platform used")


class MetricsData(BaseModel):
    """Metrics data for analytics"""
    
    timestamp: datetime = Field(default_factory=datetime.now, description="When metrics were collected")
    total_decisions: int = Field(..., description="Total number of decisions")
    decision_distribution: Dict[str, int] = Field(..., description="Distribution of decisions")
    average_confidence: float = Field(..., description="Average confidence level", ge=0.0, le=1.0)
    agent_performance: Dict[str, Dict[str, Any]] = Field(..., description="Performance metrics by agent")
    deliberation_quality: Dict[str, Any] = Field(..., description="Quality metrics")
    framework_usage: Dict[str, int] = Field(..., description="Usage of different frameworks")


class ErrorResponse(BaseModel):
    """Error response schema"""
    
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")


class HealthCheckResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="System status")
    version: str = Field(..., description="System version")
    uptime: float = Field(..., description="System uptime in seconds")
    agents_healthy: int = Field(..., description="Number of healthy agents")
    total_agents: int = Field(..., description="Total number of agents")
    timestamp: datetime = Field(default_factory=datetime.now, description="When health check was performed")


class BatchModerationRequest(BaseModel):
    """Batch request schema for content moderation"""
    requests: List[ContentModerationRequest] = Field(..., description="List of content moderation requests")

class BatchModerationResponse(BaseModel):
    """Batch response schema for content moderation"""
    results: List[ContentModerationResponse] = Field(..., description="List of content moderation responses")
