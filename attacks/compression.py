"""
JPEG compression attack.

JPEG is the most common real-world threat to spatial watermarks because it
discards high-frequency information during quantisation.
"""

import io

from PIL import Image

from .base import BaseAttack


class CompressionAttack(BaseAttack):
    """Re-encode the image as JPEG at a given quality and decode back.

    Args:
        quality: JPEG quality factor in [1, 95].  Lower → more compression.
                 Typical robustness breakpoints: 90 (mild), 70 (moderate),
                 50 (aggressive).
    """

    def __init__(self, quality: int = 75) -> None:
        if not (1 <= quality <= 95):
            raise ValueError("quality must be in [1, 95]")
        self.quality = quality

    def apply(self, image: Image.Image) -> Image.Image:
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="JPEG", quality=self.quality)
        buffer.seek(0)
        return Image.open(buffer).copy()

    def __repr__(self) -> str:
        return f"CompressionAttack(quality={self.quality})"
