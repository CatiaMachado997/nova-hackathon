# FreeSpeechAgent

Agent prioritizing free speech and expression in ethical reasoning

## Framework
Free Speech Ethics

## Capabilities
- speech_rights
- expression_analysis
- censorship_evaluation

## Tools
- training_data_loader
- llm_integration

## Configuration
- LLM Provider: openai
- Model: gpt-3.5-turbo
- Training Data: data/training/free_speech

## Usage
```python
from agents.freespeechagent_agent import FreeSpeechAgent

agent = FreeSpeechAgent()
response = await agent.deliberate(content, context)
```
