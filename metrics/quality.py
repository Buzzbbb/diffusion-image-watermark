"""
Image quality and watermark detection metrics.

Metrics
-------
psnr        Peak Signal-to-Noise Ratio (dB).
ssim        Structural Similarity Index (0–1, higher is better).
ber         Bit Error Rate (0–1, lower is better).
bit_accuracy  Fraction of correctly decoded bits (0–1, higher is better).
"""

from typing import List

import numpy as np
from PIL import Image


def psnr(original: Image.Image, processed: Image.Image) -> float:
    """Compute PSNR between two RGB images (higher is better, ∞ = identical).

    Args:
        original:  The reference (un-watermarked) image.
        processed: The processed (watermarked / attacked) image.

    Returns:
        PSNR value in dB.  Returns ``float('inf')`` when the images are
        identical.
    """
    orig = np.array(original.convert("RGB"), dtype=np.float64)
    proc = np.array(processed.convert("RGB").resize(original.size), dtype=np.float64)
    mse = np.mean((orig - proc) ** 2)
    if mse == 0.0:
        return float("inf")
    return 20.0 * np.log10(255.0 / np.sqrt(mse))


def ssim(
    original: Image.Image,
    processed: Image.Image,
    window_size: int = 11,
    k1: float = 0.01,
    k2: float = 0.03,
    data_range: float = 255.0,
) -> float:
    """Compute mean SSIM between two RGB images (higher is better).

    A simplified single-scale luminance-only SSIM is computed using a
    uniform (box) window to avoid external dependencies.

    Args:
        original:    Reference image.
        processed:   Processed image (same size as *original* expected).
        window_size: Spatial averaging window width (pixels).
        k1, k2:      SSIM stability constants.
        data_range:  Dynamic range of pixel values.

    Returns:
        SSIM value in [0, 1].
    """
    c1 = (k1 * data_range) ** 2
    c2 = (k2 * data_range) ** 2

    orig_y = np.array(original.convert("L"), dtype=np.float64)
    proc_y = np.array(
        processed.convert("RGB").resize(original.size).convert("L"),
        dtype=np.float64,
    )

    from scipy.ndimage import uniform_filter

    mu1 = uniform_filter(orig_y, size=window_size)
    mu2 = uniform_filter(proc_y, size=window_size)

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = uniform_filter(orig_y ** 2, size=window_size) - mu1_sq
    sigma2_sq = uniform_filter(proc_y ** 2, size=window_size) - mu2_sq
    sigma12 = uniform_filter(orig_y * proc_y, size=window_size) - mu1_mu2

    num = (2 * mu1_mu2 + c1) * (2 * sigma12 + c2)
    den = (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
    ssim_map = num / np.maximum(den, 1e-10)
    return float(np.mean(ssim_map))


def ber(original_bits: List[int], extracted_bits: List[int]) -> float:
    """Bit Error Rate: fraction of incorrectly decoded bits (lower is better).

    Args:
        original_bits: The ground-truth message bits.
        extracted_bits: The bits decoded from the (possibly attacked) image.

    Returns:
        BER in [0, 1].
    """
    if len(original_bits) != len(extracted_bits):
        raise ValueError(
            f"Length mismatch: original={len(original_bits)}, "
            f"extracted={len(extracted_bits)}"
        )
    if not original_bits:
        return 0.0
    errors = sum(o != e for o, e in zip(original_bits, extracted_bits))
    return errors / len(original_bits)


def bit_accuracy(original_bits: List[int], extracted_bits: List[int]) -> float:
    """Bit accuracy: fraction of correctly decoded bits (higher is better).

    Equivalent to ``1 - ber(...)``.
    """
    return 1.0 - ber(original_bits, extracted_bits)
