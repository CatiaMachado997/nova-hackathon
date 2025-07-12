#!/usr/bin/env python3
"""
Right Balancer Tool for EthIQ
Helps balance competing ethical considerations in content moderation decisions
"""

import argparse
import json
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class EthicalConsideration:
    """Represents an ethical consideration with weight and impact"""
    name: str
    description: str
    weight: float  # 0.0 to 1.0
    impact: float  # -1.0 to 1.0 (negative = harmful, positive = beneficial)
    evidence: List[str]

class RightBalancer:
    """Tool for balancing competing ethical considerations"""
    
    def __init__(self):
        self.considerations = []
        self.decision_thresholds = {
            "REMOVE": 0.7,
            "FLAG_FOR_REVIEW": 0.4,
            "ALLOW": 0.3
        }
    
    def add_consideration(self, name: str, description: str, weight: float, 
                         impact: float, evidence: Optional[List[str]] = None):
        """Add an ethical consideration"""
        if evidence is None:
            evidence = []
        
        consideration = EthicalConsideration(
            name=name,
            description=description,
            weight=weight,
            impact=impact,
            evidence=evidence
        )
        self.considerations.append(consideration)
    
    def calculate_balance(self) -> Dict[str, Any]:
        """Calculate the overall ethical balance"""
        if not self.considerations:
            return {"error": "No considerations added"}
        
        # Calculate weighted impact
        total_weight = sum(c.weight for c in self.considerations)
        weighted_impact = sum(c.weight * c.impact for c in self.considerations) / total_weight
        
        # Determine decision
        if weighted_impact <= -self.decision_thresholds["REMOVE"]:
            decision = "REMOVE"
        elif weighted_impact <= -self.decision_thresholds["FLAG_FOR_REVIEW"]:
            decision = "FLAG_FOR_REVIEW"
        else:
            decision = "ALLOW"
        
        # Generate reasoning
        reasoning = f"Balanced {len(self.considerations)} ethical considerations. "
        reasoning += f"Weighted impact: {weighted_impact:.3f}. "
        reasoning += f"Decision: {decision} based on overall ethical balance."
        
        return {
            "decision": decision,
            "confidence": abs(weighted_impact),
            "weighted_impact": weighted_impact,
            "reasoning": reasoning,
            "considerations": [
                {
                    "name": c.name,
                    "description": c.description,
                    "weight": c.weight,
                    "impact": c.impact,
                    "evidence": c.evidence
                }
                for c in self.considerations
            ]
        }
    
    def print_analysis(self):
        """Print a formatted analysis"""
        result = self.calculate_balance()
        
        if "error" in result:
            print(f"❌ {result['error']}")
            return
        
        print("🤖 EthIQ Right Balancer Analysis")
        print("=" * 50)
        print(f"📊 Decision: {result['decision']}")
        print(f"🎯 Confidence: {result['confidence']:.2%}")
        print(f"⚖️  Weighted Impact: {result['weighted_impact']:.3f}")
        print(f"💭 Reasoning: {result['reasoning']}")
        print()
        
        print("🔍 Ethical Considerations:")
        for i, consideration in enumerate(result['considerations'], 1):
            impact_symbol = "✅" if consideration['impact'] > 0 else "❌" if consideration['impact'] < 0 else "⚖️"
            print(f"  {i}. {impact_symbol} {consideration['name']} (Weight: {consideration['weight']:.2f}, Impact: {consideration['impact']:.2f})")
            print(f"     {consideration['description']}")
            if consideration['evidence']:
                for evidence in consideration['evidence']:
                    print(f"     📝 {evidence}")
            print()

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="EthIQ Right Balancer Tool")
    parser.add_argument("--content", help="Content to analyze")
    parser.add_argument("--json", help="JSON file with considerations")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    balancer = RightBalancer()
    
    if args.json:
        # Load from JSON file
        try:
            with open(args.json, 'r') as f:
                data = json.load(f)
            
            for consideration in data.get('considerations', []):
                balancer.add_consideration(
                    name=consideration['name'],
                    description=consideration['description'],
                    weight=consideration['weight'],
                    impact=consideration['impact'],
                    evidence=consideration.get('evidence', [])
                )
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            sys.exit(1)
    
    elif args.interactive:
        # Interactive mode
        print("🤖 EthIQ Right Balancer - Interactive Mode")
        print("Enter ethical considerations (press Enter with empty name to finish):")
        
        while True:
            name = input("\nConsideration name (or Enter to finish): ").strip()
            if not name:
                break
            
            description = input("Description: ").strip()
            weight = float(input("Weight (0.0-1.0): "))
            impact = float(input("Impact (-1.0 to 1.0): "))
            
            evidence = []
            print("Evidence (one per line, empty line to finish):")
            while True:
                ev = input("  ").strip()
                if not ev:
                    break
                evidence.append(ev)
            
            balancer.add_consideration(name, description, weight, impact, evidence)
    
    else:
        # Demo mode with example considerations
        print("🤖 EthIQ Right Balancer - Demo Mode")
        print("Using example considerations for demonstration...")
        
        balancer.add_consideration(
            name="Free Speech",
            description="Protecting freedom of expression",
            weight=0.3,
            impact=0.8,
            evidence=["Content is political speech", "Educational value present"]
        )
        
        balancer.add_consideration(
            name="Harm Prevention",
            description="Preventing potential harm to vulnerable groups",
            weight=0.4,
            impact=-0.6,
            evidence=["Contains controversial language", "Large audience size"]
        )
        
        balancer.add_consideration(
            name="Public Interest",
            description="Serving the public interest",
            weight=0.3,
            impact=0.4,
            evidence=["Addresses important social issue", "Promotes discussion"]
        )
    
    # Print analysis
    balancer.print_analysis()

if __name__ == "__main__":
    main()
