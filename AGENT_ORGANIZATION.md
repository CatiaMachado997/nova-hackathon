# EthIQ Agent Organization & Architecture

## 🏗️ Agent Structure Overview

EthIQ uses a **multi-agent ethical deliberation system** with the following architecture:

### **Core Agent Classes**

1. **BaseAgent** (`agents/base_agent.py`)
   - Abstract base class for all agents
   - Defines common interface: `process_task()`, `deliberate()`
   - Handles message queuing and agent communication

2. **LLMEthicsAgent** (`agents/base_agent.py`)
   - Extends BaseAgent with LLM integration
   - Supports OpenAI, Gemini, and Mock providers
   - Uses training data for few-shot prompting

3. **EthicsCommander** (`agents/ethics_commander.py`)
   - **Master orchestrator** that coordinates all other agents
   - Manages the 4-phase deliberation process
   - Handles cross-examination and consensus building

### **Specialized Ethical Agents**

All inherit from `LLMEthicsAgent` and use training data for decision-making:

- **UtilitarianAgent** (`agents/utilitarian_agent.py`)
  - Framework: Utilitarianism (maximize overall good)
  - Focus: Harm vs. benefit analysis

- **DeontologicalAgent** (`agents/deontological_agent.py`)
  - Framework: Deontological Ethics (duty-based)
  - Focus: Moral rules and rights violations

- **CulturalContextAgent** (`agents/cultural_context_agent.py`)
  - Framework: Cultural Context Ethics
  - Focus: Cultural sensitivity and diversity

- **FreeSpeechAgent** (`agents/free_speech_agent.py`)
  - Framework: Free Speech Ethics
  - Focus: Freedom of expression and speech rights

### **Support Agents**

- **ConsensusAgent** (`agents/consensus_agent.py`)
  - Synthesizes multiple ethical perspectives
  - Uses weighted analysis for final decisions

- **AuditLogger** (`agents/audit_logger.py`)
  - Logs all deliberations and decisions
  - Integrates with Notion and Cloudera

### **Integration Agents**

- **AgentOS Integration** (`agents/agentos_integration.py`)
  - GenAI AgentOS Protocol implementation
  - Agent orchestration and messaging

- **Cloudera Integration** (`agents/cloudera_integration.py`)
  - Real-time metrics streaming
  - Analytics and monitoring

## 🔄 Deliberation Workflow

```
Content Input
    ↓
1. Individual Analysis (4 ethical agents)
    ↓
2. Cross-Examination (identify conflicts/agreements)
    ↓
3. Consensus Building (weighted deliberation)
    ↓
4. Final Decision (transparent reasoning)
```

## 🛠️ Tools Organization

### **Core Tools**

- **Training Data Loader** (`tools/training_data_loader.py`)
  - Loads and parses training examples for each agent
  - Builds few-shot prompts for LLM integration

- **Right Balancer** (`tools/right-balancer.py`)
  - Balances competing ethical considerations
  - Provides weighted decision analysis

### **Testing Tools**

- **LLM Agent Tests** (`tools/test_llm_agents.py`)
  - Tests individual agent functionality
  - Uses pytest fixtures for comprehensive testing

- **Content Scenario Tests** (`tools/test_content_scenarios.py`)
  - Tests agents with various content types
  - Validates ethical decision-making

- **API Integration Tests** (`tools/test_api_llm.py`)
  - Tests API endpoints with LLM integration
  - Validates end-to-end functionality

### **Demo Tools**

- **LLM Demo** (`tools/llm_demo.py`)
  - Demonstrates different LLM providers
  - Shows agent behavior across providers

- **Agent Training Demo** (`tools/agent_training_demo.py`)
  - Shows how to use training data
  - Demonstrates prompt generation

## 📁 File Organization

```
agents/
├── __init__.py              # Agent exports
├── base_agent.py           # Base classes (BaseAgent, LLMEthicsAgent)
├── ethics_commander.py     # Master orchestrator
├── utilitarian_agent.py    # Utilitarian framework
├── deontological_agent.py  # Deontological framework
├── cultural_context_agent.py # Cultural framework
├── free_speech_agent.py    # Free speech framework
├── consensus_agent.py      # Decision synthesis
├── audit_logger.py         # Logging and integrations
├── agentos_integration.py  # GenAI AgentOS Protocol
└── cloudera_integration.py # Cloudera streaming

tools/
├── training_data_loader.py    # Training data management
├── right-balancer.py          # Ethical balancing tool
├── test_llm_agents.py         # Agent testing
├── test_content_scenarios.py  # Scenario testing
├── test_api_llm.py           # API testing
├── llm_demo.py               # LLM provider demo
└── agent_training_demo.py    # Training demo
```

## 🔧 Configuration

### **LLM Provider Configuration**
```bash
# Environment variables
LLM_PROVIDER=openai|gemini|mock
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

### **Training Data Structure**
```
data/training/
├── utilitarian/
│   ├── flagged_*.txt
│   └── approved_*.txt
├── deontological/
│   ├── flagged_*.txt
│   └── approved_*.txt
├── cultural_context/
│   ├── flagged_*.txt
│   └── approved_*.txt
└── free_speech/
    ├── flagged_*.txt
    └── approved_*.txt
```

## ✅ Quality Assurance

### **Testing Strategy**
- **Unit Tests**: Individual agent functionality
- **Integration Tests**: Agent interactions and API
- **Scenario Tests**: Real-world content examples
- **LLM Tests**: Provider-specific functionality

### **Code Quality**
- Type hints throughout
- Comprehensive error handling
- Async/await for non-blocking operations
- Modular design for extensibility

## 🚀 Future Enhancements

### **Planned Improvements**
- Machine learning from human feedback
- Additional ethical frameworks
- Multilingual support
- Real-time learning capabilities
- Human-in-the-loop oversight

### **Extensibility**
- Easy to add new ethical frameworks
- Plugin architecture for integrations
- Configurable decision thresholds
- Customizable training data formats 