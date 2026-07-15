"""
GastroTwin AI Module
====================

This package contains the AI pipeline for the GastroTwin project.

Modules:
    - config: Centralized configuration and constants
    - dataset: Data loading and preprocessing (to be added)
    - model: EfficientNet model definition (to be added)
    - train: Training pipeline (to be added)
    - evaluate: Evaluation and metrics (to be added)
    - gradcam: Explainable AI with Grad-CAM (to be added)
    - utils: Utility functions (to be added)

Author: Yuvedasri
Version: 1.0
"""

__version__ = "1.0"
__author__ = "Yuvedasri"

# Import configuration on package import
from . import config

__all__ = ['config']
