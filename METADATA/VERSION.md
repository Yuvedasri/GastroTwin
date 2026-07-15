# GastroTwin Metadata Version 1.0

**Release Date:** 2026-07-15  
**Status:** FROZEN - Ready for AI Development

---

## Version Information

**Version:** 1.0  
**Codename:** Foundation  
**Phase:** Pre-AI Metadata Complete  

---

## Files Included in v1.0

| File | Records | Description | Status |
|------|---------|-------------|--------|
| Disease_Master.csv | 8 | Disease classification reference | ✓ Complete |
| Patient_Master.csv | 50 | Synthetic patient profiles with demographics | ✓ Complete |
| Visit_History.csv | 166 | Longitudinal visits with trajectory templates | ✓ Complete |
| Risk_Assessment.csv | 166 | Dynamic risk scores per visit | ✓ Complete |
| DigitalTwin_State.csv | 50 | Current patient state snapshots | ✓ Complete |

---

## Key Features in v1.0

### 1. Clinical Trajectory Templates
- **5 trajectory types:** Healthy, Inflammatory_Progression, Stable_Chronic, Disease_Progression, Post_Procedure
- **Clinically plausible progressions:** No arbitrary disease jumps
- **Consistent patient histories:** Each patient follows one template

### 2. Ground Truth vs AI Separation
- **GroundTruth_Disease:** From Kvasir dataset (populated)
- **Predicted_Disease:** From AI classifier (empty - awaiting Phase 5)
- Clear separation prevents confusion

### 3. AI Feature Placeholders
**In Visit_History.csv:**
- Disease_Severity
- Lesion_Area, Lesion_Perimeter, Lesion_Circularity
- Texture_Score, Shape_Score
- Segmentation_Path, Image_Embedding_Path, GradCAM_Path
- Prediction_Confidence

**In DigitalTwin_State.csv:**
- Current_Severity, Previous_Severity
- Current_Lesion_Area, Previous_Lesion_Area
- Current_Confidence
- Embedding_Path, GradCAM_Path

**Status:** All empty (to be populated in Phase 5)

### 4. Trajectory Type Tracking
- Added to Visit_History.csv
- Consistent per patient
- Enables trajectory-based analysis

### 5. Enhanced Validation
- Trajectory consistency checks
- Temporal validation
- Image linkage verification
- Referential integrity

---

## Generation Scripts

All metadata files were generated using versioned scripts:

```bash
python create_disease_master.py          # v1.0
python create_patient_master.py          # v1.0  
python create_visit_history_v2.py        # v2.0 (with trajectories & AI placeholders)
python create_risk_engine.py             # v1.1 (updated for v2 compatibility)
python create_digital_twin_state_v2.py   # v2.0 (with AI placeholders)
```

**Random Seed:** 42 (for reproducibility)

---

## Statistics

### Patient Distribution
- Total Patients: 50
- Age Range: 18-80 years
- Gender: Mixed (randomized)
- Risk Factors: Smoking (50%), Diabetes (38%), Hypertension (46%), etc.

### Visit Distribution
- Total Visits: 166
- Visits per Patient: 3-4 (avg 3.32)
- Temporal Span: 18 months (2025-01-15 to 2026-07-09)
- Visit Interval: ~6 months

### Trajectory Distribution
| Trajectory Type | Patients | Percentage |
|----------------|----------|------------|
| Stable_Chronic | 16 | 32.0% |
| Disease_Progression | 10 | 20.0% |
| Inflammatory_Progression | 10 | 20.0% |
| Healthy | 8 | 16.0% |
| Post_Procedure | 6 | 12.0% |

### Disease Distribution (Final Visits)
| Disease | Patients | Percentage |
|---------|----------|------------|
| Esophagitis | 19 | 38.0% |
| Polyps | 12 | 24.0% |
| Ulcerative-Colitis | 8 | 16.0% |
| Dyed-Resection-Margins | 6 | 12.0% |
| Normal | 5 | 10.0% |

### Risk Distribution (Final Visits)
| Risk Category | Patients | Percentage |
|--------------|----------|------------|
| High | 22 | 44.0% |
| Very High | 16 | 32.0% |
| Medium | 11 | 22.0% |
| Low | 1 | 2.0% |

---

## Data Quality Assurance

### Validation Performed
✅ All patients have visits  
✅ All visits follow assigned trajectory template  
✅ Visit numbers sequential per patient  
✅ Visit dates monotonically increasing  
✅ All images exist in Kvasir dataset  
✅ All disease names match Disease_Master  
✅ All Patient_IDs exist in Patient_Master  
✅ No orphaned records  
✅ No missing core values  
✅ AI placeholders correctly empty  

### Known Limitations
⚠️ Patient linkages are synthetic (not real patients)  
⚠️ Risk weights are demonstration values (not clinically validated)  
⚠️ Trajectory templates are simplified clinical patterns  
⚠️ Fixed 6-month visit intervals (real practice varies)  
⚠️ Each visit uses different image (cannot track same lesion)  

---

## Freeze Policy

**Effective Date:** 2026-07-15

### Rules
1. **NO MANUAL EDITS:** CSV files must not be edited manually
2. **SCRIPT-ONLY UPDATES:** All changes via versioned Python scripts
3. **VERSION CONTROL:** All changes tracked in Git
4. **BACKWARD COMPATIBILITY:** Future updates must maintain compatibility
5. **VALIDATION REQUIRED:** All updates must pass validation suite

### Allowed Updates
✅ Populating AI placeholder fields (Phase 5)  
✅ Adding new columns (with migration script)  
✅ Bug fixes (with version increment)  
✅ Adding more patients (with append script)  

### Prohibited Actions
❌ Changing existing patient IDs  
❌ Modifying visit histories retroactively  
❌ Deleting records  
❌ Changing trajectory templates retroactively  
❌ Manual CSV edits  

---

## Integration with AI Pipeline

### Phase 5: AI Classifier (Next)
**Will populate:**
- Visit_History: Predicted_Disease, Prediction_Confidence
- DigitalTwin_State: Current_Confidence, AI_Status = "Completed"

### Phase 6: Explainable AI
**Will populate:**
- Visit_History: GradCAM_Path, Disease_Severity
- DigitalTwin_State: Current_Severity, Previous_Severity

### Phase 7: Feature Extraction
**Will populate:**
- Visit_History: Lesion_Area, Lesion_Perimeter, Lesion_Circularity, Texture_Score, Shape_Score, Segmentation_Path
- DigitalTwin_State: Current_Lesion_Area, Previous_Lesion_Area

### Phase 8: Embeddings
**Will populate:**
- Visit_History: Image_Embedding_Path
- DigitalTwin_State: Embedding_Path

---

## Documentation

**Comprehensive documentation available in:**
- `docs/Synthetic_Trajectory_Generation.md` - Methodology and rationale
- `METADATA_ARCHITECTURE.md` - Structure and relationships
- `README.md` - Project overview

---

## Changelog

### v1.0 (2026-07-15) - Foundation Release
- ✨ Added trajectory templates (5 types)
- ✨ Separated ground truth from AI predictions
- ✨ Added AI feature placeholders (11 fields in Visit_History, 7 in DigitalTwin_State)
- ✨ Added Trajectory_Type column
- ✨ Enhanced validation suite
- ✨ Comprehensive documentation
- 🔒 **FROZEN for AI development**

### Pre-v1.0 (2026-07-14) - Initial Creation
- Created Disease_Master.csv
- Created Patient_Master.csv
- Created Visit_History.csv (basic version)
- Created Risk_Assessment.csv
- Created DigitalTwin_State.csv (basic version)

---

## Future Versions

### Planned: v1.1 (Post-AI Phase 5)
- Populate AI prediction fields
- Update AI_Status to "Completed"
- Add model performance metrics
- Document prediction accuracy

### Planned: v2.0 (Post-Explainability Phase 6)
- Populate Grad-CAM paths
- Add severity scores
- Enhance risk model with AI features

### Planned: v3.0 (Real Data Integration)
- Replace synthetic patients with real data (when available)
- Validate trajectory templates against real progressions
- Benchmark synthetic vs real data performance

---

## Verification

To verify this version:

```bash
# Check file existence
ls METADATA/*.csv

# Verify record counts
python -c "import pandas as pd; print(pd.read_csv('METADATA/Visit_History.csv').shape)"

# Check for AI placeholders
head -n 1 METADATA/Visit_History.csv | grep "Predicted_Disease"

# Validate trajectory consistency
python validate_metadata.py  # (to be created)
```

---

## Contact

**Project:** GastroTwin  
**Repository:** https://github.com/Yuvedasri/GastroTwin  
**Version Branch:** main  
**Metadata Version Tag:** v1.0  

---

## Approval

**Metadata Frozen By:** GastroTwin Research Team  
**Date:** 2026-07-15  
**Status:** ✓ APPROVED FOR AI DEVELOPMENT  

**Digital Signature:**
```
SHA256: [To be generated on commit]
Git Commit: [To be recorded]
```

---

**🔒 This version is now FROZEN. All future changes must be scripted and versioned. 🔒**
