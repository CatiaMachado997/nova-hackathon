#!/usr/bin/env python3
"""
AutoEthos Demo Script
Demonstrates the ethical deliberation system with example scenarios
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List

from agents import EthicsCommander, AuditLogger


class AutoEthosDemo:
    """Demo class for showcasing AutoEthos capabilities"""
    
    def __init__(self):
        self.commander = EthicsCommander()
        self.audit_logger = AuditLogger()
        self.demo_scenarios = self._load_demo_scenarios()
    
    def _load_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Load demo scenarios for testing"""
        return [
            {
                "name": "Satirical Political Video",
                "content": "A satirical video criticizing government policies with humorous exaggeration and parody elements. The video uses comedy to highlight political issues but could be seen as offensive by some viewers.",
                "context": {
                    "content_type": "video",
                    "platform": "social_media",
                    "audience_size": 50000,
                    "vulnerable_audience": False,
                    "educational_value": True,
                    "public_interest": True,
                    "democratic_value": True,
                    "target_cultures": ["western"],
                    "audience_diversity": "high"
                },
                "expected_conflict": True
            },
            {
                "name": "Hate Speech Content",
                "content": "Content promoting discrimination and violence against specific ethnic groups. The material contains harmful stereotypes and incitement to hatred.",
                "context": {
                    "content_type": "text",
                    "platform": "social_media",
                    "audience_size": 1000,
                    "vulnerable_audience": True,
                    "educational_value": False,
                    "public_interest": False,
                    "democratic_value": False,
                    "target_cultures": ["global"],
                    "audience_diversity": "high"
                },
                "expected_conflict": False
            },
            {
                "name": "Educational Content with Controversial Topics",
                "content": "An educational video about historical events that includes graphic content for educational purposes. The content is academically valuable but contains sensitive material.",
                "context": {
                    "content_type": "video",
                    "platform": "educational",
                    "audience_size": 5000,
                    "vulnerable_audience": True,
                    "educational_value": True,
                    "public_interest": True,
                    "democratic_value": False,
                    "target_cultures": ["global"],
                    "audience_diversity": "medium"
                },
                "expected_conflict": True
            },
            {
                "name": "AI-Generated Misinformation",
                "content": "An AI-generated article spreading false information about health treatments. The content appears credible but contains dangerous misinformation.",
                "context": {
                    "content_type": "text",
                    "platform": "news",
                    "audience_size": 25000,
                    "vulnerable_audience": True,
                    "educational_value": False,
                    "public_interest": False,
                    "democratic_value": False,
                    "target_cultures": ["global"],
                    "audience_diversity": "high"
                },
                "expected_conflict": False
            },
            {
                "name": "Artistic Expression with Cultural Sensitivity",
                "content": "An artistic piece that explores cultural themes but may be interpreted as cultural appropriation by some communities.",
                "context": {
                    "content_type": "image",
                    "platform": "art_gallery",
                    "audience_size": 2000,
                    "vulnerable_audience": False,
                    "educational_value": True,
                    "public_interest": False,
                    "democratic_value": True,
                    "target_cultures": ["global"],
                    "audience_diversity": "high"
                },
                "expected_conflict": True
            }
        ]
    
    async def run_demo(self):
        """Run the complete demo"""
        print("=" * 80)
        print("🤖 AutoEthos - Ethical Intelligence Demo")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Initialize system
        print("🚀 Initializing AutoEthos system...")
        await self._initialize_system()
        print("✅ System initialized successfully")
        print()
        
        # Run scenarios
        print("📋 Running demo scenarios...")
        print()
        
        results = []
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"Scenario {i}: {scenario['name']}")
            print("-" * 60)
            
            result = await self._run_scenario(scenario)
            results.append(result)
            
            print()
        
        # Show summary
        print("📊 Demo Summary")
        print("=" * 60)
        await self._show_summary(results)
        
        # Show agent performance
        print("\n🤖 Agent Performance Analysis")
        print("=" * 60)
        await self._show_agent_performance()
        
        print("\n🎉 Demo completed successfully!")
    
    async def _initialize_system(self):
        """Initialize the system and agents"""
        # The agents are already initialized in the constructor
        # This is where we would add any additional setup
        await asyncio.sleep(1)  # Simulate initialization time
    
    async def _run_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single scenario"""
        print(f"Content: {scenario['content'][:100]}...")
        print(f"Context: {scenario['context']}")
        print()
        
        start_time = time.time()
        
        # Run deliberation
        response = await self.commander.deliberate(
            scenario['content'], 
            scenario['context']
        )
        
        processing_time = time.time() - start_time
        
        # Get deliberation history
        deliberation_history = self.commander.get_deliberation_history()
        latest_deliberation = deliberation_history[-1] if deliberation_history else {}
        
        # Log deliberation
        await self.audit_logger.log_deliberation({
            "type": "deliberation_log",
            "deliberation_data": latest_deliberation,
            "duration": processing_time
        })
        
        # Display results
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"🎯 Final decision: {response.decision}")
        print(f"📊 Confidence: {response.confidence:.2%}")
        print(f"🧠 Reasoning: {response.reasoning}")
        
        # Show individual agent responses
        if "individual_responses" in latest_deliberation:
            print("\n🤖 Individual Agent Responses:")
            for agent_name, agent_response in latest_deliberation["individual_responses"].items():
                print(f"  • {agent_name}: {agent_response.decision} ({agent_response.confidence:.2%})")
        
        # Show conflicts if any
        if "cross_examination" in latest_deliberation:
            conflicts = latest_deliberation["cross_examination"].get("conflicts", [])
            if conflicts:
                print(f"\n⚠️  Conflicts detected: {len(conflicts)}")
                for conflict in conflicts:
                    print(f"  • {conflict.get('description', 'Unknown conflict')}")
        
        return {
            "scenario": scenario,
            "response": response,
            "processing_time": processing_time,
            "deliberation": latest_deliberation
        }
    
    async def _show_summary(self, results: List[Dict[str, Any]]):
        """Show demo summary"""
        total_scenarios = len(results)
        decisions = [r["response"].decision for r in results]
        confidences = [r["response"].confidence for r in results]
        processing_times = [r["processing_time"] for r in results]
        
        # Decision distribution
        decision_counts = {}
        for decision in decisions:
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        print(f"Total scenarios: {total_scenarios}")
        print(f"Average confidence: {sum(confidences) / len(confidences):.2%}")
        print(f"Average processing time: {sum(processing_times) / len(processing_times):.2f}s")
        print()
        
        print("Decision distribution:")
        for decision, count in decision_counts.items():
            percentage = (count / total_scenarios) * 100
            print(f"  • {decision}: {count} ({percentage:.1f}%)")
        
        print()
        print("Scenario results:")
        for i, result in enumerate(results, 1):
            scenario = result["scenario"]
            response = result["response"]
            print(f"  {i}. {scenario['name']}: {response.decision} ({response.confidence:.2%})")
    
    async def _show_agent_performance(self):
        """Show agent performance analysis"""
        status = await self.commander.get_agent_status()
        
        print("Agent Status:")
        print(f"  • Ethics Commander: {'✅ Active' if status['commander']['is_active'] else '❌ Inactive'}")
        
        for name, agent in status["debate_agents"].items():
            status_icon = "✅" if agent["is_active"] else "❌"
            print(f"  • {name}: {status_icon} Active (Responses: {agent['response_count']})")
        
        # Show audit summary
        audit_summary = self.audit_logger.get_audit_summary()
        print(f"\nAudit Summary:")
        print(f"  • Total logs: {audit_summary['total_logs']}")
        print(f"  • Total metrics: {audit_summary['total_metrics']}")
        print(f"  • Notion logging: {'✅ Enabled' if audit_summary['notion_enabled'] else '❌ Disabled'}")
        print(f"  • Cloudera streaming: {'✅ Enabled' if audit_summary['cloudera_enabled'] else '❌ Disabled'}")


async def main():
    """Main demo function"""
    demo = AutoEthosDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main()) 