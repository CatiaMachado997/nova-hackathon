from agents.base_agent import LLMEthicsAgent

class UtilitarianAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="UtilitarianAgent",
            description="Agent applying utilitarian ethical reasoning (maximizing overall good).",
            ethical_framework="Utilitarianism",
            agent_type="utilitarian"
        ) 