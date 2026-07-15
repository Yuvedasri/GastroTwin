# GastroTwin: A Multimodal AI Framework for Longitudinal Gastrointestinal Disease Monitoring

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-Kvasir-orange.svg)](https://datasets.simula.no/kvasir/)

## 🔬 Overview

**GastroTwin** is a research framework for building Digital Twin systems that enable longitudinal monitoring of gastrointestinal diseases. The project combines medical imaging data with patient demographics and medical history to provide explainable, multimodal AI-powered risk assessment.

This framework demonstrates how Digital Twin technology can track disease progression over time, assess patient risk dynamically, and support clinical decision-making through transparent, explainable AI.

## ⚠️ Important Disclaimer

**This is a research prototype for educational and academic purposes only.**

- Risk scores and assessments are generated using **demonstration weights** that are **NOT medically validated**
- This system is **NOT intended for clinical use** or real-world medical decision-making
- All patient data is **synthetic** and generated for research purposes
- Always consult qualified healthcare professionals for medical decisions

## 🎯 Key Features

### 1. **Longitudinal Disease Tracking**
- Track disease progression across multiple visits
- Monitor treatment effectiveness over time
- Identify disease progression patterns

### 2. **Multimodal Risk Assessment**
- Combine patient demographics (age, gender, BMI)
- Incorporate medical history (smoking, diabetes, hypertension, family history)
- Evaluate current disease state
- Detect disease progression patterns

### 3. **Explainable AI**
- Every risk assessment includes detailed explanations
- Traceable decision factors
- Complete audit trail through visit history

### 4. **Image-Based Disease Classification**
- 8,000 endoscopic images from Kvasir dataset
- 8 disease classes
- Images linked to patient visits and risk assessments

## 📊 Dataset

The project uses the **Kvasir Dataset v2**, a publicly available collection of gastrointestinal endoscopic images.

**Dataset Statistics:**
- **Total Images:** 8,000
- **Classes:** 8 (3 healthy, 5 disease conditions)
- **Images per Class:** 1,000

**Classes:**
- Normal-Cecum
- Normal-Pylorus
- Normal-Z-Line
- Esophagitis
- Polyps
- Ulcerative-Colitis
- Dyed-Lifted-Polyps
- Dyed-Resection-Margins

**Citation:**
```
Pogorelov, K., et al. (2017). KVASIR: A Multi-Class Image Dataset for Computer Aided 
Gastrointestinal Disease Detection. In Proceedings of the 8th ACM on Multimedia 
Systems Conference (MMSys'17).
```

## 🗂️ Project Structure

```
GASTROTWIN/
├── DATA/
│   └── kvasir-dataset-v2/          # Image dataset (8,000 images)
│
├── METADATA/                        # Digital Twin Database
│   ├── Disease_Master.csv          # Reference table (8 diseases)
│   ├── Patient_Master.csv          # Synthetic patients (50 patients)
│   ├── Visit_History.csv           # Patient visits (160 visits)
│   └── Risk_Assessment.csv         # Risk scores with explanations
│
├── DIGITAL_TWIN/                    # (Reserved for future models)
├── MODELS/                          # (Reserved for AI models)
│
├── Scripts/
│   ├── create_disease_master.py    # Generate disease reference table
│   ├── create_patient_master.py    # Generate synthetic patients
│   ├── create_visit_history.py     # Generate patient visit history
│   ├── create_risk_engine.py       # Dynamic risk assessment engine
│   ├── data_exploration.py         # Dataset analysis and visualization
│   ├── visualize_progressions.py   # Disease progression analysis
│   └── gastrotwin_summary.py       # Complete system summary
│
├── kvasir_metadata.csv              # Image metadata
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Yuvedasri/GastroTwin.git
cd GastroTwin
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download the Kvasir Dataset**
- Download from: [Kvasir Dataset](https://datasets.simula.no/kvasir/)
- Extract to: `DATA/kvasir-dataset-v2/`

### Running the System

#### Step 1: Explore the Dataset
```bash
python data_exploration.py
```
Outputs:
- Dataset statistics
- Sample images from each class
- `kvasir_metadata.csv`

#### Step 2: Create Disease Reference Table
```bash
python create_disease_master.py
```
Outputs: `METADATA/Disease_Master.csv`

#### Step 3: Generate Synthetic Patients
```bash
python create_patient_master.py
```
Outputs: `METADATA/Patient_Master.csv` (50 patients)

#### Step 4: Generate Patient Visit History
```bash
python create_visit_history.py
```
Outputs: `METADATA/Visit_History.csv` (160 visits with realistic disease progressions)

#### Step 5: Run Risk Assessment Engine
```bash
python create_risk_engine.py
```
Outputs: `METADATA/Risk_Assessment.csv` (160 risk assessments with explanations)

#### Step 6: View System Summary
```bash
python gastrotwin_summary.py
```
Displays complete system overview and statistics

## 📈 Digital Twin Database Schema

### Table 1: Disease_Master
Reference table for all disease classifications
```
Disease_ID | Disease_Name | Category | Description
```

### Table 2: Patient_Master
Synthetic patient demographics and risk factors
```
Patient_ID | Age | Gender | Height_cm | Weight_kg | BMI | 
Smoking | Alcohol | Diabetes | Hypertension | Family_History_GI
```

### Table 3: Visit_History (Core)
Patient visits with disease progression
```
Visit_ID | Patient_ID | Visit_No | Visit_Date | Disease_ID | Disease_Name |
Image_Name | Image_Path | Symptoms | AI_Prediction | Confidence | Risk_Level
```

### Table 4: Risk_Assessment (Intelligence Layer)
Dynamic risk scores with explanations
```
Risk_ID | Patient_ID | Visit_ID | Visit_No | Visit_Date | Disease_Name |
Risk_Score | Risk_Category | Risk_Explanation
```

## 🧮 Risk Scoring Algorithm

The risk engine calculates scores using three components:

### 1. Patient Risk Factors (Baseline)
- Age > 60: +20
- Smoking: +15
- Alcohol: +5
- Diabetes: +10
- Hypertension: +10
- Family History GI: +15
- BMI ≥ 30: +10

### 2. Disease Risk Weights
- Normal: 0
- Esophagitis: +20
- Polyps: +35
- Ulcerative Colitis: +30
- Dyed Lifted Polyps: +15
- Dyed Resection Margins: +10

### 3. Disease Progression Penalties
- Normal → Disease: +10 to +15
- Disease → Worse Disease: +15
- Stable Disease: 0

### Risk Categories
- **Low (0-24):** Preventive monitoring
- **Medium (25-49):** Routine follow-up
- **High (50-74):** Intensive monitoring
- **Very High (75+):** Urgent intervention

## 📊 Sample Results

**Dataset Overview:**
- 8,000 images across 8 classes
- 50 synthetic patients with realistic profiles
- 160 patient visits (3.2 visits per patient on average)
- 160 risk assessments with explanations

**Risk Distribution:**
- Low: 20 visits (12.5%)
- Medium: 44 visits (27.5%)
- High: 59 visits (36.9%)
- Very High: 37 visits (23.1%)

**Example Patient Journey:**
```
Patient P001 (56 years, Female, Smoker, Diabetic)
├── Visit 1 (2025-01-15): Normal-Pylorus → Risk: 50 [High]
├── Visit 2 (2025-07-14): Esophagitis → Risk: 80 [Very High] ⚠️
├── Visit 3 (2026-01-10): Esophagitis → Risk: 70 [High]
└── Visit 4 (2026-07-09): Polyps → Risk: 100 [Very High] ⚠️⚠️
```

## 🔬 Research Applications

1. **Disease Progression Modeling**
   - Predict disease trajectories
   - Identify high-risk progression patterns

2. **Multimodal AI Training**
   - Combine imaging + clinical data
   - Train explainable AI models

3. **Clinical Decision Support**
   - Risk stratification
   - Treatment planning support

4. **Digital Twin Development**
   - Longitudinal patient modeling
   - "What-if" scenario analysis

## 🛠️ Future Work

- [ ] CNN-based image classification model
- [ ] LSTM-based disease progression prediction
- [ ] Risk prediction model using patient history
- [ ] Interactive web dashboard for visualization
- [ ] Integration with FHIR standards
- [ ] Real-time risk monitoring system

## 🤝 Contributing

This is a research project. Contributions, suggestions, and feedback are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

1. Pogorelov, K., et al. (2017). KVASIR: A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection.
2. Grieves, M. (2014). Digital Twin: Manufacturing Excellence through Virtual Factory Replication.
3. Tao, F., et al. (2019). Digital Twin in Industry: State-of-the-Art.

## 👥 Authors

**Yuvedasri**
- GitHub: [@Yuvedasri](https://github.com/Yuvedasri)

## 🙏 Acknowledgments

- Kvasir Dataset team at Simula Research Laboratory
- Medical AI research community
- Open-source contributors

---

**Note:** This is a research prototype. Always consult qualified healthcare professionals for medical decisions.
