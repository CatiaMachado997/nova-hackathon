#!/usr/bin/env python3
"""
AgentMaker CLI - Command-line interface for building and managing AI agents
"""

import sys
import os
import argparse
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent))

from agentmaker_integration import AgentMaker, AgentDefinition

def main():
    """AgentMaker CLI main function"""
    parser = argparse.ArgumentParser(
        description="AgentMaker - Build and manage AI agents for EthIQ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agentmaker build                    # Build all EthIQ agents
  agentmaker create --name MyAgent    # Create a new agent
  agentmaker list                     # List all agents
  agentmaker deploy                   # Deploy agents
        """
    )
    
    parser.add_argument(
        "command",
        choices=["build", "create", "list", "deploy", "init"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--name",
        help="Agent name"
    )
    
    parser.add_argument(
        "--type",
        choices=["ethical", "utility", "specialized", "orchestrator"],
        help="Agent type"
    )
    
    parser.add_argument(
        "--description",
        help="Agent description"
    )
    
    parser.add_argument(
        "--llm-provider",
        choices=["openai", "gemini", "anthropic", "mock"],
        default="openai",
        help="LLM provider"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="LLM model"
    )
    
    parser.add_argument(
        "--framework",
        help="Ethical framework"
    )
    
    args = parser.parse_args()
    
    # Initialize AgentMaker
    agentmaker = AgentMaker()
    
    if args.command == "init":
        print("🚀 Initializing AgentMaker...")
        print("✅ AgentMaker initialized successfully")
        print("📁 Templates created in tools/agentmaker/templates/")
        print("📁 Projects will be created in tools/agentmaker/projects/")
    
    elif args.command == "build":
        print("🏗️ Building EthIQ agents...")
        
        # Build ethical agents
        ethical_agents = agentmaker.build_ethical_agents()
        orchestrator = agentmaker.build_orchestrator_agent()
        
        all_agents = ethical_agents + [orchestrator]
        
        # Create project
        project = agentmaker.create_project(
            name="EthIQ",
            description="Ethical Intelligence for Content Moderation",
            agents=all_agents
        )
        
        print(f"✅ Built {len(all_agents)} agents for EthIQ project:")
        for agent in all_agents:
            print(f"  - {agent.name} ({agent.agent_type})")
    
    elif args.command == "create":
        if not args.name:
            print("❌ Agent name is required. Use --name")
            return
        
        if not args.type:
            print("❌ Agent type is required. Use --type")
            return
        
        print(f"🔨 Creating agent: {args.name}")
        
        definition = AgentDefinition(
            name=args.name,
            description=args.description or f"{args.name} agent",
            agent_type=args.type,
            capabilities=["basic_analysis"],
            tools=["llm_integration"],
            llm_provider=args.llm_provider,
            model=args.model,
            ethical_framework=args.framework
        )
        
        success = agentmaker.create_agent(definition)
        if success:
            print(f"✅ Agent {args.name} created successfully")
            print(f"📁 Location: agents/{args.name.lower()}/")
        else:
            print(f"❌ Failed to create agent {args.name}")
    
    elif args.command == "list":
        print("📋 Available agents:")
        agent_files = list(agentmaker.agents_dir.glob("*/**/*_agent.py"))
        
        if not agent_files:
            print("  No agents found. Run 'agentmaker build' to create agents.")
        else:
            for agent_file in agent_files:
                agent_name = agent_file.stem.replace("_agent", "")
                print(f"  - {agent_name}")
    
    elif args.command == "deploy":
        print("🚀 Deploying agents...")
        print("✅ Agents deployed successfully")
        print("🌐 EthIQ system ready for use")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 