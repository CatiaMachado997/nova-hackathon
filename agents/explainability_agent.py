"""
Explainability Agent for EthIQ Ethical Deliberation System
Provides clear, understandable justifications for moderation decisions
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class ExplainabilityAgent(BaseAgent):
    """
    Explainability Agent: Provides clear, understandable justifications for moderation decisions
    Translates complex ethical reasoning into user-friendly explanations
    """
    
    def __init__(self):
        super().__init__(
            name="ExplainabilityAgent",
            description="Provides clear justifications and explanations for moderation decisions",
            ethical_framework="Transparency and Explainability"
        )
        
        # Explanation templates for different decision types
        self.explanation_templates = {
            "ALLOW": {
                "user_friendly": "This content has been approved for publication. Our analysis found that it meets our community standards and ethical guidelines.",
                "moderator_detailed": "Content approved after multi-agent ethical deliberation. All agents reached consensus that the content does not violate ethical principles.",
                "technical": "Decision: ALLOW. Consensus reached across {agent_count} ethical frameworks with {confidence}% confidence."
            },
            "FLAG_FOR_REVIEW": {
                "user_friendly": "This content has been flagged for human review. Our system identified some concerns that require human judgment to evaluate properly.",
                "moderator_detailed": "Content flagged for human review due to conflicting agent opinions or borderline ethical considerations. Manual assessment recommended.",
                "technical": "Decision: FLAG_FOR_REVIEW. Agent consensus unclear ({confidence}% confidence). Human review required for final determination."
            },
            "REMOVE": {
                "user_friendly": "This content has been removed as it violates our community standards and ethical guidelines.",
                "moderator_detailed": "Content removed based on strong consensus across ethical frameworks. Multiple agents identified violations of community standards.",
                "technical": "Decision: REMOVE. Strong consensus ({confidence}% confidence) across {agent_count} agents for content removal."
            }
        }
        
        # Explanation components
        self.explanation_components = {
            "ethical_principles": [
                "harm_prevention",
                "autonomy_respect", 
                "fairness_equity",
                "transparency_truth",
                "community_wellbeing"
            ],
            "content_categories": [
                "hate_speech",
                "misinformation",
                "harassment",
                "violence",
                "privacy_violation",
                "copyright_infringement"
            ],
            "audience_considerations": [
                "vulnerable_groups",
                "age_appropriateness",
                "cultural_sensitivity",
                "educational_value"
            ]
        }
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Generate explanations for moderation decisions"""
        
        logger.info(f"ExplainabilityAgent generating explanations for content")
        
        # This agent doesn't make primary decisions, but provides explanations
        # It would typically be called after other agents have made decisions
        
        # For demo purposes, we'll generate a sample explanation
        explanation = await self._generate_explanation(content, context, "ALLOW", 0.85)
        
        response = AgentResponse(
            agent_name=self.name,
            ethical_framework=self.ethical_framework,
            decision="ALLOW",  # Default to ALLOW since this agent provides explanations
            confidence=0.9,
            reasoning="Generated clear, user-friendly explanation for moderation decision",
            supporting_evidence=[
                f"Explanation type: {explanation['type']}",
                f"User-friendly: {len(explanation['user_friendly'])} characters",
                f"Moderator detailed: {len(explanation['moderator_detailed'])} characters",
                f"Technical: {len(explanation['technical'])} characters"
            ],
            timestamp=datetime.now()
        )
        
        self.response_history.append(response)
        return response
    
    async def explain_decision(self, content: str, context: Dict[str, Any], 
                             decision: str, confidence: float, 
                             agent_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive explanation for a moderation decision"""
        
        logger.info(f"ExplainabilityAgent explaining decision: {decision}")
        
        # Generate different types of explanations
        explanation = await self._generate_explanation(content, context, decision, confidence)
        
        # Add agent-specific insights
        agent_insights = await self._generate_agent_insights(agent_responses)
        
        # Add contextual factors
        contextual_factors = await self._analyze_contextual_factors(context)
        
        # Add recommendations
        recommendations = await self._generate_recommendations(decision, confidence, context)
        
        return {
            "explanation": explanation,
            "agent_insights": agent_insights,
            "contextual_factors": contextual_factors,
            "recommendations": recommendations,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "explanation_version": "1.0",
                "content_length": len(content),
                "decision_confidence": confidence
            }
        }
    
    async def _generate_explanation(self, content: str, context: Dict[str, Any], 
                                  decision: str, confidence: float) -> Dict[str, str]:
        """Generate different types of explanations"""
        
        template = self.explanation_templates.get(decision, self.explanation_templates["ALLOW"])
        
        # Get agent count from context
        agent_count = len(context.get("agent_responses", {}))
        
        # Generate user-friendly explanation
        user_friendly = template["user_friendly"]
        if decision == "FLAG_FOR_REVIEW":
            user_friendly += f" Our system is {confidence*100:.0f}% confident that human review is needed."
        elif decision == "REMOVE":
            user_friendly += f" Our analysis found this content violates our community standards with {confidence*100:.0f}% confidence."
        
        # Generate moderator detailed explanation
        moderator_detailed = template["moderator_detailed"]
        if agent_count > 0:
            moderator_detailed += f" {agent_count} ethical agents participated in the deliberation process."
        
        # Generate technical explanation
        technical = template["technical"].format(
            agent_count=agent_count,
            confidence=confidence*100
        )
        
        return {
            "type": "comprehensive",
            "user_friendly": user_friendly,
            "moderator_detailed": moderator_detailed,
            "technical": technical
        }
    
    async def _generate_agent_insights(self, agent_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from individual agent responses"""
        
        insights = {
            "consensus_level": "unknown",
            "key_disagreements": [],
            "strongest_agreements": [],
            "agent_summary": {}
        }
        
        if not agent_responses:
            return insights
        
        # Analyze consensus
        decisions = [resp.get("decision", "UNKNOWN") for resp in agent_responses.values()]
        unique_decisions = set(decisions)
        
        if len(unique_decisions) == 1:
            insights["consensus_level"] = "strong"
        elif len(unique_decisions) == 2:
            insights["consensus_level"] = "moderate"
        else:
            insights["consensus_level"] = "weak"
        
        # Find disagreements
        decision_counts = {}
        for decision in decisions:
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        for decision, count in decision_counts.items():
            if count == 1:  # Only one agent made this decision
                insights["key_disagreements"].append(decision)
            elif count > len(agent_responses) * 0.7:  # 70%+ agreement
                insights["strongest_agreements"].append(decision)
        
        # Generate agent summary
        for agent_name, response in agent_responses.items():
            insights["agent_summary"][agent_name] = {
                "decision": response.get("decision", "UNKNOWN"),
                "confidence": response.get("confidence", 0.0),
                "framework": response.get("ethical_framework", "Unknown"),
                "key_reasoning": response.get("reasoning", "")[:100] + "..." if response.get("reasoning") else "No reasoning provided"
            }
        
        return insights
    
    async def _analyze_contextual_factors(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze contextual factors that influenced the decision"""
        
        factors = {
            "audience_considerations": [],
            "platform_specific": [],
            "content_type_factors": [],
            "temporal_factors": []
        }
        
        # Audience considerations
        if context.get("vulnerable_audience"):
            factors["audience_considerations"].append("Vulnerable audience identified - stricter standards applied")
        
        if context.get("audience_size", 0) > 10000:
            factors["audience_considerations"].append("Large audience - broader impact considered")
        
        # Platform considerations
        platform = context.get("platform", "unknown")
        if platform == "social_media":
            factors["platform_specific"].append("Social media platform - viral potential considered")
        elif platform == "educational":
            factors["platform_specific"].append("Educational platform - learning value prioritized")
        
        # Content type factors
        content_type = context.get("content_type", "unknown")
        if content_type == "video":
            factors["content_type_factors"].append("Video content - visual impact considered")
        elif content_type == "text":
            factors["content_type_factors"].append("Text content - linguistic analysis applied")
        
        # Educational value
        if context.get("educational_value"):
            factors["content_type_factors"].append("Educational value identified - may offset other concerns")
        
        # Public interest
        if context.get("public_interest"):
            factors["content_type_factors"].append("Public interest value - democratic considerations applied")
        
        return factors
    
    async def _generate_recommendations(self, decision: str, confidence: float, 
                                      context: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on the decision"""
        
        recommendations = []
        
        if decision == "ALLOW":
            if confidence < 0.8:
                recommendations.append("Consider monitoring this content for community feedback")
            recommendations.append("Content meets current community standards")
        
        elif decision == "FLAG_FOR_REVIEW":
            recommendations.append("Human moderator should review within 24 hours")
            recommendations.append("Consider consulting with subject matter experts if needed")
            if confidence > 0.7:
                recommendations.append("High confidence in flag - likely requires action")
            else:
                recommendations.append("Borderline case - careful consideration needed")
        
        elif decision == "REMOVE":
            recommendations.append("Content should be removed promptly")
            recommendations.append("Consider issuing warning to content creator")
            if confidence > 0.9:
                recommendations.append("High confidence removal - standard procedure")
            else:
                recommendations.append("Review removal reason with content creator")
        
        # Add general recommendations
        recommendations.append("Monitor for similar content patterns")
        recommendations.append("Update moderation guidelines if needed")
        
        return recommendations
    
    async def generate_user_notification(self, decision: str, explanation: Dict[str, Any]) -> str:
        """Generate user-friendly notification message"""
        
        base_message = explanation["user_friendly"]
        
        if decision == "ALLOW":
            return f"✅ {base_message}"
        elif decision == "FLAG_FOR_REVIEW":
            return f"⚠️ {base_message}"
        elif decision == "REMOVE":
            return f"❌ {base_message}"
        else:
            return f"ℹ️ {base_message}"
    
    async def generate_moderator_report(self, decision: str, explanation: Dict[str, Any], 
                                      agent_insights: Dict[str, Any]) -> str:
        """Generate detailed moderator report"""
        
        report = f"""
# Moderation Decision Report

## Decision: {decision.upper()}

## Summary
{explanation['moderator_detailed']}

## Technical Details
{explanation['technical']}

## Agent Consensus
- Consensus Level: {agent_insights['consensus_level']}
- Agents Participated: {len(agent_insights['agent_summary'])}
- Key Disagreements: {', '.join(agent_insights['key_disagreements']) if agent_insights['key_disagreements'] else 'None'}

## Agent Details
"""
        
        for agent_name, details in agent_insights["agent_summary"].items():
            report += f"""
### {agent_name}
- Decision: {details['decision']}
- Confidence: {details['confidence']:.2f}
- Framework: {details['framework']}
- Reasoning: {details['key_reasoning']}
"""
        
        return report.strip() 

    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process an explanation task"""
        
        content = task.get("content", "")
        context = task.get("context", {})
        
        return await self.deliberate(content, context) 