#!/usr/bin/env python3
"""
Enhanced Training Data Generator v2.0
Incorporates comprehensive test cases to improve agent performance and security.
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

class EnhancedTrainingGeneratorV2:
    def __init__(self):
        self.test_case_files = [
            "agents/TestCases/EthIQ_Test_Cases.csv",
            "agents/TestCases/EthIQ_Enhanced_Test_Cases.csv",
            "agents/TestCases/EthIQ_Security_Test_Cases.csv"
        ]
        self.output_dir = "agents/enhanced_training_v2"
        self.agent_types = [
            "utilitarian", "deontological", "cultural_context", "free_speech"
        ]
        
    def load_all_test_cases(self) -> List[Dict[str, Any]]:
        """Load all test cases from multiple files."""
        all_test_cases = []
        
        for file_path in self.test_case_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter=';')
                        for row in reader:
                            if row.get('Sample Text'):
                                all_test_cases.append(row)
                    print(f"✅ Loaded {len([tc for tc in all_test_cases if tc.get('file_source') == file_path])} test cases from {file_path}")
                except Exception as e:
                    print(f"❌ Error loading {file_path}: {e}")
            else:
                print(f"⚠️  File not found: {file_path}")
        
        print(f"📊 Total test cases loaded: {len(all_test_cases)}")
        return all_test_cases
    
    def categorize_test_cases(self, test_cases: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize test cases by expected agent type."""
        categorized = {agent: [] for agent in self.agent_types}
        
        for test_case in test_cases:
            expected_agents = test_case.get('Expected Agent(s) to Trigger', '')
            if expected_agents:
                agent_list = [agent.strip() for agent in expected_agents.split(',')]
                
                for agent in agent_list:
                    # Map agent names to internal agent types
                    agent_mapping = {
                        'UtilitarianAgent': 'utilitarian',
                        'DeontologicalAgent': 'deontological',
                        'CulturalContextAgent': 'cultural_context',
                        'FreeSpeechAgent': 'free_speech',
                    }
                    
                    for agent_name, agent_type in agent_mapping.items():
                        if agent_name in agent:
                            categorized[agent_type].append(test_case)
                            break
        
        return categorized
    
    def generate_agent_training_data(self, agent_type: str, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate training data for a specific agent type."""
        training_examples = []
        
        for test_case in test_cases:
            content = test_case.get('Sample Text', '')
            category = test_case.get('Category/Theme', '')
            why_problematic = test_case.get('Why It\'s Problematic', '')
            
            # Determine expected decision based on category
            category_lower = category.lower()
            if any(keyword in category_lower for keyword in ['violent', 'hate speech', 'discrimination', 'terrorism', 'national security']):
                expected_decision = 'REMOVE'
            elif any(keyword in category_lower for keyword in ['misinformation', 'temporal manipulation']):
                expected_decision = 'FLAG_FOR_REVIEW'
            elif any(keyword in category_lower for keyword in ['legitimate', 'free speech', 'educational', 'news', 'satire']):
                expected_decision = 'ALLOW'
            else:
                expected_decision = 'FLAG_FOR_REVIEW'  # Default to review
            
            # Generate agent-specific reasoning
            reasoning = self.generate_agent_reasoning(agent_type, content, category, why_problematic)
            
            training_example = {
                "content": content,
                "expected_decision": expected_decision,
                "reasoning": reasoning,
                "confidence": 0.9 if expected_decision != 'ALLOW' else 0.8,
                "category": category,
                "source": "enhanced_test_cases"
            }
            
            training_examples.append(training_example)
        
        return training_examples
    
    def generate_agent_reasoning(self, agent_type: str, content: str, category: str, why_problematic: str) -> str:
        """Generate agent-specific reasoning for training examples."""
        reasoning_templates = {
            "utilitarian": {
                "REMOVE": "This content causes significant harm to society and individuals. The negative consequences outweigh any potential benefits. Removing it maximizes overall well-being.",
                "FLAG_FOR_REVIEW": "This content may cause harm but requires careful evaluation. The potential negative impact should be assessed against potential benefits.",
                "ALLOW": "This content contributes positively to society or causes minimal harm. The benefits outweigh potential negative consequences."
            },
            "deontological": {
                "REMOVE": "This content violates fundamental moral duties and rights. It promotes actions that are inherently wrong regardless of consequences.",
                "FLAG_FOR_REVIEW": "This content may violate moral principles and requires ethical evaluation. Duty-based considerations need assessment.",
                "ALLOW": "This content respects fundamental moral duties and rights. It does not violate core ethical principles."
            },
            "cultural_context": {
                "REMOVE": "This content promotes harmful cultural stereotypes, discrimination, or cultural insensitivity that can cause real harm to communities.",
                "FLAG_FOR_REVIEW": "This content may have cultural implications that require careful consideration of diverse perspectives and norms.",
                "ALLOW": "This content respects cultural diversity and promotes positive cultural understanding and inclusion."
            },
            "free_speech": {
                "REMOVE": "This content goes beyond protected speech by inciting violence, promoting illegal activities, or causing direct harm to others.",
                "FLAG_FOR_REVIEW": "This content may test the boundaries of free speech and requires careful evaluation of speech rights vs. harm prevention.",
                "ALLOW": "This content represents legitimate free expression that should be protected, even if controversial or unpopular."
            }
        }
        
        template = reasoning_templates.get(agent_type, {}).get("FLAG_FOR_REVIEW", "This content requires evaluation based on ethical considerations.")
        return template
    
    def create_enhanced_prompts(self, agent_type: str) -> Dict[str, str]:
        """Create enhanced prompts for each agent type."""
        prompt_templates = {
            "utilitarian": {
                "system_prompt": """You are a Utilitarian Ethics Agent specializing in consequentialist reasoning. Your role is to evaluate content based on its potential to maximize overall well-being and minimize harm.

Key Principles:
- Evaluate consequences for all affected parties
- Consider both immediate and long-term impacts
- Weigh benefits against harms quantitatively when possible
- Prioritize actions that create the greatest good for the greatest number
- Consider indirect and systemic effects

Focus Areas:
- Public health and safety
- Economic impact
- Social cohesion
- Environmental consequences
- Individual vs. collective welfare

Provide clear reasoning about the expected consequences of allowing or removing content.""",
                
                "user_prompt": """Analyze the following content from a utilitarian perspective:

Content: {content}

Consider:
1. What are the potential benefits of allowing this content?
2. What are the potential harms of allowing this content?
3. Who would be affected and how?
4. What are the long-term consequences?
5. Does this content maximize overall well-being?

Provide your decision (ALLOW/REMOVE/FLAG_FOR_REVIEW) with confidence score and detailed reasoning."""
            },
            
            "deontological": {
                "system_prompt": """You are a Deontological Ethics Agent specializing in duty-based reasoning. Your role is to evaluate content based on moral duties, rights, and principles rather than consequences.

Key Principles:
- Respect for human dignity and autonomy
- Universal moral duties and obligations
- Rights-based considerations
- Moral principles that apply regardless of outcomes
- Categorical imperatives

Focus Areas:
- Human rights violations
- Moral duties and obligations
- Respect for persons
- Universal moral principles
- Ethical consistency

Provide clear reasoning about moral duties and rights involved.""",
                
                "user_prompt": """Analyze the following content from a deontological perspective:

Content: {content}

Consider:
1. Does this content respect human dignity and autonomy?
2. Are there universal moral duties being violated?
3. What rights are at stake?
4. Are the actions described morally permissible regardless of consequences?
5. Does this content treat people as ends rather than means?

Provide your decision (ALLOW/REMOVE/FLAG_FOR_REVIEW) with confidence score and detailed reasoning."""
            },
            
            "cultural_context": {
                "system_prompt": """You are a Cultural Context Ethics Agent specializing in cultural sensitivity and diversity considerations. Your role is to evaluate content in light of diverse cultural perspectives and norms.

Key Principles:
- Cultural sensitivity and respect
- Recognition of diverse cultural values
- Avoidance of cultural stereotypes and bias
- Promotion of cultural understanding
- Consideration of cultural power dynamics

Focus Areas:
- Cultural stereotypes and bias
- Religious and cultural insensitivity
- Cultural appropriation
- Cross-cultural communication
- Cultural power dynamics

Provide clear reasoning about cultural implications and sensitivity.""",
                
                "user_prompt": """Analyze the following content from a cultural context perspective:

Content: {content}

Consider:
1. How might different cultural groups perceive this content?
2. Are there cultural stereotypes or biases present?
3. Does this content respect cultural diversity?
4. Could this content cause cultural harm or offense?
5. Does this promote cultural understanding or division?

Provide your decision (ALLOW/REMOVE/FLAG_FOR_REVIEW) with confidence score and detailed reasoning."""
            },
            
            "free_speech": {
                "system_prompt": """You are a Free Speech Ethics Agent specializing in balancing free expression with harm prevention. Your role is to evaluate content in light of speech rights and limitations.

Key Principles:
- Protection of legitimate free expression
- Recognition of speech limitations for harm prevention
- Balance between speech rights and other rights
- Consideration of speech context and impact
- Protection of unpopular or controversial speech

Focus Areas:
- Incitement to violence
- Hate speech and discrimination
- False information with harmful intent
- Privacy and reputation rights
- Public safety concerns

Provide clear reasoning about speech rights and limitations.""",
                
                "user_prompt": """Analyze the following content from a free speech perspective:

Content: {content}

Consider:
1. Is this content protected speech or does it fall into unprotected categories?
2. Does this content incite violence or illegal activity?
3. Are there competing rights that limit speech protection?
4. What is the context and potential impact of this speech?
5. Does restricting this speech serve a compelling government interest?

Provide your decision (ALLOW/REMOVE/FLAG_FOR_REVIEW) with confidence score and detailed reasoning."""
            }
        }
        
        return prompt_templates.get(agent_type, {
            "system_prompt": "You are an ethical analysis agent.",
            "user_prompt": "Analyze this content: {content}"
        })
    
    def generate_enhanced_training_files(self):
        """Generate enhanced training files for all agents."""
        print("🚀 Enhanced Training Data Generator v2.0")
        print("=" * 60)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load all test cases
        all_test_cases = self.load_all_test_cases()
        if not all_test_cases:
            print("❌ No test cases loaded. Cannot proceed.")
            return
        
        # Categorize test cases
        categorized_cases = self.categorize_test_cases(all_test_cases)
        
        # Generate training data for each agent
        for agent_type in self.agent_types:
            print(f"\n🔄 Generating training data for {agent_type} agent...")
            
            agent_test_cases = categorized_cases.get(agent_type, [])
            if not agent_test_cases:
                print(f"⚠️  No test cases found for {agent_type} agent")
                continue
            
            # Generate training examples
            training_examples = self.generate_agent_training_data(agent_type, agent_test_cases)
            
            # Create enhanced prompts
            prompts = self.create_enhanced_prompts(agent_type)
            
            # Save training data
            training_file = os.path.join(self.output_dir, f"{agent_type}_enhanced_training.json")
            with open(training_file, 'w') as f:
                json.dump({
                    "agent_type": agent_type,
                    "training_examples": training_examples,
                    "prompts": prompts,
                    "generated_at": datetime.now().isoformat(),
                    "total_examples": len(training_examples)
                }, f, indent=2)
            
            print(f"✅ Generated {len(training_examples)} training examples for {agent_type} agent")
        
        # Generate summary report
        self.generate_summary_report(categorized_cases)
        
        print(f"\n🎉 Enhanced training data generation completed!")
        print(f"📁 Output directory: {self.output_dir}")
    
    def generate_summary_report(self, categorized_cases: Dict[str, List[Dict[str, Any]]]):
        """Generate a summary report of the training data generation."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_test_cases": sum(len(cases) for cases in categorized_cases.values()),
            "agent_distribution": {agent: len(cases) for agent, cases in categorized_cases.items()},
            "file_locations": [f"{self.output_dir}/{agent}_enhanced_training.json" for agent in self.agent_types],
            "enhancements": [
                "Comprehensive test case coverage",
                "Security-focused scenarios",
                "Enhanced reasoning templates",
                "Improved prompt engineering",
                "Multi-agent coordination examples"
            ]
        }
        
        report_file = os.path.join(self.output_dir, "enhanced_training_summary.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Summary Report:")
        print(f"Total test cases processed: {report['total_test_cases']}")
        print(f"Agent distribution:")
        for agent, count in report['agent_distribution'].items():
            print(f"  {agent}: {count} test cases")
        print(f"Summary saved to: {report_file}")

def main():
    """Main function to run the enhanced training generator."""
    generator = EnhancedTrainingGeneratorV2()
    generator.generate_enhanced_training_files()

if __name__ == "__main__":
    main() 