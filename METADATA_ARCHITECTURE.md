# GastroTwin Metadata Architecture

## Overview
The GastroTwin Digital Twin framework now has **5 complete metadata modules** that form the foundation for AI-powered longitudinal disease monitoring.

---

## Metadata Files Structure

```
METADATA/
├── Disease_Master.csv         (8 records)   - Disease Classification Reference
├── Patient_Master.csv         (50 records)  - Patient Demographics & Risk Factors  
├── Visit_History.csv          (160 records) - Complete Longitudinal Visit History
├── Risk_Assessment.csv        (160 records) - Visit-wise Dynamic Risk Scores
└── DigitalTwin_State.csv      (50 records)  - Current Patient State Snapshot ✨ NEW
```

---

## Module Relationships

```
┌─────────────────────┐
│ Disease_Master.csv  │ ← Reference table for all diseases
└─────────────────────┘

┌─────────────────────┐
│ Patient_Master.csv  │ ← Demographics, risk factors (age, BMI, smoking, etc.)
└──────────┬──────────┘
           │
           ├──────────────────────────────────────┐
           │                                      │
           ▼                                      ▼
┌─────────────────────┐              ┌─────────────────────┐
│ Visit_History.csv   │              │ DigitalTwin_State   │
│ (All visits)        │              │ (Latest visit only) │
└──────────┬──────────┘              └─────────────────────┘
           │                                      ▲
           ▼                                      │
┌─────────────────────┐                          │
│ Risk_Assessment.csv │──────────────────────────┘
│ (Risk per visit)    │  (Latest risk linked to current state)
└─────────────────────┘
```

---

## File Details

### 1. Disease_Master.csv
**Purpose:** Reference table for disease classification  
**Rows:** 8  
**Key Columns:**
- Disease_ID
- Disease_Name
- Category
- Severity_Level
- Description

**Example:**
```csv
D001,Normal-Cecum,Normal,0,Healthy cecum tissue
D002,Esophagitis,Inflammatory,2,Inflammation of esophagus
D003,Polyps,Pre-Cancerous,3,Abnormal tissue growth
```

---

### 2. Patient_Master.csv
**Purpose:** Patient demographics and baseline risk factors  
**Rows:** 50 synthetic patients  
**Key Columns:**
- Patient_ID
- Age, Gender, Height_cm, Weight_kg, BMI
- Smoking, Alcohol, Diabetes, Hypertension
- Family_History_GI

**Example:**
```csv
P001,45,Male,172,70,23.7,No,Yes,No,Yes,No
P002,75,Female,160,64,25.0,Yes,No,Yes,Yes,No
```

---

### 3. Visit_History.csv
**Purpose:** Complete longitudinal patient visit records  
**Rows:** 160 visits across 50 patients (2-5 visits per patient)  
**Key Columns:**
- Visit_ID, Patient_ID, Visit_No, Visit_Date
- Disease_ID, Disease_Name
- Image_Name, Image_Path
- Symptoms
- AI_Prediction, Confidence, Risk_Level (to be filled by AI module)

**Example:**
```csv
V0001,P001,1,2025-01-15,D002,Normal-Pylorus,image001.jpg,No symptoms,...
V0002,P001,2,2025-07-14,D004,Esophagitis,image145.jpg,Heartburn,...
V0003,P001,3,2026-01-10,D004,Esophagitis,image289.jpg,Chest pain,...
```

**Disease Progression Patterns:**
- Template A: Normal → Normal → Normal (Healthy)
- Template B: Normal → Esophagitis → Esophagitis (Early Disease)
- Template C: Normal → Esophagitis → Polyps (Progression)
- Template D: Ulcerative-Colitis → UC → UC (Chronic)
- Template E: Polyps → Dyed Lifted → Dyed Resection (Post-Procedure)

---

### 4. Risk_Assessment.csv
**Purpose:** Dynamic risk scores calculated for each visit  
**Rows:** 160 assessments (one per visit)  
**Key Columns:**
- Risk_ID, Patient_ID, Visit_ID, Visit_No, Visit_Date
- Disease_Name
- Risk_Score, Risk_Category
- Risk_Explanation

**Risk Calculation:**
```
Risk_Score = Patient_Baseline_Risk + Disease_Risk + Progression_Risk
```

**Risk Categories:**
- 0-24: Low
- 25-49: Medium
- 50-74: High
- 75+: Very High

**Example:**
```csv
R0001,P001,V0001,1,2025-01-15,Normal-Pylorus,50,High,Patient factors: Smoking Diabetes...
R0002,P001,V0002,2,2025-07-14,Esophagitis,80,Very High,Disease progression from Normal...
```

---

### 5. DigitalTwin_State.csv ✨ NEW
**Purpose:** Current state snapshot of each patient's Digital Twin  
**Rows:** 50 (one per patient)  
**Key Columns:**
- Patient_ID
- Current_Visit
- Current_Disease, Previous_Disease
- Risk_Score, Risk_Category
- Disease_Trend
- AI_Status, Twin_Status
- Last_Updated

**Disease Trend Logic:**
- **Initialized:** First visit, no previous data
- **Stable:** Same disease as previous visit
- **Progressing:** Disease worsening (Normal → Disease, or Disease → Worse Disease)
- **Improving:** Disease to procedure or recovery
- **Recovering:** Post-procedure improvement

**Twin Status:**
- **Initialized:** Patient has only 1 visit
- **Updated:** Patient has multiple visits
- **Archived:** (Future use - inactive patients)

**AI Status:**
- **Pending:** AI classifier not yet run
- **Completed:** (Future - after AI inference)

**Example:**
```csv
P001,V0004,Polyps,Esophagitis,100,Very High,Progressing,Pending,Updated,2026-07-15
P007,V0023,Dyed-Resection-Margins,Dyed-Lifted-Polyps,40,Medium,Recovering,Pending,Updated,2026-07-15
```

---

## Key Statistics

| Module | Records | Patients | Visits | Description |
|--------|---------|----------|--------|-------------|
| Disease_Master | 8 | - | - | Disease reference |
| Patient_Master | 50 | 50 | - | Patient profiles |
| Visit_History | 160 | 50 | 160 | All visits |
| Risk_Assessment | 160 | 50 | 160 | Risk per visit |
| DigitalTwin_State | 50 | 50 | 50 | Latest state only |

### Current Digital Twin State Distribution:
- **Risk Categories:** Low (6%), Medium (30%), High (38%), Very High (26%)
- **Disease Trends:** Stable (64%), Progressing (20%), Recovering (16%)
- **Twin Status:** All Updated (100% have multiple visits)
- **AI Status:** All Pending (100% awaiting classifier)

---

## Data Flow in GastroTwin Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1-4: METADATA (COMPLETE ✓)                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────┐
        │ Kvasir Dataset (8000 images)          │
        │ + Visit_History.csv (160 records)     │
        └───────────────┬───────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │ PHASE 5: AI Classifier (EfficientNet) │ ← NEXT
        │ - Train on Kvasir images              │
        │ - Update Visit_History with predictions│
        │ - Update DigitalTwin_State AI_Status  │
        └───────────────┬───────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │ PHASE 6: Explainable AI (Grad-CAM)    │
        │ - Generate visual explanations        │
        │ - Highlight disease regions           │
        └───────────────┬───────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │ PHASE 7: Dashboard (Streamlit)        │
        │ - Visualize Digital Twin states       │
        │ - Show longitudinal progressions      │
        │ - Display risk trends                 │
        │ - Interactive Grad-CAM explanations   │
        └───────────────────────────────────────┘
```

---

## Why This Architecture?

### Separation of Concerns:
1. **Visit_History.csv** = Historical record (never deleted, append-only)
2. **Risk_Assessment.csv** = Calculated risk per visit (can be recalculated)
3. **DigitalTwin_State.csv** = Current snapshot (updated with each new visit)

### Benefits:
- ✅ **Scalability:** Easy to add new patients and visits
- ✅ **Modularity:** Each file has a single, clear purpose
- ✅ **Traceability:** Complete audit trail of all visits
- ✅ **Performance:** Current state queries don't scan history
- ✅ **AI-Ready:** Structure supports ML pipeline integration
- ✅ **Dashboard-Ready:** Optimized for real-time visualization

---

## Future Integration Points

### When AI Classifier is Built:
1. Read images from Visit_History
2. Run EfficientNet inference
3. Update Visit_History: `AI_Prediction`, `Confidence`
4. Update DigitalTwin_State: `AI_Status` = "Completed"

### When Dashboard is Built:
1. Load DigitalTwin_State for current patient overview
2. Load Visit_History for longitudinal charts
3. Load Risk_Assessment for risk trend analysis
4. Link to Grad-CAM explanations

---

## Generation Scripts

All metadata can be regenerated using:

```bash
python create_disease_master.py        # Creates Disease_Master.csv
python create_patient_master.py        # Creates Patient_Master.csv
python create_visit_history.py         # Creates Visit_History.csv
python create_risk_engine.py           # Creates Risk_Assessment.csv
python create_digital_twin_state.py    # Creates DigitalTwin_State.csv
```

---

## Validation Checklist

✅ All patients in Patient_Master have visits  
✅ All visits in Visit_History have risk assessments  
✅ All patients in Patient_Master have Digital Twin states  
✅ DigitalTwin_State always points to latest visit  
✅ No orphaned records  
✅ No missing values  
✅ All foreign keys valid  
✅ Disease progression patterns realistic  

---

## Status: Metadata Foundation Complete ✓

The Digital Twin metadata architecture is now **complete and ready** for Phase 5: AI Model Development.

**Next Step:** Build EfficientNet classifier for automated disease detection from endoscopy images.
