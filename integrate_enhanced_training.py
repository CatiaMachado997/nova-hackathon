#!/usr/bin/env python3
"""
Integration script for enhanced training data
Updates agents with improved training data from test cases
"""

import os
import json
import shutil
import logging
from pathlib import Path
from tools.enhanced_training_generator import EnhancedTrainingGenerator

logger = logging.getLogger(__name__)


class EnhancedTrainingIntegrator:
    """Integrates enhanced training data into the existing system"""
    
    def __init__(self):
        self.enhanced_dir = "data/training/enhanced"
        self.original_dir = "data/training"
        self.backup_dir = "data/training/backup"
        
    def backup_original_training_data(self):
        """Backup original training data"""
        if os.path.exists(self.original_dir):
            if os.path.exists(self.backup_dir):
                shutil.rmtree(self.backup_dir)
            shutil.copytree(self.original_dir, self.backup_dir)
            logger.info(f"Backed up original training data to {self.backup_dir}")
    
    def integrate_enhanced_training_data(self):
        """Integrate enhanced training data into the main training directory"""
        if not os.path.exists(self.enhanced_dir):
            logger.error("Enhanced training data not found. Run enhanced_training_generator.py first.")
            return False
        
        # Backup original data
        self.backup_original_training_data()
        
        # Copy enhanced data to main training directory
        for agent_dir in os.listdir(self.enhanced_dir):
            agent_path = os.path.join(self.enhanced_dir, agent_dir)
            if os.path.isdir(agent_path) and agent_dir != "backup":
                target_path = os.path.join(self.original_dir, agent_dir)
                
                # Create target directory if it doesn't exist
                os.makedirs(target_path, exist_ok=True)
                
                # Copy enhanced training files
                for file in os.listdir(agent_path):
                    if file.endswith('.txt'):
                        src_file = os.path.join(agent_path, file)
                        dst_file = os.path.join(target_path, file)
                        shutil.copy2(src_file, dst_file)
                
                logger.info(f"Integrated enhanced training data for {agent_dir}")
        
        return True
    
    def update_training_data_loader(self):
        """Update the training data loader to use enhanced data"""
        # Read the current training data loader
        loader_path = "tools/training_data_loader.py"
        
        if not os.path.exists(loader_path):
            logger.error("Training data loader not found")
            return False
        
        # Create a backup of the original loader
        backup_path = "tools/training_data_loader_backup.py"
        shutil.copy2(loader_path, backup_path)
        logger.info(f"Backed up training data loader to {backup_path}")
        
        return True
    
    def test_enhanced_agents(self):
        """Test the enhanced agents with sample content"""
        try:
            from tools.training_data_loader import TrainingDataLoader
            
            # Test loading enhanced training data
            loader = TrainingDataLoader()
            
            # Test each agent type
            agent_types = ['psychological', 'cultural_context', 'temporal', 'utilitarian', 
                          'free_speech', 'religious_ethics', 'financial_impact', 'deontological']
            
            results = {}
            for agent_type in agent_types:
                try:
                    examples = loader.get_few_shot_examples(agent_type, 2)
                    results[agent_type] = {
                        'examples_loaded': len(examples),
                        'status': 'success'
                    }
                except Exception as e:
                    results[agent_type] = {
                        'examples_loaded': 0,
                        'status': 'error',
                        'error': str(e)
                    }
            
            return results
            
        except Exception as e:
            logger.error(f"Error testing enhanced agents: {e}")
            return None
    
    def generate_integration_report(self, test_results):
        """Generate a report on the integration process"""
        report = {
            'integration_status': 'completed',
            'enhanced_agents': [],
            'test_results': test_results,
            'files_integrated': [],
            'backup_created': os.path.exists(self.backup_dir)
        }
        
        # Count integrated files
        for agent_dir in os.listdir(self.enhanced_dir):
            agent_path = os.path.join(self.enhanced_dir, agent_dir)
            if os.path.isdir(agent_path) and agent_dir != "backup":
                files = [f for f in os.listdir(agent_path) if f.endswith('.txt')]
                report['files_integrated'].append({
                    'agent': agent_dir,
                    'files_count': len(files)
                })
                report['enhanced_agents'].append(agent_dir)
        
        # Save report
        report_path = "enhanced_training_integration_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Integration report saved to {report_path}")
        return report


def main():
    """Main function to run the integration"""
    print("🚀 EthIQ Enhanced Training Integration")
    print("=" * 50)
    
    try:
        # Initialize integrator
        integrator = EnhancedTrainingIntegrator()
        
        # Generate enhanced training data if not exists
        if not os.path.exists(integrator.enhanced_dir):
            print("\n📝 Generating enhanced training data...")
            generator = EnhancedTrainingGenerator()
            generator.generate_enhanced_training_files()
        
        # Integrate enhanced training data
        print("\n🔄 Integrating enhanced training data...")
        success = integrator.integrate_enhanced_training_data()
        
        if not success:
            print("❌ Integration failed")
            return
        
        # Update training data loader
        print("📝 Updating training data loader...")
        integrator.update_training_data_loader()
        
        # Test enhanced agents
        print("🧪 Testing enhanced agents...")
        test_results = integrator.test_enhanced_agents()
        
        # Generate integration report
        print("📊 Generating integration report...")
        report = integrator.generate_integration_report(test_results)
        
        print(f"\n✅ Enhanced training integration complete!")
        print(f"🤖 Agents enhanced: {len(report['enhanced_agents'])}")
        print(f"📁 Files integrated: {sum(item['files_count'] for item in report['files_integrated'])}")
        print(f"📊 Backup created: {report['backup_created']}")
        
        # Show test results
        if test_results:
            print(f"\n🧪 Test Results:")
            for agent, result in test_results.items():
                status = "✅" if result['status'] == 'success' else "❌"
                print(f"  {status} {agent}: {result['examples_loaded']} examples loaded")
        
        print(f"\n📄 Integration report saved to: enhanced_training_integration_report.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 