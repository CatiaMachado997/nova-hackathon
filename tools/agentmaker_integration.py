#!/usr/bin/env python3
"""
AgentMaker Integration for EthIQ
A comprehensive agent building and management system
"""

import os
import json
import yaml
import logging
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import shutil
import subprocess

logger = logging.getLogger(__name__)


@dataclass
class AgentDefinition:
    """Definition for an AI agent"""
    name: str
    description: str
    agent_type: str  # 'ethical', 'utility', 'specialized', 'orchestrator'
    capabilities: List[str]
    tools: List[str]
    llm_provider: str  # 'openai', 'gemini', 'anthropic', 'mock'
    model: str
    training_data_path: Optional[str] = None
    ethical_framework: Optional[str] = None
    dependencies: List[str] = None
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.config is None:
            self.config = {}


@dataclass
class AgentProject:
    """Agent project structure"""
    name: str
    description: str
    version: str
    agents: List[AgentDefinition]
    project_config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class AgentMaker:
    """AgentMaker - Agent building and management system"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.agents_dir = self.project_root / "agents"
        self.templates_dir = self.project_root / "tools" / "agentmaker" / "templates"
        self.projects_dir = self.project_root / "tools" / "agentmaker" / "projects"
        
        # Ensure directories exist
        self.agents_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize templates
        self._init_templates()
    
    def _init_templates(self):
        """Initialize agent templates"""
        templates = {
            "ethical_agent.py": self._get_ethical_agent_template(),
            "utility_agent.py": self._get_utility_agent_template(),
            "specialized_agent.py": self._get_specialized_agent_template(),
            "orchestrator_agent.py": self._get_orchestrator_agent_template(),
            "agent_config.yaml": self._get_config_template(),
            "requirements.txt": self._get_requirements_template(),
            "README.md": self._get_readme_template()
        }
        
        for filename, content in templates.items():
            template_path = self.templates_dir / filename
            if not template_path.exists():
                template_path.write_text(content)
    
    def create_agent(self, definition: AgentDefinition) -> bool:
        """Create a new agent based on definition"""
        try:
            logger.info(f"Creating agent: {definition.name}")
            
            # Create agent directory
            agent_dir = self.agents_dir / definition.name.lower()
            agent_dir.mkdir(exist_ok=True)
            
            # Generate agent code
            agent_code = self._generate_agent_code(definition)
            agent_file = agent_dir / f"{definition.name.lower()}_agent.py"
            agent_file.write_text(agent_code)
            
            # Generate config
            config = self._generate_agent_config(definition)
            config_file = agent_dir / "config.yaml"
            config_file.write_text(yaml.dump(config, default_flow_style=False))
            
            # Generate requirements
            requirements = self._generate_requirements(definition)
            req_file = agent_dir / "requirements.txt"
            req_file.write_text(requirements)
            
            # Generate README
            readme = self._generate_readme(definition)
            readme_file = agent_dir / "README.md"
            readme_file.write_text(readme)
            
            # Create __init__.py
            init_file = agent_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""Agent: {definition.name}"""\n')
            
            logger.info(f"✅ Agent {definition.name} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent {definition.name}: {e}")
            return False
    
    def create_project(self, name: str, description: str, agents: List[AgentDefinition]) -> AgentProject:
        """Create a new agent project"""
        try:
            logger.info(f"Creating project: {name}")
            
            project = AgentProject(
                name=name,
                description=description,
                version="1.0.0",
                agents=agents,
                project_config={
                    "framework": "EthIQ",
                    "created_by": "AgentMaker",
                    "python_version": "3.8+"
                },
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Create project directory
            project_dir = self.projects_dir / name.lower()
            project_dir.mkdir(exist_ok=True)
            
            # Save project definition
            project_file = project_dir / "project.yaml"
            project_data = asdict(project)
            project_data["created_at"] = project.created_at.isoformat()
            project_data["updated_at"] = project.updated_at.isoformat()
            project_file.write_text(yaml.dump(project_data, default_flow_style=False))
            
            # Create agents
            for agent_def in agents:
                self.create_agent(agent_def)
            
            logger.info(f"✅ Project {name} created successfully")
            return project
            
        except Exception as e:
            logger.error(f"❌ Failed to create project {name}: {e}")
            raise
    
    def build_ethical_agents(self) -> List[AgentDefinition]:
        """Build the standard EthIQ ethical agents"""
        agents = [
            AgentDefinition(
                name="UtilitarianAgent",
                description="Agent applying utilitarian ethical reasoning (maximizing overall good)",
                agent_type="ethical",
                capabilities=["utility_analysis", "cost_benefit", "consequentialist_reasoning"],
                tools=["training_data_loader", "llm_integration"],
                llm_provider="openai",
                model="gpt-3.5-turbo",
                training_data_path="data/training/utilitarian",
                ethical_framework="Utilitarianism",
                dependencies=["openai", "pydantic"],
                config={"temperature": 0.2, "max_tokens": 512}
            ),
            AgentDefinition(
                name="DeontologicalAgent",
                description="Agent applying deontological (duty-based) ethical reasoning",
                agent_type="ethical",
                capabilities=["moral_duty", "rights_analysis", "rule_based_reasoning"],
                tools=["training_data_loader", "llm_integration"],
                llm_provider="openai",
                model="gpt-3.5-turbo",
                training_data_path="data/training/deontological",
                ethical_framework="Deontological Ethics",
                dependencies=["openai", "pydantic"],
                config={"temperature": 0.2, "max_tokens": 512}
            ),
            AgentDefinition(
                name="CulturalContextAgent",
                description="Agent considering cultural context and norms in ethical reasoning",
                agent_type="ethical",
                capabilities=["cultural_sensitivity", "context_analysis", "diversity_awareness"],
                tools=["training_data_loader", "llm_integration"],
                llm_provider="openai",
                model="gpt-3.5-turbo",
                training_data_path="data/training/cultural_context",
                ethical_framework="Cultural Context Ethics",
                dependencies=["openai", "pydantic"],
                config={"temperature": 0.2, "max_tokens": 512}
            ),
            AgentDefinition(
                name="FreeSpeechAgent",
                description="Agent prioritizing free speech and expression in ethical reasoning",
                agent_type="ethical",
                capabilities=["speech_rights", "expression_analysis", "censorship_evaluation"],
                tools=["training_data_loader", "llm_integration"],
                llm_provider="openai",
                model="gpt-3.5-turbo",
                training_data_path="data/training/free_speech",
                ethical_framework="Free Speech Ethics",
                dependencies=["openai", "pydantic"],
                config={"temperature": 0.2, "max_tokens": 512}
            )
        ]
        return agents
    
    def build_orchestrator_agent(self) -> AgentDefinition:
        """Build the EthicsCommander orchestrator agent"""
        return AgentDefinition(
            name="EthicsCommander",
            description="Master agent that orchestrates ethical deliberation among specialist agents",
            agent_type="orchestrator",
            capabilities=["agent_orchestration", "consensus_building", "decision_synthesis"],
            tools=["agent_communication", "consensus_algorithm", "decision_framework"],
            llm_provider="openai",
            model="gpt-4",
            ethical_framework="Multi-Framework Orchestration",
            dependencies=["openai", "pydantic", "asyncio"],
            config={"temperature": 0.1, "max_tokens": 1024}
        )
    
    def _generate_agent_code(self, definition: AgentDefinition) -> str:
        """Generate agent code from template"""
        template = self.templates_dir / f"{definition.agent_type}_agent.py"
        if template.exists():
            code = template.read_text()
            # Replace placeholders
            code = code.replace("{{AGENT_NAME}}", definition.name)
            code = code.replace("{{AGENT_DESCRIPTION}}", definition.description)
            code = code.replace("{{ETHICAL_FRAMEWORK}}", definition.ethical_framework or "General Ethics")
            code = code.replace("{{LLM_PROVIDER}}", definition.llm_provider)
            code = code.replace("{{MODEL}}", definition.model)
            code = code.replace("{{CAPABILITIES}}", str(definition.capabilities))
            code = code.replace("{{TOOLS}}", str(definition.tools))
            return code
        else:
            return self._get_default_agent_template(definition)
    
    def _generate_agent_config(self, definition: AgentDefinition) -> Dict[str, Any]:
        """Generate agent configuration"""
        return {
            "agent": {
                "name": definition.name,
                "description": definition.description,
                "type": definition.agent_type,
                "ethical_framework": definition.ethical_framework,
                "capabilities": definition.capabilities,
                "tools": definition.tools
            },
            "llm": {
                "provider": definition.llm_provider,
                "model": definition.model,
                "config": definition.config
            },
            "training": {
                "data_path": definition.training_data_path,
                "examples_count": 10
            },
            "dependencies": definition.dependencies
        }
    
    def _generate_requirements(self, definition: AgentDefinition) -> str:
        """Generate requirements.txt for agent"""
        base_requirements = [
            "pydantic>=2.0.0",
            "asyncio",
            "logging",
            "typing"
        ]
        
        if definition.llm_provider == "openai":
            base_requirements.append("openai>=1.0.0")
        elif definition.llm_provider == "gemini":
            base_requirements.append("google-generativeai>=0.3.0")
        elif definition.llm_provider == "anthropic":
            base_requirements.append("anthropic>=0.7.0")
        
        # Add custom dependencies
        base_requirements.extend(definition.dependencies)
        
        return "\n".join(base_requirements)
    
    def _generate_readme(self, definition: AgentDefinition) -> str:
        """Generate README for agent"""
        return f"""# {definition.name}

{definition.description}

## Framework
{definition.ethical_framework}

## Capabilities
{chr(10).join(f"- {cap}" for cap in definition.capabilities)}

## Tools
{chr(10).join(f"- {tool}" for tool in definition.tools)}

## Configuration
- LLM Provider: {definition.llm_provider}
- Model: {definition.model}
- Training Data: {definition.training_data_path or "Not specified"}

## Usage
```python
from agents.{definition.name.lower()}_agent import {definition.name}

agent = {definition.name}()
response = await agent.deliberate(content, context)
```
"""
    
    def _get_ethical_agent_template(self) -> str:
        return '''"""
{{AGENT_NAME}} - {{AGENT_DESCRIPTION}}
"""

import asyncio
import logging
from typing import Dict, Any
from agents.base_agent import LLMEthicsAgent, AgentResponse

logger = logging.getLogger(__name__)


class {{AGENT_NAME}}(LLMEthicsAgent):
    """{{AGENT_DESCRIPTION}}"""
    
    def __init__(self):
        super().__init__(
            name="{{AGENT_NAME}}",
            description="{{AGENT_DESCRIPTION}}",
            ethical_framework="{{ETHICAL_FRAMEWORK}}",
            agent_type="{{AGENT_NAME.lower()}}"
        )
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform ethical deliberation using {{ETHICAL_FRAMEWORK}}"""
        
        # Build prompt with training examples
        prompt = self.build_prompt(content)
        
        # Get LLM response
        llm_response = self.call_llm(prompt)
        
        # Parse response
        decision, confidence = self._parse_decision_and_confidence(llm_response, content)
        evidence = self._extract_evidence(llm_response, content)
        
        return AgentResponse(
            decision=decision,
            confidence=confidence,
            reasoning=llm_response,
            supporting_evidence=evidence,
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
'''
    
    def _get_utility_agent_template(self) -> str:
        return '''"""
{{AGENT_NAME}} - {{AGENT_DESCRIPTION}}
"""

import asyncio
import logging
from typing import Dict, Any
from agents.base_agent import LLMEthicsAgent, AgentResponse

logger = logging.getLogger(__name__)


class {{AGENT_NAME}}(LLMEthicsAgent):
    """{{AGENT_DESCRIPTION}}"""
    
    def __init__(self):
        super().__init__(
            name="{{AGENT_NAME}}",
            description="{{AGENT_DESCRIPTION}}",
            ethical_framework="{{ETHICAL_FRAMEWORK}}",
            agent_type="{{AGENT_NAME.lower()}}"
        )
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform utility analysis"""
        
        # Build prompt with training examples
        prompt = self.build_prompt(content)
        
        # Get LLM response
        llm_response = self.call_llm(prompt)
        
        # Parse response
        decision, confidence = self._parse_decision_and_confidence(llm_response, content)
        evidence = self._extract_evidence(llm_response, content)
        
        return AgentResponse(
            decision=decision,
            confidence=confidence,
            reasoning=llm_response,
            supporting_evidence=evidence,
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
'''
    
    def _get_specialized_agent_template(self) -> str:
        return '''"""
{{AGENT_NAME}} - {{AGENT_DESCRIPTION}}
"""

import asyncio
import logging
from typing import Dict, Any
from agents.base_agent import LLMEthicsAgent, AgentResponse

logger = logging.getLogger(__name__)


class {{AGENT_NAME}}(LLMEthicsAgent):
    """{{AGENT_DESCRIPTION}}"""
    
    def __init__(self):
        super().__init__(
            name="{{AGENT_NAME}}",
            description="{{AGENT_DESCRIPTION}}",
            ethical_framework="{{ETHICAL_FRAMEWORK}}",
            agent_type="{{AGENT_NAME.lower()}}"
        )
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform specialized analysis"""
        
        # Build prompt with training examples
        prompt = self.build_prompt(content)
        
        # Get LLM response
        llm_response = self.call_llm(prompt)
        
        # Parse response
        decision, confidence = self._parse_decision_and_confidence(llm_response, content)
        evidence = self._extract_evidence(llm_response, content)
        
        return AgentResponse(
            decision=decision,
            confidence=confidence,
            reasoning=llm_response,
            supporting_evidence=evidence,
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
'''
    
    def _get_orchestrator_agent_template(self) -> str:
        return '''"""
{{AGENT_NAME}} - {{AGENT_DESCRIPTION}}
"""

import asyncio
import logging
from typing import Dict, Any, List
from agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class {{AGENT_NAME}}(BaseAgent):
    """{{AGENT_DESCRIPTION}}"""
    
    def __init__(self):
        super().__init__(
            name="{{AGENT_NAME}}",
            description="{{AGENT_DESCRIPTION}}",
            ethical_framework="{{ETHICAL_FRAMEWORK}}"
        )
        self.specialist_agents = {}
        self.active_tasks = {}
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process task by orchestrating specialist agents"""
        
        # Get specialist analyses
        specialist_responses = await self._get_specialist_analyses(
            task.get("content", ""),
            task.get("context", {}),
            task.get("task_id", "")
        )
        
        # Perform synthesis and judgment
        final_decision = await self._perform_synthesis_and_judgment(specialist_responses, task.get("task_id", ""))
        
        return final_decision
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform orchestrated deliberation"""
        task = {"content": content, "context": context}
        return await self.process_task(task)
    
    async def _get_specialist_analyses(self, content: str, context: Dict[str, Any], task_id: str) -> Dict[str, AgentResponse]:
        """Get analyses from specialist agents"""
        # Implementation for getting specialist analyses
        return {}
    
    async def _perform_synthesis_and_judgment(self, specialist_responses: Dict[str, AgentResponse], task_id: str) -> AgentResponse:
        """Perform synthesis and final judgment"""
        # Implementation for synthesis and judgment
        return AgentResponse(
            decision="ALLOW",
            confidence=0.8,
            reasoning="Synthesis complete",
            supporting_evidence=[],
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
'''
    
    def _get_config_template(self) -> str:
        return '''# Agent Configuration
agent:
  name: "{{AGENT_NAME}}"
  description: "{{AGENT_DESCRIPTION}}"
  type: "{{AGENT_TYPE}}"
  ethical_framework: "{{ETHICAL_FRAMEWORK}}"
  capabilities: {{CAPABILITIES}}
  tools: {{TOOLS}}

llm:
  provider: "{{LLM_PROVIDER}}"
  model: "{{MODEL}}"
  config:
    temperature: 0.2
    max_tokens: 512

training:
  data_path: "data/training/{{AGENT_NAME.lower()}}"
  examples_count: 10

dependencies:
  - pydantic>=2.0.0
  - asyncio
  - logging
'''
    
    def _get_requirements_template(self) -> str:
        return '''# Agent Requirements
pydantic>=2.0.0
asyncio
logging
typing
openai>=1.0.0
google-generativeai>=0.3.0
anthropic>=0.7.0
'''
    
    def _get_readme_template(self) -> str:
        return '''# {{AGENT_NAME}}

{{AGENT_DESCRIPTION}}

## Framework
{{ETHICAL_FRAMEWORK}}

## Capabilities
{{CAPABILITIES}}

## Tools
{{TOOLS}}

## Configuration
- LLM Provider: {{LLM_PROVIDER}}
- Model: {{MODEL}}

## Usage
```python
from agents.{{AGENT_NAME.lower()}}_agent import {{AGENT_NAME}}

agent = {{AGENT_NAME}}()
response = await agent.deliberate(content, context)
```
'''
    
    def _get_default_agent_template(self, definition: AgentDefinition) -> str:
        return f'''"""
{definition.name} - {definition.description}
"""

import asyncio
import logging
from typing import Dict, Any
from agents.base_agent import LLMEthicsAgent, AgentResponse

logger = logging.getLogger(__name__)


class {definition.name}(LLMEthicsAgent):
    """{definition.description}"""
    
    def __init__(self):
        super().__init__(
            name="{definition.name}",
            description="{definition.description}",
            ethical_framework="{definition.ethical_framework or 'General Ethics'}",
            agent_type="{definition.name.lower()}"
        )
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Perform deliberation"""
        
        # Build prompt with training examples
        prompt = self.build_prompt(content)
        
        # Get LLM response
        llm_response = self.call_llm(prompt)
        
        # Parse response
        decision, confidence = self._parse_decision_and_confidence(llm_response, content)
        evidence = self._extract_evidence(llm_response, content)
        
        return AgentResponse(
            decision=decision,
            confidence=confidence,
            reasoning=llm_response,
            supporting_evidence=evidence,
            agent_name=self.name,
            ethical_framework=self.ethical_framework
        )
'''


# CLI Interface
def main():
    """AgentMaker CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AgentMaker - Build and manage AI agents")
    parser.add_argument("command", choices=["create", "build", "list", "deploy"], help="Command to execute")
    parser.add_argument("--name", help="Agent or project name")
    parser.add_argument("--type", help="Agent type")
    parser.add_argument("--description", help="Agent description")
    parser.add_argument("--project", help="Project name")
    
    args = parser.parse_args()
    
    agentmaker = AgentMaker()
    
    if args.command == "create":
        if not args.name or not args.type:
            print("❌ Name and type required for create command")
            return
        
        definition = AgentDefinition(
            name=args.name,
            description=args.description or f"{args.name} agent",
            agent_type=args.type,
            capabilities=["basic_analysis"],
            tools=["llm_integration"],
            llm_provider="openai",
            model="gpt-3.5-turbo"
        )
        
        success = agentmaker.create_agent(definition)
        if success:
            print(f"✅ Agent {args.name} created successfully")
        else:
            print(f"❌ Failed to create agent {args.name}")
    
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
        
        print(f"✅ Built {len(all_agents)} agents for EthIQ project")
    
    elif args.command == "list":
        print("📋 Available agents:")
        for agent_file in agentmaker.agents_dir.glob("*/**/*_agent.py"):
            print(f"  - {agent_file.stem}")
    
    elif args.command == "deploy":
        print("🚀 Deploying agents...")
        # Implementation for deployment
        print("✅ Agents deployed successfully")


if __name__ == "__main__":
    main() 