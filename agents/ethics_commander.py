"""
Master Agent (Orchestrator) for EthIQ Ethical Deliberation System
Manages the 4 specialist agents and performs final synthesis & judgment
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
from agents.base_agent import BaseAgent, AgentResponse
from .utilitarian_agent import UtilitarianAgent
from .deontological_agent import DeontologicalAgent
from .cultural_context_agent import CulturalContextAgent
from .free_speech_agent import FreeSpeechAgent

logger = logging.getLogger(__name__)


class EthicsCommander(BaseAgent):
    """
    Master Agent (Orchestrator): Manages the 4 specialist agents and performs final synthesis & judgment
    """
    
    def __init__(self):
        super().__init__(
            name="EthicsCommander",
            description="Master agent that orchestrates ethical deliberation among 4 specialist agents and performs final synthesis & judgment",
            ethical_framework="Multi-Framework Orchestration & Synthesis"
        )
        
        # Initialize the 4 specialist agents
        self.specialist_agents = {
            "utilitarian": UtilitarianAgent(),
            "deontological": DeontologicalAgent(),
            "cultural_context": CulturalContextAgent(),
            "free_speech": FreeSpeechAgent()
        }
        
        self.active_tasks = {}
        self.deliberation_history = {}
    
    async def initialize(self):
        """Initialize AgentOS connection and all specialist agents"""
        logger.info("EthicsCommander initializing AgentOS connection...")
        await self.initialize_agentos()
        
        # Initialize all specialist agents with AgentOS
        logger.info("Initializing specialist agents with AgentOS...")
        for agent_name, agent in self.specialist_agents.items():
            try:
                await agent.initialize()
                logger.info(f"✅ {agent_name} agent initialized with AgentOS")
            except Exception as e:
                logger.warning(f"⚠️ {agent_name} agent initialization failed: {e}")
        
        logger.info("EthicsCommander initialization complete")
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a moderation task by orchestrating the 4 specialist agents"""
        
        task_id = str(uuid.uuid4())
        content = task.get("content", "")
        context = task.get("context", {})
        
        logger.info(f"EthicsCommander starting deliberation for task {task_id}")
        
        # Start deliberation process
        deliberation_result = await self._conduct_deliberation(content, context, task_id)
        
        # Create final response
        response = AgentResponse(
            agent_name=self.name,
            reasoning=deliberation_result["reasoning"],
            decision=deliberation_result["final_decision"],
            confidence=deliberation_result["confidence"],
            ethical_framework=self.ethical_framework,
            supporting_evidence=deliberation_result["evidence"]
        )
        
        self.response_history.append(response)
        return response
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct ethical deliberation on content"""
        task_id = str(uuid.uuid4())
        
        # Conduct the full deliberation process
        deliberation_result = await self._conduct_deliberation(content, context, task_id)
        
        # Return the full deliberation result with individual_contributions
        return deliberation_result
    
    async def _conduct_deliberation(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Conduct the full ethical deliberation process with 4 specialist agents"""
        
        # Phase 1: Dispatch to Specialist Agents
        logger.info(f"Phase 1: Dispatching to 4 specialist agents for task {task_id}")
        specialist_responses = await self._get_specialist_analyses(content, context, task_id)
        
        # Phase 2: Synthesis & Judgment
        logger.info(f"Phase 2: Synthesis & judgment for task {task_id}")
        final_decision = await self._perform_synthesis_and_judgment(specialist_responses, task_id)
        
        # Log deliberation
        deliberation_record = {
            "task_id": task_id,
            "timestamp": datetime.now(),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "specialist_responses": specialist_responses,
            "final_decision": final_decision
        }
        self.deliberation_history[task_id] = deliberation_record
        
        return final_decision
    
    async def _get_specialist_analyses(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, AgentResponse]:
        """Get analyses from all 4 specialist agents in parallel"""
        
        tasks = []
        for agent_name, agent in self.specialist_agents.items():
            task = {
                "content": content,
                "context": context,
                "task_id": task_id
            }
            tasks.append((agent_name, agent.process_task(task)))
        
        # Execute all analyses concurrently
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        specialist_responses = {}
        for i, (agent_name, _) in enumerate(tasks):
            if isinstance(results[i], Exception):
                logger.error(f"Specialist agent {agent_name} failed: {results[i]}")
                # Create fallback response
                specialist_responses[agent_name] = AgentResponse(
                    agent_name=agent_name,
                    reasoning=f"Analysis failed: {str(results[i])}",
                    decision="FLAG_FOR_REVIEW",
                    confidence=0.3,
                    ethical_framework=self.specialist_agents[agent_name].ethical_framework,
                    supporting_evidence=["Analysis error occurred"]
                )
            else:
                specialist_responses[agent_name] = results[i]
        
        return specialist_responses
    
    async def _perform_synthesis_and_judgment(self, specialist_responses: Dict[str, AgentResponse], task_id: str) -> Dict[str, Any]:
        """Perform synthesis and judgment based on specialist responses"""
        
        # Analyze specialist responses
        decision_counts = {"ALLOW": 0, "FLAG_FOR_REVIEW": 0, "REMOVE": 0}
        total_confidence = 0.0
        specialist_opinions = []
        
        for agent_name, response in specialist_responses.items():
            decision_counts[response.decision] += 1
            total_confidence += response.confidence
            
            specialist_opinions.append({
                "agent": agent_name,
                "framework": response.ethical_framework,
                "decision": response.decision,
                "confidence": response.confidence,
                "reasoning": response.reasoning
            })
        
        # Determine consensus
        total_agents = len(specialist_responses)
        avg_confidence = total_confidence / total_agents if total_agents > 0 else 0.5
        
        # Find the most common decision
        consensus_decision = max(decision_counts.keys(), key=lambda k: decision_counts[k])
        consensus_count = decision_counts[consensus_decision]
        
        # Calculate final confidence based on consensus and average confidence
        if consensus_count == total_agents:
            # Unanimous agreement
            final_confidence = min(0.95, avg_confidence * 1.2)
        elif consensus_count >= total_agents * 0.75:
            # Strong majority (3 out of 4)
            final_confidence = min(0.9, avg_confidence * 1.1)
        elif consensus_count >= total_agents * 0.5:
            # Simple majority (2 out of 4)
            final_confidence = avg_confidence
        else:
            # No clear consensus
            final_confidence = max(0.4, avg_confidence * 0.8)
        
        # Apply final decision logic with confidence thresholds
        if final_confidence < 0.6:
            if consensus_decision == "ALLOW":
                final_decision = "FLAG_FOR_REVIEW"
            elif consensus_decision == "REMOVE":
                final_decision = "FLAG_FOR_REVIEW"
            else:
                final_decision = consensus_decision
        else:
            final_decision = consensus_decision
        
        # Generate comprehensive reasoning
        reasoning = self._generate_synthesis_reasoning(specialist_opinions, final_decision, final_confidence, consensus_count, total_agents)
        
        # Collect all evidence
        all_evidence = []
        for response in specialist_responses.values():
            all_evidence.extend(response.supporting_evidence)
        
        # Convert specialist_opinions list to individual_contributions dict
        individual_contributions = {}
        for opinion in specialist_opinions:
            individual_contributions[opinion["agent"]] = {
                "framework": opinion["framework"],
                "decision": opinion["decision"],
                "confidence": opinion["confidence"],
                "reasoning": opinion["reasoning"]
            }
        
        return {
            "final_decision": final_decision,
            "confidence": final_confidence,
            "reasoning": reasoning,
            "evidence": all_evidence,
            "specialist_opinions": specialist_opinions,
            "individual_contributions": individual_contributions,
            "consensus_analysis": {
                "consensus_decision": consensus_decision,
                "consensus_count": consensus_count,
                "total_agents": total_agents,
                "decision_distribution": decision_counts
            }
        }
    
    def _generate_synthesis_reasoning(self, specialist_opinions: List[Dict], final_decision: str, 
                                    final_confidence: float, consensus_count: int, total_agents: int) -> str:
        """Generate comprehensive synthesis reasoning"""
        
        reasoning_parts = []
        reasoning_parts.append(f"EthicsCommander synthesis complete. Final decision: {final_decision} with {final_confidence:.2f} confidence.")
        
        # Add consensus information
        if consensus_count == total_agents:
            reasoning_parts.append(f"All {total_agents} specialist agents unanimously agree on {final_decision}.")
        elif consensus_count >= total_agents * 0.75:
            reasoning_parts.append(f"Strong consensus reached: {consensus_count} out of {total_agents} agents recommend {final_decision}.")
        elif consensus_count >= total_agents * 0.5:
            reasoning_parts.append(f"Majority consensus reached: {consensus_count} out of {total_agents} agents recommend {final_decision}.")
        else:
            reasoning_parts.append(f"No clear consensus reached. {consensus_count} out of {total_agents} agents recommend {final_decision}.")
        
        # Add specialist perspectives
        reasoning_parts.append("Specialist perspectives:")
        for opinion in specialist_opinions:
            reasoning_parts.append(f"{opinion['agent']} ({opinion['framework']}): {opinion['decision']} ({opinion['confidence']:.2f}) - {opinion['reasoning']}")
        
        # Add final synthesis
        reasoning_parts.append(f"Final synthesis: The {final_decision} decision reflects a balanced consideration of utilitarian consequences, deontological principles, cultural context, and free speech values.")
        
        if final_confidence >= 0.8:
            reasoning_parts.append("High confidence in this decision due to strong specialist agreement.")
        elif final_confidence >= 0.6:
            reasoning_parts.append("Moderate confidence in this decision with some specialist disagreement.")
        else:
            reasoning_parts.append("Lower confidence in this decision due to significant specialist disagreement.")
        
        return " ".join(reasoning_parts)
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all agents"""
        status = {
            "commander": self.get_status(),
            "specialists": {}
        }
        
        for agent_name, agent in self.specialist_agents.items():
            status["specialists"][agent_name] = agent.get_status()
        
        return status
    
    async def shutdown(self):
        """Shutdown all agents gracefully"""
        logger.info("EthicsCommander shutting down all agents...")
        
        # Shutdown specialist agents
        for agent_name, agent in self.specialist_agents.items():
            try:
                await agent.shutdown()
                logger.info(f"✅ {agent_name} agent shutdown complete")
            except Exception as e:
                logger.warning(f"⚠️ {agent_name} agent shutdown failed: {e}")
        
        # Shutdown commander
        await super().shutdown()
        logger.info("EthicsCommander shutdown complete")
    
    def _create_error_response(self, error_message: str) -> AgentResponse:
        """Create an error response when analysis fails"""
        return AgentResponse(
            agent_name=self.name,
            ethical_framework=self.ethical_framework,
            decision="FLAG_FOR_REVIEW",
            confidence=0.3,
            reasoning=f"EthicsCommander analysis failed: {error_message}",
            supporting_evidence=["Analysis error occurred"],
            timestamp=datetime.now()
        )
    
    async def _analyze_locally(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Fallback local analysis when AgentOS is unavailable"""
        # This should not be called for EthicsCommander as it always delegates to specialists
        return self._create_error_response("EthicsCommander requires specialist agents for analysis") 