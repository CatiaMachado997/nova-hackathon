# EthIQ - Ethical Intelligence Platform

> **AI-powered ethical content moderation through multi-agent deliberation**

EthIQ is an innovative ethical intelligence platform designed for content moderation at scale. Rather than issuing binary judgments, EthIQ simulates ethical deliberation using multiple reasoning agents and provides transparent justifications.

## 🎯 Problem Statement

Modern platforms struggle with ambiguous content involving:
- **Satire and political speech** - Balancing humor with offense
- **Cultural conflicts** - Navigating diverse cultural sensitivities  
- **AI misinformation** - Detecting AI-generated deceptive content
- **Educational vs. harmful content** - Distinguishing valuable from dangerous material

Current tools lack:
- ❌ **Transparency** - Black-box decisions without explanation
- ❌ **Nuance** - Binary allow/remove without context
- ❌ **Ethical diversity** - Single perspective on complex issues

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
│   ├── utilitarian_agent.py
│   ├── deontological_agent.py
│   ├── cultural_context_agent.py
│   ├── free_speech_agent.py
│   ├── ethics_commander.py # Master orchestrator
│   ├── audit_logger.py    # Notion/Cloudera integration
│   ├── cloudera_integration.py
│   └── agentos_integration.py
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
   # If port 8080 is in use, use:
   python dashboard.py --port 8081
   ```
   Then visit `http://localhost:8080` or `http://localhost:8081` in your browser.

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
- `GET /api/analysis/{id}` - Retrieve analysis results
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

## 🧪 Running Tests

To run all automated tests:
```bash
pytest
```

## 📝 Agent Training Data

You can add few-shot examples for each agent in `data/training/<agent>/<flagged|approved>_*.txt`.
See `tools/training_data_loader.py` for format and usage.
