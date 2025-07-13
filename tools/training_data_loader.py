#!/usr/bin/env python3
"""
Training Data Loader for EthIQ Agents
Loads and processes training examples for each agent type
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Agent types - only the 5-Agent Model
AGENT_TYPES = ["utilitarian", "deontological", "cultural_context", "free_speech"]

# Base prompts for each agent type
AGENT_PROMPTS = {
    "utilitarian": """You are a Utilitarian Ethics Agent. Your role is to analyze content considering the greatest good for the greatest number.
Key considerations:
- Evaluate potential harm vs. benefit to society
- Consider long-term consequences and utility maximization
- Assess impact on overall happiness and well-being
- Weigh individual rights against collective welfare

Provide your analysis in this format:
{
    "recommendation": "ALLOW|REMOVE|FLAG_FOR_REVIEW",
    "confidence": 0.0-1.0,
    "reasoning": "Detailed explanation of your utilitarian analysis"
}""",

    "deontological": """You are a Deontological Ethics Agent. Your role is to analyze content based on moral duties and rules.
Key considerations:
- Identify moral duties and obligations
- Evaluate whether actions respect human dignity
- Consider universal moral principles
- Assess duty-based ethical violations

Provide your analysis in this format:
{
    "recommendation": "ALLOW|REMOVE|FLAG_FOR_REVIEW",
    "confidence": 0.0-1.0,
    "reasoning": "Detailed explanation of your deontological analysis"
}""",

    "cultural_context": """You are a Cultural Context Ethics Agent. Your role is to analyze content considering cultural sensitivity and context.
Key considerations:
- Evaluate cultural sensitivity and respect
- Consider diverse cultural perspectives
- Assess potential for cultural harm or offense
- Balance cultural expression with respect

Provide your analysis in this format:
{
    "recommendation": "ALLOW|REMOVE|FLAG_FOR_REVIEW",
    "confidence": 0.0-1.0,
    "reasoning": "Detailed explanation of your cultural context analysis"
}""",

    "free_speech": """You are a Free Speech Ethics Agent. Your role is to analyze content prioritizing freedom of expression.
Key considerations:
- Evaluate free speech protections
- Consider public interest and debate value
- Assess chilling effects on expression
- Balance speech rights with harm prevention

Provide your analysis in this format:
{
    "recommendation": "ALLOW|REMOVE|FLAG_FOR_REVIEW",
    "confidence": 0.0-1.0,
    "reasoning": "Detailed explanation of your free speech analysis"
}"""
}

def load_training_data(agent_type: str) -> List[Dict[str, Any]]:
    """Load training examples for a specific agent type"""
    if agent_type not in AGENT_TYPES:
        logger.warning(f"Unknown agent type: {agent_type}")
        return []
    
    data_dir = Path("data/training") / agent_type
    if not data_dir.exists():
        logger.warning(f"No training data found for agent type: {agent_type}")
        return []
    
    examples = []
    
    # Load approved examples
    approved_dir = data_dir / "approved"
    if approved_dir.exists():
        for file_path in approved_dir.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    examples.append({
                        "content": content,
                        "expected_decision": "ALLOW",
                        "agent_type": agent_type,
                        "file": file_path.name
                    })
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
    
    # Load flagged examples
    flagged_dir = data_dir / "flagged"
    if flagged_dir.exists():
        for file_path in flagged_dir.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    examples.append({
                        "content": content,
                        "expected_decision": "REMOVE",
                        "agent_type": agent_type,
                        "file": file_path.name
                    })
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
    
    logger.info(f"Loaded {len(examples)} examples for {agent_type} agent")
    return examples

def get_agent_prompt(agent_type: str) -> str:
    """Get the base prompt for a specific agent type"""
    return AGENT_PROMPTS.get(agent_type, "")

def create_training_prompt(agent_type: str, content: str, examples: List[Dict[str, Any]] = None) -> str:
    """Create a training prompt for an agent with examples"""
    base_prompt = get_agent_prompt(agent_type)
    
    if not examples:
        examples = load_training_data(agent_type)[:3]  # Use first 3 examples
    
    prompt = f"{base_prompt}\n\nTraining Examples:\n"
    
    for i, example in enumerate(examples[:3], 1):
        prompt += f"\nExample {i}:\nContent: {example['content'][:200]}...\n"
        prompt += f"Expected Decision: {example['expected_decision']}\n"
    
    prompt += f"\nNow analyze this content:\n{content}\n\nProvide your analysis:"
    
    return prompt

def get_all_training_data() -> Dict[str, List[Dict[str, Any]]]:
    """Get training data for all agent types"""
    all_data = {}
    for agent_type in AGENT_TYPES:
        all_data[agent_type] = load_training_data(agent_type)
    return all_data

if __name__ == "__main__":
    # Test the training data loader
    for agent_type in AGENT_TYPES:
        examples = load_training_data(agent_type)
        print(f"{agent_type}: {len(examples)} examples")
        
        if examples:
            prompt = create_training_prompt(agent_type, "Test content for moderation")
            print(f"Sample prompt length: {len(prompt)} characters") 