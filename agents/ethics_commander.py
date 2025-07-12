"""
Ethics Commander - Master Agent for EthIQ Ethical Deliberation System
Orchestrates the ethical debate among specialized agents
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse, AgentMessage
from .utilitarian_agent import UtilitarianAgent
from .deontological_agent import DeontologicalAgent
from .cultural_context_agent import CulturalContextAgent
from .free_speech_agent import FreeSpeechAgent
from .psychological_agent import PsychologicalAgent
from .religious_ethics_agent import ReligiousEthicsAgent
from .financial_impact_agent import FinancialImpactAgent

logger = logging.getLogger(__name__)


class EthicsCommander(BaseAgent):
    """
    Ethics Commander: Master agent that orchestrates ethical deliberation
    Coordinates multiple ethical specialists to reach consensus decisions
    """
    
    def __init__(self):
        super().__init__(
            name="EthicsCommander",
            description="Master agent that orchestrates ethical deliberation among specialized agents",
            ethical_framework="Multi-Framework Orchestration"
        )
        
        # Initialize debate agents
        self.debate_agents = {
            "utilitarian": UtilitarianAgent(),
            "deontological": DeontologicalAgent(),
            "cultural": CulturalContextAgent(),
            "free_speech": FreeSpeechAgent(),
            "psychological": PsychologicalAgent(),
            "religious_ethics": ReligiousEthicsAgent(),
            "financial_impact": FinancialImpactAgent()
        }
        
        self.active_tasks = {}
        self.deliberation_history = []
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a moderation task by orchestrating ethical deliberation"""
        
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
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Conduct ethical deliberation on content"""
        task = {
            "content": content,
            "context": context
        }
        return await self.process_task(task)
    
    async def _conduct_deliberation(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Conduct the full ethical deliberation process"""
        
        # Phase 1: Individual Analysis
        logger.info(f"Phase 1: Individual analysis for task {task_id}")
        individual_responses = await self._get_individual_analyses(content, context, task_id)
        
        # Phase 2: Cross-Examination
        logger.info(f"Phase 2: Cross-examination for task {task_id}")
        cross_examination = await self._conduct_cross_examination(individual_responses, task_id)
        
        # Phase 3: Consensus Building
        logger.info(f"Phase 3: Consensus building for task {task_id}")
        consensus = await self._build_consensus(individual_responses, cross_examination, task_id)
        
        # Phase 4: Final Decision
        logger.info(f"Phase 4: Final decision for task {task_id}")
        final_decision = await self._make_final_decision(consensus, task_id)
        
        # Log deliberation
        deliberation_record = {
            "task_id": task_id,
            "timestamp": datetime.now(),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "individual_responses": individual_responses,
            "cross_examination": cross_examination,
            "consensus": consensus,
            "final_decision": final_decision
        }
        self.deliberation_history.append(deliberation_record)
        
        return final_decision
    
    async def _get_individual_analyses(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, AgentResponse]:
        """Get individual analyses from all debate agents"""
        
        tasks = []
        for agent_name, agent in self.debate_agents.items():
            task = {
                "content": content,
                "context": context,
                "task_id": task_id
            }
            tasks.append((agent_name, agent.process_task(task)))
        
        # Execute all analyses concurrently
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        individual_responses = {}
        for i, (agent_name, _) in enumerate(tasks):
            if isinstance(results[i], Exception):
                logger.error(f"Agent {agent_name} failed: {results[i]}")
                # Create fallback response
                individual_responses[agent_name] = AgentResponse(
                    agent_name=agent_name,
                    reasoning=f"Analysis failed: {str(results[i])}",
                    decision="FLAG_FOR_REVIEW",
                    confidence=0.3,
                    ethical_framework=self.debate_agents[agent_name].ethical_framework,
                    supporting_evidence=["Analysis error occurred"]
                )
            else:
                individual_responses[agent_name] = results[i]
        
        return individual_responses
    
    async def _conduct_cross_examination(self, individual_responses: Dict[str, AgentResponse], task_id: str) -> Dict[str, Any]:
        """Conduct cross-examination among agents"""
        
        cross_examination = {
            "conflicts": [],
            "agreements": [],
            "questions": [],
            "clarifications": []
        }
        
        # Identify conflicts and agreements
        decisions = {name: resp.decision for name, resp in individual_responses.items()}
        confidences = {name: resp.confidence for name, resp in individual_responses.items()}
        
        # Find conflicts
        unique_decisions = set(decisions.values())
        if len(unique_decisions) > 1:
            cross_examination["conflicts"].append({
                "type": "decision_conflict",
                "decisions": decisions,
                "description": f"Agents disagree on final decision: {unique_decisions}"
            })
        
        # Find agreements
        if len(unique_decisions) == 1:
            cross_examination["agreements"].append({
                "type": "unanimous_decision",
                "decision": list(unique_decisions)[0],
                "description": "All agents agree on the decision"
            })
        
        # Generate questions for clarification
        for agent_name, response in individual_responses.items():
            if response.confidence < 0.7:
                cross_examination["questions"].append({
                    "agent": agent_name,
                    "question": f"Low confidence ({response.confidence:.2f}) - needs clarification",
                    "context": response.reasoning
                })
        
        return cross_examination
    
    async def _build_consensus(self, individual_responses: Dict[str, AgentResponse], 
                             cross_examination: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Build consensus from individual responses and cross-examination"""
        
        # Calculate weighted decision
        decision_scores = {"ALLOW": 0.0, "FLAG_FOR_REVIEW": 0.0, "REMOVE": 0.0}
        
        for agent_name, response in individual_responses.items():
            weight = response.confidence
            decision_scores[response.decision] += weight
        
        # Determine consensus decision
        consensus_decision = max(decision_scores.keys(), key=lambda k: decision_scores[k])
        total_weight = sum(decision_scores.values())
        consensus_confidence = decision_scores[consensus_decision] / total_weight if total_weight > 0 else 0.5
        
        # Build consensus reasoning
        consensus_reasoning = f"Consensus reached through weighted deliberation. "
        consensus_reasoning += f"Decision scores: {decision_scores}. "
        consensus_reasoning += f"Final decision: {consensus_decision} with {consensus_confidence:.2f} confidence."
        
        # Collect supporting evidence
        all_evidence = []
        for response in individual_responses.values():
            all_evidence.extend(response.supporting_evidence)
        
        consensus = {
            "decision": consensus_decision,
            "confidence": consensus_confidence,
            "reasoning": consensus_reasoning,
            "evidence": all_evidence,
            "individual_contributions": {
                name: {
                    "decision": resp.decision,
                    "confidence": resp.confidence,
                    "framework": resp.ethical_framework
                }
                for name, resp in individual_responses.items()
            },
            "cross_examination_results": cross_examination
        }
        
        return consensus
    
    async def _make_final_decision(self, consensus: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Make the final decision based on consensus"""
        
        # Apply final decision logic
        final_decision = consensus["decision"]
        final_confidence = consensus["confidence"]
        
        # Adjust decision based on confidence and conflicts
        if final_confidence < 0.6:
            if final_decision == "ALLOW":
                final_decision = "FLAG_FOR_REVIEW"
            elif final_decision == "REMOVE":
                final_decision = "FLAG_FOR_REVIEW"
        
        # Build final reasoning
        final_reasoning = f"EthicsCommander final decision: {final_decision}. "
        final_reasoning += f"Based on multi-agent deliberation with {final_confidence:.2f} confidence. "
        final_reasoning += consensus["reasoning"]
        
        return {
            "final_decision": final_decision,
            "confidence": final_confidence,
            "reasoning": final_reasoning,
            "evidence": consensus["evidence"],
            "deliberation_summary": {
                "agents_consulted": len(consensus["individual_contributions"]),
                "consensus_reached": final_confidence > 0.6,
                "conflicts_resolved": len(consensus["cross_examination_results"]["conflicts"]),
                "deliberation_quality": "high" if final_confidence > 0.8 else "medium"
            }
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "commander": self.get_status(),
            "debate_agents": {}
        }
        
        for name, agent in self.debate_agents.items():
            status["debate_agents"][name] = agent.get_status()
        
        return status
    
    async def shutdown_all_agents(self):
        """Shutdown all agents"""
        await self.shutdown()
        for agent in self.debate_agents.values():
            await agent.shutdown()
        logger.info("All agents shut down")
    
    def get_deliberation_history(self) -> List[Dict[str, Any]]:
        """Get deliberation history"""
        return self.deliberation_history 