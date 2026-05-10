"""
Spatial-domain watermark using Least Significant Bit (LSB) steganography.

The message bits are embedded one-per-pixel into the lowest bit of the red
channel.  Capacity is therefore equal to the number of pixels in the image.
"""

from typing import List

import numpy as np
from PIL import Image

from .base import BaseWatermark


class SpatialWatermark(BaseWatermark):
    """LSB watermark: embed/extract bits via the pixel least-significant bit.

    Args:
        channel: Colour channel index to modify (0=R, 1=G, 2=B).  Default 0.
    """

    def __init__(self, channel: int = 0) -> None:
        if channel not in (0, 1, 2):
            raise ValueError("channel must be 0 (R), 1 (G), or 2 (B)")
        self.channel = channel

    # ------------------------------------------------------------------
    def embed(self, image: Image.Image, message: List[int]) -> Image.Image:
        """Embed *message* bits into the LSB of the selected channel.

        Raises:
            ValueError: if the message is longer than the image capacity.
        """
        img = image.convert("RGB")
        pixels = np.array(img, dtype=np.uint8)
        h, w, _ = pixels.shape
        capacity = h * w

        if len(message) > capacity:
            raise ValueError(
                f"Message length {len(message)} exceeds image capacity {capacity}"
            )

        flat = pixels[:, :, self.channel].flatten().copy()
        for idx, bit in enumerate(message):
            flat[idx] = (flat[idx] & 0xFE) | (int(bit) & 1)

        pixels[:, :, self.channel] = flat.reshape(h, w)
        return Image.fromarray(pixels, "RGB")

    # ------------------------------------------------------------------
    def extract(self, image: Image.Image, message_length: int) -> List[int]:
        """Extract *message_length* bits from the LSB of the selected channel."""
        img = image.convert("RGB")
        pixels = np.array(img, dtype=np.uint8)
        flat = pixels[:, :, self.channel].flatten()
        return [int(flat[i] & 1) for i in range(message_length)]

    def __repr__(self) -> str:
        return f"SpatialWatermark(channel={self.channel})"
