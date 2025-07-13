#!/usr/bin/env python3
"""
Agent Improvement System for EthIQ
Uses test cases and column descriptions to enhance agent performance
"""

import csv
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """Represents a test case for agent evaluation"""
    id: str
    sample_text: str
    category: str
    why_problematic: str
    expected_agents: List[str]
    notes: str
    final_decision: Optional[str] = None
    confidence_score: Optional[float] = None
    correct: Optional[str] = None
    success_reason: Optional[str] = None
    mental_health_score: Optional[float] = None
    expected_mental_health: Optional[str] = None
    match: Optional[str] = None
    analysis_summary: Optional[str] = None
    analysis_relevance: Optional[str] = None
    missing_points: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    agent_responses: Optional[str] = None
    suggested_fix: Optional[str] = None


@dataclass
class ColumnDescription:
    """Represents a column description for understanding data structure"""
    column_name: str
    purpose: str
    description: str = ""


class AgentImprovementSystem:
    """System for improving agents using test cases and feedback"""
    
    def __init__(self, test_cases_path: str = "agents/TestCases/EthIQ_Test_Cases.csv",
                 column_descriptions_path: str = "agents/TestCases/EthIQ_Column_Descriptions.csv"):
        self.test_cases_path = test_cases_path
        self.column_descriptions_path = column_descriptions_path
        self.test_cases: List[TestCase] = []
        self.column_descriptions: List[ColumnDescription] = []
        self.agent_performance: Dict[str, Dict[str, Any]] = {}
        self.improvement_suggestions: Dict[str, List[str]] = {}
        
        self._load_data()
    
    def _load_data(self):
        """Load test cases and column descriptions"""
        try:
            # Load column descriptions
            with open(self.column_descriptions_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    if row.get('Column Name') and row.get('Purpose'):
                        self.column_descriptions.append(ColumnDescription(
                            column_name=row['Column Name'],
                            purpose=row['Purpose'],
                            description=row.get('', '')
                        ))
            
            # Load test cases
            with open(self.test_cases_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    if row.get('ID') and row.get('Sample Text'):
                        expected_agents = [agent.strip() for agent in row.get('Expected Agent(s) to Trigger', '').split(',') if agent.strip()]
                        
                        test_case = TestCase(
                            id=row['ID'],
                            sample_text=row['Sample Text'],
                            category=row.get('Category/Theme', ''),
                            why_problematic=row.get('Why It\'s Problematic', ''),
                            expected_agents=expected_agents,
                            notes=row.get('Notes', ''),
                            final_decision=row.get('Final System Decision'),
                            confidence_score=float(row.get('Confidence Score', 0)) if row.get('Confidence Score') else None,
                            correct=row.get('Correct? (Y/N/Partial)'),
                            success_reason=row.get('Success/Failure Reason'),
                            mental_health_score=float(row.get('Mental Health Score (System Output)', 0)) if row.get('Mental Health Score (System Output)') else None,
                            expected_mental_health=row.get('Expected Mental Health Impact'),
                            match=row.get('Match? (Y/N)'),
                            analysis_summary=row.get('Analysis Text Summary'),
                            analysis_relevance=row.get('Analysis Relevance'),
                            missing_points=row.get('Missing Points?'),
                            improvement_suggestions=row.get('Improvement Suggestions'),
                            agent_responses=row.get('Notes on Agent Responses'),
                            suggested_fix=row.get('Suggested Fix')
                        )
                        self.test_cases.append(test_case)
            
            logger.info(f"Loaded {len(self.test_cases)} test cases and {len(self.column_descriptions)} column descriptions")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def analyze_agent_performance(self) -> Dict[str, Any]:
        """Analyze performance of each agent based on test cases"""
        agent_stats = {}
        
        for test_case in self.test_cases:
            if not test_case.expected_agents:
                continue
                
            for agent in test_case.expected_agents:
                if agent not in agent_stats:
                    agent_stats[agent] = {
                        'total_expected': 0,
                        'correct_decisions': 0,
                        'incorrect_decisions': 0,
                        'partial_decisions': 0,
                        'categories': set(),
                        'confidence_scores': [],
                        'improvement_areas': []
                    }
                
                agent_stats[agent]['total_expected'] += 1
                agent_stats[agent]['categories'].add(test_case.category)
                
                if test_case.confidence_score:
                    agent_stats[agent]['confidence_scores'].append(test_case.confidence_score)
                
                if test_case.correct:
                    if test_case.correct.upper() == 'Y':
                        agent_stats[agent]['correct_decisions'] += 1
                    elif test_case.correct.upper() == 'N':
                        agent_stats[agent]['incorrect_decisions'] += 1
                    elif test_case.correct.upper() == 'PARTIAL':
                        agent_stats[agent]['partial_decisions'] += 1
                
                if test_case.improvement_suggestions:
                    agent_stats[agent]['improvement_areas'].append({
                        'test_case_id': test_case.id,
                        'suggestion': test_case.improvement_suggestions
                    })
        
        # Calculate success rates
        for agent, stats in agent_stats.items():
            total = stats['total_expected']
            if total > 0:
                stats['success_rate'] = (stats['correct_decisions'] / total) * 100
                stats['partial_rate'] = (stats['partial_decisions'] / total) * 100
                stats['failure_rate'] = (stats['incorrect_decisions'] / total) * 100
                
                if stats['confidence_scores']:
                    stats['avg_confidence'] = sum(stats['confidence_scores']) / len(stats['confidence_scores'])
                else:
                    stats['avg_confidence'] = 0
                
                stats['categories'] = list(stats['categories'])
            else:
                stats['success_rate'] = 0
                stats['partial_rate'] = 0
                stats['failure_rate'] = 0
                stats['avg_confidence'] = 0
        
        self.agent_performance = agent_stats
        return agent_stats
    
    def generate_improvement_suggestions(self) -> Dict[str, List[str]]:
        """Generate specific improvement suggestions for each agent"""
        suggestions = {}
        
        for agent, stats in self.agent_performance.items():
            agent_suggestions = []
            
            # Analyze performance patterns
            if stats['failure_rate'] > 50:
                agent_suggestions.append(f"High failure rate ({stats['failure_rate']:.1f}%) - needs prompt refinement")
            
            if stats['avg_confidence'] < 0.7:
                agent_suggestions.append(f"Low average confidence ({stats['avg_confidence']:.2f}) - needs decision logic improvement")
            
            # Analyze improvement areas from test cases
            for improvement in stats['improvement_areas']:
                agent_suggestions.append(f"Test case {improvement['test_case_id']}: {improvement['suggestion']}")
            
            # Category-specific suggestions
            categories = stats['categories']
            if 'Mental Health' in categories or 'Psychological' in categories:
                agent_suggestions.append("Consider adding more mental health sensitivity training examples")
            
            if 'Temporal' in categories:
                agent_suggestions.append("Enhance temporal context detection capabilities")
            
            if 'Financial' in categories:
                agent_suggestions.append("Improve financial scam detection patterns")
            
            if 'Religious' in categories:
                agent_suggestions.append("Add more religious sensitivity training examples")
            
            suggestions[agent] = agent_suggestions
        
        self.improvement_suggestions = suggestions
        return suggestions
    
    def create_enhanced_training_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create enhanced training data based on test cases"""
        enhanced_data = {}
        
        for test_case in self.test_cases:
            if not test_case.expected_agents:
                continue
            
            # Create training examples for each expected agent
            for agent in test_case.expected_agents:
                if agent not in enhanced_data:
                    enhanced_data[agent] = []
                
                # Determine decision based on test case
                decision = "FLAGGED"  # Default for problematic content
                if test_case.final_decision:
                    decision = test_case.final_decision
                
                # Create training example
                training_example = {
                    'content': test_case.sample_text,
                    'category': test_case.category,
                    'why_problematic': test_case.why_problematic,
                    'expected_decision': decision,
                    'confidence': test_case.confidence_score or 0.8,
                    'reasoning': test_case.analysis_summary or f"Content flagged due to {test_case.category} concerns",
                    'notes': test_case.notes,
                    'improvement_suggestions': test_case.improvement_suggestions
                }
                
                enhanced_data[agent].append(training_example)
        
        return enhanced_data
    
    def generate_agent_prompt_improvements(self) -> Dict[str, str]:
        """Generate improved prompts for each agent based on test cases"""
        prompt_improvements = {}
        
        for agent, stats in self.agent_performance.items():
            # Get test cases for this agent
            agent_test_cases = [tc for tc in self.test_cases if agent in tc.expected_agents]
            
            # Analyze common failure patterns
            failure_cases = [tc for tc in agent_test_cases if tc.correct and tc.correct.upper() == 'N']
            partial_cases = [tc for tc in agent_test_cases if tc.correct and tc.correct.upper() == 'PARTIAL']
            
            improvement_text = f"# {agent} Prompt Improvements\n\n"
            
            if failure_cases:
                improvement_text += "## Critical Failure Cases:\n"
                for case in failure_cases[:3]:  # Top 3 failures
                    improvement_text += f"- **{case.id}**: {case.sample_text[:100]}...\n"
                    improvement_text += f"  - Expected: {case.why_problematic}\n"
                    improvement_text += f"  - Issue: {case.success_reason or 'Decision incorrect'}\n"
                    improvement_text += f"  - Fix: {case.suggested_fix or 'Improve detection logic'}\n\n"
            
            if partial_cases:
                improvement_text += "## Partial Success Cases:\n"
                for case in partial_cases[:3]:  # Top 3 partial
                    improvement_text += f"- **{case.id}**: {case.sample_text[:100]}...\n"
                    improvement_text += f"  - Issue: {case.missing_points or 'Incomplete analysis'}\n"
                    improvement_text += f"  - Improvement: {case.improvement_suggestions or 'Enhance analysis depth'}\n\n"
            
            # Add general improvements
            improvement_text += "## General Improvements:\n"
            for suggestion in self.improvement_suggestions.get(agent, []):
                improvement_text += f"- {suggestion}\n"
            
            prompt_improvements[agent] = improvement_text
        
        return prompt_improvements
    
    def export_improvement_report(self, output_path: str = "agent_improvement_report.json"):
        """Export comprehensive improvement report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_test_cases': len(self.test_cases),
                'total_agents_analyzed': len(self.agent_performance),
                'overall_success_rate': sum(stats['success_rate'] for stats in self.agent_performance.values()) / len(self.agent_performance) if self.agent_performance else 0
            },
            'agent_performance': self.agent_performance,
            'improvement_suggestions': self.improvement_suggestions,
            'enhanced_training_data': self.create_enhanced_training_data(),
            'prompt_improvements': self.generate_agent_prompt_improvements(),
            'test_case_analysis': [
                {
                    'id': tc.id,
                    'category': tc.category,
                    'expected_agents': tc.expected_agents,
                    'performance': tc.correct,
                    'suggestions': tc.improvement_suggestions
                }
                for tc in self.test_cases
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Improvement report exported to {output_path}")
        return report
    
    def get_agent_ranking(self) -> List[Tuple[str, float]]:
        """Get ranking of agents by performance"""
        if not self.agent_performance:
            self.analyze_agent_performance()
        
        rankings = []
        for agent, stats in self.agent_performance.items():
            # Calculate composite score (success rate + confidence + partial credit)
            score = stats['success_rate'] + (stats['partial_rate'] * 0.5) + (stats['avg_confidence'] * 10)
            rankings.append((agent, score))
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)


def main():
    """Main function to run the agent improvement system"""
    print("🚀 EthIQ Agent Improvement System")
    print("=" * 50)
    
    # Initialize the system
    improvement_system = AgentImprovementSystem()
    
    # Analyze performance
    print("\n📊 Analyzing agent performance...")
    performance = improvement_system.analyze_agent_performance()
    
    # Generate suggestions
    print("💡 Generating improvement suggestions...")
    suggestions = improvement_system.generate_improvement_suggestions()
    
    # Get rankings
    print("🏆 Agent performance rankings:")
    rankings = improvement_system.get_agent_ranking()
    for i, (agent, score) in enumerate(rankings, 1):
        stats = performance[agent]
        print(f"{i}. {agent}: {stats['success_rate']:.1f}% success, {stats['avg_confidence']:.2f} avg confidence")
    
    # Export report
    print("\n📄 Exporting improvement report...")
    report = improvement_system.export_improvement_report()
    
    print(f"\n✅ Analysis complete! Report saved to agent_improvement_report.json")
    print(f"📈 Overall success rate: {report['summary']['overall_success_rate']:.1f}%")


if __name__ == "__main__":
    main() 