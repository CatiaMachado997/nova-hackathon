"""
Main FastAPI Application for EthIQ Ethical Deliberation System
Provides REST API endpoints for content moderation and agent management
"""

import asyncio
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from contextlib import asynccontextmanager
import uuid

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

# Global variables
ethics_commander: Optional[EthicsCommander] = None
audit_logger: Optional[AuditLogger] = None

# Initialize agents
def initialize_agents():
    """Initialize all agents"""
    global ethics_commander, audit_logger
    
    # Initialize specialist agents
    utilitarian_agent = UtilitarianAgent()
    deontological_agent = DeontologicalAgent()
    cultural_context_agent = CulturalContextAgent()
    free_speech_agent = FreeSpeechAgent()
    
    # Initialize master agent
    ethics_commander = EthicsCommander()
    
    # Initialize supporting systems
    audit_logger = AuditLogger()
    
    return {
        "ethics_commander": ethics_commander,
        "utilitarian_agent": utilitarian_agent,
        "deontological_agent": deontological_agent,
        "cultural_context_agent": cultural_context_agent,
        "free_speech_agent": free_speech_agent,
        "audit_logger": audit_logger
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
        if not ethics_commander:
            raise HTTPException(status_code=500, detail="Ethics commander not initialized")
        
        deliberation_result = await ethics_commander.deliberate(request.content, request.dict())
        
        deliberation_time = time.time() - start_time
        logging.info(f"Deliberation completed in {deliberation_time:.2f}s. Decision: {deliberation_result.decision}")
        
        # Create cross-examination result
        cross_examination = CrossExaminationResult(
            conflicts=[],
            agreements=[],
            questions=[],
            clarifications=[]
        )
        
        # Convert specialist_opinions (list) to dict for individual_contributions
        individual_contributions = {}
        if hasattr(deliberation_result, 'supporting_evidence') and isinstance(deliberation_result.supporting_evidence, list):
            for item in deliberation_result.supporting_evidence:
                if isinstance(item, dict) and 'agent' in item:
                    agent_name = str(item.get('agent', ''))
                    if agent_name in ['utilitarian', 'deontological', 'cultural_context', 'free_speech']:
                        individual_contributions[agent_name] = {
                            'framework': str(item.get('framework', 'Unknown')),
                            'decision': str(item.get('decision', 'UNKNOWN')),
                            'confidence': float(item.get('confidence', 0.0)),
                            'reasoning': str(item.get('reasoning', '')),
                            'supporting_evidence': item.get('supporting_evidence', [])
                        }
        # Pass this dict to ConsensusResult
        
        # If no individual contributions found, create default ones
        if not individual_contributions:
            individual_contributions = {
                "utilitarian": {
                    'framework': 'Utilitarianism',
                    'decision': deliberation_result.decision,
                    'confidence': deliberation_result.confidence,
                    'reasoning': deliberation_result.reasoning
                },
                "deontological": {
                    'framework': 'Deontological Ethics',
                    'decision': deliberation_result.decision,
                    'confidence': deliberation_result.confidence,
                    'reasoning': deliberation_result.reasoning
                },
                "cultural_context": {
                    'framework': 'Cultural Context Ethics',
                    'decision': deliberation_result.decision,
                    'confidence': deliberation_result.confidence,
                    'reasoning': deliberation_result.reasoning
                },
                "free_speech": {
                    'framework': 'Free Speech Ethics',
                    'decision': deliberation_result.decision,
                    'confidence': deliberation_result.confidence,
                    'reasoning': deliberation_result.reasoning
                }
            }
        
        consensus = ConsensusResult(
            decision=deliberation_result.decision,
            confidence=deliberation_result.confidence,
            reasoning=deliberation_result.reasoning,
            evidence=deliberation_result.supporting_evidence,
            individual_contributions=individual_contributions,
            cross_examination_results=cross_examination
        )
        
        # Create deliberation summary
        deliberation_summary = DeliberationSummary(
            agents_consulted=4,  # We have 4 specialist agents
            consensus_reached=True,
            conflicts_resolved=0,
            deliberation_quality="high"
        )
        
        # Create individual responses (simplified for now)
        individual_responses = {
            "utilitarian": AgentResponse(
                agent_name="UtilitarianAgent",
                ethical_framework="Utilitarianism",
                decision=deliberation_result.decision,
                confidence=deliberation_result.confidence,
                reasoning=deliberation_result.reasoning,
                supporting_evidence=deliberation_result.supporting_evidence
            ),
            "deontological": AgentResponse(
                agent_name="DeontologicalAgent",
                ethical_framework="Deontological Ethics",
                decision=deliberation_result.decision,
                confidence=deliberation_result.confidence,
                reasoning=deliberation_result.reasoning,
                supporting_evidence=deliberation_result.supporting_evidence
            ),
            "cultural_context": AgentResponse(
                agent_name="CulturalContextAgent",
                ethical_framework="Cultural Context Ethics",
                decision=deliberation_result.decision,
                confidence=deliberation_result.confidence,
                reasoning=deliberation_result.reasoning,
                supporting_evidence=deliberation_result.supporting_evidence
            ),
            "free_speech": AgentResponse(
                agent_name="FreeSpeechAgent",
                ethical_framework="Free Speech Ethics",
                decision=deliberation_result.decision,
                confidence=deliberation_result.confidence,
                reasoning=deliberation_result.reasoning,
                supporting_evidence=deliberation_result.supporting_evidence
            )
        }
        
        # Create response
        response = ContentModerationResponse(
            task_id=str(uuid.uuid4()),
            final_decision=deliberation_result.decision,
            confidence=deliberation_result.confidence,
            reasoning=deliberation_result.reasoning,
            evidence=deliberation_result.supporting_evidence,
            deliberation_summary=deliberation_summary,
            individual_responses=individual_responses,
            cross_examination=cross_examination,
            consensus=consensus,
            processing_time=deliberation_time
        )
        
        # Log to audit system
        if audit_logger:
            background_tasks.add_task(audit_logger.log_deliberation, {
                "deliberation_data": {
                    "task_id": response.task_id,
                    "content_preview": request.content[:100] + "..." if len(request.content) > 100 else request.content,
                    "final_decision": response.final_decision,
                    "individual_responses": response.individual_responses,
                    "cross_examination": response.cross_examination,
                    "consensus": response.consensus
                },
                "duration": deliberation_time
            })
        
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
        timestamp=datetime.now(),
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
        version="2.0.0",
        uptime=0.0,
        agents_healthy=5,
        total_agents=5,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
