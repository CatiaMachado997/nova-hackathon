#!/usr/bin/env python3
"""
Demo script showing how to use training data with EthIQ agents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.training_data_loader import TrainingDataLoader, create_agent_prompt

def demo_training_data_usage():
    """Demonstrate how to use training data with agents"""
    
    print("🤖 EthIQ Agent Training Data Demo")
    print("=" * 50)
    
    # Initialize training data loader
    loader = TrainingDataLoader()
    
    # Show training statistics
    print("\n📊 Training Data Statistics:")
    stats = loader.get_training_stats()
    for agent, stat in stats.items():
        print(f"  {agent.upper()}: {stat['total_examples']} examples "
              f"({stat['flagged_examples']} flagged, {stat['approved_examples']} approved)")
    
    # Test content to analyze
    test_contents = [
        "Let's organize a peaceful climate protest to raise awareness about environmental issues.",
        "We should lie to customers about our product's safety to increase sales.",
        "Let's celebrate diverse cultural traditions in our workplace.",
        "We should coordinate a harassment campaign against our critics."
    ]
    
    # Agent types
    agent_types = ["utilitarian", "deontological", "cultural_context", "free_speech"]
    
    print(f"\n🧪 Testing {len(test_contents)} content examples with training data...")
    
    for i, content in enumerate(test_contents, 1):
        print(f"\n--- Test Content {i} ---")
        print(f"Content: {content}")
        
        for agent_type in agent_types:
            # Create prompt with training examples
            prompt = create_agent_prompt(agent_type, content, num_examples=2)
            
            # For demo purposes, we'll show the prompt structure
            # In real usage, you would send this to an LLM
            print(f"\n{agent_type.upper()} Agent Prompt (first 200 chars):")
            print(f"  {prompt[:200]}...")
            
            # Simulate agent response (in real implementation, this would call an LLM)
            print(f"  [Agent would analyze with training examples]")
    
    print(f"\n✅ Demo completed!")
    print(f"\n💡 To use with real LLMs:")
    print(f"   1. Send the generated prompts to your chosen LLM (OpenAI, Anthropic, etc.)")
    print(f"   2. Parse the LLM response to extract decision, confidence, and reasoning")
    print(f"   3. Use the structured output in your moderation system")

def demo_prompt_generation():
    """Show how to generate prompts for different scenarios"""
    
    print("\n🎯 Prompt Generation Examples")
    print("=" * 30)
    
    # Example 1: Controversial content
    content1 = "We should use violence to achieve our political goals."
    prompt1 = create_agent_prompt("utilitarian", content1)
    print(f"\nUtilitarian analysis of violent content:")
    print(f"Prompt length: {len(prompt1)} characters")
    print(f"First 150 chars: {prompt1[:150]}...")
    
    # Example 2: Cultural content
    content2 = "Let's respectfully learn about and celebrate Indigenous traditions."
    prompt2 = create_agent_prompt("cultural_context", content2)
    print(f"\nCultural context analysis of respectful content:")
    print(f"Prompt length: {len(prompt2)} characters")
    print(f"First 150 chars: {prompt2[:150]}...")

if __name__ == "__main__":
    demo_training_data_usage()
    demo_prompt_generation() 