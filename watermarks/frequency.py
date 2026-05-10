"""
Frequency-domain watermark using DCT spread-spectrum.

Each message bit modulates a pseudo-random sequence added to mid-frequency
DCT coefficients of the luminance channel.  This is the classical approach
used by Cox et al. (1997) and is robust against JPEG compression.

Algorithm
---------
Embed
    1. Convert image to YCbCr; apply 2-D DCT to the Y channel.
    2. For each bit i, generate a PN sequence p_i from (key, i).
    3. Add strength * (2*bit - 1) * p_i to the mid-frequency DCT region.
    4. Apply inverse DCT and convert back to RGB.

Extract
    1. Recompute DCT; for each PN sequence p_i, compute dot product with
       the corresponding DCT region.  Sign determines the extracted bit.
"""

from typing import List

import numpy as np
from PIL import Image
from scipy.fft import dctn, idctn

from .base import BaseWatermark

# Fraction of the DCT spectrum treated as "mid-frequency"
_LOW_FRAC = 0.05
_HIGH_FRAC = 0.50


class FrequencyWatermark(BaseWatermark):
    """DCT spread-spectrum watermark.

    Args:
        key:      Integer seed for the pseudo-random sequence generator.
        strength: Embedding strength α.  Larger values are more robust but
                  more perceptible.  Typical range 0.05–0.30.
    """

    def __init__(self, key: int = 42, strength: float = 0.15) -> None:
        self.key = key
        self.strength = strength

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_mid_indices(self, n_total: int) -> np.ndarray:
        """Return the flat DCT coefficient indices in the mid-frequency band."""
        low = int(n_total * _LOW_FRAC)
        high = int(n_total * _HIGH_FRAC)
        return np.arange(low, high)

    def _pn_sequence(self, bit_index: int, length: int) -> np.ndarray:
        """Bipolar PN sequence ∈ {-1, +1} for a given bit index."""
        rng = np.random.default_rng([self.key, bit_index])
        return rng.choice([-1.0, 1.0], size=length)

    # ------------------------------------------------------------------
    def embed(self, image: Image.Image, message: List[int]) -> Image.Image:
        img = image.convert("YCbCr")
        y, cb, cr = [np.array(c, dtype=np.float64) for c in img.split()]

        # 2-D DCT of Y channel
        dct_y = dctn(y, norm="ortho")
        flat = dct_y.flatten()

        mid_idx = self._get_mid_indices(len(flat))
        if len(message) > len(mid_idx):
            raise ValueError(
                f"Message length {len(message)} exceeds DCT capacity {len(mid_idx)}"
            )

        for i, bit in enumerate(message):
            pn = self._pn_sequence(i, 1)[0]  # scalar ±1
            # Additive modulation: +α for bit=1, −α for bit=0
            flat[mid_idx[i]] += self.strength * (2 * bit - 1) * pn

        dct_y_mod = flat.reshape(dct_y.shape)
        y_mod = np.clip(idctn(dct_y_mod, norm="ortho"), 0, 255)

        y_img = Image.fromarray(y_mod.astype(np.uint8), "L")
        cb_img = Image.fromarray(cb.astype(np.uint8), "L")
        cr_img = Image.fromarray(cr.astype(np.uint8), "L")

        watermarked = Image.merge("YCbCr", (y_img, cb_img, cr_img))
        return watermarked.convert("RGB")

    # ------------------------------------------------------------------
    def extract(self, image: Image.Image, message_length: int) -> List[int]:
        img = image.convert("YCbCr")
        y = np.array(img.split()[0], dtype=np.float64)

        dct_y = dctn(y, norm="ortho")
        flat = dct_y.flatten()
        mid_idx = self._get_mid_indices(len(flat))

        bits: List[int] = []
        for i in range(message_length):
            pn = self._pn_sequence(i, 1)[0]
            # Correlation: if positive → bit 1, negative → bit 0
            corr = flat[mid_idx[i]] * pn
            bits.append(1 if corr >= 0 else 0)
        return bits

    def __repr__(self) -> str:
        return f"FrequencyWatermark(key={self.key}, strength={self.strength})"
