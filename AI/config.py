"""
GastroTwin AI Configuration Module
===================================

Centralized configuration file for the GastroTwin AI Pipeline.
All hyperparameters, paths, and constants are defined here.

This is the SINGLE SOURCE OF TRUTH for the entire AI system.
No hardcoded values should exist in other AI modules.

Usage:
    from AI.config import *
    # or
    import AI.config as cfg

Author: Yuvedasri
Version: 1.0
Date: 2026-07-15
"""

import os
from pathlib import Path
import torch

# ============================================================================
# 1. PROJECT INFORMATION
# ============================================================================

PROJECT_NAME = "GastroTwin"
VERSION = "1.0"
AUTHOR = "Yuvedasri"
DESCRIPTION = "Multimodal AI Framework for Longitudinal Gastrointestinal Disease Monitoring"
DATASET_NAME = "Kvasir v2"
MODEL_NAME = "EfficientNet-B0"
FRAMEWORK = "PyTorch"

# ============================================================================
# 2. DIRECTORY PATHS
# ============================================================================

# Root directory (project base)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Core directories
DATA_DIR = PROJECT_ROOT / "DATA"
METADATA_DIR = PROJECT_ROOT / "METADATA"
MODELS_DIR = PROJECT_ROOT / "MODELS"
RESULTS_DIR = PROJECT_ROOT / "RESULTS"
AI_DIR = PROJECT_ROOT / "AI"
DOCS_DIR = PROJECT_ROOT / "docs"
DIGITAL_TWIN_DIR = PROJECT_ROOT / "DIGITAL_TWIN"

# Kvasir dataset
KVASIR_DATASET_PATH = DATA_DIR / "kvasir-dataset-v2"

# Metadata files (v1.0)
DISEASE_MASTER_CSV = METADATA_DIR / "Disease_Master.csv"
PATIENT_MASTER_CSV = METADATA_DIR / "Patient_Master.csv"
VISIT_HISTORY_CSV = METADATA_DIR / "Visit_History.csv"
RISK_ASSESSMENT_CSV = METADATA_DIR / "Risk_Assessment.csv"
DIGITAL_TWIN_STATE_CSV = METADATA_DIR / "DigitalTwin_State.csv"
KVASIR_METADATA_CSV = PROJECT_ROOT / "kvasir_metadata.csv"

# Dataset splits (to be created by data pipeline)
TRAIN_CSV = METADATA_DIR / "train_split.csv"
VALIDATION_CSV = METADATA_DIR / "val_split.csv"
TEST_CSV = METADATA_DIR / "test_split.csv"

# Create directories if they don't exist
for directory in [MODELS_DIR, RESULTS_DIR, AI_DIR, DIGITAL_TWIN_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# ============================================================================
# 3. DATASET CONFIGURATION
# ============================================================================

NUM_CLASSES = 8

# Class names (must match Kvasir v2 dataset folders)
CLASS_NAMES = [
    "dyed-lifted-polyps",
    "dyed-resection-margins",
    "esophagitis",
    "normal-cecum",
    "normal-pylorus",
    "normal-z-line",
    "polyps",
    "ulcerative-colitis"
]

# Mapped class names (human-readable for reports)
CLASS_NAMES_READABLE = {
    "dyed-lifted-polyps": "Dyed Lifted Polyps",
    "dyed-resection-margins": "Dyed Resection Margins",
    "esophagitis": "Esophagitis",
    "normal-cecum": "Normal Cecum",
    "normal-pylorus": "Normal Pylorus",
    "normal-z-line": "Normal Z-Line",
    "polyps": "Polyps",
    "ulcerative-colitis": "Ulcerative Colitis"
}

# Class to index mapping
CLASS_TO_IDX = {class_name: idx for idx, class_name in enumerate(CLASS_NAMES)}
IDX_TO_CLASS = {idx: class_name for class_name, idx in CLASS_TO_IDX.items()}

# Total images in Kvasir v2 (for reference)
TOTAL_IMAGES = 8000
IMAGES_PER_CLASS = 1000

# ============================================================================
# 4. IMAGE CONFIGURATION
# ============================================================================

# Image dimensions (EfficientNet-B0 default)
IMAGE_SIZE = (224, 224)
IMAGE_HEIGHT = IMAGE_SIZE[0]
IMAGE_WIDTH = IMAGE_SIZE[1]
IMAGE_CHANNELS = 3

# Normalization (ImageNet statistics - EfficientNet was pretrained on ImageNet)
NORMALIZATION_MEAN = [0.485, 0.456, 0.406]
NORMALIZATION_STD = [0.229, 0.224, 0.225]

# Image format
IMAGE_FORMAT = "RGB"
IMAGE_EXTENSION = ".jpg"

# ============================================================================
# 5. DATASET SPLIT CONFIGURATION
# ============================================================================

# Split ratios (must sum to 1.0)
TRAIN_SPLIT = 0.70      # 70% for training
VALIDATION_SPLIT = 0.15  # 15% for validation
TEST_SPLIT = 0.15        # 15% for testing

# Random seed for reproducibility
RANDOM_SEED = 42

# Stratified split (ensure balanced classes)
STRATIFIED_SPLIT = True

# ============================================================================
# 6. DATA AUGMENTATION CONFIGURATION
# ============================================================================

# Training augmentation
USE_AUGMENTATION = True

AUGMENTATION_CONFIG = {
    'rotation_range': 20,           # Degrees
    'width_shift_range': 0.1,       # Fraction of total width
    'height_shift_range': 0.1,      # Fraction of total height
    'shear_range': 0.1,
    'zoom_range': 0.1,
    'horizontal_flip': True,
    'vertical_flip': False,         # Not typical for endoscopy
    'brightness_range': (0.8, 1.2),
    'fill_mode': 'nearest'
}

# ============================================================================
# 7. TRAINING CONFIGURATION
# ============================================================================

# Batch size
BATCH_SIZE = 32

# Number of training epochs
NUM_EPOCHS = 20

# Learning rate
LEARNING_RATE = 0.001

# Learning rate scheduler
USE_LR_SCHEDULER = True
LR_SCHEDULER_TYPE = "ReduceLROnPlateau"  # Options: "ReduceLROnPlateau", "StepLR", "CosineAnnealing"
LR_SCHEDULER_PATIENCE = 3  # For ReduceLROnPlateau
LR_SCHEDULER_FACTOR = 0.1  # Multiply LR by this factor
LR_SCHEDULER_MIN_LR = 1e-6

# Optimizer
OPTIMIZER = "Adam"  # Options: "Adam", "SGD", "AdamW"
WEIGHT_DECAY = 1e-4  # L2 regularization
MOMENTUM = 0.9  # For SGD

# Loss function
LOSS_FUNCTION = "CrossEntropyLoss"  # Options: "CrossEntropyLoss", "FocalLoss"

# Early stopping
USE_EARLY_STOPPING = True
EARLY_STOPPING_PATIENCE = 5  # Stop if no improvement for N epochs
EARLY_STOPPING_MIN_DELTA = 0.001  # Minimum change to qualify as improvement

# Gradient clipping
USE_GRADIENT_CLIPPING = True
GRADIENT_CLIP_VALUE = 1.0

# Mixed precision training (faster on modern GPUs)
USE_MIXED_PRECISION = True

# ============================================================================
# 8. MODEL CONFIGURATION
# ============================================================================

# EfficientNet variant
EFFICIENTNET_VARIANT = "efficientnet-b0"  # Options: b0, b1, b2, b3, b4, b5, b6, b7

# Transfer learning
USE_PRETRAINED = True  # Use ImageNet pretrained weights
FREEZE_BACKBONE = False  # Freeze early layers for transfer learning

# Dropout
DROPOUT_RATE = 0.2

# ============================================================================
# 9. DATALOADER CONFIGURATION
# ============================================================================

# Number of worker processes for data loading
NUM_WORKERS = 4  # Adjust based on CPU cores (typically 4-8)

# Pin memory (faster data transfer to GPU)
PIN_MEMORY = True

# Shuffle training data
SHUFFLE_TRAIN = True
SHUFFLE_VAL = False
SHUFFLE_TEST = False

# Drop last incomplete batch
DROP_LAST = False

# ============================================================================
# 10. DEVICE CONFIGURATION
# ============================================================================

# Automatically detect GPU availability
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
USE_CUDA = torch.cuda.is_available()
NUM_GPUS = torch.cuda.device_count() if USE_CUDA else 0

# Multi-GPU training
USE_DATA_PARALLEL = NUM_GPUS > 1

# ============================================================================
# 11. MODEL SAVING CONFIGURATION
# ============================================================================

# Model checkpoints directory
CHECKPOINT_DIR = MODELS_DIR / "checkpoints"
CHECKPOINT_DIR.mkdir(exist_ok=True, parents=True)

# Best model (highest validation accuracy)
BEST_MODEL_PATH = MODELS_DIR / "best_model.pth"

# Last model (final epoch)
LAST_MODEL_PATH = MODELS_DIR / "last_model.pth"

# Checkpoint format
CHECKPOINT_FORMAT = "efficientnet_epoch_{epoch:02d}_acc_{acc:.4f}.pth"

# Save frequency
SAVE_EVERY_N_EPOCHS = 5  # Save checkpoint every N epochs
SAVE_BEST_ONLY = True  # Only save when validation accuracy improves

# ============================================================================
# 12. EVALUATION CONFIGURATION
# ============================================================================

# Evaluation results directory
EVALUATION_DIR = RESULTS_DIR / "evaluation"
EVALUATION_DIR.mkdir(exist_ok=True, parents=True)

# Confusion matrix
CONFUSION_MATRIX_PATH = EVALUATION_DIR / "confusion_matrix.png"
CONFUSION_MATRIX_NORMALIZED_PATH = EVALUATION_DIR / "confusion_matrix_normalized.png"

# ROC curves
ROC_CURVE_PATH = EVALUATION_DIR / "roc_curves.png"
ROC_AUC_PATH = EVALUATION_DIR / "roc_auc_scores.json"

# Classification report
CLASSIFICATION_REPORT_PATH = EVALUATION_DIR / "classification_report.txt"
CLASSIFICATION_REPORT_JSON = EVALUATION_DIR / "classification_report.json"

# Per-class metrics
PER_CLASS_METRICS_PATH = EVALUATION_DIR / "per_class_metrics.csv"

# Predictions
PREDICTIONS_CSV = EVALUATION_DIR / "test_predictions.csv"

# Misclassified samples
MISCLASSIFIED_DIR = EVALUATION_DIR / "misclassified"
MISCLASSIFIED_DIR.mkdir(exist_ok=True, parents=True)
SAVE_MISCLASSIFIED = True
MAX_MISCLASSIFIED_SAMPLES = 50

# ============================================================================
# 13. EXPLAINABLE AI CONFIGURATION (Grad-CAM)
# ============================================================================

# Grad-CAM output directory
GRADCAM_OUTPUT_DIR = RESULTS_DIR / "gradcam"
GRADCAM_OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Target layer for Grad-CAM (EfficientNet-B0)
GRADCAM_TARGET_LAYER = "features"  # Will be adjusted based on model architecture

# Heatmap visualization
HEATMAP_ALPHA = 0.4  # Overlay transparency (0=transparent, 1=opaque)
HEATMAP_COLORMAP = "jet"  # Options: "jet", "viridis", "hot", "cool"

# Save options
SAVE_HEATMAPS = True
GRADCAM_IMAGE_FORMAT = "png"

# Generate Grad-CAM for
GRADCAM_FOR_CORRECT = True  # Correctly classified samples
GRADCAM_FOR_INCORRECT = True  # Misclassified samples
MAX_GRADCAM_SAMPLES_PER_CLASS = 10

# ============================================================================
# 14. LOGGING CONFIGURATION
# ============================================================================

# Logs directory
LOG_DIR = RESULTS_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)

# Log file
LOG_FILE = LOG_DIR / "training.log"

# Tensorboard logs
TENSORBOARD_DIR = LOG_DIR / "tensorboard"
TENSORBOARD_DIR.mkdir(exist_ok=True, parents=True)
USE_TENSORBOARD = True

# Logging level
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"

# Console output
VERBOSE = True  # Print progress to console
PROGRESS_BAR = True  # Show progress bars during training

# ============================================================================
# 15. EXPERIMENT TRACKING
# ============================================================================

# Experiment name (auto-generated with timestamp if None)
EXPERIMENT_NAME = None  # Will be set as "exp_YYYYMMDD_HHMMSS"

# Track experiments
TRACK_EXPERIMENTS = True

# Metrics to track
TRACKED_METRICS = [
    "train_loss",
    "train_accuracy",
    "val_loss",
    "val_accuracy",
    "learning_rate",
    "epoch_time"
]

# ============================================================================
# 16. DIGITAL TWIN INTEGRATION
# ============================================================================

# Update Digital Twin state after prediction
UPDATE_DIGITAL_TWIN = True

# Fields to populate in Visit_History.csv
POPULATE_FIELDS = [
    "Predicted_Disease",
    "Prediction_Confidence",
    "Image_Embedding_Path",
    "GradCAM_Path"
]

# Embedding extraction
EXTRACT_EMBEDDINGS = True
EMBEDDING_DIM = 1280  # EfficientNet-B0 feature dimension
EMBEDDINGS_DIR = RESULTS_DIR / "embeddings"
EMBEDDINGS_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================================
# 17. VALIDATION AND TESTING
# ============================================================================

# Test-Time Augmentation (TTA)
USE_TTA = False  # Predict on augmented versions and average
TTA_AUGMENTATIONS = 5

# Confidence threshold for predictions
CONFIDENCE_THRESHOLD = 0.5  # For binary decisions if needed

# Calculate additional metrics
CALCULATE_TOP_K_ACCURACY = True
TOP_K = [1, 3, 5]  # Top-1, Top-3, Top-5 accuracy

# ============================================================================
# 18. REPRODUCIBILITY
# ============================================================================

# Set all random seeds
SEED_EVERYTHING = True

# Deterministic algorithms (may impact performance)
USE_DETERMINISTIC_ALGORITHMS = False

# Benchmark mode (faster but non-deterministic)
CUDNN_BENCHMARK = True if USE_CUDA and not USE_DETERMINISTIC_ALGORITHMS else False

# ============================================================================
# 19. PERFORMANCE OPTIMIZATION
# ============================================================================

# Automatic Mixed Precision (AMP) scaler
AMP_ENABLED = USE_MIXED_PRECISION and USE_CUDA

# Prefetch factor for data loading
PREFETCH_FACTOR = 2

# Persistent workers (keep workers alive between epochs)
PERSISTENT_WORKERS = NUM_WORKERS > 0

# ============================================================================
# 20. DEBUGGING AND DEVELOPMENT
# ============================================================================

# Debug mode (use subset of data for quick testing)
DEBUG_MODE = False
DEBUG_SAMPLES = 100  # Use only N samples per split in debug mode

# Profiling
ENABLE_PROFILING = False

# Save intermediate outputs
SAVE_INTERMEDIATE_OUTPUTS = False

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

def validate_config():
    """
    Validate configuration settings and check for common issues.
    """
    errors = []
    warnings = []
    
    # Check split ratios
    total_split = TRAIN_SPLIT + VALIDATION_SPLIT + TEST_SPLIT
    if abs(total_split - 1.0) > 1e-6:
        errors.append(f"Dataset splits must sum to 1.0, got {total_split}")
    
    # Check paths exist
    if not DATA_DIR.exists():
        warnings.append(f"DATA_DIR does not exist: {DATA_DIR}")
    
    if not KVASIR_DATASET_PATH.exists():
        warnings.append(f"Kvasir dataset not found: {KVASIR_DATASET_PATH}")
    
    # Check batch size
    if BATCH_SIZE < 1:
        errors.append(f"BATCH_SIZE must be positive, got {BATCH_SIZE}")
    
    # Check epochs
    if NUM_EPOCHS < 1:
        errors.append(f"NUM_EPOCHS must be positive, got {NUM_EPOCHS}")
    
    # Check learning rate
    if LEARNING_RATE <= 0:
        errors.append(f"LEARNING_RATE must be positive, got {LEARNING_RATE}")
    
    # Check image size
    if len(IMAGE_SIZE) != 2 or IMAGE_SIZE[0] < 1 or IMAGE_SIZE[1] < 1:
        errors.append(f"Invalid IMAGE_SIZE: {IMAGE_SIZE}")
    
    # Check num workers
    if NUM_WORKERS < 0:
        errors.append(f"NUM_WORKERS cannot be negative, got {NUM_WORKERS}")
    
    return errors, warnings

# ============================================================================
# CONFIGURATION SUMMARY
# ============================================================================

def print_config():
    """
    Print a formatted summary of the configuration.
    """
    print("=" * 80)
    print(f"{PROJECT_NAME.upper()} AI CONFIGURATION")
    print("=" * 80)
    
    print(f"\n📋 PROJECT INFORMATION")
    print(f"  Project Name      : {PROJECT_NAME}")
    print(f"  Version           : {VERSION}")
    print(f"  Author            : {AUTHOR}")
    print(f"  Dataset           : {DATASET_NAME}")
    print(f"  Model             : {MODEL_NAME}")
    
    print(f"\n📁 DIRECTORY PATHS")
    print(f"  Project Root      : {PROJECT_ROOT}")
    print(f"  Data Directory    : {DATA_DIR}")
    print(f"  Models Directory  : {MODELS_DIR}")
    print(f"  Results Directory : {RESULTS_DIR}")
    
    print(f"\n🖼️  DATASET CONFIGURATION")
    print(f"  Number of Classes : {NUM_CLASSES}")
    print(f"  Total Images      : {TOTAL_IMAGES}")
    print(f"  Image Size        : {IMAGE_WIDTH} x {IMAGE_HEIGHT}")
    print(f"  Image Channels    : {IMAGE_CHANNELS}")
    
    print(f"\n📊 DATASET SPLIT")
    print(f"  Train Split       : {TRAIN_SPLIT * 100:.0f}%")
    print(f"  Validation Split  : {VALIDATION_SPLIT * 100:.0f}%")
    print(f"  Test Split        : {TEST_SPLIT * 100:.0f}%")
    print(f"  Random Seed       : {RANDOM_SEED}")
    
    print(f"\n🎓 TRAINING CONFIGURATION")
    print(f"  Batch Size        : {BATCH_SIZE}")
    print(f"  Number of Epochs  : {NUM_EPOCHS}")
    print(f"  Learning Rate     : {LEARNING_RATE}")
    print(f"  Optimizer         : {OPTIMIZER}")
    print(f"  Weight Decay      : {WEIGHT_DECAY}")
    print(f"  Use Augmentation  : {USE_AUGMENTATION}")
    print(f"  Early Stopping    : {USE_EARLY_STOPPING}")
    
    print(f"\n💻 DEVICE CONFIGURATION")
    print(f"  Device            : {DEVICE}")
    print(f"  CUDA Available    : {USE_CUDA}")
    print(f"  Number of GPUs    : {NUM_GPUS}")
    print(f"  Mixed Precision   : {USE_MIXED_PRECISION}")
    print(f"  Num Workers       : {NUM_WORKERS}")
    
    print(f"\n💾 MODEL SAVING")
    print(f"  Best Model Path   : {BEST_MODEL_PATH}")
    print(f"  Checkpoint Dir    : {CHECKPOINT_DIR}")
    print(f"  Save Best Only    : {SAVE_BEST_ONLY}")
    
    print(f"\n📈 EVALUATION")
    print(f"  Evaluation Dir    : {EVALUATION_DIR}")
    print(f"  Save Misclassified: {SAVE_MISCLASSIFIED}")
    
    print(f"\n🔍 EXPLAINABLE AI")
    print(f"  Grad-CAM Enabled  : {SAVE_HEATMAPS}")
    print(f"  Grad-CAM Dir      : {GRADCAM_OUTPUT_DIR}")
    print(f"  Heatmap Alpha     : {HEATMAP_ALPHA}")
    
    # Validate configuration
    errors, warnings = validate_config()
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
        print("\n❌ Configuration validation failed!")
        print("=" * 80)
        return False
    else:
        print("\n✅ Configuration validated successfully!")
        print("=" * 80)
        return True

# ============================================================================
# AUTO-PRINT ON IMPORT
# ============================================================================

if __name__ == "__main__":
    # Print configuration when running this file directly
    print_config()
else:
    # Optionally print when imported (can be disabled)
    if VERBOSE:
        print(f"\n✓ {PROJECT_NAME} configuration loaded (v{VERSION})")
        print(f"  Device: {DEVICE}")
        print(f"  Model: {MODEL_NAME}")
        print(f"  Classes: {NUM_CLASSES}")
