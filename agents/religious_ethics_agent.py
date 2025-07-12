from agents.base_agent import LLMEthicsAgent

class ReligiousEthicsAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="ReligiousEthicsAgent",
            description="Agent considering moral implications from diverse religious worldviews (Christianity, Islam, Buddhism, etc.).",
            ethical_framework="Religious Ethics",
            agent_type="religious_ethics"
        ) 