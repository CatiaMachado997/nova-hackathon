#!/usr/bin/env python3
"""
Script to clean enhanced training data by removing entries for deleted agents
"""

import json
import os

def clean_enhanced_training_data():
    """Remove entries for deleted agents from enhanced training data"""
    
    # Path to the enhanced training data file
    file_path = "data/training/enhanced/enhanced_training_data.json"
    
    # Read the current data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Remove entries that reference deleted agents
    cleaned_data = []
    deleted_keywords = ["psychological", "religious_ethics", "financial_impact", "temporal", "explainability"]
    
    for entry in data:
        # Check if entry contains references to deleted agents
        should_keep = True
        entry_text = json.dumps(entry).lower()
        
        for keyword in deleted_keywords:
            if keyword in entry_text:
                should_keep = False
                break
        
        if should_keep:
            cleaned_data.append(entry)
    
    # Write the cleaned data back
    with open(file_path, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"Cleaned enhanced training data: {len(data)} -> {len(cleaned_data)} entries")
    print(f"Removed {len(data) - len(cleaned_data)} entries with deleted agent references")

if __name__ == "__main__":
    clean_enhanced_training_data() 