"""
Consensus Agent for EthIQ Ethical Deliberation System
Synthesizes multiple ethical perspectives into a final decision
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class ConsensusAgent(BaseAgent):
    """
    Consensus Agent: Synthesizes ethical perspectives into final decision
    Combines insights from all debate agents with weighted analysis
    """
    
    def __init__(self):
        super().__init__(
            name="ConsensusAgent",
            description="Synthesizes multiple ethical perspectives into a final decision with comprehensive justification",
            ethical_framework="Multi-Perspective Synthesis"
        )
        
        # Framework weights for different ethical perspectives
        self.framework_weights = {
            "Utilitarianism": 0.25,
            "Deontological Ethics": 0.25,
            "Cultural Ethics": 0.20,
            "Free Speech Ethics": 0.30
        }
        
        # Decision thresholds
        self.decision_thresholds = {
            "REMOVE": 0.7,
            "FLAG_FOR_REVIEW": 0.4,
            "ALLOW": 0.3
        }
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process task by synthesizing multiple ethical perspectives"""
        
        agent_responses = task.get("agent_responses", {})
        content = task.get("content", "")
        context = task.get("context", {})
        
        return await self.synthesize_perspectives(agent_responses, content, context)
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content (not used directly, requires agent responses)"""
        raise NotImplementedError("ConsensusAgent requires agent responses for deliberation")
    
    async def synthesize_perspectives(self, agent_responses: Dict[str, AgentResponse], 
                                    content: str, context: Dict[str, Any]) -> AgentResponse:
        """Synthesize multiple ethical perspectives into a final decision"""
        
        logger.info(f"ConsensusAgent synthesizing {len(agent_responses)} perspectives")
        
        # Analyze individual perspectives
        perspective_analysis = self._analyze_perspectives(agent_responses)
        
        # Calculate weighted consensus
        consensus_scores = self._calculate_consensus_scores(agent_responses)
        
        # Determine final decision
        final_decision = self._determine_final_decision(consensus_scores, perspective_analysis)
        
        # Generate comprehensive reasoning
        reasoning = self._generate_comprehensive_reasoning(
            agent_responses, consensus_scores, perspective_analysis, final_decision
        )
        
        # Collect all evidence
        all_evidence = self._collect_all_evidence(agent_responses, perspective_analysis)
        
        # Calculate final confidence
        final_confidence = self._calculate_final_confidence(consensus_scores, perspective_analysis)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=reasoning,
            decision=final_decision["decision"],
            confidence=final_confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=all_evidence
        )
        
        self.response_history.append(response)
        return response
    
    def _analyze_perspectives(self, agent_responses: Dict[str, AgentResponse]) -> Dict[str, Any]:
        """Analyze the different ethical perspectives"""
        
        analysis = {
            "perspectives": {},
            "agreements": [],
            "conflicts": [],
            "confidence_distribution": {},
            "framework_coverage": set()
        }
        
        decisions = {}
        confidences = {}
        
        for agent_name, response in agent_responses.items():
            # Store perspective details
            analysis["perspectives"][agent_name] = {
                "framework": response.ethical_framework,
                "decision": response.decision,
                "confidence": response.confidence,
                "reasoning": response.reasoning,
                "evidence": response.supporting_evidence
            }
            
            decisions[agent_name] = response.decision
            confidences[agent_name] = response.confidence
            analysis["framework_coverage"].add(response.ethical_framework)
        
        # Find agreements and conflicts
        unique_decisions = set(decisions.values())
        if len(unique_decisions) == 1:
            analysis["agreements"].append({
                "type": "unanimous",
                "decision": list(unique_decisions)[0],
                "agents": list(decisions.keys())
            })
        else:
            # Group by decision
            decision_groups = {}
            for agent, decision in decisions.items():
                if decision not in decision_groups:
                    decision_groups[decision] = []
                decision_groups[decision].append(agent)
            
            analysis["conflicts"].append({
                "type": "decision_conflict",
                "groups": decision_groups,
                "description": f"Agents disagree: {unique_decisions}"
            })
        
        # Analyze confidence distribution
        analysis["confidence_distribution"] = {
            "high": [name for name, conf in confidences.items() if conf > 0.8],
            "medium": [name for name, conf in confidences.items() if 0.5 <= conf <= 0.8],
            "low": [name for name, conf in confidences.items() if conf < 0.5]
        }
        
        return analysis
    
    def _calculate_consensus_scores(self, agent_responses: Dict[str, AgentResponse]) -> Dict[str, float]:
        """Calculate weighted consensus scores for each decision"""
        
        scores = {"ALLOW": 0.0, "FLAG_FOR_REVIEW": 0.0, "REMOVE": 0.0}
        
        for agent_name, response in agent_responses.items():
            # Get framework weight
            framework_weight = self.framework_weights.get(response.ethical_framework, 0.25)
            
            # Calculate weighted contribution
            contribution = response.confidence * framework_weight
            scores[response.decision] += contribution
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        return scores
    
    def _determine_final_decision(self, consensus_scores: Dict[str, float], 
                                perspective_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the final decision based on consensus scores and analysis"""
        
        # Find the highest scoring decision
        best_decision = max(consensus_scores.keys(), key=lambda k: consensus_scores[k])
        best_score = consensus_scores[best_decision]
        
        # Check if we have unanimous agreement
        has_unanimous = len(perspective_analysis["agreements"]) > 0
        
        # Determine confidence level
        if has_unanimous and best_score > 0.6:
            confidence_level = "high"
        elif best_score > 0.5:
            confidence_level = "medium"
        else:
            confidence_level = "low"
        
        # Apply decision logic
        if best_decision == "REMOVE" and best_score >= self.decision_thresholds["REMOVE"]:
            final_decision = "REMOVE"
        elif best_decision == "ALLOW" and best_score >= self.decision_thresholds["ALLOW"]:
            final_decision = "ALLOW"
        else:
            final_decision = "FLAG_FOR_REVIEW"
        
        return {
            "decision": final_decision,
            "consensus_score": best_score,
            "confidence_level": confidence_level,
            "has_unanimous_agreement": has_unanimous,
            "all_scores": consensus_scores
        }
    
    def _generate_comprehensive_reasoning(self, agent_responses: Dict[str, AgentResponse],
                                        consensus_scores: Dict[str, float],
                                        perspective_analysis: Dict[str, Any],
                                        final_decision: Dict[str, Any]) -> str:
        """Generate comprehensive reasoning for the final decision"""
        
        reasoning = f"ConsensusAgent synthesis complete. Final decision: {final_decision['decision']}. "
        reasoning += f"Consensus score: {final_decision['consensus_score']:.2f}. "
        
        # Add agreement/conflict information
        if final_decision["has_unanimous_agreement"]:
            agreement = perspective_analysis["agreements"][0]
            reasoning += f"All agents unanimously agree on {agreement['decision']}. "
        elif perspective_analysis["conflicts"]:
            reasoning += f"Agents have conflicting perspectives. "
        
        # Add framework coverage
        framework_count = len(perspective_analysis["framework_coverage"])
        reasoning += f"Analysis covered {framework_count} ethical frameworks: "
        reasoning += ", ".join(perspective_analysis["framework_coverage"]) + ". "
        
        # Add confidence distribution
        high_conf = len(perspective_analysis["confidence_distribution"]["high"])
        medium_conf = len(perspective_analysis["confidence_distribution"]["medium"])
        reasoning += f"Confidence levels: {high_conf} high, {medium_conf} medium. "
        
        # Add individual perspectives summary
        reasoning += "Individual perspectives: "
        for agent_name, response in agent_responses.items():
            reasoning += f"{agent_name} ({response.ethical_framework}): {response.decision} "
            reasoning += f"({response.confidence:.2f}), "
        
        reasoning = reasoning.rstrip(", ") + "."
        
        return reasoning
    
    def _collect_all_evidence(self, agent_responses: Dict[str, AgentResponse],
                            perspective_analysis: Dict[str, Any]) -> List[str]:
        """Collect all supporting evidence from all agents"""
        
        evidence = []
        
        # Add evidence from each agent
        for agent_name, response in agent_responses.items():
            for item in response.supporting_evidence:
                evidence.append(f"{agent_name}: {item}")
        
        # Add consensus evidence
        if perspective_analysis["agreements"]:
            evidence.append("Unanimous agreement among all agents")
        
        if perspective_analysis["conflicts"]:
            evidence.append("Conflicting perspectives identified and resolved")
        
        # Add framework coverage evidence
        frameworks = list(perspective_analysis["framework_coverage"])
        evidence.append(f"Multi-framework analysis: {', '.join(frameworks)}")
        
        return evidence
    
    def _calculate_final_confidence(self, consensus_scores: Dict[str, float],
                                  perspective_analysis: Dict[str, Any]) -> float:
        """Calculate final confidence score"""
        
        # Base confidence from consensus score
        best_score = max(consensus_scores.values())
        base_confidence = best_score
        
        # Adjust for agreement/conflict
        if perspective_analysis["agreements"]:
            base_confidence *= 1.2  # Boost for agreement
        elif perspective_analysis["conflicts"]:
            base_confidence *= 0.8  # Reduce for conflicts
        
        # Adjust for confidence distribution
        high_conf_count = len(perspective_analysis["confidence_distribution"]["high"])
        total_agents = len(perspective_analysis["perspectives"])
        
        if high_conf_count / total_agents > 0.7:
            base_confidence *= 1.1  # Boost for high confidence agents
        elif high_conf_count / total_agents < 0.3:
            base_confidence *= 0.9  # Reduce for low confidence agents
        
        # Ensure confidence is within bounds
        return max(0.1, min(0.95, base_confidence))
    
    def get_synthesis_summary(self) -> Dict[str, Any]:
        """Get summary of synthesis capabilities"""
        return {
            "agent_name": self.name,
            "frameworks_supported": list(self.framework_weights.keys()),
            "framework_weights": self.framework_weights,
            "decision_thresholds": self.decision_thresholds,
            "synthesis_count": len(self.response_history)
        } 