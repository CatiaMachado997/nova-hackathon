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

from agents.ethics_commander import EthicsCommander
from agents.audit_logger import AuditLogger
from agents.agentos_integration import initialize_agentos_protocol, orchestrate_with_agentos, get_agentos_status
from agents.cloudera_integration import initialize_cloudera_integration, stream_to_cloudera, get_cloudera_metrics, get_cloudera_analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for agents
ethics_commander = None
audit_logger = None
start_time = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global ethics_commander, audit_logger, start_time
    
    # Startup
    logger.info("Starting EthIQ Ethical Deliberation System...")
    start_time = time.time()
    
    # Initialize agents
    ethics_commander = EthicsCommander()
    audit_logger = AuditLogger()
    
    # Initialize GenAI AgentOS Protocol integration
    logger.info("Initializing GenAI AgentOS Protocol integration...")
    agentos_initialized = await initialize_agentos_protocol({
        "ethics_commander": ethics_commander,
        "audit_logger": audit_logger
    })
    if agentos_initialized:
        logger.info("✅ GenAI AgentOS Protocol integration initialized")
    else:
        logger.warning("⚠️ GenAI AgentOS Protocol integration failed")
    
    # Initialize Cloudera integration
    logger.info("Initializing Cloudera integration...")
    cloudera_initialized = await initialize_cloudera_integration()
    if cloudera_initialized:
        logger.info("✅ Cloudera integration initialized")
    else:
        logger.warning("⚠️ Cloudera integration failed")
    
    logger.info("Agents initialized successfully")
    yield
    
    # Shutdown
    logger.info("Shutting down EthIQ system...")
    if ethics_commander:
        await ethics_commander.shutdown_all_agents()
    logger.info("System shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="EthIQ - Ethical Intelligence API",
    description="AI-powered ethical content moderation through multi-agent deliberation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the ethics commander
async def get_ethics_commander() -> EthicsCommander:
    if ethics_commander is None:
        raise HTTPException(status_code=503, detail="Ethics Commander not initialized")
    return ethics_commander


# Dependency to get the audit logger
async def get_audit_logger() -> AuditLogger:
    if audit_logger is None:
        raise HTTPException(status_code=503, detail="Audit Logger not initialized")
    return audit_logger


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with system information"""
    return {
        "name": "EthIQ - Ethical Intelligence",
        "description": "AI-powered ethical content moderation through multi-agent deliberation",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    global start_time
    
    uptime = time.time() - start_time if start_time else 0
    
    # Check agent health
    agents_healthy = 0
    total_agents = 0
    
    if ethics_commander:
        status = await ethics_commander.get_agent_status()
        total_agents = 1 + len(status.get("debate_agents", {}))
        agents_healthy = sum(1 for agent in status.get("debate_agents", {}).values() 
                           if agent.get("is_active", False))
        if status.get("commander", {}).get("is_active", False):
            agents_healthy += 1
    
    system_health = "healthy" if agents_healthy == total_agents and total_agents > 0 else "degraded"
    
    return HealthCheckResponse(
        status=system_health,
        version="1.0.0",
        uptime=uptime,
        agents_healthy=agents_healthy,
        total_agents=total_agents,
        timestamp=datetime.now()
    )


@app.post("/api/moderate", response_model=ContentModerationResponse)
async def moderate_content(
    request: ContentModerationRequest,
    background_tasks: BackgroundTasks,
    commander: EthicsCommander = Depends(get_ethics_commander),
    logger_agent: AuditLogger = Depends(get_audit_logger)
):
    """Submit content for ethical analysis and moderation"""
    
    start_time = time.time()
    
    try:
        # Prepare context for deliberation
        context = {
            "audience_size": request.audience_size,
            "vulnerable_audience": request.vulnerable_audience,
            "educational_value": request.educational_value,
            "public_interest": request.public_interest,
            "democratic_value": request.democratic_value,
            "target_cultures": request.target_cultures,
            "audience_diversity": request.audience_diversity,
            "platform": request.platform,
            "content_type": request.content_type,
            **request.context
        }
        
        # Conduct ethical deliberation
        logger.info(f"Starting ethical deliberation for content: {request.content[:100]}...")
        
        response = await commander.deliberate(request.content, context)
        
        processing_time = time.time() - start_time
        
        # Get deliberation history for detailed response
        deliberation_history = commander.get_deliberation_history()
        latest_deliberation = deliberation_history[-1] if deliberation_history else {}
        
        # Extract individual responses
        individual_responses = {}
        if "individual_responses" in latest_deliberation:
            for agent_name, agent_response in latest_deliberation["individual_responses"].items():
                individual_responses[agent_name] = AgentResponse(
                    agent_name=agent_response.agent_name,
                    ethical_framework=agent_response.ethical_framework,
                    decision=agent_response.decision,
                    confidence=agent_response.confidence,
                    reasoning=agent_response.reasoning,
                    supporting_evidence=agent_response.supporting_evidence,
                    timestamp=agent_response.timestamp
                )
        
        # Extract cross-examination results
        cross_examination = CrossExaminationResult(
            conflicts=latest_deliberation.get("cross_examination", {}).get("conflicts", []),
            agreements=latest_deliberation.get("cross_examination", {}).get("agreements", []),
            questions=latest_deliberation.get("cross_examination", {}).get("questions", []),
            clarifications=latest_deliberation.get("cross_examination", {}).get("clarifications", [])
        )
        
        # Extract consensus results
        consensus_data = latest_deliberation.get("consensus", {})
        consensus = ConsensusResult(
            decision=consensus_data.get("decision", response.decision),
            confidence=consensus_data.get("confidence", response.confidence),
            reasoning=consensus_data.get("reasoning", response.reasoning),
            evidence=consensus_data.get("evidence", response.supporting_evidence),
            individual_contributions=consensus_data.get("individual_contributions", {}),
            cross_examination_results=cross_examination
        )
        
        # Create deliberation summary
        deliberation_summary = DeliberationSummary(
            agents_consulted=len(individual_responses),
            consensus_reached=consensus_data.get("confidence", 0) > 0.6,
            conflicts_resolved=len(cross_examination.conflicts),
            deliberation_quality="high" if consensus_data.get("confidence", 0) > 0.8 else "medium"
        )
        
        # Create response
        moderation_response = ContentModerationResponse(
            task_id=latest_deliberation.get("task_id", "unknown"),
            final_decision=response.decision,
            confidence=response.confidence,
            reasoning=response.reasoning,
            evidence=response.supporting_evidence,
            deliberation_summary=deliberation_summary,
            individual_responses=individual_responses,
            cross_examination=cross_examination,
            consensus=consensus,
            processing_time=processing_time,
            timestamp=datetime.now()
        )
        
        # Log deliberation in background
        background_tasks.add_task(
            log_deliberation_background,
            logger_agent,
            latest_deliberation,
            processing_time
        )
        
        logger.info(f"Deliberation completed in {processing_time:.2f}s. Decision: {response.decision}")
        
        return moderation_response
        
    except Exception as e:
        logger.error(f"Error during moderation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Moderation failed: {str(e)}")


async def log_deliberation_background(
    audit_logger: AuditLogger,
    deliberation_data: Dict[str, Any],
    processing_time: float
):
    """Background task to log deliberation"""
    try:
        await audit_logger.log_deliberation({
            "type": "deliberation_log",
            "deliberation_data": deliberation_data,
            "duration": processing_time
        })
    except Exception as e:
        logger.error(f"Failed to log deliberation: {e}")


@app.get("/api/analysis/{task_id}", response_model=ContentModerationResponse)
async def get_analysis(task_id: str, commander: EthicsCommander = Depends(get_ethics_commander)):
    """Retrieve analysis results for a specific task"""
    
    deliberation_history = commander.get_deliberation_history()
    
    # Find the deliberation with matching task_id
    for deliberation in deliberation_history:
        if deliberation.get("task_id") == task_id:
            # Reconstruct response from deliberation history
            # This would be similar to the moderation endpoint logic
            return JSONResponse(content={"message": "Analysis found", "task_id": task_id})
    
    raise HTTPException(status_code=404, detail=f"Analysis not found for task {task_id}")


@app.get("/api/history", response_model=List[AuditLogEntry])
async def get_moderation_history(logger_agent: AuditLogger = Depends(get_audit_logger)):
    """Get moderation history"""
    
    audit_logs = logger_agent.audit_logs
    
    history = []
    for log in audit_logs:
        history.append(AuditLogEntry(
            task_id=log.get("task_id", "unknown"),
            timestamp=datetime.fromisoformat(log.get("timestamp", datetime.now().isoformat())),
            content_preview=log.get("content_preview", ""),
            final_decision=log.get("final_decision", {}).get("decision", "unknown"),
            agents_involved=log.get("metadata", {}).get("agents_involved", 0),
            deliberation_duration=log.get("metadata", {}).get("deliberation_duration", 0),
            platform=log.get("metadata", {}).get("platform", "EthIQ")
        ))
    
    return history


@app.get("/api/agents", response_model=SystemStatus)
async def get_agents_status(commander: EthicsCommander = Depends(get_ethics_commander)):
    """Get status of all agents"""
    
    status = await commander.get_agent_status()
    
    # Convert to response format
    commander_status = AgentStatus(
        name=status["commander"]["name"],
        description=status["commander"]["description"],
        ethical_framework=status["commander"]["ethical_framework"],
        is_active=status["commander"]["is_active"],
        queue_size=status["commander"]["queue_size"],
        response_count=status["commander"]["response_count"]
    )
    
    debate_agents = {}
    for name, agent_status in status["debate_agents"].items():
        debate_agents[name] = AgentStatus(
            name=agent_status["name"],
            description=agent_status["description"],
            ethical_framework=agent_status["ethical_framework"],
            is_active=agent_status["is_active"],
            queue_size=agent_status["queue_size"],
            response_count=agent_status["response_count"]
        )
    
    total_agents = 1 + len(debate_agents)
    active_agents = sum(1 for agent in debate_agents.values() if agent.is_active)
    if commander_status.is_active:
        active_agents += 1
    
    system_health = "healthy" if active_agents == total_agents else "degraded"
    
    return SystemStatus(
        commander=commander_status,
        debate_agents=debate_agents,
        total_agents=total_agents,
        active_agents=active_agents,
        system_health=system_health
    )


@app.post("/api/agents/configure")
async def configure_agents(
    configuration: Dict[str, Any],
    commander: EthicsCommander = Depends(get_ethics_commander)
):
    """Configure agent parameters"""
    
    # This would implement agent configuration logic
    # For now, return a simple response
    return {"message": "Agent configuration updated", "configuration": configuration}


@app.get("/api/agents/status")
async def get_agent_status(commander: EthicsCommander = Depends(get_ethics_commander)):
    """Check agent status"""
    
    status = await commander.get_agent_status()
    return {"status": "operational", "agents": status}


@app.get("/api/analytics/summary", response_model=MetricsData)
async def get_analytics_summary(logger_agent: AuditLogger = Depends(get_audit_logger)):
    """Get moderation statistics"""
    
    # Calculate metrics from audit logs
    total_decisions = len(logger_agent.audit_logs)
    
    decision_distribution = {"ALLOW": 0, "REMOVE": 0, "FLAG_FOR_REVIEW": 0}
    framework_usage = {}
    total_confidence = 0.0
    
    for log in logger_agent.audit_logs:
        decision = log.get("final_decision", {}).get("decision", "UNKNOWN")
        if decision in decision_distribution:
            decision_distribution[decision] += 1
        
        # Count framework usage
        responses = log.get("individual_responses", {})
        for response in responses.values():
            framework = response.get("ethical_framework", "Unknown")
            framework_usage[framework] = framework_usage.get(framework, 0) + 1
        
        # Calculate average confidence
        if "consensus" in log and "confidence" in log["consensus"]:
            total_confidence += log["consensus"]["confidence"]
    
    average_confidence = total_confidence / total_decisions if total_decisions > 0 else 0.0
    
    return MetricsData(
        total_decisions=total_decisions,
        decision_distribution=decision_distribution,
        average_confidence=average_confidence,
        agent_performance={},  # Would calculate from actual data
        deliberation_quality={},  # Would calculate from actual data
        framework_usage=framework_usage
    )


@app.get("/api/analytics/trends")
async def get_analytics_trends(logger_agent: AuditLogger = Depends(get_audit_logger)):
    """Get trend analysis"""
    
    # This would implement trend analysis
    # For now, return basic structure
    return {
        "trends": {
            "decision_trends": {},
            "confidence_trends": {},
            "agent_performance_trends": {}
        },
        "period": "last_30_days"
    }


@app.post("/api/analytics/export")
async def export_analytics(
    export_request: Dict[str, Any],
    logger_agent: AuditLogger = Depends(get_audit_logger)
):
    """Export analytics data"""
    
    # This would implement data export functionality
    return {
        "message": "Analytics export initiated",
        "export_id": "export_123",
        "format": export_request.get("format", "json"),
        "period": export_request.get("period", "all")
    }


@app.get("/api/integrations/agentos/status")
async def get_agentos_integration_status():
    """Get GenAI AgentOS Protocol integration status"""
    try:
        status = await get_agentos_status()
        return {
            "integration": "GenAI AgentOS Protocol",
            "status": "active" if status.get("total_agents", 0) > 0 else "inactive",
            "details": status
        }
    except Exception as e:
        logger.error(f"AgentOS status check failed: {e}")
        return {"integration": "GenAI AgentOS Protocol", "status": "error", "error": str(e)}


@app.get("/api/integrations/cloudera/status")
async def get_cloudera_integration_status():
    """Get Cloudera integration status"""
    try:
        metrics = await get_cloudera_metrics()
        return {
            "integration": "Cloudera",
            "status": "active" if metrics.get("cloudera_integration") else "inactive",
            "details": metrics
        }
    except Exception as e:
        logger.error(f"Cloudera status check failed: {e}")
        return {"integration": "Cloudera", "status": "error", "error": str(e)}


@app.get("/api/integrations/cloudera/analytics")
async def get_cloudera_analytics(time_range: str = "24h"):
    """Get Cloudera analytics data"""
    try:
        analytics = await get_cloudera_analytics(time_range)
        return {
            "integration": "Cloudera",
            "time_range": time_range,
            "data": analytics
        }
    except Exception as e:
        logger.error(f"Cloudera analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


@app.post("/api/moderate/agentos")
async def moderate_content_with_agentos(
    request: ContentModerationRequest,
    background_tasks: BackgroundTasks,
    commander: EthicsCommander = Depends(get_ethics_commander),
    logger_agent: AuditLogger = Depends(get_audit_logger)
):
    """Submit content for ethical analysis using GenAI AgentOS Protocol"""
    
    start_time = time.time()
    
    try:
        # Prepare context for deliberation
        context = {
            "audience_size": request.audience_size,
            "vulnerable_audience": request.vulnerable_audience,
            "educational_value": request.educational_value,
            "public_interest": request.public_interest,
            "democratic_value": request.democratic_value,
            "target_cultures": request.target_cultures,
            "audience_diversity": request.audience_diversity,
            "platform": request.platform,
            "content_type": request.content_type,
            **request.context
        }
        
        # Generate task ID
        task_id = f"agentos_{int(time.time() * 1000)}"
        
        # Conduct ethical deliberation using AgentOS Protocol
        logger.info(f"Starting AgentOS Protocol deliberation for content: {request.content[:100]}...")
        
        agentos_response = await orchestrate_with_agentos(task_id, request.content, context)
        
        # Extract mock values from agentos_response
        final_decision = agentos_response.get("final_decision", {}).get("decision", "ALLOW")
        confidence = agentos_response.get("final_decision", {}).get("confidence", 1.0)
        reasoning = agentos_response.get("final_decision", {}).get("reasoning", "Decision made via GenAI AgentOS Protocol.")
        evidence = agentos_response.get("final_decision", {}).get("evidence", ["GenAI AgentOS Protocol mock evidence"])
        deliberation_summary = agentos_response.get("deliberation_summary", None)
        individual_responses = agentos_response.get("individual_responses", {})
        cross_examination = agentos_response.get("cross_examination", None)
        consensus = agentos_response.get("consensus", None)
        processing_time = time.time() - start_time
        
        # Fallback to traditional if mock is empty
        if not final_decision or final_decision == {}:
            traditional_response = await commander.deliberate(request.content, context)
            final_decision = traditional_response.final_decision
            confidence = traditional_response.confidence
            reasoning = f"AgentOS Protocol fallback. {traditional_response.reasoning}"
            evidence = traditional_response.evidence
            deliberation_summary = traditional_response.deliberation_summary
            individual_responses = traditional_response.individual_responses
            cross_examination = traditional_response.cross_examination
            consensus = traditional_response.consensus
        
        # Stream to Cloudera
        background_tasks.add_task(
            stream_to_cloudera,
            "moderation_event",
            {
                "task_id": task_id,
                "content": request.content[:100] + "...",
                "final_decision": final_decision,
                "confidence": confidence,
                "processing_time": processing_time,
                "individual_responses": individual_responses,
                "context": context,
                "protocol_used": "GenAI AgentOS Protocol"
            }
        )
        
        # Log deliberation
        background_tasks.add_task(
            log_deliberation_background,
            logger_agent,
            {
                "task_id": task_id,
                "protocol": "GenAI AgentOS Protocol",
                "agentos_response": agentos_response,
                "processing_time": processing_time
            },
            processing_time
        )
        
        return ContentModerationResponse(
            task_id=task_id,
            final_decision=final_decision,
            confidence=confidence,
            reasoning=reasoning,
            evidence=evidence,
            deliberation_summary=deliberation_summary,
            individual_responses=individual_responses,
            cross_examination=cross_examination,
            consensus=consensus,
            processing_time=processing_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"AgentOS Protocol moderation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Moderation failed: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            details={"exception": str(exc)}
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
