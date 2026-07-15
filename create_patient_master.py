"""
Create Patient_Master Table
Generates synthetic patient data for the GastroTwin Digital Twin system
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Ensure METADATA folder exists
os.makedirs("METADATA", exist_ok=True)

# Configuration
NUM_PATIENTS = 50

print("="*60)
print("GENERATING PATIENT_MASTER TABLE")
print("="*60)
print(f"\nCreating {NUM_PATIENTS} synthetic patients...\n")

# Generate patient data
patient_data = []

for i in range(1, NUM_PATIENTS + 1):
    # Patient ID with zero-padding
    patient_id = f"P{i:03d}"
    
    # Random age between 18-80
    age = np.random.randint(18, 81)
    
    # Random gender
    gender = np.random.choice(["Male", "Female"])
    
    # Random height (cm) - typically 150-190
    height_cm = np.random.randint(150, 191)
    
    # Random weight (kg) - typically 45-100
    weight_kg = np.random.randint(45, 101)
    
    # Calculate BMI: weight(kg) / (height(m))^2
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    # Random risk factors (Yes/No)
    smoking = np.random.choice(["Yes", "No"])
    alcohol = np.random.choice(["Yes", "No"])
    diabetes = np.random.choice(["Yes", "No"])
    hypertension = np.random.choice(["Yes", "No"])
    family_history_gi = np.random.choice(["Yes", "No"])
    
    # Append patient record
    patient_data.append({
        "Patient_ID": patient_id,
        "Age": age,
        "Gender": gender,
        "Height_cm": height_cm,
        "Weight_kg": weight_kg,
        "BMI": bmi,
        "Smoking": smoking,
        "Alcohol": alcohol,
        "Diabetes": diabetes,
        "Hypertension": hypertension,
        "Family_History_GI": family_history_gi
    })

# Create DataFrame
patient_df = pd.DataFrame(patient_data)

# Save CSV
output_path = "METADATA/Patient_Master.csv"
patient_df.to_csv(output_path, index=False)

# Statistics
print("="*60)
print("PATIENT STATISTICS")
print("="*60)
print(f"\nTotal Patients: {len(patient_df)}")
print(f"\nAge Range: {patient_df['Age'].min()} - {patient_df['Age'].max()} years")
print(f"Average Age: {patient_df['Age'].mean():.1f} years")

print(f"\nGender Distribution:")
print(f"  - Male: {len(patient_df[patient_df['Gender'] == 'Male'])}")
print(f"  - Female: {len(patient_df[patient_df['Gender'] == 'Female'])}")

print(f"\nBMI Range: {patient_df['BMI'].min()} - {patient_df['BMI'].max()}")
print(f"Average BMI: {patient_df['BMI'].mean():.1f}")

print(f"\nRisk Factors:")
print(f"  - Smoking: {len(patient_df[patient_df['Smoking'] == 'Yes'])} patients")
print(f"  - Alcohol: {len(patient_df[patient_df['Alcohol'] == 'Yes'])} patients")
print(f"  - Diabetes: {len(patient_df[patient_df['Diabetes'] == 'Yes'])} patients")
print(f"  - Hypertension: {len(patient_df[patient_df['Hypertension'] == 'Yes'])} patients")
print(f"  - Family History GI: {len(patient_df[patient_df['Family_History_GI'] == 'Yes'])} patients")

print("\n" + "="*60)
print("SAMPLE PATIENT RECORDS (First 10)")
print("="*60)
print(patient_df.head(10).to_string(index=False))

print("\n" + "="*60)
print(f"✓ Patient_Master.csv created successfully!")
print(f"Location: {output_path}")
print("="*60)
print("\n✓ Table 2 Complete - Ready for Table 3 (Visit_History)!")
