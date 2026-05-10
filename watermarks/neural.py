"""
Neural-network-based watermark.

Design
------
A key-seeded *decoder* network (a lightweight CNN) is fixed at construction
time.  To embed a message the encoder finds the minimal additive perturbation
δ such that decoder(image + δ) ≈ message, using gradient descent.  To extract
the message a single forward pass through the decoder is sufficient.

This approach is:
  * Training-free (no large dataset required).
  * Key-secure: different keys yield different decoders.
  * Differentiable: the decoder can be fine-tuned for specific robustness
    requirements.

Dependencies
------------
Requires PyTorch (``torch``).  Import will raise ``ImportError`` if torch is
not available so that the rest of the package degrades gracefully.
"""

from typing import List

import numpy as np
from PIL import Image

from .base import BaseWatermark

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torchvision import transforms

    _TORCH_AVAILABLE = True

    # -----------------------------------------------------------------------
    # Network definitions (only when torch is present)
    # -----------------------------------------------------------------------

    class _DecoderNet(nn.Module):
        """Lightweight CNN that maps an image to a bit vector."""

        def __init__(self, message_length: int) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv2d(3, 32, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 32, kernel_size=3, padding=1, stride=2),
                nn.ReLU(),
                nn.Conv2d(32, 64, kernel_size=3, padding=1, stride=2),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d(4),
                nn.Flatten(),
                nn.Linear(64 * 4 * 4, 128),
                nn.ReLU(),
                nn.Linear(128, message_length),
                nn.Sigmoid(),
            )

        def forward(self, x: "torch.Tensor") -> "torch.Tensor":
            return self.net(x)

except ImportError:  # pragma: no cover
    _TORCH_AVAILABLE = False


# ---------------------------------------------------------------------------
# Public watermark class
# ---------------------------------------------------------------------------

class NeuralWatermark(BaseWatermark):
    """Neural watermark using a key-seeded fixed decoder network.

    Args:
        key:            Integer seed that determines the decoder's weights.
        message_length: Number of bits in the watermark message.
        strength:       L2 regularisation weight on the perturbation δ.
                        Smaller → less perceptible but potentially less robust.
        n_steps:        Number of optimisation steps for embedding.
        lr:             Learning rate for the Adam optimiser.
    """

    def __init__(
        self,
        key: int = 2024,
        message_length: int = 48,
        strength: float = 0.05,
        n_steps: int = 200,
        lr: float = 5e-3,
    ) -> None:
        if not _TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch is required for NeuralWatermark. "
                "Install it with: pip install torch torchvision"
            )
        self.key = key
        self.message_length = message_length
        self.strength = strength
        self.n_steps = n_steps
        self.lr = lr

        # Build decoder with fixed, key-seeded weights
        torch.manual_seed(key)
        self._decoder = _DecoderNet(message_length)
        self._decoder.eval()
        for p in self._decoder.parameters():
            p.requires_grad_(False)

        self._to_tensor = transforms.ToTensor()
        self._to_pil = transforms.ToPILImage()

    # ------------------------------------------------------------------
    def embed(self, image: Image.Image, message: List[int]) -> Image.Image:
        """Optimise a perturbation δ and return image + δ.

        Args:
            image:   Input PIL image (RGB, any size).
            message: Binary message of length == self.message_length.

        Raises:
            ValueError: if len(message) != self.message_length.
        """
        if len(message) != self.message_length:
            raise ValueError(
                f"Expected message of length {self.message_length}, "
                f"got {len(message)}"
            )

        img_t = self._to_tensor(image.convert("RGB")).unsqueeze(0)  # 1×3×H×W
        target = torch.tensor(message, dtype=torch.float32).unsqueeze(0)  # 1×L

        delta = torch.zeros_like(img_t, requires_grad=True)
        optimiser = torch.optim.Adam([delta], lr=self.lr)

        for _ in range(self.n_steps):
            optimiser.zero_grad()
            watermarked = torch.clamp(img_t + delta, 0.0, 1.0)
            predicted = self._decoder(watermarked)
            loss_msg = F.binary_cross_entropy(predicted, target)
            loss_reg = self.strength * delta.pow(2).mean()
            (loss_msg + loss_reg).backward()
            optimiser.step()

        with torch.no_grad():
            watermarked = torch.clamp(img_t + delta, 0.0, 1.0)

        return self._to_pil(watermarked.squeeze(0))

    # ------------------------------------------------------------------
    def extract(self, image: Image.Image, message_length: int) -> List[int]:
        """Run the decoder forward pass and threshold at 0.5.

        Args:
            image:          (Possibly attacked) PIL image.
            message_length: Should equal self.message_length.
        """
        img_t = self._to_tensor(image.convert("RGB")).unsqueeze(0)
        with torch.no_grad():
            probs = self._decoder(img_t).squeeze(0).numpy()
        return [int(p >= 0.5) for p in probs]

    def __repr__(self) -> str:
        return (
            f"NeuralWatermark(key={self.key}, "
            f"message_length={self.message_length}, "
            f"n_steps={self.n_steps})"
        )
