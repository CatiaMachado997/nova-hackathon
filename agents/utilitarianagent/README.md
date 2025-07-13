# UtilitarianAgent

Agent applying utilitarian ethical reasoning (maximizing overall good)

## Framework
Utilitarianism

## Capabilities
- utility_analysis
- cost_benefit
- consequentialist_reasoning

## Tools
- training_data_loader
- llm_integration

## Configuration
- LLM Provider: openai
- Model: gpt-3.5-turbo
- Training Data: data/training/utilitarian

## Usage
```python
from agents.utilitarianagent_agent import UtilitarianAgent

agent = UtilitarianAgent()
response = await agent.deliberate(content, context)
```
