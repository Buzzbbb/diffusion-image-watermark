"""
Perturbation attacks: Gaussian noise and Gaussian blur.

These are the most common robustness tests for watermarking schemes.
"""

import numpy as np
from PIL import Image, ImageFilter

from .base import BaseAttack


class GaussianNoiseAttack(BaseAttack):
    """Add zero-mean Gaussian noise to the image.

    Args:
        std: Standard deviation of the noise in pixel units [0, 255].
             Typical values: 5–25.
    """

    def __init__(self, std: float = 10.0) -> None:
        self.std = std

    def apply(self, image: Image.Image) -> Image.Image:
        arr = np.array(image.convert("RGB"), dtype=np.float32)
        noise = np.random.normal(0, self.std, arr.shape)
        noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy, "RGB")

    def __repr__(self) -> str:
        return f"GaussianNoiseAttack(std={self.std})"


class GaussianBlurAttack(BaseAttack):
    """Apply Gaussian blur to the image.

    Args:
        radius: Blur radius (in pixels).  Typical values: 1–5.
    """

    def __init__(self, radius: float = 2.0) -> None:
        self.radius = radius

    def apply(self, image: Image.Image) -> Image.Image:
        return image.convert("RGB").filter(ImageFilter.GaussianBlur(self.radius))

    def __repr__(self) -> str:
        return f"GaussianBlurAttack(radius={self.radius})"


class BrightnessAttack(BaseAttack):
    """Adjust image brightness by adding a fixed offset.

    Args:
        delta: Pixel offset in [-255, 255].  Positive → brighter.
    """

    def __init__(self, delta: float = 20.0) -> None:
        self.delta = delta

    def apply(self, image: Image.Image) -> Image.Image:
        arr = np.array(image.convert("RGB"), dtype=np.float32)
        adjusted = np.clip(arr + self.delta, 0, 255).astype(np.uint8)
        return Image.fromarray(adjusted, "RGB")

    def __repr__(self) -> str:
        return f"BrightnessAttack(delta={self.delta})"


class PerturbationAttack(BaseAttack):
    """Composite perturbation: noise followed by blur.

    Args:
        noise_std:   Gaussian noise standard deviation (pixel units).
        blur_radius: Gaussian blur radius (pixels).  Set to 0 to skip.
    """

    def __init__(self, noise_std: float = 10.0, blur_radius: float = 1.0) -> None:
        self.noise_std = noise_std
        self.blur_radius = blur_radius
        self._noise = GaussianNoiseAttack(noise_std)
        self._blur = GaussianBlurAttack(blur_radius)

    def apply(self, image: Image.Image) -> Image.Image:
        img = self._noise.apply(image)
        if self.blur_radius > 0:
            img = self._blur.apply(img)
        return img

    def __repr__(self) -> str:
        return (
            f"PerturbationAttack(noise_std={self.noise_std}, "
            f"blur_radius={self.blur_radius})"
        )
