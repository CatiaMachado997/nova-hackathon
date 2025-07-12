from agents.base_agent import LLMEthicsAgent

class PsychologicalAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="PsychologicalAgent",
            description="Agent evaluating emotional and mental health impact, especially around trauma, distress, or vulnerable groups.",
            ethical_framework="Psychological Ethics",
            agent_type="psychological"
        ) 