#!/usr/bin/env python3
"""
UtilitarianAgent for GenAI AgentOS Protocol
Ethical reasoning agent that applies utilitarian principles (maximizing overall good)
"""

import asyncio
import os
import json
import logging
from typing import Any, Annotated, Dict, List
from datetime import datetime
from dotenv import load_dotenv

# Import the real GenAI AgentOS session
try:
    from genai_session.session import GenAISession
except ImportError:
    # Fallback to mock if not available
    class GenAISession:
        def __init__(self, jwt_token=""):
            self.jwt_token = jwt_token
            self.logger = logging.getLogger(__name__)
        
        def bind(self, name, description):
            def decorator(func):
                return func
            return decorator
        
        async def process_events(self):
            self.logger.info("Mock GenAISession processing events")

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GenAI AgentOS session
session = GenAISession(jwt_token=os.environ.get("AGENTOS_JWT_TOKEN", ""))

class UtilitarianReasoning:
    """Utilitarian ethical reasoning logic"""
    
    def __init__(self):
        self.ethical_framework = "Utilitarianism"
        self.principles = [
            "Maximize overall happiness and well-being",
            "Minimize suffering and harm",
            "Consider consequences for all affected parties",
            "Evaluate long-term vs short-term benefits"
        ]
    
    def analyze_content(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content from a utilitarian perspective"""
        
        # Extract key information from content and context
        content_lower = content.lower()
        context_type = context.get("type", "general")
        platform = context.get("platform", "unknown")
        vulnerable_audience = context.get("vulnerable_audience", False)
        
        # Utilitarian analysis patterns
        harmful_keywords = [
            "kill", "suicide", "harm", "hurt", "dangerous", "toxic",
            "hate", "violence", "threat", "abuse", "bully"
        ]
        
        beneficial_keywords = [
            "help", "support", "educate", "inform", "positive", "constructive",
            "benefit", "improve", "heal", "inspire", "empower"
        ]
        
        # Count harmful vs beneficial indicators
        harmful_count = sum(1 for word in harmful_keywords if word in content_lower)
        beneficial_count = sum(1 for word in beneficial_keywords if word in content_lower)
        
        # Calculate utility score (-1 to 1, where 1 is maximum utility)
        total_indicators = harmful_count + beneficial_count
        if total_indicators == 0:
            utility_score = 0.0
        else:
            utility_score = (beneficial_count - harmful_count) / total_indicators
        
        # Determine decision based on utility
        if utility_score > 0.3:
            decision = "ALLOW"
            confidence = min(0.9, 0.7 + utility_score * 0.2)
        elif utility_score < -0.3:
            decision = "REMOVE"
            confidence = min(0.9, 0.7 + abs(utility_score) * 0.2)
        else:
            decision = "FLAG_FOR_REVIEW"
            confidence = 0.6
        
        # Adjust for vulnerable audience
        if vulnerable_audience and harmful_count > 0:
            decision = "REMOVE"
            confidence = min(0.95, confidence + 0.1)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(content, utility_score, harmful_count, beneficial_count, context)
        
        return {
            "decision": decision,
            "confidence": confidence,
            "utility_score": utility_score,
            "harmful_indicators": harmful_count,
            "beneficial_indicators": beneficial_count,
            "reasoning": reasoning,
            "ethical_framework": self.ethical_framework,
            "principles_applied": self.principles
        }
    
    def _generate_reasoning(self, content: str, utility_score: float, harmful_count: int, beneficial_count: int, context: Dict[str, Any]) -> str:
        """Generate detailed utilitarian reasoning"""
        
        if utility_score > 0.5:
            return f"Utilitarian analysis shows strong positive utility (score: {utility_score:.2f}). Content contains {beneficial_count} beneficial indicators and {harmful_count} harmful indicators. The overall benefit to society outweighs potential harms, supporting ALLOW decision."
        
        elif utility_score < -0.5:
            return f"Utilitarian analysis shows strong negative utility (score: {utility_score:.2f}). Content contains {harmful_count} harmful indicators and {beneficial_count} beneficial indicators. The potential harm to society outweighs benefits, requiring REMOVE decision."
        
        else:
            return f"Utilitarian analysis shows neutral utility (score: {utility_score:.2f}). Content contains {beneficial_count} beneficial and {harmful_count} harmful indicators. Requires human review to assess nuanced consequences."

# Initialize utilitarian reasoning engine
utilitarian_engine = UtilitarianReasoning()

@session.bind(
    name="analyze_content_utilitarian", 
    description="Analyze content from a utilitarian ethical perspective, considering overall happiness and well-being"
)
async def analyze_content_utilitarian(
    agent_context,
    content: Annotated[str, "Content to analyze for ethical implications"],
    context: Annotated[Dict[str, Any], "Context information including platform, audience, and content type"] = {}
) -> Dict[str, Any]:
    """
    Analyze content using utilitarian ethical reasoning
    
    Args:
        content: The content to analyze
        context: Additional context (platform, audience type, etc.)
    
    Returns:
        Dict containing decision, confidence, reasoning, and analysis details
    """
    
    agent_context.logger.info(f"UtilitarianAgent analyzing content: {content[:100]}...")
    
    if not context:
        context = {"type": "general", "platform": "unknown"}
    
    try:
        # Perform utilitarian analysis
        analysis = utilitarian_engine.analyze_content(content, context)
        
        # Add metadata
        analysis.update({
            "agent_id": "utilitarian_agent",
            "agent_type": "ethical_reasoning",
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "context": context
        })
        
        agent_context.logger.info(f"UtilitarianAgent decision: {analysis['decision']} (confidence: {analysis['confidence']:.2f})")
        
        return analysis
        
    except Exception as e:
        agent_context.logger.error(f"Error in utilitarian analysis: {e}")
        return {
            "error": str(e),
            "decision": "FLAG_FOR_REVIEW",
            "confidence": 0.5,
            "agent_id": "utilitarian_agent",
            "timestamp": datetime.now().isoformat()
        }

@session.bind(
    name="get_utilitarian_principles", 
    description="Get the core principles of utilitarian ethical reasoning"
)
async def get_utilitarian_principles(agent_context) -> Dict[str, Any]:
    """Get the core principles of utilitarian ethics"""
    
    return {
        "ethical_framework": "Utilitarianism",
        "principles": utilitarian_engine.principles,
        "description": "Utilitarian ethics focuses on maximizing overall happiness and well-being while minimizing suffering",
        "agent_id": "utilitarian_agent",
        "timestamp": datetime.now().isoformat()
    }

@session.bind(
    name="health_check", 
    description="Check the health and status of the UtilitarianAgent"
)
async def health_check(agent_context) -> Dict[str, Any]:
    """Health check for the UtilitarianAgent"""
    
    return {
        "status": "healthy",
        "agent_id": "utilitarian_agent",
        "agent_type": "ethical_reasoning",
        "ethical_framework": "Utilitarianism",
        "capabilities": [
            "content_analysis",
            "utility_calculation", 
            "ethical_reasoning",
            "decision_making"
        ],
        "timestamp": datetime.now().isoformat()
    }

async def main():
    """Main function to run the UtilitarianAgent"""
    logger.info("Starting UtilitarianAgent for GenAI AgentOS Protocol...")
    logger.info(f"Ethical Framework: {utilitarian_engine.ethical_framework}")
    logger.info(f"Principles: {len(utilitarian_engine.principles)} core principles")
    
    try:
        await session.process_events()
    except KeyboardInterrupt:
        logger.info("UtilitarianAgent stopped by user")
    except Exception as e:
        logger.error(f"Error in UtilitarianAgent: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 