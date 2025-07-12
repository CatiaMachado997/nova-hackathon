<<<<<<< HEAD
# EthIQ – Ethical Intelligence for Content Moderation  
*“It’s not just moderation. It’s the future of ethical intelligence.”*
=======
# EthIQ - Ethical Intelligence Platform
>>>>>>> 00cfaa9 (Rename project from AutoEthos to EthIQ - Complete rebranding with all functionality preserved)

## Overview

<<<<<<< HEAD
**EthIQ** is an AI-powered ethical moderation system designed to handle complex and sensitive content decisions with depth, transparency, and nuance. Rather than issuing binary judgments, EthIQ simulates ethical deliberation using multiple reasoning agents that represent diverse moral perspectives.
=======
EthIQ is an innovative ethical intelligence platform designed for content moderation at scale. Rather than issuing binary judgments, EthIQ simulates ethical deliberation using multiple reasoning agents and provides transparent justifications.
>>>>>>> 00cfaa9 (Rename project from AutoEthos to EthIQ - Complete rebranding with all functionality preserved)

### How It Works

A modular multi-agent system enables dynamic ethical reasoning:

- **Ethics Commander** – Accepts moderation tasks and coordinates the debate process.
- **Debate Agents**:
  - `UtilitarianAgent`: Weighs harm vs. benefit  
  - `DeontologicalAgent`: Evaluates rule-based violations  
  - `CulturalContextAgent`: Considers cultural sensitivities  
  - `FreeSpeechAgent`: Assesses implications on expression and censorship  
  - `PsychologicalAgent`: Evaluates emotional and mental health impact, especially around trauma, distress, or vulnerable groups  
  - `ReligiousEthicsAgent`: Considers moral implications from diverse religious worldviews (e.g., Christianity, Islam, Buddhism)  
  - `FinancialImpactAgent`: Evaluates financial consequences at two levels:
    - **Platform-level**: Advertising risk, brand trust, compliance fines, user churn  
    - **Personal-level**: Creator monetization, user income disruption, community economic well-being  
- **Consensus Agent** – Synthesizes diverse views into a final decision with clear justification

<<<<<<< HEAD
---
=======
## 🚀 Solution: Multi-Agent Ethical Deliberation

EthIQ enables AI to reason like ethicists, not just rule enforcers:

### 🤖 Agent Architecture

1. **Ethics Commander** - Master agent that orchestrates deliberation
2. **Debate Agents** - Specialized ethical perspectives:
   - **UtilitarianAgent** - Weighs harm vs. benefit
   - **DeontologicalAgent** - Considers rule violations  
   - **CulturalContextAgent** - Evaluates cultural sensitivity
   - **FreeSpeechAgent** - Assesses freedom of expression
3. **Consensus Agent** - Synthesizes perspectives into final decision
4. **Audit Logger** - Logs process to Notion, streams metrics to Cloudera

### 🔄 Deliberation Workflow

```
Content Input → Individual Analysis → Cross-Examination → Consensus Building → Final Decision
```

1. **Individual Analysis**: Each agent analyzes content from their ethical framework
2. **Cross-Examination**: Agents identify conflicts and agreements
3. **Consensus Building**: Weighted deliberation resolves disagreements
4. **Final Decision**: Transparent decision with comprehensive reasoning

## 🏗️ Project Structure

```
nova-hackathon/
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── ethics_commander.py # Master orchestrator
│   ├── debate_agents.py   # Ethical specialists
│   ├── consensus_agent.py # Decision synthesizer
│   └── audit_logger.py    # Notion/Cloudera integration
├── api/                   # FastAPI REST API
│   ├── main.py           # API endpoints
│   └── schemas.py        # Pydantic models
├── templates/            # Dashboard HTML templates
├── static/              # Dashboard assets
│   ├── css/
│   └── js/
├── dashboard.py         # Flask web dashboard
├── demo.py             # Demo scenarios
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd nova-hackathon
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the demo**:
   ```bash
   python demo.py
   ```

4. **Start the API server**:
   ```bash
   cd api
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Start the dashboard**:
   ```bash
   python dashboard.py
   ```

### Environment Variables (Optional)

Create a `.env` file for external integrations:

```env
# Notion Integration
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id

# Cloudera Integration  
CLOUDERA_HOST=your_cloudera_host
CLOUDERA_PORT=9092
CLOUDERA_TOPIC=ethiq-metrics
CLOUDERA_USERNAME=your_username
CLOUDERA_PASSWORD=your_password
```

## LLM Provider Configuration

You can configure which LLM provider to use for agent moderation:

- `LLM_PROVIDER=openai` (default, uses OpenAI GPT-3.5/4)
- `LLM_PROVIDER=gemini` (uses Google Gemini)
- `LLM_PROVIDER=mock` (returns a mock response for local/dev)

Set the following environment variables in your `.env`:

```
LLM_PROVIDER=openai  # or gemini or mock
OPENAI_API_KEY=your_openai_api_key  # for OpenAI
GOOGLE_API_KEY=your_google_api_key  # for Gemini
```

The system will automatically use the correct API and model based on your configuration.

## 🎮 Usage Examples

### Command Line Demo

```bash
python demo.py
```

This runs 5 example scenarios demonstrating different ethical challenges.

### API Usage

```python
import requests

# Submit content for moderation
response = requests.post("http://localhost:8000/api/moderate", json={
    "content": "A satirical video about politics",
    "content_type": "video",
    "audience_size": 50000,
    "educational_value": True,
    "public_interest": True
})

result = response.json()
print(f"Decision: {result['final_decision']}")
print(f"Confidence: {result['confidence']}")
print(f"Reasoning: {result['reasoning']}")
```

### Web Dashboard

Visit `http://localhost:8080` for the interactive dashboard featuring:
- Real-time content moderation
- Agent status monitoring
- Analytics and trends
- Moderation history

## 🔧 API Endpoints

### Content Moderation
- `POST /api/moderate` - Submit content for ethical analysis
- `GET /api/analysis/{task_id}` - Retrieve analysis results
- `GET /api/history` - View moderation history

### Agent Management
- `GET /api/agents` - List available AI agents
- `POST /api/agents/configure` - Configure agent parameters
- `GET /api/agents/status` - Check agent status

### Analytics
- `GET /api/analytics/summary` - Get moderation statistics
- `GET /api/analytics/trends` - View trend analysis
- `POST /api/analytics/export` - Export data
>>>>>>> 00cfaa9 (Rename project from AutoEthos to EthIQ - Complete rebranding with all functionality preserved)

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

## 📘 Documentation (Coming Soon)

> This section will include:

- ✅ Setup instructions  
- ✅ Usage guide and examples  
- ✅ System architecture overview  
- ✅ Agent structure and behaviors  
- ✅ API endpoints (if any)  
- ✅ Dependencies and installation steps  

*Stay tuned for the full developer documentation.*

---

> **EthIQ** enables responsible moderation that considers not just rules—but real human impact.
