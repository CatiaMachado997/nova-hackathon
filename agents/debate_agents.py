"""
Debate Agents for AutoEthos Ethical Deliberation System
Each agent represents a different ethical framework for content moderation
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class UtilitarianAgent(BaseAgent):
    """
    Utilitarian Agent: Weighs harm vs. benefit
    Focuses on maximizing overall happiness and minimizing suffering
    """
    
    def __init__(self):
        super().__init__(
            name="UtilitarianAgent",
            description="Weighs potential harm against benefits to determine the greatest good for the greatest number",
            ethical_framework="Utilitarianism"
        )
        self.harm_indicators = [
            "violence", "hate speech", "harassment", "misinformation", 
            "discrimination", "bullying", "threats", "harmful content"
        ]
        self.benefit_indicators = [
            "education", "awareness", "discussion", "satire", "artistic expression",
            "political speech", "scientific information", "public interest"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context)
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content from a utilitarian perspective"""
        
        # Analyze potential harms
        harm_score = self._calculate_harm_score(content, context)
        
        # Analyze potential benefits
        benefit_score = self._calculate_benefit_score(content, context)
        
        # Calculate net utility
        net_utility = benefit_score - harm_score
        
        # Determine decision based on net utility
        if net_utility > 0.3:
            decision = "ALLOW"
            confidence = min(0.9, (net_utility + 0.5))
        elif net_utility > -0.2:
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.6
        else:
            decision = "REMOVE"
            confidence = min(0.9, abs(net_utility))
        
        reasoning = f"Utilitarian analysis: Net utility = {net_utility:.2f} "
        reasoning += f"(Benefits: {benefit_score:.2f}, Harms: {harm_score:.2f}). "
        reasoning += f"Decision: {decision} based on maximizing overall welfare."
        
        supporting_evidence = self._extract_evidence(content)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=reasoning,
            decision=decision,
            confidence=confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=supporting_evidence
        )
        
        self.response_history.append(response)
        return response
    
    def _calculate_harm_score(self, content: str, context: Dict[str, Any]) -> float:
        """Calculate potential harm score (0-1)"""
        score = 0.0
        content_lower = content.lower()
        
        # Check for harm indicators
        for indicator in self.harm_indicators:
            if indicator in content_lower:
                score += 0.2
        
        # Context factors
        audience_size = context.get("audience_size", 1)
        if audience_size > 10000:
            score *= 1.5
        
        vulnerable_audience = context.get("vulnerable_audience", False)
        if vulnerable_audience:
            score *= 1.3
        
        return min(1.0, score)
    
    def _calculate_benefit_score(self, content: str, context: Dict[str, Any]) -> float:
        """Calculate potential benefit score (0-1)"""
        score = 0.0
        content_lower = content.lower()
        
        # Check for benefit indicators
        for indicator in self.benefit_indicators:
            if indicator in content_lower:
                score += 0.15
        
        # Context factors
        educational_value = context.get("educational_value", False)
        if educational_value:
            score += 0.3
        
        public_interest = context.get("public_interest", False)
        if public_interest:
            score += 0.2
        
        return min(1.0, score)
    
    def _extract_evidence(self, content: str) -> List[str]:
        """Extract supporting evidence from content"""
        evidence = []
        content_lower = content.lower()
        
        for indicator in self.harm_indicators + self.benefit_indicators:
            if indicator in content_lower:
                evidence.append(f"Contains '{indicator}' indicators")
        
        return evidence


class DeontologicalAgent(BaseAgent):
    """
    Deontological Agent: Considers rule violations
    Focuses on duty, rights, and universal moral principles
    """
    
    def __init__(self):
        super().__init__(
            name="DeontologicalAgent",
            description="Evaluates content based on universal moral principles and rights",
            ethical_framework="Deontological Ethics"
        )
        self.moral_rules = {
            "respect_persons": "Treat people as ends, not means",
            "truth_telling": "Do not lie or deceive",
            "non_maleficence": "Do not cause harm",
            "autonomy": "Respect individual autonomy",
            "dignity": "Respect human dignity"
        }
        self.rights_violations = [
            "privacy_violation", "defamation", "harassment", "discrimination",
            "intimidation", "coercion", "exploitation"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context)
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content from a deontological perspective"""
        
        # Check for rule violations
        violations = self._check_moral_rules(content, context)
        
        # Count serious violations
        serious_violations = len([v for v in violations if v["severity"] == "high"])
        minor_violations = len([v for v in violations if v["severity"] == "low"])
        
        # Determine decision based on violations
        if serious_violations > 0:
            decision = "REMOVE"
            confidence = min(0.95, 0.7 + (serious_violations * 0.1))
        elif minor_violations > 2:
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.7
        else:
            decision = "ALLOW"
            confidence = 0.8
        
        reasoning = f"Deontological analysis: {serious_violations} serious violations, "
        reasoning += f"{minor_violations} minor violations. "
        reasoning += f"Decision: {decision} based on moral duty and rights."
        
        supporting_evidence = [v["description"] for v in violations]
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=reasoning,
            decision=decision,
            confidence=confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=supporting_evidence
        )
        
        self.response_history.append(response)
        return response
    
    def _check_moral_rules(self, content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check content against moral rules"""
        violations = []
        content_lower = content.lower()
        
        # Check for rights violations
        for violation in self.rights_violations:
            if violation.replace("_", " ") in content_lower:
                violations.append({
                    "rule": violation,
                    "severity": "high",
                    "description": f"Potential {violation.replace('_', ' ')}"
                })
        
        # Check for deception
        if any(word in content_lower for word in ["fake", "false", "misleading", "hoax"]):
            violations.append({
                "rule": "truth_telling",
                "severity": "medium",
                "description": "Potential deception or false information"
            })
        
        # Check for harm to dignity
        if any(word in content_lower for word in ["dehumanizing", "degrading", "humiliating"]):
            violations.append({
                "rule": "dignity",
                "severity": "high",
                "description": "Content may violate human dignity"
            })
        
        return violations


class CulturalContextAgent(BaseAgent):
    """
    Cultural Context Agent: Evaluates cultural sensitivity
    Considers cultural norms, values, and sensitivities
    """
    
    def __init__(self):
        super().__init__(
            name="CulturalContextAgent",
            description="Evaluates content sensitivity across different cultural contexts",
            ethical_framework="Cultural Ethics"
        )
        self.cultural_sensitivities = {
            "religious": ["blasphemy", "sacrilege", "religious_offense"],
            "ethnic": ["racial_stereotypes", "ethnic_slurs", "cultural_appropriation"],
            "gender": ["gender_stereotypes", "sexism", "misogyny", "misandry"],
            "national": ["national_stereotypes", "xenophobia", "patriotism"],
            "generational": ["age_stereotypes", "generational_conflict"]
        }
        self.cultural_benefits = [
            "cultural_education", "diversity_celebration", "cross_cultural_dialogue",
            "cultural_awareness", "inclusive_content"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context)
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content from a cultural sensitivity perspective"""
        
        # Get cultural context
        target_cultures = context.get("target_cultures", ["global"])
        audience_diversity = context.get("audience_diversity", "high")
        
        # Analyze cultural sensitivities
        sensitivity_score = self._calculate_sensitivity_score(content, target_cultures)
        
        # Analyze cultural benefits
        benefit_score = self._calculate_cultural_benefit_score(content)
        
        # Determine decision
        if sensitivity_score > 0.7:
            decision = "REMOVE"
            confidence = min(0.9, sensitivity_score + 0.1)
        elif sensitivity_score > 0.4:
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.7
        elif benefit_score > 0.5:
            decision = "ALLOW"
            confidence = 0.8
        else:
            decision = "ALLOW"
            confidence = 0.6
        
        reasoning = f"Cultural analysis: Sensitivity score = {sensitivity_score:.2f}, "
        reasoning += f"Cultural benefit score = {benefit_score:.2f}. "
        reasoning += f"Decision: {decision} considering cultural context."
        
        supporting_evidence = self._extract_cultural_evidence(content, target_cultures)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=reasoning,
            decision=decision,
            confidence=confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=supporting_evidence
        )
        
        self.response_history.append(response)
        return response
    
    def _calculate_sensitivity_score(self, content: str, target_cultures: List[str]) -> float:
        """Calculate cultural sensitivity score (0-1)"""
        score = 0.0
        content_lower = content.lower()
        
        for category, indicators in self.cultural_sensitivities.items():
            for indicator in indicators:
                if indicator.replace("_", " ") in content_lower:
                    score += 0.2
        
        # Adjust for global audience
        if "global" in target_cultures:
            score *= 1.2
        
        return min(1.0, score)
    
    def _calculate_cultural_benefit_score(self, content: str) -> float:
        """Calculate cultural benefit score (0-1)"""
        score = 0.0
        content_lower = content.lower()
        
        for benefit in self.cultural_benefits:
            if benefit.replace("_", " ") in content_lower:
                score += 0.25
        
        return min(1.0, score)
    
    def _extract_cultural_evidence(self, content: str, target_cultures: List[str]) -> List[str]:
        """Extract cultural evidence from content"""
        evidence = []
        content_lower = content.lower()
        
        for category, indicators in self.cultural_sensitivities.items():
            for indicator in indicators:
                if indicator.replace("_", " ") in content_lower:
                    evidence.append(f"Cultural sensitivity: {category} - {indicator}")
        
        for benefit in self.cultural_benefits:
            if benefit.replace("_", " ") in content_lower:
                evidence.append(f"Cultural benefit: {benefit}")
        
        return evidence


class FreeSpeechAgent(BaseAgent):
    """
    Free Speech Agent: Assesses freedom of expression
    Prioritizes open discourse and democratic values
    """
    
    def __init__(self):
        super().__init__(
            name="FreeSpeechAgent",
            description="Evaluates content based on freedom of expression and democratic discourse principles",
            ethical_framework="Free Speech Ethics"
        )
        self.speech_categories = {
            "political": ["political_speech", "government_criticism", "policy_discussion"],
            "artistic": ["artistic_expression", "creative_content", "satire", "parody"],
            "educational": ["educational_content", "scientific_discussion", "academic_debate"],
            "journalistic": ["news_reporting", "investigative_journalism", "public_interest"],
            "personal": ["personal_opinion", "individual_expression", "self_expression"]
        }
        self.speech_restrictions = [
            "incitement_to_violence", "true_threats", "fighting_words",
            "obscenity", "defamation", "commercial_speech"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        content = task.get("content", "")
        context = task.get("context", {})
        return await self.deliberate(content, context)
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content from a free speech perspective"""
        
        # Analyze speech value
        speech_value = self._calculate_speech_value(content, context)
        
        # Check for legitimate restrictions
        restrictions = self._check_speech_restrictions(content)
        
        # Determine decision
        if restrictions:
            decision = "REMOVE"
            confidence = 0.8
        elif speech_value > 0.7:
            decision = "ALLOW"
            confidence = 0.9
        elif speech_value > 0.4:
            decision = "ALLOW"
            confidence = 0.7
        else:
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.6
        
        reasoning = f"Free speech analysis: Speech value = {speech_value:.2f}, "
        reasoning += f"Restrictions found: {len(restrictions)}. "
        reasoning += f"Decision: {decision} prioritizing freedom of expression."
        
        supporting_evidence = self._extract_speech_evidence(content)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=reasoning,
            decision=decision,
            confidence=confidence,
            ethical_framework=self.ethical_framework,
            supporting_evidence=supporting_evidence
        )
        
        self.response_history.append(response)
        return response
    
    def _calculate_speech_value(self, content: str, context: Dict[str, Any]) -> float:
        """Calculate the value of speech for democratic discourse (0-1)"""
        score = 0.0
        content_lower = content.lower()
        
        for category, indicators in self.speech_categories.items():
            for indicator in indicators:
                if indicator.replace("_", " ") in content_lower:
                    score += 0.2
        
        # Context factors
        public_platform = context.get("public_platform", True)
        if public_platform:
            score *= 1.2
        
        democratic_value = context.get("democratic_value", False)
        if democratic_value:
            score += 0.3
        
        return min(1.0, score)
    
    def _check_speech_restrictions(self, content: str) -> List[str]:
        """Check for legitimate speech restrictions"""
        restrictions = []
        content_lower = content.lower()
        
        for restriction in self.speech_restrictions:
            if restriction.replace("_", " ") in content_lower:
                restrictions.append(restriction)
        
        return restrictions
    
    def _extract_speech_evidence(self, content: str) -> List[str]:
        """Extract speech-related evidence from content"""
        evidence = []
        content_lower = content.lower()
        
        for category, indicators in self.speech_categories.items():
            for indicator in indicators:
                if indicator.replace("_", " ") in content_lower:
                    evidence.append(f"Speech category: {category} - {indicator}")
        
        for restriction in self.speech_restrictions:
            if restriction.replace("_", " ") in content_lower:
                evidence.append(f"Speech restriction: {restriction}")
        
        return evidence 