"""
GastroTwin Risk Engine
Dynamic risk assessment system for longitudinal disease monitoring

IMPORTANT DISCLAIMER:
This risk engine is a PROTOTYPE DEMONSTRATION for the GastroTwin Digital Twin framework.
The scoring rules are HEURISTIC and intended ONLY to demonstrate longitudinal risk tracking
using publicly available datasets. This output is for CLINICAL DECISION SUPPORT RESEARCH,
NOT for real-world medical decision making. Risk weights are NOT medically validated.

Author: GastroTwin Research Project
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("="*80)
print("GASTROTWIN RISK ENGINE - DYNAMIC RISK ASSESSMENT SYSTEM")
print("="*80)
print("\n⚠️  DISCLAIMER: This is a research prototype using demonstration weights.")
print("    Risk scores are NOT medically validated and are for research purposes only.\n")

# ============================================================================
# CONFIGURATION - Risk Scoring Weights (DEMONSTRATION ONLY)
# ============================================================================

# Patient Risk Factors
PATIENT_RISK_WEIGHTS = {
    'age_over_60': 20,
    'smoking_yes': 15,
    'alcohol_yes': 5,
    'diabetes_yes': 10,
    'hypertension_yes': 10,
    'family_history_gi_yes': 15,
    'bmi_over_30': 10
}

# Disease Risk Weights
DISEASE_RISK_WEIGHTS = {
    'Normal-Cecum': 0,
    'Normal-Pylorus': 0,
    'Normal-Z-Line': 0,
    'Esophagitis': 20,
    'Polyps': 35,
    'Ulcerative-Colitis': 30,
    'Dyed-Lifted-Polyps': 15,
    'Dyed-Resection-Margins': 10
}

# Disease Progression Weights
PROGRESSION_WEIGHTS = {
    # Normal to Disease
    ('Normal-Cecum', 'Esophagitis'): 10,
    ('Normal-Cecum', 'Polyps'): 15,
    ('Normal-Pylorus', 'Esophagitis'): 10,
    ('Normal-Pylorus', 'Polyps'): 15,
    ('Normal-Z-Line', 'Esophagitis'): 10,
    ('Normal-Z-Line', 'Polyps'): 15,
    
    # Disease Progression
    ('Esophagitis', 'Polyps'): 15,
    ('Esophagitis', 'Ulcerative-Colitis'): 15,
    ('Polyps', 'Dyed-Lifted-Polyps'): 5,
    ('Dyed-Lifted-Polyps', 'Dyed-Resection-Margins'): 5,
    
    # Stable disease (same to same)
    ('Esophagitis', 'Esophagitis'): 0,
    ('Polyps', 'Polyps'): 0,
    ('Ulcerative-Colitis', 'Ulcerative-Colitis'): 0,
    ('Normal-Cecum', 'Normal-Cecum'): 0,
    ('Normal-Pylorus', 'Normal-Pylorus'): 0,
    ('Normal-Z-Line', 'Normal-Z-Line'): 0,
}

# Risk Categories
def get_risk_category(score):
    """Categorize risk score into risk levels"""
    if score < 25:
        return "Low"
    elif score < 50:
        return "Medium"
    elif score < 75:
        return "High"
    else:
        return "Very High"

# ============================================================================
# LOAD DATA
# ============================================================================

print("[1/6] Loading patient and visit data...")
patient_df = pd.read_csv("METADATA/Patient_Master.csv")
visit_df = pd.read_csv("METADATA/Visit_History.csv")

print(f"  ✓ Loaded {len(patient_df)} patients")
print(f"  ✓ Loaded {len(visit_df)} visits")

# ============================================================================
# CALCULATE PATIENT BASELINE RISK
# ============================================================================

print("\n[2/6] Calculating patient baseline risk factors...")

def calculate_patient_baseline_risk(patient_row):
    """Calculate baseline risk score from patient factors"""
    risk_score = 0
    risk_factors = []
    
    # Age > 60
    if patient_row['Age'] > 60:
        risk_score += PATIENT_RISK_WEIGHTS['age_over_60']
        risk_factors.append(f"Age {patient_row['Age']}")
    
    # Smoking
    if patient_row['Smoking'] == 'Yes':
        risk_score += PATIENT_RISK_WEIGHTS['smoking_yes']
        risk_factors.append("Smoking")
    
    # Alcohol
    if patient_row['Alcohol'] == 'Yes':
        risk_score += PATIENT_RISK_WEIGHTS['alcohol_yes']
        risk_factors.append("Alcohol use")
    
    # Diabetes
    if patient_row['Diabetes'] == 'Yes':
        risk_score += PATIENT_RISK_WEIGHTS['diabetes_yes']
        risk_factors.append("Diabetes")
    
    # Hypertension
    if patient_row['Hypertension'] == 'Yes':
        risk_score += PATIENT_RISK_WEIGHTS['hypertension_yes']
        risk_factors.append("Hypertension")
    
    # Family History
    if patient_row['Family_History_GI'] == 'Yes':
        risk_score += PATIENT_RISK_WEIGHTS['family_history_gi_yes']
        risk_factors.append("Family history of GI disease")
    
    # BMI >= 30
    if patient_row['BMI'] >= 30:
        risk_score += PATIENT_RISK_WEIGHTS['bmi_over_30']
        risk_factors.append(f"BMI {patient_row['BMI']}")
    
    return risk_score, risk_factors

# Calculate baseline risk for all patients
patient_baseline_risk = {}
for _, patient in patient_df.iterrows():
    patient_id = patient['Patient_ID']
    baseline_score, factors = calculate_patient_baseline_risk(patient)
    patient_baseline_risk[patient_id] = {
        'score': baseline_score,
        'factors': factors
    }

print(f"  ✓ Calculated baseline risk for {len(patient_baseline_risk)} patients")

# ============================================================================
# CALCULATE VISIT-LEVEL RISK SCORES
# ============================================================================

print("\n[3/6] Calculating visit-level risk scores...")

risk_assessments = []
risk_id_counter = 1

# Process each patient's visits
for patient_id in visit_df['Patient_ID'].unique():
    # Get all visits for this patient, sorted by visit number
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    
    # Get patient baseline risk
    baseline_risk = patient_baseline_risk[patient_id]['score']
    baseline_factors = patient_baseline_risk[patient_id]['factors']
    
    previous_disease = None
    
    for idx, visit in patient_visits.iterrows():
        # Start with baseline patient risk
        total_risk_score = baseline_risk
        risk_explanation_parts = []
        
        # Add baseline factors to explanation
        if baseline_factors:
            risk_explanation_parts.append(f"Patient factors: {', '.join(baseline_factors)}")
        else:
            risk_explanation_parts.append("No significant patient risk factors")
        
        # Add disease risk
        # Use GroundTruth_Disease if available (v2), else Disease_Name (v1)
        current_disease = visit.get('GroundTruth_Disease', visit.get('Disease_Name', 'Unknown'))
        disease_risk = DISEASE_RISK_WEIGHTS.get(current_disease, 0)
        total_risk_score += disease_risk
        
        if disease_risk > 0:
            risk_explanation_parts.append(f"{current_disease} (disease risk)")
        else:
            risk_explanation_parts.append(f"{current_disease} (healthy)")
        
        # Add progression risk (if not first visit)
        if previous_disease is not None:
            progression_key = (previous_disease, current_disease)
            progression_risk = PROGRESSION_WEIGHTS.get(progression_key, 0)
            
            if progression_risk > 0:
                total_risk_score += progression_risk
                risk_explanation_parts.append(f"Disease progression from {previous_disease}")
            elif previous_disease == current_disease and disease_risk > 0:
                risk_explanation_parts.append("Stable chronic condition")
            elif previous_disease != current_disease:
                risk_explanation_parts.append(f"Changed from {previous_disease}")
        
        # Determine risk category
        risk_category = get_risk_category(total_risk_score)
        
        # Create comprehensive risk explanation
        risk_explanation = "; ".join(risk_explanation_parts)
        
        # Create risk assessment record
        risk_assessment = {
            'Risk_ID': f"R{risk_id_counter:04d}",
            'Patient_ID': patient_id,
            'Visit_ID': visit['Visit_ID'],
            'Visit_No': visit['Visit_No'],
            'Visit_Date': visit['Visit_Date'],
            'Disease_Name': current_disease,
            'Risk_Score': total_risk_score,
            'Risk_Category': risk_category,
            'Risk_Explanation': risk_explanation
        }
        
        risk_assessments.append(risk_assessment)
        risk_id_counter += 1
        
        # Update previous disease for next iteration
        previous_disease = current_disease

print(f"  ✓ Generated {len(risk_assessments)} risk assessments")

# ============================================================================
# CREATE DATAFRAME AND SAVE
# ============================================================================

print("\n[4/6] Creating Risk_Assessment DataFrame...")
risk_df = pd.DataFrame(risk_assessments)

output_path = "METADATA/Risk_Assessment.csv"
risk_df.to_csv(output_path, index=False)
print(f"  ✓ Saved to {output_path}")

# ============================================================================
# STATISTICS AND ANALYSIS
# ============================================================================

print("\n[5/6] Analyzing risk assessment results...")

print(f"\n{'='*80}")
print("RISK ASSESSMENT STATISTICS")
print(f"{'='*80}")

print(f"\nTotal Risk Assessments: {len(risk_df)}")
print(f"Average Risk Score: {risk_df['Risk_Score'].mean():.1f}")
print(f"Risk Score Range: {risk_df['Risk_Score'].min()} - {risk_df['Risk_Score'].max()}")
print(f"Median Risk Score: {risk_df['Risk_Score'].median():.1f}")

print(f"\nRisk Category Distribution:")
risk_category_counts = risk_df['Risk_Category'].value_counts()
for category in ['Low', 'Medium', 'High', 'Very High']:
    count = risk_category_counts.get(category, 0)
    percentage = (count / len(risk_df)) * 100
    print(f"  - {category:12}: {count:3d} visits ({percentage:5.1f}%)")

print(f"\nDisease Risk Distribution:")
disease_risk_avg = risk_df.groupby('Disease_Name')['Risk_Score'].mean().sort_values(ascending=False)
for disease, avg_score in disease_risk_avg.items():
    print(f"  - {disease:30}: Avg Risk = {avg_score:.1f}")

# ============================================================================
# EXAMPLE PATIENT PROGRESSIONS
# ============================================================================

print(f"\n{'='*80}")
print("EXAMPLE PATIENT RISK PROGRESSIONS")
print(f"{'='*80}")

example_patients = ['P001', 'P002', 'P010', 'P015']

for patient_id in example_patients:
    patient_risk = risk_df[risk_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    
    if len(patient_risk) > 0:
        print(f"\n{patient_id} Risk Progression:")
        for _, row in patient_risk.iterrows():
            print(f"  Visit {row['Visit_No']} ({row['Visit_Date']}): "
                  f"Score={row['Risk_Score']:2d} [{row['Risk_Category']:9s}] - {row['Disease_Name']}")

# ============================================================================
# HIGH-RISK PATIENTS ALERT
# ============================================================================

print(f"\n{'='*80}")
print("HIGH-RISK PATIENT ALERTS")
print(f"{'='*80}")

high_risk_visits = risk_df[risk_df['Risk_Category'].isin(['High', 'Very High'])]
high_risk_patients = high_risk_visits['Patient_ID'].unique()

print(f"\nPatients with High/Very High Risk Visits: {len(high_risk_patients)}")
print(f"Total High/Very High Risk Visits: {len(high_risk_visits)}")

print("\nTop 10 Highest Risk Assessments:")
top_risks = risk_df.nlargest(10, 'Risk_Score')[['Patient_ID', 'Visit_No', 'Disease_Name', 
                                                   'Risk_Score', 'Risk_Category']]
print(top_risks.to_string(index=False))

# ============================================================================
# SUMMARY
# ============================================================================

print(f"\n{'='*80}")
print("✓ RISK ENGINE EXECUTION COMPLETE")
print(f"{'='*80}")
print(f"\nOutput File: {output_path}")
print(f"Total Records: {len(risk_df)}")
print(f"\nKey Insights:")
print(f"  - {risk_category_counts.get('Low', 0)} low-risk visits (preventive monitoring)")
print(f"  - {risk_category_counts.get('Medium', 0)} medium-risk visits (routine follow-up)")
print(f"  - {risk_category_counts.get('High', 0)} high-risk visits (intensive monitoring)")
print(f"  - {risk_category_counts.get('Very High', 0)} very high-risk visits (urgent intervention)")

print(f"\n{'='*80}")
print("⚠️  REMEMBER: These risk scores are for RESEARCH DEMONSTRATION only.")
print("   Not validated for clinical use. Patient safety requires expert review.")
print(f"{'='*80}")

print("\n✓ GastroTwin Digital Twin Database Complete!")
print("  All 4 core tables created:")
print("    1. Disease_Master.csv")
print("    2. Patient_Master.csv")
print("    3. Visit_History.csv")
print("    4. Risk_Assessment.csv")
print("\n  Ready for Phase 4: AI Model Development")
