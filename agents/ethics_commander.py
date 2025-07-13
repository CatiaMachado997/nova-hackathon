"""
Master Agent (Orchestrator) for EthIQ Ethical Deliberation System
Manages the 4 specialist agents and performs final synthesis & judgment
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse
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
        self.deliberation_history = []
    
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
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Conduct ethical deliberation on content"""
        task = {
            "content": content,
            "context": context
        }
        return await self.process_task(task)
    
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
        self.deliberation_history.append(deliberation_record)
        
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
        
        return {
            "final_decision": final_decision,
            "confidence": final_confidence,
            "reasoning": reasoning,
            "evidence": all_evidence,
            "specialist_opinions": specialist_opinions,
            "consensus_analysis": {
                "total_agents": total_agents,
                "consensus_decision": consensus_decision,
                "consensus_count": consensus_count,
                "decision_distribution": decision_counts,
                "average_confidence": avg_confidence
            }
        }
    
    def _generate_synthesis_reasoning(self, specialist_opinions: List[Dict], final_decision: str, 
                                    final_confidence: float, consensus_count: int, total_agents: int) -> str:
        """Generate comprehensive reasoning for the final decision"""
        
        reasoning = f"EthicsCommander synthesis complete. Final decision: {final_decision} with {final_confidence:.2f} confidence. "
        
        # Add consensus information
        if consensus_count == total_agents:
            reasoning += f"All {total_agents} specialist agents unanimously agree on {final_decision}. "
        elif consensus_count >= total_agents * 0.75:
            reasoning += f"Strong consensus reached: {consensus_count} out of {total_agents} agents recommend {final_decision}. "
        elif consensus_count >= total_agents * 0.5:
            reasoning += f"Majority consensus: {consensus_count} out of {total_agents} agents recommend {final_decision}. "
        else:
            reasoning += f"No clear consensus among agents. "
        
        # Add individual specialist perspectives
        reasoning += "Specialist perspectives: "
        for opinion in specialist_opinions:
            reasoning += f"{opinion['agent']} ({opinion['framework']}): {opinion['decision']} "
            reasoning += f"({opinion['confidence']:.2f}) - {opinion['reasoning'][:100]}... "
        
        # Add synthesis explanation
        reasoning += f"Final synthesis: The {final_decision} decision reflects a balanced consideration of "
        reasoning += "utilitarian consequences, deontological principles, cultural context, and free speech values. "
        
        if final_confidence >= 0.8:
            reasoning += "High confidence in this decision due to strong specialist agreement. "
        elif final_confidence >= 0.6:
            reasoning += "Moderate confidence with some specialist disagreement resolved through synthesis. "
        else:
            reasoning += "Lower confidence due to significant specialist disagreement - human review recommended. "
        
        return reasoning
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "commander": self.get_status(),
            "specialist_agents": {}
        }
        
        for agent_name, agent in self.specialist_agents.items():
            status["specialist_agents"][agent_name] = agent.get_status()
        
        return status
    
    async def shutdown(self):
        """Gracefully shutdown all agents"""
        logger.info(f"{self.name} shutting down all specialist agents")
        
        # Shutdown specialist agents
        for agent_name, agent in self.specialist_agents.items():
            await agent.shutdown()
        
        # Shutdown commander
        await super().shutdown()
        logger.info("All agents shut down") 