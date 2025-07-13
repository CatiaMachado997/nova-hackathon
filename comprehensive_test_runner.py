#!/usr/bin/env python3
"""
Comprehensive Test Runner for EthIQ Agent Performance Enhancement
Tests all enhanced and security test cases to improve agent performance and stability.
"""

import asyncio
import csv
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import requests
import pandas as pd

class ComprehensiveTestRunner:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.test_results = []
        self.performance_metrics = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "average_response_time": 0,
            "agent_performance": {},
            "decision_distribution": {},
            "confidence_scores": []
        }
        
    def load_test_cases(self, file_path: str) -> List[Dict[str, Any]]:
        """Load test cases from CSV file."""
        test_cases = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    if row.get('Sample Text'):  # Skip empty rows
                        test_cases.append(row)
            print(f"✅ Loaded {len(test_cases)} test cases from {file_path}")
            return test_cases
        except Exception as e:
            print(f"❌ Error loading test cases from {file_path}: {e}")
            return []
    
    def check_api_health(self) -> bool:
        """Check if the EthIQ API is running and healthy."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy":
                    print("✅ EthIQ API is healthy and running")
                    return True
            print("❌ EthIQ API is not healthy")
            return False
        except Exception as e:
            print(f"❌ Cannot connect to EthIQ API: {e}")
            return False
    
    async def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case against the EthIQ API."""
        start_time = time.time()
        
        try:
            # Prepare the moderation request
            payload = {
                "content": test_case["Sample Text"],
                "user_id": f"test_user_{test_case.get('ID', 'unknown')}",
                "context": {
                    "platform": "test_platform",
                    "content_type": "text",
                    "test_case_id": test_case.get('ID', 'unknown')
                }
            }
            
            # Send request to API
            response = requests.post(
                f"{self.api_url}/api/moderate",
                json=payload,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "test_id": test_case.get('ID', 'unknown'),
                    "content": test_case["Sample Text"],
                    "category": test_case.get('Category/Theme', 'unknown'),
                    "expected_agents": test_case.get('Expected Agent(s) to Trigger', ''),
                    "api_response": result,
                    "response_time": response_time,
                    "status": "success",
                    "decision": result.get('decision', 'unknown'),
                    "confidence": result.get('confidence', 0.0),
                    "explanation": result.get('explanation', ''),
                    "agents_triggered": list(result.get('agent_analysis', {}).keys()) if result.get('agent_analysis') else []
                }
            else:
                return {
                    "test_id": test_case.get('ID', 'unknown'),
                    "content": test_case["Sample Text"],
                    "category": test_case.get('Category/Theme', 'unknown'),
                    "expected_agents": test_case.get('Expected Agent(s) to Trigger', ''),
                    "api_response": None,
                    "response_time": response_time,
                    "status": "error",
                    "error": f"API returned status {response.status_code}",
                    "decision": "unknown",
                    "confidence": 0.0,
                    "explanation": "",
                    "agents_triggered": []
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "test_id": test_case.get('ID', 'unknown'),
                "content": test_case["Sample Text"],
                "category": test_case.get('Category/Theme', 'unknown'),
                "expected_agents": test_case.get('Expected Agent(s) to Trigger', ''),
                "api_response": None,
                "response_time": response_time,
                "status": "error",
                "error": str(e),
                "decision": "unknown",
                "confidence": 0.0,
                "explanation": "",
                "agents_triggered": []
            }
    
    def analyze_test_result(self, test_case: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the result of a single test case."""
        analysis = {
            "test_id": result["test_id"],
            "content_preview": result["content"][:100] + "..." if len(result["content"]) > 100 else result["content"],
            "category": result["category"],
            "expected_agents": result["expected_agents"],
            "actual_agents": result["agents_triggered"],
            "decision": result["decision"],
            "confidence": result["confidence"],
            "response_time": result["response_time"],
            "status": result["status"]
        }
        
        # Analyze agent triggering
        expected_agent_list = [agent.strip() for agent in result["expected_agents"].split(",") if agent.strip()]
        actual_agent_list = result["agents_triggered"]
        
        # Check if expected agents were triggered
        triggered_expected = [agent for agent in expected_agent_list if any(expected in agent for expected in expected_agent_list)]
        analysis["expected_agents_triggered"] = len(triggered_expected)
        analysis["expected_agents_total"] = len(expected_agent_list)
        analysis["agent_trigger_accuracy"] = len(triggered_expected) / len(expected_agent_list) if expected_agent_list else 0
        
        # Analyze decision appropriateness
        category = result["category"].lower()
        decision = result["decision"]
        
        # Define expected decisions for different categories
        expected_decisions = {
            "violent threats": ["REMOVE", "FLAG_FOR_REVIEW"],
            "hate speech": ["REMOVE", "FLAG_FOR_REVIEW"],
            "discrimination": ["REMOVE", "FLAG_FOR_REVIEW"],
            "misinformation": ["FLAG_FOR_REVIEW", "REMOVE"],
            "financial crime": ["REMOVE", "FLAG_FOR_REVIEW"],
            "cybersecurity": ["REMOVE", "FLAG_FOR_REVIEW"],
            "national security": ["REMOVE"],
            "terrorism": ["REMOVE"],
            "legitimate": ["ALLOW"],
            "free speech": ["ALLOW"],
            "educational": ["ALLOW"],
            "news": ["ALLOW"],
            "satire": ["ALLOW"]
        }
        
        expected_decision = None
        for key, decisions in expected_decisions.items():
            if key in category:
                expected_decision = decisions[0]  # Take the first expected decision
                break
        
        analysis["expected_decision"] = expected_decision
        analysis["decision_correct"] = decision == expected_decision if expected_decision else None
        analysis["decision_confidence"] = result["confidence"] if result["confidence"] else 0.0
        
        return analysis
    
    async def run_comprehensive_tests(self):
        """Run comprehensive tests on all test case files."""
        print("🚀 Starting Comprehensive EthIQ Agent Performance Test")
        print("=" * 60)
        
        # Check API health
        if not self.check_api_health():
            print("❌ Cannot proceed without a healthy API")
            return
        
        # Load all test case files
        test_files = [
            "agents/TestCases/EthIQ_Test_Cases.csv",
            "agents/TestCases/EthIQ_Enhanced_Test_Cases.csv", 
            "agents/TestCases/EthIQ_Security_Test_Cases.csv"
        ]
        
        all_test_cases = []
        for file_path in test_files:
            test_cases = self.load_test_cases(file_path)
            all_test_cases.extend(test_cases)
        
        print(f"📊 Total test cases loaded: {len(all_test_cases)}")
        
        # Run tests
        print("\n🔄 Running comprehensive tests...")
        start_time = time.time()
        
        for i, test_case in enumerate(all_test_cases, 1):
            print(f"Testing {i}/{len(all_test_cases)}: {test_case.get('ID', 'unknown')} - {test_case['Sample Text'][:50]}...")
            
            result = await self.run_single_test(test_case)
            analysis = self.analyze_test_result(test_case, result)
            
            self.test_results.append(analysis)
            
            # Update performance metrics
            self.performance_metrics["total_tests"] += 1
            if result["status"] == "success":
                self.performance_metrics["passed_tests"] += 1
            else:
                self.performance_metrics["failed_tests"] += 1
            
            # Track response times
            self.performance_metrics["confidence_scores"].append(result.get("confidence", 0.0))
            
            # Track decision distribution
            decision = result.get("decision", "unknown")
            self.performance_metrics["decision_distribution"][decision] = self.performance_metrics["decision_distribution"].get(decision, 0) + 1
            
            # Track agent performance
            for agent in result.get("agents_triggered", []):
                if agent not in self.performance_metrics["agent_performance"]:
                    self.performance_metrics["agent_performance"][agent] = {"triggered": 0, "successful": 0}
                self.performance_metrics["agent_performance"][agent]["triggered"] += 1
        
        total_time = time.time() - start_time
        self.performance_metrics["average_response_time"] = total_time / len(all_test_cases)
        
        print(f"\n✅ Comprehensive testing completed in {total_time:.2f} seconds")
        
        # Generate reports
        self.generate_performance_report()
        self.generate_detailed_report()
        self.generate_improvement_recommendations()
    
    def generate_performance_report(self):
        """Generate a performance summary report."""
        print("\n📊 PERFORMANCE SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = self.performance_metrics["total_tests"]
        passed_tests = self.performance_metrics["passed_tests"]
        failed_tests = self.performance_metrics["failed_tests"]
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed Tests: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Failed Tests: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"Average Response Time: {self.performance_metrics['average_response_time']:.3f} seconds")
        
        if self.performance_metrics["confidence_scores"]:
            avg_confidence = sum(self.performance_metrics["confidence_scores"]) / len(self.performance_metrics["confidence_scores"])
            print(f"Average Confidence Score: {avg_confidence:.3f}")
        
        print(f"\nDecision Distribution:")
        for decision, count in self.performance_metrics["decision_distribution"].items():
            percentage = count / total_tests * 100
            print(f"  {decision}: {count} ({percentage:.1f}%)")
        
        print(f"\nAgent Performance:")
        for agent, stats in self.performance_metrics["agent_performance"].items():
            print(f"  {agent}: Triggered {stats['triggered']} times")
    
    def generate_detailed_report(self):
        """Generate a detailed analysis report."""
        print("\n📋 DETAILED ANALYSIS REPORT")
        print("=" * 60)
        
        # Analyze decision accuracy
        correct_decisions = [r for r in self.test_results if r.get("decision_correct") is True]
        incorrect_decisions = [r for r in self.test_results if r.get("decision_correct") is False]
        unclear_decisions = [r for r in self.test_results if r.get("decision_correct") is None]
        
        print(f"Decision Accuracy Analysis:")
        print(f"  Correct Decisions: {len(correct_decisions)} ({len(correct_decisions)/len(self.test_results)*100:.1f}%)")
        print(f"  Incorrect Decisions: {len(incorrect_decisions)} ({len(incorrect_decisions)/len(self.test_results)*100:.1f}%)")
        print(f"  Unclear/No Expected: {len(unclear_decisions)} ({len(unclear_decisions)/len(self.test_results)*100:.1f}%)")
        
        # Analyze agent triggering accuracy
        agent_trigger_scores = [r.get("agent_trigger_accuracy", 0) for r in self.test_results]
        avg_agent_accuracy = sum(agent_trigger_scores) / len(agent_trigger_scores) if agent_trigger_scores else 0
        print(f"\nAgent Triggering Accuracy: {avg_agent_accuracy:.3f}")
        
        # Show problematic test cases
        print(f"\nProblematic Test Cases (Low Confidence or Incorrect Decisions):")
        problematic = [r for r in self.test_results if r.get("confidence", 0) < 0.5 or r.get("decision_correct") is False]
        
        for i, test in enumerate(problematic[:10], 1):  # Show top 10
            print(f"  {i}. {test['test_id']}: {test['content_preview']}")
            print(f"     Decision: {test['decision']} (Expected: {test.get('expected_decision', 'unknown')})")
            print(f"     Confidence: {test.get('confidence', 0):.3f}")
            print()
    
    def generate_improvement_recommendations(self):
        """Generate improvement recommendations based on test results."""
        print("\n🔧 IMPROVEMENT RECOMMENDATIONS")
        print("=" * 60)
        
        recommendations = []
        
        # Analyze decision patterns
        decision_dist = self.performance_metrics["decision_distribution"]
        if decision_dist.get("ALLOW", 0) > decision_dist.get("REMOVE", 0) * 2:
            recommendations.append("⚠️  System may be too permissive - consider adjusting thresholds for REMOVE decisions")
        
        if decision_dist.get("REMOVE", 0) > decision_dist.get("ALLOW", 0) * 2:
            recommendations.append("⚠️  System may be too restrictive - consider adjusting thresholds for ALLOW decisions")
        
        # Analyze confidence scores
        low_confidence_tests = [r for r in self.test_results if r.get("confidence", 0) < 0.3]
        if len(low_confidence_tests) > len(self.test_results) * 0.2:
            recommendations.append("⚠️  High number of low-confidence decisions - consider improving training data")
        
        # Analyze agent triggering
        agent_performance = self.performance_metrics["agent_performance"]
        for agent, stats in agent_performance.items():
            if stats["triggered"] < 5:
                recommendations.append(f"⚠️  {agent} triggered very rarely - consider reviewing training data")
        
        # Analyze response times
        if self.performance_metrics["average_response_time"] > 2.0:
            recommendations.append("⚠️  Slow response times - consider optimizing agent processing")
        
        # Security-specific recommendations
        security_tests = [r for r in self.test_results if "security" in r.get("category", "").lower()]
        if security_tests:
            security_failures = [r for r in security_tests if r.get("decision") == "ALLOW"]
            if len(security_failures) > 0:
                recommendations.append("🚨 CRITICAL: Security-related content incorrectly allowed - immediate review required")
        
        if not recommendations:
            recommendations.append("✅ System performance appears good - continue monitoring")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"comprehensive_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "performance_metrics": self.performance_metrics,
                "test_results": self.test_results,
                "recommendations": recommendations
            }, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {results_file}")

async def main():
    """Main function to run comprehensive tests."""
    runner = ComprehensiveTestRunner()
    await runner.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main()) 