"""
Visualize Patient Disease Progressions
Shows how the Digital Twin tracks disease progression over time
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
visit_df = pd.read_csv("METADATA/Visit_History.csv")
patient_df = pd.read_csv("METADATA/Patient_Master.csv")

print("="*70)
print("DIGITAL TWIN - DISEASE PROGRESSION ANALYSIS")
print("="*70)

# Show example patient progressions
print("\nExample Patient Progressions:\n")

example_patients = ['P001', 'P002', 'P006', 'P010', 'P015']

for patient_id in example_patients:
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    patient_info = patient_df[patient_df['Patient_ID'] == patient_id].iloc[0]
    
    print(f"{patient_id} (Age: {patient_info['Age']}, Gender: {patient_info['Gender']})")
    
    progression = []
    for _, visit in patient_visits.iterrows():
        progression.append(f"  Visit {visit['Visit_No']} ({visit['Visit_Date']}): "
                          f"{visit['Disease_Name']} - {visit['Symptoms']}")
    
    print("\n".join(progression))
    print()

# Analyze progression patterns
print("="*70)
print("PROGRESSION PATTERN ANALYSIS")
print("="*70)

# Count different progression types
progressions = []
for patient_id in visit_df['Patient_ID'].unique():
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    disease_sequence = list(patient_visits['Disease_Name'])
    progressions.append(" → ".join(disease_sequence))

print(f"\nTotal Unique Progression Patterns: {len(set(progressions))}")
print("\nMost Common Progressions:")

from collections import Counter
progression_counts = Counter(progressions)
for progression, count in progression_counts.most_common(10):
    print(f"  {count:2d} patients: {progression}")

# Disease transition analysis
print("\n" + "="*70)
print("DISEASE TRANSITION ANALYSIS")
print("="*70)

transitions = []
for patient_id in visit_df['Patient_ID'].unique():
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    diseases = list(patient_visits['Disease_Name'])
    
    for i in range(len(diseases) - 1):
        transitions.append((diseases[i], diseases[i+1]))

print("\nMost Common Disease Transitions:")
transition_counts = Counter(transitions)
for (from_disease, to_disease), count in transition_counts.most_common(10):
    print(f"  {count:2d}x: {from_disease} → {to_disease}")

print("\n" + "="*70)
print("✓ Progression Analysis Complete!")
print("="*70)
