#!/usr/bin/env python3
"""
Test script for agent improvement system
"""

from tools.agent_improvement_system import AgentImprovementSystem

def main():
    print("🚀 Testing EthIQ Agent Improvement System")
    print("=" * 50)
    
    try:
        # Initialize the system
        improvement_system = AgentImprovementSystem()
        
        # Analyze performance
        print("\n📊 Analyzing agent performance...")
        performance = improvement_system.analyze_agent_performance()
        
        print(f"✅ Loaded {len(improvement_system.test_cases)} test cases")
        print(f"✅ Analyzed {len(performance)} agents")
        
        # Show top agents
        print("\n🏆 Top performing agents:")
        rankings = improvement_system.get_agent_ranking()
        for i, (agent, score) in enumerate(rankings[:5], 1):
            stats = performance[agent]
            print(f"{i}. {agent}: {stats['success_rate']:.1f}% success")
        
        # Generate suggestions
        print("\n💡 Generating improvement suggestions...")
        suggestions = improvement_system.generate_improvement_suggestions()
        
        for agent, agent_suggestions in suggestions.items():
            if agent_suggestions:
                print(f"\n📝 {agent} improvements:")
                for suggestion in agent_suggestions[:3]:  # Show top 3
                    print(f"  - {suggestion}")
        
        # Export report
        print("\n📄 Exporting improvement report...")
        report = improvement_system.export_improvement_report()
        
        print(f"\n✅ Analysis complete!")
        print(f"📈 Overall success rate: {report['summary']['overall_success_rate']:.1f}%")
        print(f"📊 Report saved to: agent_improvement_report.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 