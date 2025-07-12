from agents.base_agent import LLMEthicsAgent

class FreeSpeechAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="FreeSpeechAgent",
            description="Agent prioritizing free speech and expression in ethical reasoning.",
            ethical_framework="Free Speech Ethics",
            agent_type="free_speech"
        ) 