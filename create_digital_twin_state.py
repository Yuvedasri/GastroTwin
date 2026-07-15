"""
GastroTwin Digital Twin State Module
Creates a snapshot of the current state of each patient's Digital Twin

IMPORTANT: This module does NOT modify existing files.
It reads from:
  - Patient_Master.csv
  - Visit_History.csv
  - Risk_Assessment.csv

And creates a NEW file:
  - DigitalTwin_State.csv (one row per patient with latest state)

Author: GastroTwin Research Project
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

print("="*80)
print("GASTROTWIN DIGITAL TWIN STATE MODULE")
print("="*80)
print("\nCreating current state snapshot for all Digital Twins...")
print("This represents the LATEST clinical state of each patient.\n")

# ============================================================================
# LOAD EXISTING DATA (READ ONLY - NO MODIFICATIONS)
# ============================================================================

print("[1/5] Loading existing metadata files...")

# Load Patient Master
patient_df = pd.read_csv("METADATA/Patient_Master.csv")
print(f"  ✓ Loaded {len(patient_df)} patients from Patient_Master.csv")

# Load Visit History
visit_df = pd.read_csv("METADATA/Visit_History.csv")
print(f"  ✓ Loaded {len(visit_df)} visits from Visit_History.csv")

# Load Risk Assessment
risk_df = pd.read_csv("METADATA/Risk_Assessment.csv")
print(f"  ✓ Loaded {len(risk_df)} risk assessments from Risk_Assessment.csv")

# ============================================================================
# DISEASE TREND LOGIC
# ============================================================================

print("\n[2/5] Defining disease progression logic...")

def determine_disease_trend(previous_disease, current_disease):
    """
    Determine the disease trend based on previous and current disease states.
    
    Logic:
    - No previous visit → Initialized
    - Same disease → Stable
    - Normal → Disease → Progressing
    - Disease → Worse Disease → Progressing
    - Polyps → Dyed Lifted Polyps → Improving (post-procedure)
    - Dyed Lifted Polyps → Dyed Resection Margins → Recovering
    """
    
    # No previous visit
    if pd.isna(previous_disease) or previous_disease is None:
        return "Initialized"
    
    # Same disease
    if previous_disease == current_disease:
        return "Stable"
    
    # Define disease severity hierarchy
    normal_states = ['Normal-Cecum', 'Normal-Pylorus', 'Normal-Z-Line']
    disease_states = ['Esophagitis', 'Polyps', 'Ulcerative-Colitis']
    procedure_states = ['Dyed-Lifted-Polyps', 'Dyed-Resection-Margins']
    
    # Normal to Disease = Progressing
    if previous_disease in normal_states and current_disease in disease_states:
        return "Progressing"
    
    # Disease progression patterns
    progression_map = {
        ('Esophagitis', 'Polyps'): 'Progressing',
        ('Esophagitis', 'Ulcerative-Colitis'): 'Progressing',
        ('Polyps', 'Ulcerative-Colitis'): 'Progressing',
    }
    
    if (previous_disease, current_disease) in progression_map:
        return progression_map[(previous_disease, current_disease)]
    
    # Post-procedure improvement patterns
    if previous_disease == 'Polyps' and current_disease == 'Dyed-Lifted-Polyps':
        return "Improving"
    
    if previous_disease == 'Dyed-Lifted-Polyps' and current_disease == 'Dyed-Resection-Margins':
        return "Recovering"
    
    # Disease to Normal = Improving
    if previous_disease in disease_states and current_disease in normal_states:
        return "Improving"
    
    # Disease to procedure = Improving
    if previous_disease in disease_states and current_disease in procedure_states:
        return "Improving"
    
    # Default: Changed
    return "Changed"

print("  ✓ Disease trend logic defined")

# ============================================================================
# CREATE DIGITAL TWIN STATE FOR EACH PATIENT
# ============================================================================

print("\n[3/5] Processing Digital Twin states for all patients...")

digital_twin_states = []
last_updated = datetime.now().strftime("%Y-%m-%d")

initialized_count = 0
updated_count = 0

for patient_id in patient_df['Patient_ID']:
    # Get all visits for this patient
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    
    if len(patient_visits) == 0:
        print(f"  ⚠ Warning: Patient {patient_id} has no visits. Skipping...")
        continue
    
    # Get the latest visit
    latest_visit = patient_visits.iloc[-1]
    current_visit_id = latest_visit['Visit_ID']
    current_visit_no = latest_visit['Visit_No']
    current_disease = latest_visit['Disease_Name']
    
    # Get previous disease (if exists)
    if len(patient_visits) > 1:
        previous_disease = patient_visits.iloc[-2]['Disease_Name']
        twin_status = "Updated"
        updated_count += 1
    else:
        previous_disease = None
        twin_status = "Initialized"
        initialized_count += 1
    
    # Get the latest risk assessment
    patient_risks = risk_df[risk_df['Patient_ID'] == patient_id]
    latest_risk = patient_risks[patient_risks['Visit_ID'] == current_visit_id].iloc[0]
    
    risk_score = latest_risk['Risk_Score']
    risk_category = latest_risk['Risk_Category']
    
    # Determine disease trend
    disease_trend = determine_disease_trend(previous_disease, current_disease)
    
    # AI Status (always Pending since classifier not built yet)
    ai_status = "Pending"
    
    # Create Digital Twin State record
    twin_state = {
        'Patient_ID': patient_id,
        'Current_Visit': current_visit_id,
        'Current_Disease': current_disease,
        'Previous_Disease': previous_disease if previous_disease else 'None',
        'Risk_Score': risk_score,
        'Risk_Category': risk_category,
        'Disease_Trend': disease_trend,
        'AI_Status': ai_status,
        'Twin_Status': twin_status,
        'Last_Updated': last_updated
    }
    
    digital_twin_states.append(twin_state)

print(f"  ✓ Processed {len(digital_twin_states)} Digital Twin states")

# ============================================================================
# CREATE DATAFRAME AND VALIDATE
# ============================================================================

print("\n[4/5] Creating and validating DigitalTwin_State DataFrame...")

twin_state_df = pd.DataFrame(digital_twin_states)

# Validation checks
validation_passed = True

# Check 1: Every patient has exactly one row
if len(twin_state_df) != len(patient_df):
    print(f"  ✗ ERROR: Expected {len(patient_df)} rows, got {len(twin_state_df)}")
    validation_passed = False
else:
    print(f"  ✓ All {len(patient_df)} patients have Digital Twin states")

# Check 2: No missing values
missing_values = twin_state_df.isnull().sum().sum()
if missing_values > 0:
    print(f"  ✗ ERROR: Found {missing_values} missing values")
    validation_passed = False
else:
    print("  ✓ No missing values")

# Check 3: All Patient_IDs exist in Patient_Master
invalid_patients = set(twin_state_df['Patient_ID']) - set(patient_df['Patient_ID'])
if invalid_patients:
    print(f"  ✗ ERROR: Invalid Patient IDs found: {invalid_patients}")
    validation_passed = False
else:
    print("  ✓ All Patient IDs are valid")

# Check 4: All Current_Visit IDs exist in Visit_History
invalid_visits = set(twin_state_df['Current_Visit']) - set(visit_df['Visit_ID'])
if invalid_visits:
    print(f"  ✗ ERROR: Invalid Visit IDs found: {invalid_visits}")
    validation_passed = False
else:
    print("  ✓ All Current_Visit IDs are valid")

if not validation_passed:
    print("\n✗ VALIDATION FAILED - Digital Twin State NOT created")
    exit(1)

# ============================================================================
# SAVE TO FILE
# ============================================================================

print("\n[5/5] Saving Digital Twin State to file...")

output_path = "METADATA/DigitalTwin_State.csv"
twin_state_df.to_csv(output_path, index=False)
print(f"  ✓ Saved to {output_path}")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("DIGITAL TWIN STATE CREATED")
print("="*80)

print(f"\nPatients Processed    : {len(twin_state_df)}")
print(f"Twin States Created   : {len(twin_state_df)}")

print(f"\nTwin Status Distribution:")
print(f"  - Initialized : {initialized_count} patients (first visit)")
print(f"  - Updated     : {updated_count} patients (multiple visits)")

print(f"\nAI Status:")
print(f"  - Pending     : {len(twin_state_df)} patients (classifier not yet built)")

print(f"\nDisease Trend Distribution:")
trend_counts = twin_state_df['Disease_Trend'].value_counts()
for trend, count in trend_counts.items():
    print(f"  - {trend:12}: {count} patients")

print(f"\nRisk Category Distribution:")
risk_counts = twin_state_df['Risk_Category'].value_counts()
for category in ['Low', 'Medium', 'High', 'Very High']:
    count = risk_counts.get(category, 0)
    percentage = (count / len(twin_state_df)) * 100
    print(f"  - {category:12}: {count:2d} patients ({percentage:5.1f}%)")

print(f"\nCurrent Disease Distribution:")
disease_counts = twin_state_df['Current_Disease'].value_counts()
for disease, count in disease_counts.items():
    print(f"  - {disease:30}: {count} patients")

# ============================================================================
# EXAMPLE RECORDS
# ============================================================================

print("\n" + "="*80)
print("EXAMPLE DIGITAL TWIN STATES")
print("="*80)

# Show a few example patients with different trends
example_patients = ['P001', 'P002', 'P005', 'P007', 'P015']

for patient_id in example_patients:
    if patient_id in twin_state_df['Patient_ID'].values:
        patient_state = twin_state_df[twin_state_df['Patient_ID'] == patient_id].iloc[0]
        print(f"\n{patient_id}:")
        print(f"  Current Visit    : {patient_state['Current_Visit']}")
        print(f"  Current Disease  : {patient_state['Current_Disease']}")
        print(f"  Previous Disease : {patient_state['Previous_Disease']}")
        print(f"  Disease Trend    : {patient_state['Disease_Trend']}")
        print(f"  Risk Score       : {patient_state['Risk_Score']} ({patient_state['Risk_Category']})")
        print(f"  Twin Status      : {patient_state['Twin_Status']}")
        print(f"  Last Updated     : {patient_state['Last_Updated']}")

# ============================================================================
# ARCHITECTURE SUMMARY
# ============================================================================

print("\n" + "="*80)
print("GASTROTWIN DIGITAL TWIN ARCHITECTURE - METADATA COMPLETE")
print("="*80)

print("""
Current Metadata Modules:

1. Disease_Master.csv        → Disease Classification Reference
2. Patient_Master.csv        → Patient Demographics & Risk Factors
3. Visit_History.csv         → Complete Longitudinal Visit History
4. Risk_Assessment.csv       → Visit-wise Dynamic Risk Scores
5. DigitalTwin_State.csv     → Current Patient State Snapshot (NEW)

Relationship:
  Patient_Master  ─────┬───→  Visit_History  ───→  Risk_Assessment
                       │
                       └───→  DigitalTwin_State (latest state only)

Next Steps:
  Phase 5: AI Classifier (EfficientNet)
  Phase 6: Explainable AI (Grad-CAM)
  Phase 7: Interactive Dashboard

The Digital Twin foundation is now complete!
""")

print("="*80)
print("✓ COMPLETED SUCCESSFULLY")
print("="*80)
