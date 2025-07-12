from agents.base_agent import LLMEthicsAgent

class CulturalContextAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="CulturalContextAgent",
            description="Agent considering cultural context and norms in ethical reasoning.",
            ethical_framework="Cultural Context Ethics",
            agent_type="cultural_context"
        ) 