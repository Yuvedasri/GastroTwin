"""
Create Visit_History Table
Links patients to their medical visits with realistic disease progressions
This is the core of the Digital Twin system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

print("="*70)
print("GENERATING VISIT_HISTORY TABLE - DIGITAL TWIN CORE")
print("="*70)

# Load existing tables
print("\n[1/6] Loading existing data...")
disease_df = pd.read_csv("METADATA/Disease_Master.csv")
patient_df = pd.read_csv("METADATA/Patient_Master.csv")
kvasir_df = pd.read_csv("kvasir_metadata.csv")

print(f"  ✓ Loaded {len(disease_df)} diseases")
print(f"  ✓ Loaded {len(patient_df)} patients")
print(f"  ✓ Loaded {len(kvasir_df)} images")

# Disease-specific symptoms
SYMPTOMS = {
    "normal-cecum": ["No symptoms"],
    "normal-pylorus": ["No symptoms"],
    "normal-z-line": ["No symptoms"],
    "esophagitis": [
        "Heartburn",
        "Chest pain",
        "Difficulty swallowing",
        "Heartburn, Chest pain"
    ],
    "polyps": [
        "Abdominal discomfort",
        "Rectal bleeding",
        "Abdominal discomfort, Rectal bleeding"
    ],
    "ulcerative-colitis": [
        "Abdominal pain",
        "Diarrhea",
        "Blood in stool",
        "Abdominal pain, Diarrhea"
    ],
    "dyed-lifted-polyps": [
        "Post-polypectomy follow-up"
    ],
    "dyed-resection-margins": [
        "Post-procedure review"
    ]
}

# Disease progression templates (realistic clinical scenarios)
PROGRESSION_TEMPLATES = [
    # Template A: Healthy (30% of patients)
    ["normal-cecum", "normal-cecum", "normal-cecum"],
    ["normal-pylorus", "normal-pylorus", "normal-pylorus"],
    ["normal-z-line", "normal-z-line", "normal-z-line"],
    
    # Template B: Early Disease (20% of patients)
    ["normal-z-line", "esophagitis", "esophagitis"],
    ["normal-cecum", "polyps", "polyps"],
    
    # Template C: Progression (20% of patients)
    ["normal-z-line", "esophagitis", "polyps"],
    ["normal-pylorus", "esophagitis", "esophagitis", "polyps"],
    
    # Template D: Chronic (15% of patients)
    ["ulcerative-colitis", "ulcerative-colitis", "ulcerative-colitis"],
    ["ulcerative-colitis", "ulcerative-colitis", "ulcerative-colitis", "ulcerative-colitis"],
    
    # Template E: Post Procedure (15% of patients)
    ["polyps", "dyed-lifted-polyps", "dyed-resection-margins"],
    ["polyps", "polyps", "dyed-lifted-polyps", "dyed-resection-margins"],
]

# Map Kvasir folder names to disease names in Disease_Master
DISEASE_MAPPING = {
    "normal-cecum": "Normal-Cecum",
    "normal-pylorus": "Normal-Pylorus",
    "normal-z-line": "Normal-Z-Line",
    "esophagitis": "Esophagitis",
    "polyps": "Polyps",
    "ulcerative-colitis": "Ulcerative-Colitis",
    "dyed-lifted-polyps": "Dyed-Lifted-Polyps",
    "dyed-resection-margins": "Dyed-Resection-Margins"
}

print("\n[2/6] Preparing image database...")
# Create image lookup by disease
image_by_disease = {}
for disease_folder in DISEASE_MAPPING.keys():
    disease_images = kvasir_df[kvasir_df['Disease'] == disease_folder]
    image_by_disease[disease_folder] = disease_images.reset_index(drop=True)
    print(f"  ✓ {disease_folder}: {len(disease_images)} images available")

print("\n[3/6] Generating patient visit histories...")

visit_history = []
visit_counter = 1
base_date = datetime(2025, 1, 15)

for idx, patient_row in patient_df.iterrows():
    patient_id = patient_row['Patient_ID']
    
    # Select a random progression template
    progression = np.random.choice(range(len(PROGRESSION_TEMPLATES)))
    disease_sequence = PROGRESSION_TEMPLATES[progression]
    
    # Number of visits for this patient (2-5 visits)
    num_visits = len(disease_sequence)
    
    # Generate visits for this patient
    for visit_no in range(1, num_visits + 1):
        visit_id = f"V{visit_counter:04d}"
        
        # Calculate visit date (6-month intervals)
        visit_date = base_date + timedelta(days=(visit_no - 1) * 180)
        visit_date_str = visit_date.strftime("%Y-%m-%d")
        
        # Get disease for this visit
        disease_folder = disease_sequence[visit_no - 1]
        disease_name_mapped = DISEASE_MAPPING[disease_folder]
        
        # Get Disease_ID from Disease_Master
        disease_info = disease_df[disease_df['Disease_Name'] == disease_name_mapped]
        disease_id = disease_info['Disease_ID'].values[0]
        
        # Select a random image for this disease
        available_images = image_by_disease[disease_folder]
        selected_image = available_images.sample(n=1).iloc[0]
        
        # Get symptoms for this disease
        symptoms = np.random.choice(SYMPTOMS[disease_folder])
        
        # Create visit record
        visit_record = {
            "Visit_ID": visit_id,
            "Patient_ID": patient_id,
            "Visit_No": visit_no,
            "Visit_Date": visit_date_str,
            "Disease_ID": disease_id,
            "Disease_Name": disease_name_mapped,
            "Image_Name": selected_image['Image_Name'],
            "Image_Path": selected_image['Image_Path'],
            "Symptoms": symptoms,
            "AI_Prediction": "",
            "Confidence": "",
            "Risk_Level": ""
        }
        
        visit_history.append(visit_record)
        visit_counter += 1
    
    if (idx + 1) % 10 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(patient_df)} patients...")

print(f"  ✓ Generated {len(visit_history)} total visits")

print("\n[4/6] Creating Visit_History DataFrame...")
visit_df = pd.DataFrame(visit_history)

print("\n[5/6] Analyzing visit statistics...")

# Statistics
total_visits = len(visit_df)
total_patients = visit_df['Patient_ID'].nunique()
avg_visits = total_visits / total_patients

print(f"\n{'='*70}")
print("VISIT HISTORY STATISTICS")
print(f"{'='*70}")
print(f"\nTotal Visits: {total_visits}")
print(f"Total Patients: {total_patients}")
print(f"Average Visits per Patient: {avg_visits:.1f}")
print(f"Visit Date Range: {visit_df['Visit_Date'].min()} to {visit_df['Visit_Date'].max()}")

print(f"\nDisease Distribution:")
disease_counts = visit_df['Disease_Name'].value_counts()
for disease, count in disease_counts.items():
    percentage = (count / total_visits) * 100
    print(f"  - {disease}: {count} visits ({percentage:.1f}%)")

print(f"\nVisits per Patient Distribution:")
visits_per_patient = visit_df.groupby('Patient_ID').size().value_counts().sort_index()
for num_visits, count in visits_per_patient.items():
    print(f"  - {num_visits} visits: {count} patients")

print("\n[6/6] Saving Visit_History.csv...")
output_path = "METADATA/Visit_History.csv"
visit_df.to_csv(output_path, index=False)

print(f"\n{'='*70}")
print("SAMPLE VISIT RECORDS (First 15)")
print(f"{'='*70}")
sample_cols = ['Visit_ID', 'Patient_ID', 'Visit_No', 'Visit_Date', 'Disease_Name', 'Symptoms']
print(visit_df[sample_cols].head(15).to_string(index=False))

print(f"\n{'='*70}")
print("EXAMPLE: Patient Visit Progression")
print(f"{'='*70}")
# Show one patient's full history
example_patient = visit_df[visit_df['Patient_ID'] == 'P001']
print(f"\nPatient P001 Visit History:")
for _, row in example_patient.iterrows():
    print(f"  Visit {row['Visit_No']} ({row['Visit_Date']}): {row['Disease_Name']} - {row['Symptoms']}")

print(f"\n{'='*70}")
print(f"✓ Visit_History.csv created successfully!")
print(f"Location: {output_path}")
print(f"Total Records: {len(visit_df)}")
print(f"{'='*70}")
print("\n✓ Table 3 Complete - Digital Twin Database Ready!")
print("  Next: Create Risk_Rules to enable AI-powered risk assessment")
