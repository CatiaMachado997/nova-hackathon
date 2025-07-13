"""
Temporal Agent for EthIQ Ethical Deliberation System
Detects misleading use of old content and temporal context issues
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class TemporalAgent(BaseAgent):
    """
    Temporal Agent: Analyzes content for temporal context and flags misleading use of old information
    Detects outdated content, historical misrepresentation, and temporal manipulation
    """
    
    def __init__(self):
        super().__init__(
            name="TemporalAgent",
            description="Detects misleading use of old content and temporal context issues",
            ethical_framework="Temporal Ethics and Historical Accuracy"
        )
        
        # Temporal analysis patterns
        self.temporal_indicators = {
            "date_patterns": [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY
                r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',
                r'\b(?:yesterday|today|tomorrow|last week|next week|last month|next month|last year|next year)\b'
            ],
            "time_indicators": [
                r'\b(?:years?|months?|weeks?|days?|hours?|minutes?)\s+(?:ago|before|later|after)\b',
                r'\b(?:in\s+)?\d+\s+(?:years?|months?|weeks?|days?)\b',
                r'\b(?:recently|lately|previously|formerly|historically|traditionally)\b'
            ],
            "context_indicators": [
                r'\b(?:breaking|latest|new|update|developing|just in)\b',
                r'\b(?:old|outdated|archived|historical|past|former)\b',
                r'\b(?:current|present|now|today|modern|contemporary)\b'
            ]
        }
        
        # Misleading patterns
        self.misleading_patterns = [
            r'\b(?:always|never|forever|permanent|unchanged|same)\b',
            r'\b(?:outdated|old|archived|historical)\s+(?:but|however|still|yet)\b',
            r'\b(?:breaking|latest|new)\s+(?:news|update|information)\b.*\b(?:old|past|historical)\b'
        ]
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Analyze content for temporal context and misleading use of old information"""
        
        logger.info(f"TemporalAgent analyzing content for temporal context")
        
        # Extract temporal information
        temporal_analysis = await self._analyze_temporal_context(content, context)
        
        # Detect misleading patterns
        misleading_flags = await self._detect_misleading_patterns(content, temporal_analysis)
        
        # Assess temporal risk
        risk_assessment = await self._assess_temporal_risk(content, temporal_analysis, misleading_flags)
        
        # Generate decision
        decision, confidence, reasoning = await self._generate_temporal_decision(
            content, temporal_analysis, misleading_flags, risk_assessment
        )
        
        response = AgentResponse(
            agent_name=self.name,
            ethical_framework=self.ethical_framework,
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            supporting_evidence=[
                f"Temporal indicators found: {len(temporal_analysis['indicators'])}",
                f"Misleading patterns detected: {len(misleading_flags)}",
                f"Temporal risk level: {risk_assessment['risk_level']}",
                f"Content age indicators: {temporal_analysis['age_indicators']}",
                f"Context relevance: {temporal_analysis['context_relevance']}"
            ],
            timestamp=datetime.now()
        )
        
        self.response_history.append(response)
        return response
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process a temporal analysis task"""
        
        content = task.get("content", "")
        context = task.get("context", {})
        
        return await self.deliberate(content, context)
    
    async def _analyze_temporal_context(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal context of the content"""
        
        analysis = {
            "indicators": [],
            "dates_found": [],
            "age_indicators": [],
            "context_relevance": "unknown",
            "temporal_manipulation_risk": 0.0
        }
        
        # Find date patterns
        for pattern in self.temporal_indicators["date_patterns"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis["dates_found"].extend(matches)
        
        # Find time indicators
        for pattern in self.temporal_indicators["time_indicators"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis["age_indicators"].extend(matches)
        
        # Find context indicators
        for pattern in self.temporal_indicators["context_indicators"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis["indicators"].extend(matches)
        
        # Assess context relevance
        current_indicators = len([i for i in analysis["indicators"] if i.lower() in ["current", "present", "now", "today", "modern", "contemporary"]])
        old_indicators = len([i for i in analysis["indicators"] if i.lower() in ["old", "outdated", "archived", "historical", "past", "former"]])
        
        if current_indicators > old_indicators:
            analysis["context_relevance"] = "current"
        elif old_indicators > current_indicators:
            analysis["context_relevance"] = "historical"
        else:
            analysis["context_relevance"] = "mixed"
        
        return analysis
    
    async def _detect_misleading_patterns(self, content: str, temporal_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect patterns that might indicate misleading use of old content"""
        
        flags = []
        
        # Check for misleading patterns
        for pattern in self.misleading_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                flags.append({
                    "pattern": pattern,
                    "match": match,
                    "severity": "medium",
                    "description": f"Potential misleading temporal pattern: {match}"
                })
        
        # Check for contradiction between "breaking" and old content
        if re.search(r'\b(?:breaking|latest|new)\b', content, re.IGNORECASE) and temporal_analysis["context_relevance"] == "historical":
            flags.append({
                "pattern": "breaking_historical_contradiction",
                "match": "Breaking news with historical context",
                "severity": "high",
                "description": "Content claims to be 'breaking' but contains historical/old information"
            })
        
        # Check for outdated statistics or facts
        if temporal_analysis["dates_found"]:
            for date_str in temporal_analysis["dates_found"]:
                try:
                    # Try to parse the date
                    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    else:
                        continue
                    
                    # Check if date is more than 2 years old
                    if (datetime.now() - date_obj).days > 730:
                        flags.append({
                            "pattern": "outdated_information",
                            "match": date_str,
                            "severity": "medium",
                            "description": f"Content references information from {date_str} (may be outdated)"
                        })
                except:
                    continue
        
        return flags
    
    async def _assess_temporal_risk(self, content: str, temporal_analysis: Dict[str, Any], misleading_flags: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the overall temporal risk of the content"""
        
        risk_score = 0.0
        risk_factors = []
        
        # Factor 1: Number of misleading patterns
        high_severity_flags = len([f for f in misleading_flags if f["severity"] == "high"])
        medium_severity_flags = len([f for f in misleading_flags if f["severity"] == "medium"])
        
        risk_score += high_severity_flags * 0.3
        risk_score += medium_severity_flags * 0.15
        
        if high_severity_flags > 0:
            risk_factors.append(f"{high_severity_flags} high-severity temporal issues")
        if medium_severity_flags > 0:
            risk_factors.append(f"{medium_severity_flags} medium-severity temporal issues")
        
        # Factor 2: Context relevance mismatch
        if temporal_analysis["context_relevance"] == "mixed":
            risk_score += 0.2
            risk_factors.append("Mixed temporal context indicators")
        
        # Factor 3: Outdated information
        outdated_count = len([f for f in misleading_flags if f["pattern"] == "outdated_information"])
        if outdated_count > 0:
            risk_score += min(outdated_count * 0.1, 0.3)
            risk_factors.append(f"{outdated_count} potentially outdated references")
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.4:
            risk_level = "medium"
        elif risk_score >= 0.2:
            risk_level = "low"
        else:
            risk_level = "minimal"
        
        return {
            "risk_score": min(risk_score, 1.0),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "temporal_analysis": temporal_analysis,
            "misleading_flags": misleading_flags
        }
    
    async def _generate_temporal_decision(self, content: str, temporal_analysis: Dict[str, Any], 
                                        misleading_flags: List[Dict[str, Any]], risk_assessment: Dict[str, Any]) -> tuple:
        """Generate decision based on temporal analysis"""
        
        risk_level = risk_assessment["risk_level"]
        risk_score = risk_assessment["risk_score"]
        
        if risk_level == "high":
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.85
            reasoning = f"High temporal risk detected ({risk_score:.2f}). Content may be using old information in misleading ways. Multiple temporal issues identified: {', '.join(risk_assessment['risk_factors'])}"
        
        elif risk_level == "medium":
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.7
            reasoning = f"Medium temporal risk detected ({risk_score:.2f}). Some temporal context issues identified: {', '.join(risk_assessment['risk_factors'])}"
        
        elif risk_level == "low":
            decision = "ALLOW"
            confidence = 0.8
            reasoning = f"Low temporal risk detected ({risk_score:.2f}). Minor temporal context issues but not significantly misleading: {', '.join(risk_assessment['risk_factors'])}"
        
        else:  # minimal
            decision = "ALLOW"
            confidence = 0.9
            reasoning = f"Minimal temporal risk detected ({risk_score:.2f}). Content appears to have appropriate temporal context."
        
        return decision, confidence, reasoning 