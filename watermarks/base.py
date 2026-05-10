"""Abstract base class for all watermark algorithms."""

from abc import ABC, abstractmethod
from typing import List
from PIL import Image


class BaseWatermark(ABC):
    """Common interface for watermark embed / extract operations."""

    @abstractmethod
    def embed(self, image: Image.Image, message: List[int]) -> Image.Image:
        """Embed *message* bits into *image* and return the watermarked image.

        Args:
            image:   Input PIL image (RGB, any size).
            message: Binary message as a list of 0/1 integers.

        Returns:
            Watermarked PIL image of the same size.
        """

    @abstractmethod
    def extract(self, image: Image.Image, message_length: int) -> List[int]:
        """Extract watermark bits from *image*.

        Args:
            image:          (Possibly attacked) PIL image.
            message_length: Number of bits to extract.

        Returns:
            List of extracted bits (0 or 1).
        """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_bits(text: str) -> List[int]:
        """Encode a UTF-8 string to a flat list of bits."""
        bits: List[int] = []
        for byte in text.encode("utf-8"):
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)
        return bits

    @staticmethod
    def _from_bits(bits: List[int]) -> str:
        """Decode a flat list of bits back to a UTF-8 string."""
        chars = []
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for b in bits[i : i + 8]:
                byte = (byte << 1) | b
            chars.append(chr(byte))
        return "".join(chars)
