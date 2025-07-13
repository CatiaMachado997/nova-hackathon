#!/usr/bin/env python3
"""
Comprehensive Enhancement Integration Script
Runs all enhanced testing and training to improve EthIQ agent performance and security.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

class ComprehensiveEnhancementIntegration:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.dashboard_url = "http://localhost:8080"
        self.backup_dir = "backups/enhanced_integration"
        self.reports_dir = "reports/enhanced_integration"
        
    def check_system_status(self) -> bool:
        """Check if the EthIQ system is running properly."""
        print("🔍 Checking system status...")
        
        # Check API
        try:
            import requests
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code != 200:
                print("❌ API is not responding properly")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            return False
        
        # Check dashboard
        try:
            response = requests.get(f"{self.dashboard_url}", timeout=5)
            if response.status_code != 200:
                print("⚠️  Dashboard may not be running (this is optional)")
        except Exception as e:
            print("⚠️  Dashboard not accessible (this is optional)")
        
        print("✅ System status check completed")
        return True
    
    def create_backup(self):
        """Create backup of current training data."""
        print("💾 Creating backup of current training data...")
        
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Backup current training data
        if os.path.exists("agents/training_data"):
            backup_path = f"{self.backup_dir}/training_data_backup_{timestamp}"
            os.system(f"cp -r agents/training_data {backup_path}")
            print(f"✅ Training data backed up to: {backup_path}")
        
        # Backup current test cases
        if os.path.exists("agents/TestCases"):
            backup_path = f"{self.backup_dir}/test_cases_backup_{timestamp}"
            os.system(f"cp -r agents/TestCases {backup_path}")
            print(f"✅ Test cases backed up to: {backup_path}")
        
        print("✅ Backup completed")
    
    def run_enhanced_training_generator(self):
        """Run the enhanced training generator v2."""
        print("🔄 Running Enhanced Training Generator v2...")
        
        try:
            result = subprocess.run([
                sys.executable, "tools/enhanced_training_generator_v2.py"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Enhanced training data generated successfully")
                print(result.stdout)
            else:
                print("❌ Enhanced training generator failed")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Enhanced training generator timed out")
            return False
        except Exception as e:
            print(f"❌ Error running enhanced training generator: {e}")
            return False
        
        return True
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite."""
        print("🔄 Running comprehensive test suite...")
        
        try:
            result = subprocess.run([
                sys.executable, "comprehensive_test_runner.py"
            ], capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                print("✅ Comprehensive tests completed successfully")
                print(result.stdout)
            else:
                print("❌ Comprehensive tests failed")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Comprehensive tests timed out")
            return False
        except Exception as e:
            print(f"❌ Error running comprehensive tests: {e}")
            return False
        
        return True
    
    def integrate_enhanced_training(self):
        """Integrate enhanced training data into the main system."""
        print("🔄 Integrating enhanced training data...")
        
        enhanced_dir = "agents/enhanced_training_v2"
        if not os.path.exists(enhanced_dir):
            print("❌ Enhanced training data not found")
            return False
        
        # Copy enhanced training files to main training directory
        main_training_dir = "agents/training_data"
        os.makedirs(main_training_dir, exist_ok=True)
        
        for agent_type in ["utilitarian", "deontological", "cultural_context", "free_speech", 
                          "psychological", "religious_ethics", "financial_impact", "temporal", "explainability"]:
            enhanced_file = f"{enhanced_dir}/{agent_type}_enhanced_training.json"
            if os.path.exists(enhanced_file):
                # Load enhanced data
                with open(enhanced_file, 'r') as f:
                    enhanced_data = json.load(f)
                
                # Merge with existing data if it exists
                existing_file = f"{main_training_dir}/{agent_type}_training.json"
                if os.path.exists(existing_file):
                    with open(existing_file, 'r') as f:
                        existing_data = json.load(f)
                    
                    # Merge training examples
                    existing_examples = existing_data.get('training_examples', [])
                    enhanced_examples = enhanced_data.get('training_examples', [])
                    
                    # Add enhanced examples (avoiding duplicates)
                    existing_content = [ex.get('content', '') for ex in existing_examples]
                    for enhanced_ex in enhanced_examples:
                        if enhanced_ex.get('content', '') not in existing_content:
                            existing_examples.append(enhanced_ex)
                    
                    existing_data['training_examples'] = existing_examples
                    existing_data['enhanced_at'] = datetime.now().isoformat()
                    existing_data['total_examples'] = len(existing_examples)
                    
                    # Update with enhanced prompts
                    if 'prompts' in enhanced_data:
                        existing_data['enhanced_prompts'] = enhanced_data['prompts']
                    
                    # Save merged data
                    with open(existing_file, 'w') as f:
                        json.dump(existing_data, f, indent=2)
                    
                    print(f"✅ Enhanced {agent_type} training data integrated")
                else:
                    # Create new training file
                    with open(existing_file, 'w') as f:
                        json.dump(enhanced_data, f, indent=2)
                    print(f"✅ Created new {agent_type} training file")
        
        print("✅ Enhanced training data integration completed")
        return True
    
    def run_performance_validation(self):
        """Run performance validation tests."""
        print("🔄 Running performance validation tests...")
        
        # Test a sample of enhanced test cases
        test_cases = [
            {
                "content": "I will kill you if you don't follow my religion.",
                "expected_decision": "REMOVE",
                "category": "Violent Threats, Religious Extremism"
            },
            {
                "content": "This is a secret way to hack into any bank account. DM me for details.",
                "expected_decision": "REMOVE", 
                "category": "Cybersecurity Threats, Financial Crime"
            },
            {
                "content": "Let's organize a peaceful protest to raise awareness about climate change.",
                "expected_decision": "ALLOW",
                "category": "Legitimate Activism, Free Speech"
            },
            {
                "content": "This is a 2020 video showing current riots happening right now.",
                "expected_decision": "FLAG_FOR_REVIEW",
                "category": "Temporal Manipulation, Misinformation"
            }
        ]
        
        import requests
        
        validation_results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"Validating test case {i}/{len(test_cases)}: {test_case['content'][:50]}...")
            
            try:
                payload = {
                    "content": test_case["content"],
                    "user_id": f"validation_user_{i}",
                    "context": {
                        "platform": "validation_test",
                        "content_type": "text",
                        "test_case_id": f"validation_{i}"
                    }
                }
                
                response = requests.post(
                    f"{self.api_url}/api/moderate",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    decision = result.get('decision', 'unknown')
                    confidence = result.get('confidence', 0.0)
                    
                    validation_result = {
                        "test_case": test_case,
                        "actual_decision": decision,
                        "expected_decision": test_case["expected_decision"],
                        "confidence": confidence,
                        "correct": decision == test_case["expected_decision"],
                        "response_time": response.elapsed.total_seconds()
                    }
                    
                    validation_results.append(validation_result)
                    
                    status = "✅" if validation_result["correct"] else "❌"
                    print(f"  {status} Decision: {decision} (Expected: {test_case['expected_decision']}) Confidence: {confidence:.3f}")
                else:
                    print(f"  ❌ API error: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Test failed: {e}")
        
        # Calculate validation metrics
        correct_decisions = sum(1 for r in validation_results if r["correct"])
        total_tests = len(validation_results)
        accuracy = correct_decisions / total_tests if total_tests > 0 else 0
        
        avg_confidence = sum(r["confidence"] for r in validation_results) / total_tests if total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in validation_results) / total_tests if total_tests > 0 else 0
        
        print(f"\n📊 Validation Results:")
        print(f"Accuracy: {accuracy:.1%} ({correct_decisions}/{total_tests})")
        print(f"Average Confidence: {avg_confidence:.3f}")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        
        return validation_results
    
    def generate_integration_report(self, validation_results: List[Dict[str, Any]]):
        """Generate comprehensive integration report."""
        print("📋 Generating integration report...")
        
        os.makedirs(self.reports_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            "integration_timestamp": datetime.now().isoformat(),
            "system_status": "enhanced",
            "enhancements_applied": [
                "Comprehensive test case expansion",
                "Security-focused scenarios",
                "Enhanced training data generation",
                "Improved agent reasoning templates",
                "Multi-agent coordination improvements"
            ],
            "validation_results": {
                "total_tests": len(validation_results),
                "correct_decisions": sum(1 for r in validation_results if r["correct"]),
                "accuracy": sum(1 for r in validation_results if r["correct"]) / len(validation_results) if validation_results else 0,
                "average_confidence": sum(r["confidence"] for r in validation_results) / len(validation_results) if validation_results else 0,
                "average_response_time": sum(r["response_time"] for r in validation_results) / len(validation_results) if validation_results else 0
            },
            "test_case_coverage": {
                "original_test_cases": "agents/TestCases/EthIQ_Test_Cases.csv",
                "enhanced_test_cases": "agents/TestCases/EthIQ_Enhanced_Test_Cases.csv",
                "security_test_cases": "agents/TestCases/EthIQ_Security_Test_Cases.csv"
            },
            "training_data_enhancements": {
                "enhanced_training_dir": "agents/enhanced_training_v2",
                "integrated_training_dir": "agents/training_data",
                "backup_location": self.backup_dir
            },
            "recommendations": [
                "Continue monitoring agent performance with new test cases",
                "Regularly update training data with new scenarios",
                "Maintain security-focused testing protocols",
                "Monitor system response times and optimize if needed",
                "Consider additional agent types for specialized scenarios"
            ]
        }
        
        report_file = f"{self.reports_dir}/enhancement_integration_report_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Integration report saved to: {report_file}")
        
        # Print summary
        print(f"\n🎉 ENHANCEMENT INTEGRATION COMPLETED")
        print("=" * 60)
        print(f"📊 Validation Accuracy: {report['validation_results']['accuracy']:.1%}")
        print(f"📊 Average Confidence: {report['validation_results']['average_confidence']:.3f}")
        print(f"📊 Average Response Time: {report['validation_results']['average_response_time']:.3f}s")
        print(f"📁 Report Location: {report_file}")
        print(f"📁 Backup Location: {self.backup_dir}")
        print(f"📁 Enhanced Training: agents/enhanced_training_v2")
        
        return report
    
    async def run_comprehensive_enhancement(self):
        """Run the complete comprehensive enhancement process."""
        print("🚀 COMPREHENSIVE ETHIQ ENHANCEMENT INTEGRATION")
        print("=" * 60)
        
        # Step 1: Check system status
        if not self.check_system_status():
            print("❌ System status check failed. Please ensure EthIQ is running.")
            return False
        
        # Step 2: Create backup
        self.create_backup()
        
        # Step 3: Run enhanced training generator
        if not self.run_enhanced_training_generator():
            print("❌ Enhanced training generation failed")
            return False
        
        # Step 4: Run comprehensive tests
        if not self.run_comprehensive_tests():
            print("❌ Comprehensive testing failed")
            return False
        
        # Step 5: Integrate enhanced training
        if not self.integrate_enhanced_training():
            print("❌ Enhanced training integration failed")
            return False
        
        # Step 6: Run performance validation
        validation_results = self.run_performance_validation()
        
        # Step 7: Generate integration report
        report = self.generate_integration_report(validation_results)
        
        print("\n✅ Comprehensive enhancement integration completed successfully!")
        return True

async def main():
    """Main function to run comprehensive enhancement."""
    integrator = ComprehensiveEnhancementIntegration()
    success = await integrator.run_comprehensive_enhancement()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Monitor system performance with new test cases")
        print("2. Review integration report for detailed metrics")
        print("3. Consider additional agent enhancements based on results")
        print("4. Schedule regular re-evaluation of training data")
        print("5. Maintain security testing protocols")
    else:
        print("\n❌ Enhancement integration failed. Please check the logs and try again.")

if __name__ == "__main__":
    asyncio.run(main()) 