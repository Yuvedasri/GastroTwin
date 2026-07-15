"""
Create Disease_Master Table
This is the reference table for all disease classifications in the GastroTwin system
"""

import pandas as pd
import os

# Ensure METADATA folder exists
os.makedirs("METADATA", exist_ok=True)

# Disease information - All 8 classes from Kvasir dataset
disease_data = [
    {
        "Disease_ID": "D001",
        "Disease_Name": "Normal-Cecum",
        "Category": "Healthy",
        "Description": "Normal cecum with no abnormalities"
    },
    {
        "Disease_ID": "D002",
        "Disease_Name": "Normal-Pylorus",
        "Category": "Healthy",
        "Description": "Normal pylorus with no abnormalities"
    },
    {
        "Disease_ID": "D003",
        "Disease_Name": "Normal-Z-Line",
        "Category": "Healthy",
        "Description": "Normal Z-line (gastroesophageal junction)"
    },
    {
        "Disease_ID": "D004",
        "Disease_Name": "Esophagitis",
        "Category": "Disease",
        "Description": "Inflammation of the esophagus"
    },
    {
        "Disease_ID": "D005",
        "Disease_Name": "Polyps",
        "Category": "Disease",
        "Description": "Abnormal tissue growth in the GI tract"
    },
    {
        "Disease_ID": "D006",
        "Disease_Name": "Ulcerative-Colitis",
        "Category": "Disease",
        "Description": "Chronic inflammatory bowel disease"
    },
    {
        "Disease_ID": "D007",
        "Disease_Name": "Dyed-Lifted-Polyps",
        "Category": "Disease",
        "Description": "Polyps after dye spraying and lifting procedure"
    },
    {
        "Disease_ID": "D008",
        "Disease_Name": "Dyed-Resection-Margins",
        "Category": "Disease",
        "Description": "Resection margins after dye spraying procedure"
    }
]

# Create DataFrame
disease_df = pd.DataFrame(disease_data)

# Save CSV
output_path = "METADATA/Disease_Master.csv"
disease_df.to_csv(output_path, index=False)

print("="*60)
print("✓ Disease_Master.csv created successfully!")
print("="*60)
print(f"\nLocation: {output_path}")
print(f"Total Diseases: {len(disease_df)}")
print(f"\nBreakdown:")
print(f"  - Healthy: {len(disease_df[disease_df['Category'] == 'Healthy'])}")
print(f"  - Disease: {len(disease_df[disease_df['Category'] == 'Disease'])}")
print("\n" + "="*60)
print("Disease Master Table:")
print("="*60)
print(disease_df.to_string(index=False))
print("\n✓ Table 1 Complete - Ready for Phase 2!")
