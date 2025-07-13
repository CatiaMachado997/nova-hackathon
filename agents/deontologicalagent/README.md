# DeontologicalAgent

Agent applying deontological (duty-based) ethical reasoning

## Framework
Deontological Ethics

## Capabilities
- moral_duty
- rights_analysis
- rule_based_reasoning

## Tools
- training_data_loader
- llm_integration

## Configuration
- LLM Provider: openai
- Model: gpt-3.5-turbo
- Training Data: data/training/deontological

## Usage
```python
from agents.deontologicalagent_agent import DeontologicalAgent

agent = DeontologicalAgent()
response = await agent.deliberate(content, context)
```
