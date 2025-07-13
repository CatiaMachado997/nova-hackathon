"""
Main FastAPI Application for EthIQ Ethical Deliberation System
Provides REST API endpoints for content moderation and agent management
"""

import asyncio
import time
import logging
from typing import Dict, Any, List
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.schemas import (
    ContentModerationRequest,
    ContentModerationResponse,
    AgentResponse,
    CrossExaminationResult,
    ConsensusResult,
    DeliberationSummary,
    SystemStatus,
    AgentStatus,
    AuditLogEntry,
    MetricsData,
    ErrorResponse,
    HealthCheckResponse
)

from agents import (
    EthicsCommander,
    UtilitarianAgent,
    DeontologicalAgent,
    CulturalContextAgent,
    FreeSpeechAgent
)

from agents.audit_logger import AuditLogger
from agents.cloudera_integration import ClouderaIntegration

# Global variables
ethics_commander: EthicsCommander = None
audit_logger: AuditLogger = None
cloudera_integration: ClouderaIntegration = None

# Initialize agents
def initialize_agents():
    """Initialize all agents"""
    global ethics_commander, audit_logger, cloudera_integration
    
    # Initialize specialist agents
    utilitarian_agent = UtilitarianAgent()
    deontological_agent = DeontologicalAgent()
    cultural_context_agent = CulturalContextAgent()
    free_speech_agent = FreeSpeechAgent()
    
    # Initialize master agent
    ethics_commander = EthicsCommander()
    
    # Initialize supporting systems
    audit_logger = AuditLogger()
    cloudera_integration = ClouderaIntegration()
    
    return {
        "ethics_commander": ethics_commander,
        "utilitarian_agent": utilitarian_agent,
        "deontological_agent": deontological_agent,
        "cultural_context_agent": cultural_context_agent,
        "free_speech_agent": free_speech_agent,
        "audit_logger": audit_logger,
        "cloudera_integration": cloudera_integration
    }

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logging.info("Starting EthIQ Ethical Deliberation System...")
    initialize_agents()
    logging.info("Agents initialized successfully")
    yield
    # Shutdown
    logging.info("Shutting down EthIQ system...")
    if ethics_commander:
        await ethics_commander.shutdown()
    logging.info("System shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="EthIQ Ethical Deliberation API",
    description="Multi-agent ethical deliberation system for content moderation",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.post("/api/moderate", response_model=ContentModerationResponse)
async def moderate_content(request: ContentModerationRequest, background_tasks: BackgroundTasks):
    """Main content moderation endpoint"""
    try:
        start_time = time.time()
        
        logging.info(f"Starting ethical deliberation for content: {request.content[:50]}...")
        
        # Perform ethical deliberation
        deliberation_result = await ethics_commander.deliberate(request.content)
        
        deliberation_time = time.time() - start_time
        logging.info(f"Deliberation completed in {deliberation_time:.2f}s. Decision: {deliberation_result.decision}")
        
        # Extract synthesis data
        synthesis_data = deliberation_result.metadata.get("synthesis", {})
        
        # Create cross-examination result
        cross_examination = CrossExaminationResult(
            questions_asked=len(synthesis_data.get("cross_examination", [])),
            clarifications_requested=len([q for q in synthesis_data.get("cross_examination", []) if q.get("type") == "clarification"]),
            conflicts_resolved=len([q for q in synthesis_data.get("cross_examination", []) if q.get("type") == "conflict_resolution"])
        )
        
        # Create consensus result
        consensus_analysis = synthesis_data.get("consensus_analysis", {})
        consensus = ConsensusResult(
            decision=deliberation_result.decision,
            confidence=deliberation_result.confidence,
            reasoning=deliberation_result.reasoning,
            consensus_reached=consensus_analysis.get("consensus_count", 0) >= consensus_analysis.get("total_agents", 0) * 0.5,
            agreement_level=consensus_analysis.get("consensus_count", 0) / consensus_analysis.get("total_agents", 1)
        )
        
        # Create deliberation summary
        summary = DeliberationSummary(
            total_agents=4,  # Only the 4 specialist agents
            active_agents=4,
            deliberation_time=deliberation_time,
            cross_examination=cross_examination,
            consensus=consensus,
            individual_contributions=synthesis_data.get("individual_contributions", {})
        )
        
        # Create response
        response = ContentModerationResponse(
            task_id=deliberation_result.task_id,
            decision=deliberation_result.decision,
            confidence=deliberation_result.confidence,
            reasoning=deliberation_result.reasoning,
            summary=summary,
            metadata=deliberation_result.metadata
        )
        
        # Background tasks
        background_tasks.add_task(audit_logger.log_deliberation, deliberation_result)
        background_tasks.add_task(cloudera_integration.stream_event, "moderation", deliberation_result)
        
        return response
        
    except Exception as e:
        logging.error(f"Error during moderation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents", response_model=List[AgentStatus])
async def get_agents():
    """Get status of all agents"""
    agents = [
        AgentStatus(
            name="EthicsCommander",
            description="Master agent that orchestrates ethical deliberation among 4 specialist agents and performs final synthesis & judgment",
            ethical_framework="Multi-Framework Orchestration & Synthesis",
            is_active=True,
            queue_size=0,
            response_count=0
        ),
        AgentStatus(
            name="UtilitarianAgent",
            description="Agent applying utilitarian ethical reasoning (maximizing overall good).",
            ethical_framework="Utilitarianism",
            is_active=True,
            queue_size=0,
            response_count=0
        ),
        AgentStatus(
            name="DeontologicalAgent",
            description="Agent applying deontological (duty-based) ethical reasoning.",
            ethical_framework="Deontological Ethics",
            is_active=True,
            queue_size=0,
            response_count=0
        ),
        AgentStatus(
            name="CulturalContextAgent",
            description="Agent considering cultural context and norms in ethical reasoning.",
            ethical_framework="Cultural Context Ethics",
            is_active=True,
            queue_size=0,
            response_count=0
        ),
        AgentStatus(
            name="FreeSpeechAgent",
            description="Agent prioritizing free speech and expression in ethical reasoning.",
            ethical_framework="Free Speech Ethics",
            is_active=True,
            queue_size=0,
            response_count=0
        )
    ]
    return agents

@app.get("/api/analytics/summary", response_model=MetricsData)
async def get_analytics_summary():
    """Get analytics summary"""
    return MetricsData(
        timestamp=datetime.now().isoformat(),
        total_decisions=0,
        decision_distribution={"ALLOW": 0, "REMOVE": 0, "FLAG_FOR_REVIEW": 0},
        average_confidence=0.0,
        agent_performance={},
        deliberation_quality={},
        framework_usage={}
    )

@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="2.0.0",
        agents_active=5,
        system_uptime=0
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
