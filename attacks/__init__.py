"""
Attack modules for watermark robustness evaluation.

Available attack families:
    - PerturbationAttack – Gaussian noise and Gaussian blur
    - CompressionAttack  – JPEG re-encoding at configurable quality levels
    - CropAttack         – cropping (with optional padding/resize to restore size)
"""

from .perturbation import PerturbationAttack
from .compression import CompressionAttack
from .crop import CropAttack

__all__ = ["PerturbationAttack", "CompressionAttack", "CropAttack"]
