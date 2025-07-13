# CulturalContextAgent

Agent considering cultural context and norms in ethical reasoning

## Framework
Cultural Context Ethics

## Capabilities
- cultural_sensitivity
- context_analysis
- diversity_awareness

## Tools
- training_data_loader
- llm_integration

## Configuration
- LLM Provider: openai
- Model: gpt-3.5-turbo
- Training Data: data/training/cultural_context

## Usage
```python
from agents.culturalcontextagent_agent import CulturalContextAgent

agent = CulturalContextAgent()
response = await agent.deliberate(content, context)
```
