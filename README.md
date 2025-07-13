# EthIQ – Ethical Intelligence for Content Moderation  
*"It's not just moderation. It's the future of ethical intelligence."*

## Overview

**EthIQ** is an AI-powered ethical moderation system designed to handle complex and sensitive content decisions with depth, transparency, and nuance. Rather than issuing binary judgments, EthIQ simulates ethical deliberation using multiple reasoning agents that represent diverse moral perspectives.

### How It Works

A modular multi-agent system enables dynamic ethical reasoning through a **4-phase deliberation process**:

#### **Phase 1: Individual Analysis**
Each specialized agent analyzes content independently:
- **`UtilitarianAgent`**: Weighs harm vs. benefit using consequentialist ethics
- **`DeontologicalAgent`**: Evaluates rule-based violations and moral duties
- **`CulturalContextAgent`**: Considers cultural sensitivities and diversity
- **`FreeSpeechAgent`**: Assesses implications on expression and censorship rights
- **`PsychologicalAgent`**: Evaluates emotional and mental health impact, especially around trauma, distress, or vulnerable groups
- **`ReligiousEthicsAgent`**: Considers moral implications from diverse religious worldviews (e.g., Christianity, Islam, Buddhism)
- **`FinancialImpactAgent`**: Evaluates financial consequences at two levels:
  - **Platform-level**: Advertising risk, brand trust, compliance fines, user churn
  - **Personal-level**: Creator monetization, user income disruption, community economic well-being

#### **Phase 2: Cross-Examination**
The Ethics Commander identifies:
- **Conflicts**: Where agents disagree on decisions
- **Agreements**: Unanimous consensus points
- **Questions**: Areas needing clarification
- **Confidence Levels**: Reliability of each agent's assessment

#### **Phase 3: Consensus Building**
The system synthesizes perspectives using:
- **Weighted Analysis**: Combines agent decisions with confidence scores
- **Framework Balancing**: Considers multiple ethical perspectives
- **Conflict Resolution**: Addresses disagreements through deliberation

#### **Phase 4: Final Decision**
The Consensus Agent produces:
- **Transparent Reasoning**: Clear explanation of the decision process
- **Confidence Score**: Overall reliability of the decision
- **Supporting Evidence**: Key factors that influenced the outcome
- **Audit Trail**: Complete record for accountability

#### **Supporting Infrastructure**
- **`AuditLogger`**: Logs deliberations to Notion and streams metrics to Cloudera
- **`ConsensusAgent`**: Synthesizes multiple perspectives into final decisions
- **GenAI AgentOS Protocol**: Enables agent orchestration and messaging
- **Real-time Dashboard**: Web interface for monitoring and interaction

---

## The Problem

Modern digital platforms struggle with ethically ambiguous content that current moderation tools are unequipped to handle. These include:

- Emotionally triggering or mentally damaging content  
- Satirical and politically charged content  
- Cultural and **religious** conflicts  
- AI-generated misinformation or harmful deepfakes  

Most moderation systems are rule-based, opaque, and inflexible—leading to inconsistent enforcement, backlash, and harm to users' psychological, cultural, spiritual, and financial well-being.

---

## Psychological Context

Content exposure affects mental and emotional health. Research shows:

- **Ambiguous or harsh content** can increase **anxiety**, **cognitive dissonance**, and **online aggression**  
- **Perceived censorship** without explanation erodes **trust** and triggers **reactance** (psychological pushback when freedom is restricted)  
- **Lack of cultural or spiritual sensitivity** leads to exclusion, identity invalidation, and offense  
- **Unmoderated misinformation** contributes to confusion, fear, and mental fatigue—especially in health, politics, and religion  

The addition of the `PsychologicalAgent`, `ReligiousEthicsAgent`, and `FinancialImpactAgent` ensures moderation decisions consider mental safety, moral diversity, and both platform and user-level economics.

---

## Applications

EthIQ can ethically moderate content across a wide range of sectors:

- **Social Media & Video Platforms**: Facebook, X (Twitter), YouTube, TikTok, Reddit, etc.  
- **E-commerce & UGC Platforms**: Filter reviews, comments, and chats with ethical precision  
- **News & Media**: Moderate comments and AI content to reduce emotional harm and bias  
- **Government & Public Sector**: Combat misinformation and maintain civic trust  
- **AI Developers & Model Providers**: Ensure content generation aligns with ethical frameworks  
- **Healthcare Organizations**: Protect mental health in patient communities and filter harmful or misleading medical content  

---

## Why EthIQ Can Succeed

- Modular, explainable agent-based architecture  
- Innovative ethical debate simulation by AI  
- Tackles moderation challenges in the AI age  
- Sensitive to **psychological**, **religious**, **financial** (platform + personal), and cultural factors  
- **Built-in transparency** for trust, auditability, and defensible decision-making  

---

## 📘 Documentation

### 🚀 Quick Start

#### Prerequisites
- Python 3.8+
- pip or conda

#### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nova-hackathon
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

#### Running the System

**Option 1: Interactive Startup Script**
```bash
python start.py
```
Choose from the menu:
- Run system test
- Run demo scenarios  
- Start API server
- Start web dashboard
- Start API + Dashboard (recommended)

**Option 2: Manual Startup**

Start the API server:
```bash
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Start the web dashboard:
```bash
python dashboard.py
```

Run the demo:
```bash
python demo.py
```

#### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Web Dashboard**: http://localhost:8080
- **API Health Check**: http://localhost:8000/health

### System Architecture

The system consists of several key components:

#### Core Agents
- **EthicsCommander**: Master orchestrator that coordinates deliberation
- **UtilitarianAgent**: Evaluates harm vs. benefit using utilitarian ethics
- **DeontologicalAgent**: Applies duty-based ethical reasoning
- **CulturalContextAgent**: Considers cultural sensitivity and diversity
- **FreeSpeechAgent**: Assesses freedom of expression implications
- **PsychologicalAgent**: Evaluates emotional and mental health impact
- **ReligiousEthicsAgent**: Considers diverse religious perspectives
- **FinancialImpactAgent**: Evaluates financial consequences at platform and personal levels
- **ConsensusAgent**: Synthesizes multiple perspectives into final decisions
- **AuditLogger**: Logs deliberations and streams metrics

#### API Endpoints

**Content Moderation**:
- `POST /api/moderate` - Submit content for ethical analysis
- `GET /api/analysis/{task_id}` - Retrieve analysis results
- `GET /api/history` - View moderation history

**Agent Management**:
- `GET /api/agents` - List available AI agents
- `POST /api/agents/configure` - Configure agent parameters
- `GET /api/agents/status` - Check agent status

**Analytics**:
- `GET /api/analytics/summary` - Get moderation statistics
- `GET /api/analytics/trends` - View trend analysis
- `POST /api/analytics/export` - Export data

**Integrations**:
- `GET /api/integrations/agentos/status` - GenAI AgentOS Protocol status
- `GET /api/integrations/cloudera/status` - Cloudera integration status
- `GET /api/integrations/cloudera/analytics` - Cloudera analytics data

#### Web Dashboard

The dashboard provides:
- Real-time moderation interface
- Agent status monitoring
- Analytics and trends visualization
- Integration status tracking
- Moderation history review

### Usage Examples

#### Basic Content Moderation

```python
import requests

# Submit content for moderation
response = requests.post("http://localhost:8000/api/moderate", json={
    "content": "Your content here",
    "content_type": "text",
    "platform": "social_media",
    "audience_size": 1000,
    "vulnerable_audience": False,
    "educational_value": True,
    "public_interest": True,
    "context": {
        "additional_info": "Any additional context"
    }
})

result = response.json()
print(f"Decision: {result['final_decision']}")
print(f"Confidence: {result['confidence']}")
print(f"Reasoning: {result['reasoning']}")
```

#### Using the Python API

```python
from agents import EthicsCommander

# Initialize the system
commander = EthicsCommander()

# Conduct ethical deliberation
response = await commander.deliberate(
    content="Content to moderate",
    context={
        "audience_size": 1000,
        "vulnerable_audience": False,
        "educational_value": True
    }
)

print(f"Decision: {response.decision}")
print(f"Confidence: {response.confidence}")
```

### Training Data

The system uses training data for few-shot prompting:

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
├── free_speech/
│   ├── flagged_*.txt
│   └── approved_*.txt
├── psychological/
│   ├── flagged_*.txt
│   └── approved_*.txt
├── religious_ethics/
│   ├── flagged_*.txt
│   └── approved_*.txt
└── financial_impact/
    ├── flagged_*.txt
    └── approved_*.txt
```

### Configuration

#### Environment Variables

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# LLM Providers
LLM_PROVIDER=openai|gemini|mock
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key

# Integrations
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id
CLOUDERA_HOST=your_cloudera_host
CLOUDERA_PORT=9092
CLOUDERA_TOPIC=ethiq-metrics
```

#### LLM Provider Configuration

The system supports multiple LLM providers:
- **OpenAI**: GPT-3.5-turbo for ethical deliberation
- **Google Gemini**: Alternative LLM provider
- **Mock**: For development and testing

### Project Structure

```
nova-hackathon/
├── agents/              # AI agent implementations
│   ├── base_agent.py    # Base classes
│   ├── ethics_commander.py
│   ├── utilitarian_agent.py
│   ├── deontological_agent.py
│   ├── cultural_context_agent.py
│   ├── free_speech_agent.py
│   ├── psychological_agent.py
│   ├── religious_ethics_agent.py
│   ├── financial_impact_agent.py
│   ├── consensus_agent.py
│   ├── audit_logger.py
│   ├── agentos_integration.py
│   └── cloudera_integration.py
├── api/                 # FastAPI application
│   ├── main.py         # API endpoints
│   └── schemas.py      # Pydantic models
├── tools/              # Utility tools
│   ├── training_data_loader.py
│   ├── right-balancer.py
│   ├── test_*.py       # Testing tools
│   └── llm_demo.py
├── data/training/      # Training examples
├── static/             # Dashboard assets
├── templates/          # Dashboard templates
├── dashboard.py        # Web dashboard
├── demo.py            # Demo scenarios
├── start.py           # Startup script
└── requirements.txt    # Dependencies
```

### Testing

Run the system test:
```bash
python test_system.py
```

Run individual tests:
```bash
pytest tools/test_*.py
```

### Code Quality

The project follows:
- Type hints throughout
- Comprehensive error handling
- Async/await for non-blocking operations
- Modular design for extensibility
- Pydantic models for validation

### 🌟 Features

#### Multi-Agent Ethical Deliberation
- **4-Phase Process**: Individual analysis → Cross-examination → Consensus building → Final decision
- **Weighted Analysis**: Combines multiple ethical frameworks with confidence scoring
- **Transparent Reasoning**: Full audit trail of deliberation process

#### Real-Time Integrations
- **GenAI AgentOS Protocol**: Agent orchestration and messaging
- **Cloudera Streaming**: Real-time metrics and analytics
- **Notion Integration**: Audit logging and documentation

#### Web Dashboard
- **Real-time Monitoring**: Agent status and system health
- **Interactive Moderation**: Submit content and view results
- **Analytics Dashboard**: Decision trends and performance metrics
- **Integration Status**: Monitor external service connections

#### API-First Design
- **RESTful Endpoints**: Complete API for integration
- **WebSocket Support**: Real-time updates via Socket.IO
- **Comprehensive Documentation**: Auto-generated OpenAPI docs

---

> **EthIQ** enables responsible moderation that considers not just rules—but real human impact.
