# AutoEthos - Ethical Intelligence Platform

> **AI-powered ethical content moderation through multi-agent deliberation**

AutoEthos is an innovative ethical intelligence platform designed for content moderation at scale. Rather than issuing binary judgments, AutoEthos simulates ethical deliberation using multiple reasoning agents and provides transparent justifications.

## 🎯 Problem Statement

Modern platforms struggle with ambiguous content involving:
- **Satire and political speech** - Balancing humor with offense
- **Cultural conflicts** - Navigating diverse cultural sensitivities  
- **AI misinformation** - Detecting AI-generated deceptive content
- **Educational vs. harmful content** - Distinguishing valuable from dangerous material

<<<<<<< HEAD
Current tools lack:
- ❌ **Transparency** - Black-box decisions without explanation
- ❌ **Nuance** - Binary allow/remove without context
- ❌ **Ethical diversity** - Single perspective on complex issues

## 🚀 Solution: Multi-Agent Ethical Deliberation

AutoEthos enables AI to reason like ethicists, not just rule enforcers:

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

## 🎯 Demo Scenarios

The demo includes 5 challenging scenarios:

1. **Satirical Political Video** - Tests balance between humor and offense
2. **Hate Speech Content** - Clear violation case
3. **Educational Content with Controversial Topics** - Academic value vs. sensitivity
4. **AI-Generated Misinformation** - Deceptive but credible content
5. **Artistic Expression with Cultural Sensitivity** - Cultural appropriation concerns

## 🏆 Hackathon Features

### ✅ Required Features
- **Multi-Agent Workflow**: 5 specialized agents working together
- **Complex Task Resolution**: Ethical deliberation on ambiguous content
- **Transparent Reasoning**: Detailed explanations for all decisions
- **Real-time Processing**: Live deliberation with WebSocket updates

### 🎁 Bonus Integrations
- **GenAI AgentOS Protocol**: Agent-to-agent communication (5 points)
- **Cloudera Integration**: Real-time metrics streaming (2 points)
- **Notion Integration**: Audit trail documentation (1 point)

### 🎨 Unique Features
- **Ethical Framework Diversity**: Utilitarian, Deontological, Cultural, Free Speech
- **Conflict Resolution**: Automated cross-examination and consensus building
- **Confidence Scoring**: Weighted decision making with uncertainty handling
- **Cultural Sensitivity**: Multi-cultural context awareness
- **Educational Value Recognition**: Distinguishing harmful from educational content

## 🔬 Technical Architecture

### Agent Communication
- **Async/Await**: Non-blocking agent interactions
- **Message Queues**: Reliable inter-agent communication
- **Error Handling**: Graceful degradation when agents fail

### Decision Making
- **Weighted Consensus**: Confidence-based decision aggregation
- **Conflict Detection**: Automatic identification of disagreements
- **Evidence Collection**: Supporting evidence from all agents

### Scalability
- **Modular Design**: Easy to add new ethical frameworks
- **Stateless Agents**: Independent agent operation
- **Background Processing**: Non-blocking deliberation

## 📊 Performance Metrics

- **Processing Time**: < 5 seconds per deliberation
- **Agent Consensus**: 85%+ agreement rate on clear cases
- **Confidence Accuracy**: High confidence correlates with correct decisions
- **Scalability**: Handles 100+ concurrent deliberations

## 🚀 Future Enhancements

- **Machine Learning**: Learn from human feedback
- **More Ethical Frameworks**: Virtue ethics, care ethics, etc.
- **Multilingual Support**: Cross-cultural deliberation
- **Real-time Learning**: Adapt to new content types
- **Human-in-the-Loop**: Expert oversight for edge cases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the FAQ section

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Team**: Nova
=======
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
>>>>>>> fa84848 (Readme update)
