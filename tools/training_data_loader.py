#!/usr/bin/env python3
"""
Training Data Loader for EthIQ Agents
Provides few-shot examples and training data for improved agent performance
"""

import os
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TrainingExample:
    """Represents a training example with content and analysis"""
    content: str
    analysis: str
    decision: str
    confidence: float
    reasoning: str

class TrainingDataLoader:
    """Loads and manages training data for agent few-shot prompting"""
    
    def __init__(self, data_dir: str = "data/training"):
        self.data_dir = data_dir
        self.agent_data = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all training data for all agents"""
        agents = ["utilitarian", "deontological", "cultural_context", "free_speech"]
        
        for agent in agents:
            agent_dir = os.path.join(self.data_dir, agent)
            if os.path.exists(agent_dir):
                self.agent_data[agent] = self._load_agent_data(agent_dir)
                logger.info(f"Loaded {len(self.agent_data[agent])} examples for {agent} agent")
    
    def _load_agent_data(self, agent_dir: str) -> List[TrainingExample]:
        """Load training data for a specific agent"""
        examples = []
        
        # Load flagged examples
        flagged_files = [f for f in os.listdir(agent_dir) if f.startswith("flagged_")]
        for file in flagged_files:
            file_path = os.path.join(agent_dir, file)
            example = self._parse_training_file(file_path)
            if example:
                examples.append(example)
        
        # Load approved examples
        approved_files = [f for f in os.listdir(agent_dir) if f.startswith("approved_")]
        for file in approved_files:
            file_path = os.path.join(agent_dir, file)
            example = self._parse_training_file(file_path)
            if example:
                examples.append(example)
        
        return examples
    
    def _parse_training_file(self, file_path: str) -> Optional[TrainingExample]:
        """Parse a training file and extract the example"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the structured format
            lines = content.strip().split('\n')
            
            # Extract content (everything after "Content: " until the next section)
            content_start = content.find("Content: ") + 9
            analysis_start = content.find("Analysis: ")
            content_text = content[content_start:analysis_start].strip()
            
            # Extract analysis
            analysis_start = content.find("Analysis: ") + 10
            decision_start = content.find("Decision: ")
            analysis_text = content[analysis_start:decision_start].strip()
            
            # Extract decision
            decision_start = content.find("Decision: ") + 10
            confidence_start = content.find("Confidence: ")
            decision_text = content[decision_start:confidence_start].strip()
            
            # Extract confidence
            confidence_start = content.find("Confidence: ") + 12
            reasoning_start = content.find("Reasoning: ")
            confidence_text = content[confidence_start:reasoning_start].strip()
            confidence = float(confidence_text)
            
            # Extract reasoning
            reasoning_start = content.find("Reasoning: ") + 11
            reasoning_text = content[reasoning_start:].strip()
            
            return TrainingExample(
                content=content_text,
                analysis=analysis_text,
                decision=decision_text,
                confidence=confidence,
                reasoning=reasoning_text
            )
            
        except Exception as e:
            logger.error(f"Error parsing training file {file_path}: {e}")
            return None
    
    def get_few_shot_examples(self, agent_type: str, num_examples: int = 3, 
                            include_flagged: bool = True, include_approved: bool = True) -> List[TrainingExample]:
        """Get few-shot examples for a specific agent type"""
        if agent_type not in self.agent_data:
            logger.warning(f"No training data found for agent type: {agent_type}")
            return []
        
        examples = self.agent_data[agent_type]
        
        # Filter by decision type if specified
        filtered_examples = []
        for example in examples:
            if include_flagged and "FLAGGED" in example.decision:
                filtered_examples.append(example)
            elif include_approved and "APPROVED" in example.decision:
                filtered_examples.append(example)
        
        # Randomly sample examples
        if len(filtered_examples) <= num_examples:
            return filtered_examples
        else:
            return random.sample(filtered_examples, num_examples)
    
    def format_examples_for_prompt(self, examples: List[TrainingExample]) -> str:
        """Format examples into a prompt-friendly string"""
        if not examples:
            return ""
        
        formatted = "Here are some examples of content moderation decisions:\n\n"
        
        for i, example in enumerate(examples, 1):
            formatted += f"Example {i}:\n"
            formatted += f"Content: {example.content}\n"
            formatted += f"Analysis: {example.analysis}\n"
            formatted += f"Decision: {example.decision}\n"
            formatted += f"Confidence: {example.confidence}\n"
            formatted += f"Reasoning: {example.reasoning}\n\n"
        
        return formatted
    
    def get_agent_prompt_template(self, agent_type: str) -> str:
        """Get a prompt template for a specific agent type"""
        templates = {
            "utilitarian": """You are a Utilitarian Ethics Agent. Your role is to analyze content from a utilitarian perspective, considering the greatest good for the greatest number.

Key principles:
- Evaluate consequences and outcomes
- Consider overall happiness and well-being
- Weigh benefits against harms
- Focus on maximizing positive impact

{examples}

Now analyze the following content from a utilitarian perspective:""",
            
            "deontological": """You are a Deontological Ethics Agent. Your role is to analyze content from a deontological perspective, focusing on moral duties and principles.

Key principles:
- Evaluate actions based on moral rules and duties
- Consider universalizability (could everyone act this way?)
- Respect human dignity and autonomy
- Focus on intentions and principles, not just outcomes

{examples}

Now analyze the following content from a deontological perspective:""",
            
            "cultural_context": """You are a Cultural Context Agent. Your role is to analyze content considering cultural sensitivity, diversity, and respect for different traditions.

Key principles:
- Consider cultural context and significance
- Respect cultural diversity and traditions
- Avoid cultural appropriation and stereotypes
- Promote cultural understanding and inclusion

{examples}

Now analyze the following content from a cultural context perspective:""",
            
            "free_speech": """You are a Free Speech Agent. Your role is to analyze content considering free speech principles and the balance between expression and harm.

Key principles:
- Support robust debate and diverse viewpoints
- Protect political speech and criticism
- Distinguish between protected speech and harmful content
- Consider when speech crosses into incitement or harassment

{examples}

Now analyze the following content from a free speech perspective:"""
        }
        
        return templates.get(agent_type, "Analyze the following content:")
    
    def create_agent_prompt(self, agent_type: str, content: str, num_examples: int = 2) -> str:
        """Create a complete prompt for an agent with few-shot examples"""
        examples = self.get_few_shot_examples(agent_type, num_examples)
        examples_text = self.format_examples_for_prompt(examples)
        
        template = self.get_agent_prompt_template(agent_type)
        prompt = template.format(examples=examples_text)
        prompt += f"\n\nContent to analyze: {content}\n\n"
        prompt += "Please provide your analysis in the following format:\n"
        prompt += "Analysis: [Your ethical analysis]\n"
        prompt += "Decision: [APPROVED/FLAGGED with brief reason]\n"
        prompt += "Confidence: [0.0-1.0]\n"
        prompt += "Reasoning: [Detailed explanation of your reasoning]"
        
        return prompt
    
    def get_training_stats(self) -> Dict[str, Dict]:
        """Get statistics about the training data"""
        stats = {}
        
        for agent_type, examples in self.agent_data.items():
            flagged_count = sum(1 for ex in examples if "FLAGGED" in ex.decision)
            approved_count = sum(1 for ex in examples if "APPROVED" in ex.decision)
            
            stats[agent_type] = {
                "total_examples": len(examples),
                "flagged_examples": flagged_count,
                "approved_examples": approved_count,
                "avg_confidence": sum(ex.confidence for ex in examples) / len(examples) if examples else 0
            }
        
        return stats

# Convenience functions
def load_training_data(data_dir: str = "data/training") -> TrainingDataLoader:
    """Load training data from the specified directory"""
    return TrainingDataLoader(data_dir)

def get_agent_examples(agent_type: str, num_examples: int = 3) -> List[TrainingExample]:
    """Get training examples for a specific agent"""
    loader = TrainingDataLoader()
    return loader.get_few_shot_examples(agent_type, num_examples)

def create_agent_prompt(agent_type: str, content: str, num_examples: int = 2) -> str:
    """Create a prompt for an agent with training examples"""
    loader = TrainingDataLoader()
    return loader.create_agent_prompt(agent_type, content, num_examples)

if __name__ == "__main__":
    # Test the training data loader
    loader = TrainingDataLoader()
    
    print("Training Data Statistics:")
    stats = loader.get_training_stats()
    for agent, stat in stats.items():
        print(f"\n{agent.upper()}:")
        print(f"  Total examples: {stat['total_examples']}")
        print(f"  Flagged: {stat['flagged_examples']}")
        print(f"  Approved: {stat['approved_examples']}")
        print(f"  Average confidence: {stat['avg_confidence']:.2f}")
    
    # Test prompt creation
    test_content = "Let's organize a peaceful protest to raise awareness about climate change."
    prompt = loader.create_agent_prompt("utilitarian", test_content)
    print(f"\n\nSample Utilitarian Prompt:\n{prompt[:500]}...") 