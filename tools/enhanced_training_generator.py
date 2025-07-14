#!/usr/bin/env python3
"""
Enhanced Training Data Generator for EthIQ Agents
Creates improved training examples from test cases
"""

import os
import json
import logging
from typing import Dict, List, Any
from pathlib import Path
from tools.agent_improvement_system import AgentImprovementSystem

logger = logging.getLogger(__name__)


class EnhancedTrainingGenerator:
    """Generates enhanced training data for agents based on test cases"""
    
    def __init__(self, output_dir: str = "data/training/enhanced"):
        self.output_dir = output_dir
        self.improvement_system = AgentImprovementSystem()
        self.agent_mapping = {
            'UtilitarianAgent': 'utilitarian',
            'DeontologicalAgent': 'deontological',
            'CulturalContextAgent': 'cultural_context',
            'FreeSpeechAgent': 'free_speech'
        }
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_enhanced_training_files(self):
        """Generate enhanced training files for each agent"""
        enhanced_data = self.improvement_system.create_enhanced_training_data()
        
        for agent_name, training_examples in enhanced_data.items():
            # Map agent name to directory name
            agent_dir = self.agent_mapping.get(agent_name, agent_name.lower())
            agent_output_dir = os.path.join(self.output_dir, agent_dir)
            
            # Create agent directory
            Path(agent_output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate training files
            self._generate_agent_training_files(agent_output_dir, training_examples, agent_name)
            
            logger.info(f"Generated {len(training_examples)} training examples for {agent_name}")
    
    def _generate_agent_training_files(self, output_dir: str, examples: List[Dict], agent_name: str):
        """Generate training files for a specific agent"""
        for i, example in enumerate(examples, 1):
            # Determine if this should be flagged or approved
            is_flagged = example['expected_decision'] in ['FLAGGED', 'REMOVE', 'FLAG_FOR_REVIEW']
            prefix = "flagged" if is_flagged else "approved"
            
            filename = f"{prefix}_{i}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Create training content
            content = self._format_training_example(example, agent_name)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _format_training_example(self, example: Dict, agent_name: str) -> str:
        """Format a training example for file output"""
        content = f"""Content: {example['content']}

Analysis: This content falls under the category of {example['category']}. {example['why_problematic']}

Decision: {example['expected_decision']}

Confidence: {example['confidence']}

Reasoning: {example['reasoning']}

Notes: {example['notes']}

Improvement Context: {example.get('improvement_suggestions', 'No specific improvements noted')}

Agent: {agent_name}
Category: {example['category']}
"""
        return content
    
    def generate_agent_prompt_enhancements(self):
        """Generate enhanced prompts for each agent based on test cases"""
        prompt_improvements = self.improvement_system.generate_agent_prompt_improvements()
        
        enhanced_prompts = {}
        
        for agent_name, improvement_text in prompt_improvements.items():
            # Get base prompt template
            base_prompt = self._get_base_prompt(agent_name)
            
            # Enhance with test case insights
            enhanced_prompt = self._enhance_prompt_with_test_cases(base_prompt, agent_name)
            
            enhanced_prompts[agent_name] = enhanced_prompt
        
        return enhanced_prompts
    
    def _get_base_prompt(self, agent_name: str) -> str:
        """Get base prompt template for an agent"""
        base_prompts = {
            'UtilitarianAgent': """You are a Utilitarian Ethics Agent. Your role is to analyze content from a utilitarian perspective, considering the greatest good for the greatest number.

Key principles:
- Evaluate consequences and outcomes
- Consider overall happiness and well-being
- Weigh benefits against harms
- Focus on maximizing positive impact

{examples}

Now analyze the following content from a utilitarian perspective:""",
            
            'DeontologicalAgent': """You are a Deontological Ethics Agent. Your role is to analyze content from a deontological perspective, focusing on moral duties and principles.

Key principles:
- Evaluate actions based on moral rules and duties
- Consider universalizability (could everyone act this way?)
- Respect human dignity and autonomy
- Focus on intentions and principles, not just outcomes

{examples}

Now analyze the following content from a deontological perspective:""",
            
            'CulturalContextAgent': """You are a Cultural Context Agent. Your role is to analyze content considering cultural sensitivity, diversity, and respect for different traditions.

Key principles:
- Consider cultural context and significance
- Respect cultural diversity and traditions
- Avoid cultural appropriation and stereotypes
- Promote cultural understanding and inclusion

{examples}

Now analyze the following content from a cultural context perspective:""",
            
            'FreeSpeechAgent': """You are a Free Speech Agent. Your role is to analyze content considering free speech principles and the balance between expression and harm.

Key principles:
- Support robust debate and diverse viewpoints
- Protect political speech and criticism
- Distinguish between protected speech and harmful content
- Consider when speech crosses into incitement or harassment

{examples}

Now analyze the following content from a free speech perspective:""",
        }
        
        return base_prompts.get(agent_name, "Analyze the following content:")
    
    def _enhance_prompt_with_test_cases(self, base_prompt: str, agent_name: str) -> str:
        """Enhance prompt with insights from test cases"""
        # Get test cases for this agent
        agent_test_cases = [tc for tc in self.improvement_system.test_cases if agent_name in tc.expected_agents]
        
        if not agent_test_cases:
            return base_prompt
        
        # Add specific guidance based on test cases
        enhancement = "\n\n## Enhanced Guidance Based on Test Cases:\n"
        
        # Add category-specific guidance
        categories = set(tc.category for tc in agent_test_cases)
        for category in categories:
            category_cases = [tc for tc in agent_test_cases if tc.category == category]
            enhancement += f"\n### {category}:\n"
            enhancement += f"- Pay special attention to content involving {category.lower()}\n"
            enhancement += f"- Look for patterns like: {', '.join(set(tc.why_problematic[:50] + '...' for tc in category_cases[:3]))}\n"
        
        # Add common failure patterns
        failure_cases = [tc for tc in agent_test_cases if tc.correct and tc.correct.upper() == 'N']
        if failure_cases:
            enhancement += "\n### Common Failure Patterns to Avoid:\n"
            for case in failure_cases[:3]:
                enhancement += f"- {case.why_problematic[:100]}...\n"
        
        enhanced_prompt = base_prompt + enhancement
        return enhanced_prompt
    
    def update_training_data_loader(self):
        """Update the training data loader to include enhanced data"""
        # This would modify the training data loader to use enhanced data
        enhanced_data_path = os.path.join(self.output_dir, "enhanced_training_data.json")
        
        enhanced_data = self.improvement_system.create_enhanced_training_data()
        
        with open(enhanced_data_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Enhanced training data saved to {enhanced_data_path}")
        return enhanced_data_path
    
    def generate_agent_improvement_report(self):
        """Generate a comprehensive improvement report"""
        report = {
            'timestamp': self.improvement_system.export_improvement_report(),
            'enhanced_training': {
                'total_examples_generated': sum(len(examples) for examples in self.improvement_system.create_enhanced_training_data().values()),
                'agents_enhanced': list(self.improvement_system.create_enhanced_training_data().keys()),
                'output_directory': self.output_dir
            },
            'prompt_enhancements': self.generate_agent_prompt_enhancements(),
            'recommendations': {
                'next_steps': [
                    "1. Review generated training examples for accuracy",
                    "2. Test enhanced prompts with sample content",
                    "3. Update agent implementations with new training data",
                    "4. Run performance tests to measure improvements",
                    "5. Iterate based on new test results"
                ]
            }
        }
        
        report_path = os.path.join(self.output_dir, "improvement_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Improvement report saved to {report_path}")
        return report


def main():
    """Main function to run the enhanced training generator"""
    print("🚀 EthIQ Enhanced Training Generator")
    print("=" * 50)
    
    try:
        # Initialize the generator
        generator = EnhancedTrainingGenerator()
        
        # Generate enhanced training files
        print("\n📝 Generating enhanced training files...")
        generator.generate_enhanced_training_files()
        
        # Generate prompt enhancements
        print("💡 Generating prompt enhancements...")
        enhanced_prompts = generator.generate_agent_prompt_enhancements()
        
        # Update training data loader
        print("🔄 Updating training data loader...")
        enhanced_data_path = generator.update_training_data_loader()
        
        # Generate comprehensive report
        print("📊 Generating improvement report...")
        report = generator.generate_agent_improvement_report()
        
        print(f"\n✅ Enhanced training generation complete!")
        print(f"📁 Output directory: {generator.output_dir}")
        print(f"📊 Enhanced data: {enhanced_data_path}")
        print(f"🤖 Agents enhanced: {len(enhanced_prompts)}")
        
        # Show sample enhancements
        print(f"\n📝 Sample prompt enhancements:")
        for agent, prompt in list(enhanced_prompts.items())[:2]:
            print(f"\n{agent}:")
            print(f"  Length: {len(prompt)} characters")
            print(f"  Enhanced with test case insights")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 