from agents.base_agent import LLMEthicsAgent

class DeontologicalAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="DeontologicalAgent",
            description="Agent applying deontological (duty-based) ethical reasoning.",
            ethical_framework="Deontological Ethics",
            agent_type="deontological"
        ) 