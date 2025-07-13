# UtilitarianAgent for GenAI AgentOS Protocol

## Overview

The UtilitarianAgent is an ethical reasoning agent that applies utilitarian principles to content moderation and ethical decision-making. It analyzes content by considering the overall happiness and well-being of all affected parties, following the principle of "the greatest good for the greatest number."

## Ethical Framework

**Utilitarianism**: A consequentialist ethical theory that evaluates actions based on their outcomes and consequences, specifically focusing on maximizing overall happiness and minimizing suffering.

### Core Principles

1. **Maximize overall happiness and well-being**
2. **Minimize suffering and harm**
3. **Consider consequences for all affected parties**
4. **Evaluate long-term vs short-term benefits**

## Capabilities

### Primary Functions

- **Content Analysis**: Analyze text content for ethical implications
- **Utility Calculation**: Calculate utility scores based on beneficial vs harmful indicators
- **Decision Making**: Provide ethical decisions (ALLOW/REMOVE/FLAG_FOR_REVIEW)
- **Reasoning Generation**: Provide detailed explanations for decisions

### Bound Functions

1. **`analyze_content_utilitarian`**: Main content analysis function
2. **`get_utilitarian_principles`**: Get core utilitarian principles
3. **`health_check`**: Agent health and status check

## Usage

### Running the Agent

```bash
cd agents/agentos_agents/utilitarian
python main.py
```

### Environment Variables

- `AGENTOS_JWT_TOKEN`: JWT token for AgentOS authentication

### Example Analysis

The agent analyzes content by:

1. **Keyword Analysis**: Identifies harmful and beneficial keywords
2. **Utility Scoring**: Calculates utility score (-1 to 1)
3. **Context Consideration**: Factors in audience vulnerability, platform, etc.
4. **Decision Making**: Provides ethical decision with confidence score

## Integration

This agent is designed to work with the GenAI AgentOS Protocol and can be integrated into the EthIQ ethical deliberation system as a specialist agent for utilitarian reasoning.

## Development

The agent uses a fallback mock implementation when the real `genai-session` package is not available, ensuring compatibility during development and testing. 