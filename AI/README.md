# GastroTwin AI Module

**Version:** 1.0  
**Status:** Module 1 Complete - Configuration Layer  
**Next:** Module 2 - Dataset Pipeline

---

## 📋 Overview

This directory contains the AI pipeline for the GastroTwin project. The pipeline is designed to be modular, maintainable, and research-quality.

**Current Status:**
- ✅ Module 1: Configuration (`config.py`)
- ⏳ Module 2: Dataset Pipeline
- ⏳ Module 3: EfficientNet Model
- ⏳ Module 4: Training Pipeline
- ⏳ Module 5: Evaluation & Metrics
- ⏳ Module 6: Grad-CAM Explainability
- ⏳ Module 7: Digital Twin Integration

---

## 🗂️ Module Structure

```
AI/
├── __init__.py           # Package initialization
├── config.py             # ✅ Centralized configuration (Module 1)
├── README.md             # This file
│
├── dataset.py            # ⏳ Data loading and preprocessing (Module 2)
├── model.py              # ⏳ EfficientNet model definition (Module 3)
├── train.py              # ⏳ Training pipeline (Module 4)
├── evaluate.py           # ⏳ Evaluation and metrics (Module 5)
├── gradcam.py            # ⏳ Grad-CAM explainability (Module 6)
├── integrate.py          # ⏳ Digital Twin integration (Module 7)
└── utils.py              # ⏳ Utility functions
```

---

## ✅ Module 1: Configuration (`config.py`)

### Purpose
Centralized configuration module that serves as the **single source of truth** for all AI pipeline constants, hyperparameters, and paths.

### Key Features

**1. Project Information**
- Project name, version, author
- Dataset and model metadata

**2. Directory Paths (20+ paths)**
- Auto-configured using `pathlib.Path`
- All paths relative to project root
- Auto-creates necessary directories

**3. Dataset Configuration**
- 8 Kvasir v2 classes
- Class name mappings
- Class-to-index conversions

**4. Image Configuration**
- Image size: 224x224 (EfficientNet-B0)
- ImageNet normalization statistics
- RGB format

**5. Dataset Split**
- Train: 70%, Validation: 15%, Test: 15%
- Random seed: 42 (reproducibility)
- Stratified split support

**6. Data Augmentation**
- Configurable augmentation parameters
- Rotation, shift, zoom, flip, brightness

**7. Training Configuration**
- Batch size: 32
- Epochs: 20
- Learning rate: 0.001
- Optimizer: Adam
- Early stopping: Enabled
- Learning rate scheduler: ReduceLROnPlateau

**8. Model Configuration**
- EfficientNet-B0
- Pretrained on ImageNet
- Dropout: 0.2

**9. Device Configuration**
- Auto-detects GPU/CPU
- Multi-GPU support
- Mixed precision training

**10. Model Saving**
- Best model path
- Checkpoint directory
- Auto-save best models

**11. Evaluation Paths**
- Confusion matrix
- ROC curves
- Classification report
- Misclassified samples

**12. Explainable AI (Grad-CAM)**
- Output directory
- Heatmap settings (alpha, colormap)
- Sample generation limits

**13. Logging**
- Training logs
- TensorBoard support
- Experiment tracking

**14. Digital Twin Integration**
- Auto-update Visit_History
- Populate AI prediction fields
- Extract embeddings

**15. Validation**
- Auto-validates configuration
- Checks split ratios
- Verifies paths
- Reports errors/warnings

### Usage

**Basic Import:**
```python
from AI.config import *
```

**Selective Import:**
```python
import AI.config as cfg

batch_size = cfg.BATCH_SIZE
device = cfg.DEVICE
num_classes = cfg.NUM_CLASSES
```

**Access Paths:**
```python
from AI.config import TRAIN_CSV, MODELS_DIR, BEST_MODEL_PATH

# Load training data
train_df = pd.read_csv(TRAIN_CSV)

# Save model
torch.save(model.state_dict(), BEST_MODEL_PATH)
```

**Print Configuration:**
```python
python AI/config.py
```

**Output:**
```
================================================================================
GASTROTWIN AI CONFIGURATION
================================================================================

📋 PROJECT INFORMATION
  Project Name      : GastroTwin
  Version           : 1.0
  Author            : Yuvedasri
  Dataset           : Kvasir v2
  Model             : EfficientNet-B0

📁 DIRECTORY PATHS
  Project Root      : /path/to/GASTROTWIN
  Data Directory    : /path/to/GASTROTWIN/DATA
  ...

✅ Configuration validated successfully!
```

### Configuration Sections

| Section | Variables | Description |
|---------|-----------|-------------|
| Project Info | 6 | Project metadata |
| Paths | 20+ | All directory paths |
| Dataset | 10 | Class names, mappings |
| Image | 8 | Size, channels, normalization |
| Splits | 4 | Train/val/test ratios |
| Augmentation | 10 | Augmentation parameters |
| Training | 15 | Hyperparameters |
| Model | 5 | Architecture settings |
| Dataloader | 6 | Loading configuration |
| Device | 4 | GPU/CPU settings |
| Saving | 5 | Model checkpoint paths |
| Evaluation | 10 | Metrics and outputs |
| Grad-CAM | 8 | Explainability settings |
| Logging | 7 | Log paths and levels |
| Digital Twin | 5 | Integration settings |

**Total: 120+ configuration variables**

### Key Benefits

✅ **No Hardcoded Values:** All constants in one place  
✅ **Easy Modification:** Change once, apply everywhere  
✅ **Validation:** Auto-checks for errors  
✅ **Documentation:** Self-documenting with comments  
✅ **Reproducibility:** Fixed random seeds  
✅ **Flexibility:** Easy to customize for experiments  
✅ **Type Safety:** Uses pathlib.Path for all paths  

---

## 🔧 Customization Guide

### Changing Hyperparameters

**Example 1: Increase batch size**
```python
# In config.py, change:
BATCH_SIZE = 32  # Default
# To:
BATCH_SIZE = 64  # Larger batch
```

**Example 2: Change learning rate**
```python
# In config.py, change:
LEARNING_RATE = 0.001  # Default
# To:
LEARNING_RATE = 0.0001  # Lower for fine-tuning
```

**Example 3: Use different optimizer**
```python
# In config.py, change:
OPTIMIZER = "Adam"  # Default
# To:
OPTIMIZER = "SGD"  # Stochastic Gradient Descent
```

### Adding New Configurations

**Example: Add new evaluation metric**
```python
# In config.py, add to EVALUATION CONFIGURATION section:
CALCULATE_F1_SCORE = True
F1_AVERAGE = "weighted"  # Options: "micro", "macro", "weighted"
```

### Experiment Tracking

**Example: Run experiment with custom name**
```python
# In config.py, change:
EXPERIMENT_NAME = None  # Auto-generated
# To:
EXPERIMENT_NAME = "exp_high_lr_dropout_03"  # Custom name
```

---

## 🎯 Design Principles

### 1. Single Source of Truth
- All constants defined once in `config.py`
- No hardcoded values in other modules
- Import config at the top of each module

### 2. Modularity
- Configuration separate from implementation
- Easy to swap configurations
- Support for multiple experiments

### 3. Validation
- Auto-validates on import
- Catches configuration errors early
- Prevents runtime failures

### 4. Documentation
- Every section well-commented
- Clear variable names
- Usage examples provided

### 5. Reproducibility
- Fixed random seeds
- Deterministic operations
- All settings version-controlled

---

## 📚 Configuration Variables Reference

### Essential Variables

**Most frequently used:**
```python
DEVICE              # torch.device("cuda" or "cpu")
BATCH_SIZE          # 32
NUM_EPOCHS          # 20
LEARNING_RATE       # 0.001
NUM_CLASSES         # 8
IMAGE_SIZE          # (224, 224)
CLASS_NAMES         # List of 8 class names
BEST_MODEL_PATH     # Path to save best model
TRAIN_CSV           # Path to training split
VALIDATION_CSV      # Path to validation split
TEST_CSV            # Path to test split
```

**Paths:**
```python
PROJECT_ROOT        # Base project directory
DATA_DIR            # DATA/ directory
METADATA_DIR        # METADATA/ directory
MODELS_DIR          # MODELS/ directory
RESULTS_DIR         # RESULTS/ directory
KVASIR_DATASET_PATH # DATA/kvasir-dataset-v2/
```

**Class Information:**
```python
CLASS_NAMES         # ["dyed-lifted-polyps", "dyed-resection-margins", ...]
CLASS_TO_IDX        # {"dyed-lifted-polyps": 0, ...}
IDX_TO_CLASS        # {0: "dyed-lifted-polyps", ...}
CLASS_NAMES_READABLE  # {"dyed-lifted-polyps": "Dyed Lifted Polyps", ...}
```

---

## 🚀 Next Steps

### Module 2: Dataset Pipeline (`dataset.py`)

**Will implement:**
1. Custom Dataset class for Kvasir
2. Data loading from CSV splits
3. Image preprocessing and augmentation
4. DataLoader creation
5. Train/val/test split generation
6. Class balancing

**Will use from config.py:**
- `KVASIR_DATASET_PATH`
- `TRAIN_CSV`, `VALIDATION_CSV`, `TEST_CSV`
- `IMAGE_SIZE`, `BATCH_SIZE`
- `NORMALIZATION_MEAN`, `NORMALIZATION_STD`
- `AUGMENTATION_CONFIG`
- `NUM_WORKERS`, `PIN_MEMORY`

---

## ✅ Validation Checklist

When creating new AI modules, ensure they:

- [ ] Import configuration from `config.py`
- [ ] Use config paths (no hardcoded paths)
- [ ] Use config hyperparameters
- [ ] Don't duplicate configuration
- [ ] Handle config validation errors
- [ ] Document any new config needs

---

## 📖 Example Usage in Future Modules

**Dataset Module (Module 2):**
```python
from AI.config import (
    KVASIR_DATASET_PATH, IMAGE_SIZE,
    NORMALIZATION_MEAN, NORMALIZATION_STD,
    BATCH_SIZE, NUM_WORKERS
)

class KvasirDataset(Dataset):
    def __init__(self):
        self.image_size = IMAGE_SIZE
        self.mean = NORMALIZATION_MEAN
        self.std = NORMALIZATION_STD
```

**Training Module (Module 4):**
```python
from AI.config import (
    DEVICE, BATCH_SIZE, NUM_EPOCHS,
    LEARNING_RATE, BEST_MODEL_PATH
)

def train():
    model = model.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    for epoch in range(NUM_EPOCHS):
        # Training loop
        ...
    
    torch.save(model.state_dict(), BEST_MODEL_PATH)
```

---

## 🔍 Troubleshooting

### Configuration Not Loading

**Problem:** Import error when loading config
```
ImportError: cannot import name 'config' from 'AI'
```

**Solution:** Ensure you're in the project root directory
```bash
cd GASTROTWIN
python -c "from AI.config import DEVICE; print(DEVICE)"
```

### Path Not Found

**Problem:** Configuration shows path warnings
```
⚠️  WARNINGS: Kvasir dataset not found
```

**Solution:** Download Kvasir dataset to `DATA/kvasir-dataset-v2/`

### CUDA Not Available

**Problem:** Device shows CPU even though you have GPU
```
Device: cpu
CUDA Available: False
```

**Solution:** Install PyTorch with CUDA support
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## 📊 Configuration Summary

**Statistics:**
- **Total Variables:** 120+
- **Configuration Sections:** 20
- **Auto-Created Directories:** 8
- **Validation Checks:** 7
- **Lines of Code:** 600+
- **Documentation:** Comprehensive inline comments

**Status:** ✅ Production-Ready

---

## 📝 Version History

### v1.0 (2026-07-15)
- ✨ Initial release
- ✨ 20 configuration sections
- ✨ 120+ variables
- ✨ Auto-validation
- ✨ Comprehensive documentation
- ✅ **FROZEN - Ready for AI Pipeline Development**

---

**Configuration is ready. Proceed to Module 2: Dataset Pipeline.** 🚀
