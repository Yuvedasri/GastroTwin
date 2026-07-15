"""
GastroTwin Visit History Generator v2.0
Creates longitudinal patient visit histories with clinically meaningful trajectories

IMPROVEMENTS IN V2.0:
- Trajectory templates (Healthy, Inflammatory, Stable, Progression, Post-Procedure)
- Trajectory_Type column for each visit
- Ground truth vs. AI prediction separation
- AI feature placeholders (empty until Phase 5)
- Enhanced validation and documentation

Author: GastroTwin Research Project
Version: 2.0 (Metadata v1.0)
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

print("="*80)
print("GASTROTWIN VISIT HISTORY GENERATOR V2.0")
print("Creating Longitudinal Patient Trajectories with Clinical Templates")
print("="*80)

# ============================================================================
# CLINICAL TRAJECTORY TEMPLATES
# ============================================================================

print("\n[1/7] Defining clinical trajectory templates...")

TRAJECTORY_TEMPLATES = {
    'Healthy': {
        'visits': ['Normal-Cecum', 'Normal-Pylorus', 'Normal-Z-Line'],
        'count': 3,
        'description': 'Routine surveillance with no findings',
        'population_pct': 16
    },
    'Inflammatory_Progression': {
        'visits': ['Normal-Z-Line', 'Esophagitis', 'Esophagitis', 'Polyps'],
        'count': 4,
        'description': 'Development and progression of inflammatory disease',
        'population_pct': 20
    },
    'Stable_Chronic': {
        'visits': ['Ulcerative-Colitis', 'Ulcerative-Colitis', 'Ulcerative-Colitis'],
        'count': 3,
        'description': 'Chronic disease under management',
        'population_pct': 32
    },
    'Disease_Progression': {
        'visits': ['Normal-Cecum', 'Esophagitis', 'Polyps'],
        'count': 3,
        'description': 'Disease worsening despite intervention',
        'population_pct': 20
    },
    'Post_Procedure': {
        'visits': ['Polyps', 'Dyed-Lifted-Polyps', 'Dyed-Resection-Margins'],
        'count': 3,
        'description': 'Polypectomy with staged resection',
        'population_pct': 12
    }
}

# Alternative trajectories for variety
TRAJECTORY_VARIANTS = {
    'Healthy': [
        ['Normal-Cecum', 'Normal-Cecum', 'Normal-Cecum'],
        ['Normal-Pylorus', 'Normal-Pylorus', 'Normal-Pylorus'],
        ['Normal-Z-Line', 'Normal-Z-Line', 'Normal-Z-Line'],
    ],
    'Stable_Chronic': [
        ['Ulcerative-Colitis', 'Ulcerative-Colitis', 'Ulcerative-Colitis', 'Ulcerative-Colitis'],
        ['Polyps', 'Polyps', 'Polyps'],
        ['Esophagitis', 'Esophagitis', 'Esophagitis'],
    ]
}

print(f"  ✓ Defined {len(TRAJECTORY_TEMPLATES)} trajectory templates")

# ============================================================================
# DISEASE-SPECIFIC SYMPTOMS
# ============================================================================

SYMPTOMS = {
    "Normal-Cecum": ["No symptoms"],
    "Normal-Pylorus": ["No symptoms"],
    "Normal-Z-Line": ["No symptoms"],
    "Esophagitis": ["Heartburn", "Chest pain", "Difficulty swallowing", "Regurgitation"],
    "Polyps": ["Abdominal discomfort", "Rectal bleeding", "Change in bowel habits"],
    "Ulcerative-Colitis": ["Abdominal pain", "Diarrhea", "Blood in stool", "Weight loss"],
    "Dyed-Lifted-Polyps": ["Post-polypectomy follow-up", "Mild discomfort"],
    "Dyed-Resection-Margins": ["Post-procedure review", "Healing assessment"]
}

# ============================================================================
# LOAD EXISTING DATA
# ============================================================================

print("\n[2/7] Loading existing metadata...")

# Load Disease Master
disease_df = pd.read_csv("METADATA/Disease_Master.csv")
print(f"  ✓ Loaded {len(disease_df)} diseases from Disease_Master.csv")

# Load Patient Master
patient_df = pd.read_csv("METADATA/Patient_Master.csv")
print(f"  ✓ Loaded {len(patient_df)} patients from Patient_Master.csv")

# Load Kvasir Metadata
kvasir_df = pd.read_csv("kvasir_metadata.csv")
print(f"  ✓ Loaded {len(kvasir_df)} images from kvasir_metadata.csv")

# ============================================================================
# ASSIGN TRAJECTORY TEMPLATES TO PATIENTS
# ============================================================================

print("\n[3/7] Assigning trajectory templates to patients...")

# Calculate number of patients per template
total_patients = len(patient_df)
template_assignments = {}

for template_name, template_info in TRAJECTORY_TEMPLATES.items():
    count = int(total_patients * template_info['population_pct'] / 100)
    template_assignments[template_name] = count

# Adjust for rounding
assigned_total = sum(template_assignments.values())
if assigned_total < total_patients:
    # Add remaining to most common template
    template_assignments['Stable_Chronic'] += (total_patients - assigned_total)

# Create patient-template mapping
patient_templates = {}
patient_ids = patient_df['Patient_ID'].tolist()
random.shuffle(patient_ids)

current_idx = 0
for template_name, count in template_assignments.items():
    for i in range(count):
        if current_idx < len(patient_ids):
            patient_templates[patient_ids[current_idx]] = template_name
            current_idx += 1

print(f"  ✓ Assigned templates to {len(patient_templates)} patients")
for template_name, count in template_assignments.items():
    print(f"    - {template_name}: {count} patients")

# ============================================================================
# GENERATE VISIT HISTORIES
# ============================================================================

print("\n[4/7] Generating visit histories with trajectory templates...")

visits = []
visit_id_counter = 1
start_date = datetime(2025, 1, 15)

for patient_id in patient_df['Patient_ID']:
    # Get assigned trajectory
    trajectory_type = patient_templates.get(patient_id, 'Stable_Chronic')
    template = TRAJECTORY_TEMPLATES[trajectory_type]
    
    # Get disease sequence
    if trajectory_type in TRAJECTORY_VARIANTS:
        # Use a variant for variety
        disease_sequence = random.choice(TRAJECTORY_VARIANTS[trajectory_type])
    else:
        disease_sequence = template['visits']
    
    # Generate visits
    for visit_no, disease_name in enumerate(disease_sequence, start=1):
        # Calculate visit date (6-month intervals)
        visit_date = start_date + timedelta(days=180 * (visit_no - 1))
        visit_date_str = visit_date.strftime("%Y-%m-%d")
        
        # Get Disease_ID
        disease_row = disease_df[disease_df['Disease_Name'] == disease_name]
        if len(disease_row) == 0:
            print(f"  ⚠ Warning: Disease '{disease_name}' not found in Disease_Master")
            continue
        disease_id = disease_row.iloc[0]['Disease_ID']
        
        # Select Kvasir image for this disease
        # Convert disease name to Kvasir format (e.g., "Polyps" -> "polyps")
        kvasir_disease_name = disease_name.lower().replace(' ', '-')
        disease_images = kvasir_df[kvasir_df['Disease'].str.lower() == kvasir_disease_name.lower()]
        if len(disease_images) == 0:
            print(f"  ⚠ Warning: No images for disease '{disease_name}' (searched for '{kvasir_disease_name}')")
            continue
        
        selected_image = disease_images.sample(n=1, random_state=visit_id_counter).iloc[0]
        
        # Select symptoms
        symptom_list = SYMPTOMS.get(disease_name, ["No specific symptoms"])
        if len(symptom_list) > 1:
            selected_symptoms = ", ".join(random.sample(symptom_list, k=min(2, len(symptom_list))))
        else:
            selected_symptoms = symptom_list[0]
        
        # Create visit record with AI placeholders
        visit = {
            'Visit_ID': f"V{visit_id_counter:04d}",
            'Patient_ID': patient_id,
            'Visit_No': visit_no,
            'Visit_Date': visit_date_str,
            'Trajectory_Type': trajectory_type,
            
            # Ground Truth (from Kvasir)
            'Disease_ID': disease_id,
            'GroundTruth_Disease': disease_name,
            'Image_Name': selected_image['Image_Name'],
            'Image_Path': selected_image['Image_Path'],
            'Symptoms': selected_symptoms,
            
            # AI Predictions (empty until Phase 5)
            'Predicted_Disease': '',
            'Prediction_Confidence': '',
            
            # Lesion Features (empty until Phase 5)
            'Disease_Severity': '',
            'Lesion_Area': '',
            'Lesion_Perimeter': '',
            'Lesion_Circularity': '',
            'Texture_Score': '',
            'Shape_Score': '',
            
            # AI Output Paths (empty until Phase 5)
            'Segmentation_Path': '',
            'Image_Embedding_Path': '',
            'GradCAM_Path': '',
            
            # Legacy fields for backward compatibility
            'Risk_Level': ''
        }
        
        visits.append(visit)
        visit_id_counter += 1

print(f"  ✓ Generated {len(visits)} visits across {len(patient_df)} patients")

# ============================================================================
# CREATE DATAFRAME AND VALIDATE
# ============================================================================

print("\n[5/7] Creating and validating Visit_History DataFrame...")

visit_df = pd.DataFrame(visits)

# Validation checks
validation_passed = True

# Check 1: All patients have visits
patients_with_visits = visit_df['Patient_ID'].nunique()
if patients_with_visits != len(patient_df):
    print(f"  ✗ ERROR: Expected {len(patient_df)} patients, found {patients_with_visits}")
    validation_passed = False
else:
    print(f"  ✓ All {len(patient_df)} patients have visits")

# Check 2: Trajectory consistency per patient
for patient_id in visit_df['Patient_ID'].unique():
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id]
    trajectory_types = patient_visits['Trajectory_Type'].unique()
    if len(trajectory_types) > 1:
        print(f"  ✗ ERROR: Patient {patient_id} has inconsistent trajectories: {trajectory_types}")
        validation_passed = False

print("  ✓ Trajectory consistency validated")

# Check 3: Visit numbers are sequential
for patient_id in visit_df['Patient_ID'].unique():
    patient_visits = visit_df[visit_df['Patient_ID'] == patient_id].sort_values('Visit_No')
    visit_numbers = patient_visits['Visit_No'].tolist()
    expected = list(range(1, len(visit_numbers) + 1))
    if visit_numbers != expected:
        print(f"  ✗ ERROR: Patient {patient_id} has non-sequential visits: {visit_numbers}")
        validation_passed = False

print("  ✓ Visit numbering validated")

# Check 4: All images exist in Kvasir
invalid_images = set(visit_df['Image_Name']) - set(kvasir_df['Image_Name'])
if invalid_images:
    print(f"  ✗ ERROR: Invalid images found: {list(invalid_images)[:5]}... ({len(invalid_images)} total)")
    validation_passed = False
else:
    print("  ✓ All images exist in Kvasir dataset")

if not validation_passed:
    print("\n✗ VALIDATION FAILED")
    exit(1)

# ============================================================================
# SAVE TO FILE
# ============================================================================

print("\n[6/7] Saving Visit_History to file...")

output_path = "METADATA/Visit_History.csv"
visit_df.to_csv(output_path, index=False)
print(f"  ✓ Saved to {output_path}")

# ============================================================================
# STATISTICS
# ============================================================================

print("\n[7/7] Summary statistics...")

print(f"\n{'='*80}")
print("VISIT HISTORY GENERATION COMPLETE")
print(f"{'='*80}")

print(f"\nTotal Records: {len(visit_df)}")
print(f"Total Patients: {visit_df['Patient_ID'].nunique()}")
print(f"Date Range: {visit_df['Visit_Date'].min()} to {visit_df['Visit_Date'].max()}")

print(f"\nVisits Per Patient Distribution:")
visits_per_patient = visit_df.groupby('Patient_ID').size().value_counts().sort_index()
for count, freq in visits_per_patient.items():
    print(f"  - {count} visits: {freq} patients")

print(f"\nTrajectory Type Distribution:")
trajectory_dist = visit_df.groupby('Patient_ID')['Trajectory_Type'].first().value_counts()
for trajectory, count in trajectory_dist.items():
    percentage = (count / len(patient_df)) * 100
    print(f"  - {trajectory:25}: {count:2d} patients ({percentage:5.1f}%)")

print(f"\nDisease Distribution (All Visits):")
disease_dist = visit_df['GroundTruth_Disease'].value_counts()
for disease, count in disease_dist.items():
    percentage = (count / len(visit_df)) * 100
    print(f"  - {disease:30}: {count:3d} visits ({percentage:5.1f}%)")

print(f"\nAI Placeholder Columns (Empty Until Phase 5):")
ai_columns = [
    'Predicted_Disease', 'Prediction_Confidence',
    'Disease_Severity', 'Lesion_Area', 'Lesion_Perimeter',
    'Lesion_Circularity', 'Texture_Score', 'Shape_Score',
    'Segmentation_Path', 'Image_Embedding_Path', 'GradCAM_Path'
]
for col in ai_columns:
    empty_count = visit_df[col].isna().sum() + (visit_df[col] == '').sum()
    print(f"  - {col:25}: {empty_count}/{len(visit_df)} empty (expected)")

print(f"\n{'='*80}")
print("✓ VISIT HISTORY V2.0 CREATED SUCCESSFULLY")
print(f"{'='*80}")
print("\nNext Steps:")
print("  1. Run: python create_risk_engine.py")
print("  2. Run: python create_digital_twin_state_v2.py")
print("  3. Verify all metadata with validation scripts")
print("\nMetadata Version: v1.0")
