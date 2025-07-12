from agents.base_agent import LLMEthicsAgent

class FinancialImpactAgent(LLMEthicsAgent):
    def __init__(self):
        super().__init__(
            name="FinancialImpactAgent",
            description="Agent evaluating financial consequences at platform-level (advertising risk, brand trust, compliance fines, user churn) and personal-level (creator monetization, user income disruption, community economic well-being).",
            ethical_framework="Financial Impact Ethics",
            agent_type="financial_impact"
        ) 