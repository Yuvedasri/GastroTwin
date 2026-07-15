"""
Test Disease Lookup - Demonstrates how Disease_Master will be used
"""

import pandas as pd

# Load Disease Master
disease_df = pd.read_csv("METADATA/Disease_Master.csv")

print("="*60)
print("DISEASE LOOKUP DEMONSTRATION")
print("="*60)

# Simulate AI predictions
predictions = ["D004", "D005", "D003", "D006"]

print("\nSimulating AI Predictions:\n")

for pred_id in predictions:
    # Lookup disease info
    disease_info = disease_df[disease_df['Disease_ID'] == pred_id]
    
    if not disease_info.empty:
        print(f"Prediction: {pred_id}")
        print(f"  ├─ Disease: {disease_info['Disease_Name'].values[0]}")
        print(f"  ├─ Category: {disease_info['Category'].values[0]}")
        print(f"  └─ Description: {disease_info['Description'].values[0]}")
        print()

print("="*60)
print("✓ This is how the system will reference disease information")
print("  instead of hardcoding it everywhere!")
print("="*60)
