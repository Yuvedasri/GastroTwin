# Synthetic Longitudinal Patient Trajectory Generation for GastroTwin

## Executive Summary

This document describes the methodology used to create synthetic longitudinal patient trajectories for the GastroTwin Digital Twin framework. The approach addresses a critical gap in publicly available medical imaging datasets: the lack of repeated visits from the same patients over time.

---

## 1. Motivation and Research Gap

### 1.1 The Longitudinal Data Problem

Most publicly available gastrointestinal endoscopy datasets, including Kvasir-v2, provide:
- ✅ High-quality labeled images
- ✅ Multiple disease categories
- ✅ Large sample sizes

But they lack:
- ❌ Patient identifiers linking multiple images
- ❌ Temporal information (visit dates)
- ❌ Disease progression data
- ❌ Longitudinal follow-up records

### 1.2 Why Longitudinal Data Matters for Digital Twins

A Digital Twin is not a single-point prediction system. It requires:

1. **Temporal Context:** How has the patient's condition changed?
2. **Progression Tracking:** Is the disease stable, worsening, or improving?
3. **Risk Evolution:** How does risk change over time?
4. **Treatment Response:** Did interventions lead to improvement?
5. **Predictive Capability:** What is the likely future trajectory?

**Without longitudinal data, we cannot build a true Digital Twin.**

### 1.3 Why Real Longitudinal Data is Unavailable

Real longitudinal medical data faces significant barriers:

- **Privacy Regulations:** HIPAA, GDPR prevent sharing patient identifiers
- **Clinical Practice:** Follow-up images rarely published in datasets
- **Data Collection Costs:** Expensive to track patients over months/years
- **Institutional Silos:** Data fragmented across hospitals
- **Publication Bias:** Research focuses on diagnosis, not monitoring

**Result:** No publicly available longitudinal GI endoscopy dataset exists.

---

## 2. Synthetic Trajectory Design Approach

### 2.1 Design Philosophy

Since real longitudinal data is unavailable, we created **clinically plausible synthetic trajectories** by:

1. Using real Kvasir images as the visual foundation
2. Designing realistic disease progression templates
3. Assigning synthetic patient identifiers
4. Creating temporal sequences that match clinical patterns
5. Documenting all assumptions transparently

**This approach allows Digital Twin research to proceed while being transparent about data limitations.**

### 2.2 Clinical Trajectory Templates

We designed **5 trajectory templates** based on gastroenterological clinical patterns:

#### Template A: Healthy Surveillance
```
Normal → Normal → Normal
```
**Clinical Context:** Routine screening with no findings  
**Population:** 16% of synthetic patients  
**Temporal Pattern:** 6-month intervals  
**Clinical Reasoning:** Low-risk patients in surveillance programs

#### Template B: Inflammatory Progression
```
Normal → Esophagitis → Esophagitis (or Polyps if progressing)
```
**Clinical Context:** Development and monitoring of inflammatory disease  
**Population:** 20% of synthetic patients  
**Temporal Pattern:** 6-month follow-ups after initial diagnosis  
**Clinical Reasoning:** Esophagitis requires monitoring; may progress to complications

#### Template C: Stable Chronic Disease
```
Ulcerative Colitis → Ulcerative Colitis → Ulcerative Colitis
Polyps → Polyps → Polyps
```
**Clinical Context:** Chronic disease under management  
**Population:** 32% of synthetic patients  
**Temporal Pattern:** Regular monitoring every 6 months  
**Clinical Reasoning:** Chronic conditions require ongoing surveillance

#### Template D: Disease Progression
```
Normal → Esophagitis → Polyps
Normal → Polyps → Polyps
```
**Clinical Context:** Disease worsening despite intervention  
**Population:** 20% of synthetic patients  
**Temporal Pattern:** Initial diagnosis, then progression at 6-month intervals  
**Clinical Reasoning:** Some patients progress despite treatment

#### Template E: Post-Procedure Recovery
```
Polyps → Dyed-Lifted-Polyps → Dyed-Resection-Margins
```
**Clinical Context:** Polypectomy with staged resection  
**Population:** 12% of synthetic patients  
**Temporal Pattern:** Procedure → Immediate follow-up → Final assessment  
**Clinical Reasoning:** Standard post-polypectomy monitoring protocol

### 2.3 Template Assignment Strategy

Each synthetic patient was assigned ONE trajectory template based on:

1. **Random Sampling:** Templates assigned with realistic population frequencies
2. **Visit Count:** Determined by template (2-4 visits)
3. **Consistency Enforcement:** All visits follow the assigned template
4. **No Template Mixing:** Patients cannot switch between templates

This ensures **clinically coherent longitudinal histories**.

---

## 3. Synthetic Patient Generation Process

### 3.1 Patient Master Creation

For each of 50 synthetic patients:

```python
Patient Profile = {
    Patient_ID: "P001" to "P050"
    Demographics: Age (18-80), Gender, Height, Weight, BMI
    Risk Factors: Smoking, Alcohol, Diabetes, Hypertension, Family_History_GI
    Trajectory_Template: Assigned from Templates A-E
}
```

**Key Decision:** Patient risk factors were randomized independently of trajectory to simulate real-world variability where high-risk patients may remain healthy and low-risk patients may develop disease.

### 3.2 Visit History Construction

For each patient:

```python
For each visit in trajectory:
    1. Assign Visit_ID (sequential: V0001, V0002, ...)
    2. Set Visit_Date (6-month intervals from 2025-01-15)
    3. Select Disease_Name from assigned template
    4. Choose Kvasir image matching disease category
    5. Assign disease-appropriate symptoms
    6. Leave AI fields empty (Pending)
    7. Record Trajectory_Type
```

**Temporal Logic:**
- Visit 1: 2025-01-15
- Visit 2: 2025-07-14 (≈6 months later)
- Visit 3: 2026-01-10 (≈6 months later)
- Visit 4: 2026-07-09 (≈6 months later)

### 3.3 Image Selection Strategy

From the Kvasir-v2 dataset (8000 images, 8 categories):

```python
For each visit:
    1. Identify required disease category from template
    2. Filter Kvasir images by disease folder
    3. Randomly select one image from that category
    4. Record image filename and path
    5. Link to Visit_History.csv
```

**Important:** Each visit uses a REAL Kvasir image. Only the patient linkage and temporal sequencing are synthetic.

---

## 4. Risk Assessment Integration

### 4.1 Rule-Based Risk Prototype

Since AI risk models require training data, we implemented a **heuristic risk engine** as a prototype:

```python
Risk_Score = Patient_Baseline_Risk + Disease_Severity_Weight + Progression_Weight
```

**Patient Baseline Risk Factors:**
- Age > 60: +20
- Smoking: +15
- Diabetes: +10
- Hypertension: +10
- Family History: +15
- BMI ≥ 30: +10

**Disease Severity Weights:**
- Normal: 0
- Esophagitis: 20
- Polyps: 35
- Ulcerative Colitis: 30
- Post-Procedure: 10-15

**Progression Weights:**
- Normal → Disease: +10
- Disease → Worse Disease: +15
- Stable Chronic: +0
- Improving: -5

**Risk Categories:**
- 0-24: Low
- 25-49: Medium
- 50-74: High
- 75+: Very High

**Note:** These weights are **demonstration values only** and not medically validated. They will be replaced by ML-based risk models in Phase 5.

---

## 5. Digital Twin State Snapshots

### 5.1 Current State Representation

For each patient, we maintain a **latest state snapshot**:

```python
DigitalTwin_State = {
    Current_Visit: Latest visit ID
    Current_Disease: Most recent diagnosis
    Previous_Disease: Prior visit diagnosis
    Disease_Trend: Stable | Progressing | Improving | Recovering
    Risk_Score: Latest calculated risk
    Twin_Status: Initialized | Updated
    AI_Status: Pending | Completed
}
```

**Disease Trend Logic:**
- Same disease → Stable
- Normal → Disease → Progressing
- Disease → Worse → Progressing
- Polyp → Post-procedure → Improving
- Post-procedure → Resection → Recovering

### 5.2 AI Integration Placeholders

Fields reserved for AI module (currently empty):

```
Disease_Severity
Lesion_Area
Lesion_Perimeter
Lesion_Circularity
Texture_Score
Shape_Score
Segmentation_Path
Image_Embedding_Path
GradCAM_Path
Prediction_Confidence
Predicted_Disease
```

These will be populated automatically after:
- Phase 5: EfficientNet classifier training
- Phase 6: Grad-CAM explainability generation
- Phase 7: Lesion segmentation and feature extraction

---

## 6. Validation and Quality Assurance

### 6.1 Data Integrity Checks

Every generation script includes validation:

✅ **Referential Integrity:**
- All Patient_IDs exist in Patient_Master
- All Visit_IDs exist in Visit_History
- All Disease_Names match Disease_Master

✅ **Temporal Consistency:**
- Visit dates increase monotonically per patient
- Visit numbers sequential (1, 2, 3, 4)
- No duplicate visit IDs

✅ **Trajectory Consistency:**
- All visits follow assigned template
- No arbitrary disease jumps
- Trajectory_Type consistent per patient

✅ **Image Linkage:**
- All images exist in Kvasir dataset
- Image disease matches visit disease
- Paths correctly formatted

### 6.2 Statistical Validation

Generated dataset statistics:

| Metric | Value |
|--------|-------|
| Total Patients | 50 |
| Total Visits | 160 |
| Visits per Patient | 2-4 (avg 3.2) |
| Temporal Span | 18 months |
| Trajectory Templates | 5 |
| Disease Categories | 8 |
| Unique Images Used | 160 (2% of Kvasir) |

**Disease Distribution (Final Visits):**
- Normal: 30% (15 patients)
- Polyps: 34% (17 patients)
- Esophagitis: 10% (5 patients)
- Ulcerative Colitis: 10% (5 patients)
- Post-Procedure: 16% (8 patients)

**Risk Distribution (Final Visits):**
- Low: 6% (3 patients)
- Medium: 30% (15 patients)
- High: 38% (19 patients)
- Very High: 26% (13 patients)

---

## 7. Limitations and Transparency

### 7.1 Known Limitations

**L1. Synthetic Patient Linkage**
- Patient identifiers are artificial
- Real patients do not exist
- Cannot validate against real clinical outcomes

**L2. Template Simplification**
- Real disease trajectories are more complex
- Some clinical patterns not represented
- Treatment effects not explicitly modeled

**L3. Fixed Temporal Intervals**
- All follow-ups at 6-month intervals
- Real clinical practice has variable timing
- Emergency visits not modeled

**L4. Image Reuse**
- Each visit uses a different image
- Real patients would show same anatomical features
- Cannot track lesion-specific changes

**L5. Heuristic Risk Model**
- Risk weights are demonstration values
- Not clinically validated
- Will be replaced by ML models

### 7.2 Mitigation Strategies

**M1. Transparent Documentation**
- All limitations clearly stated
- Synthetic nature emphasized
- Not claimed as real patient data

**M2. Clinically Informed Design**
- Trajectory templates based on clinical patterns
- Risk factors aligned with medical literature
- Disease progressions realistic

**M3. Future Validation**
- Framework designed for real data integration
- Can swap synthetic patients with real data
- All scripts support data replacement

**M4. Methodological Rigor**
- Reproducible generation process
- Version-controlled scripts
- Comprehensive validation checks

---

## 8. Future Integration with Real Data

### 8.1 Data Replacement Strategy

The synthetic trajectory framework is designed to be **directly replaceable** with real longitudinal data:

```python
# Current: Synthetic patients
patients = generate_synthetic_patients(n=50, templates=TEMPLATES)

# Future: Real patients (when available)
patients = load_real_patients(hospital_database, 
                               anonymization=True,
                               consent=True)
```

**Requirements for real data integration:**
1. Patient identifiers (anonymized)
2. Visit dates
3. Endoscopy images per visit
4. Ground truth diagnoses
5. Clinical metadata (age, risk factors)

### 8.2 Validation Against Real Data

When real longitudinal data becomes available:

1. **Compare Trajectory Distributions:** Do real patients follow similar patterns?
2. **Validate Risk Model:** How well do heuristic scores correlate with outcomes?
3. **Refine Templates:** Update template definitions based on real progressions
4. **Benchmark AI Models:** Compare synthetic-trained vs. real-trained performance

---

## 9. Contribution to Digital Twin Research

### 9.1 Novel Methodological Contribution

This work contributes:

1. **First Synthetic Longitudinal GI Dataset:** No prior work has created synthetic temporal sequences for GI endoscopy
2. **Template-Based Trajectory Generation:** Reusable framework for other medical domains
3. **Transparent Synthetic Data Methodology:** Clear documentation of limitations and assumptions
4. **AI-Ready Structure:** Designed for seamless ML integration

### 9.2 Enables Digital Twin Development

Without this synthetic data:
- ❌ Cannot develop Digital Twin algorithms
- ❌ Cannot test longitudinal prediction models
- ❌ Cannot design temporal dashboards
- ❌ Cannot validate explainability methods

With this synthetic data:
- ✅ Digital Twin framework can be developed
- ✅ ML pipelines can be tested
- ✅ Dashboards can be prototyped
- ✅ Ready for real data when available

---

## 10. Ethical Considerations

### 10.1 No Real Patient Data

- No real patient information used
- No privacy concerns
- No IRB approval required
- No consent issues

### 10.2 Clear Labeling

- All data clearly marked as **synthetic**
- No deceptive representation
- Limitations transparently documented
- Not used for clinical decision-making

### 10.3 Research Purpose Only

This synthetic dataset is intended **solely for**:
- Algorithm development
- Framework design
- Proof-of-concept demonstrations
- Academic research

It is **explicitly NOT** for:
- Clinical diagnosis
- Treatment decisions
- Patient risk assessment
- Regulatory approval

---

## 11. Reproducibility

### 11.1 Generation Scripts

All synthetic data can be regenerated using:

```bash
# Step 1: Disease classification reference
python create_disease_master.py

# Step 2: Synthetic patient profiles
python create_patient_master.py

# Step 3: Longitudinal visit histories
python create_visit_history.py

# Step 4: Dynamic risk assessment
python create_risk_engine.py

# Step 5: Current Digital Twin states
python create_digital_twin_state.py
```

### 11.2 Version Control

All scripts are version-controlled in GitHub:
- Repository: https://github.com/Yuvedasri/GastroTwin
- Branch: main
- Metadata Version: v1.0

### 11.3 Random Seed Control

For reproducibility, all random operations use seeded generators:
```python
np.random.seed(42)
random.seed(42)
```

---

## 12. Conclusion

The synthetic longitudinal trajectory generation methodology provides a **pragmatic solution** to the absence of publicly available longitudinal medical imaging data. While the patient linkages are synthetic, the images are real, the clinical patterns are plausible, and the framework is designed for seamless integration with real data when it becomes available.

This approach enables Digital Twin research to proceed **transparently and ethically** while acknowledging limitations and preparing for future validation against real-world data.

---

## References

1. Kvasir-v2 Dataset: https://datasets.simula.no/kvasir/
2. Pogorelov, K., et al. (2017). KVASIR: A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection. ACM MMSys.
3. Digital Twin Definition: Grieves, M. (2014). Digital Twin: Manufacturing Excellence through Virtual Factory Replication.
4. Longitudinal Medical Data Challenges: Jensen, P. B., et al. (2012). Mining electronic health records. Nature Reviews Genetics.

---

## Appendix A: Template Definition Table

| Template | Name | Visit 1 | Visit 2 | Visit 3 | Visit 4 | Population | Clinical Context |
|----------|------|---------|---------|---------|---------|------------|------------------|
| A | Healthy | Normal | Normal | Normal | - | 16% | Routine surveillance |
| B | Inflammatory | Normal | Esophagitis | Esophagitis | Polyps* | 20% | Progressive inflammation |
| C | Stable | Disease | Disease | Disease | Disease | 32% | Chronic management |
| D | Progression | Normal | Disease | Worse | - | 20% | Worsening condition |
| E | Post-Procedure | Polyps | Dyed-Lifted | Dyed-Resection | - | 12% | Polypectomy recovery |

*Some patients progress to Polyps in Visit 4

---

## Appendix B: Metadata File Relationships

```
Disease_Master.csv (Reference)
    ↓
Patient_Master.csv (50 patients + assigned templates)
    ↓
    ├──→ Visit_History.csv (160 visits following templates)
    │        ↓
    │    Risk_Assessment.csv (160 risk scores)
    │        ↓
    └──→ DigitalTwin_State.csv (50 current states)
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-07-15  
**Authors:** GastroTwin Research Team  
**Status:** Metadata v1.0 Frozen
