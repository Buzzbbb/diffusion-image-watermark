"""
Watermark algorithms for diffusion-generated images.

Three families are provided:
    - SpatialWatermark  – LSB embedding in the pixel domain
    - FrequencyWatermark – DCT spread-spectrum in the frequency domain
    - NeuralWatermark    – optimization-based neural embedding using a
                           key-seeded decoder network
"""

from .spatial import SpatialWatermark
from .frequency import FrequencyWatermark
from .neural import NeuralWatermark

__all__ = ["SpatialWatermark", "FrequencyWatermark", "NeuralWatermark"]
