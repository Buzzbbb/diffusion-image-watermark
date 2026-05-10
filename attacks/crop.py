"""
Crop attack: remove a border of the image and optionally restore the original
dimensions by padding or resizing.

Cropping destroys the absolute pixel positions used by spatial watermarks and
also alters the DCT structure, making it a challenging attack for all watermark
families.
"""

from PIL import Image, ImageOps

from .base import BaseAttack


class CropAttack(BaseAttack):
    """Crop a fractional border from each side of the image.

    Args:
        crop_fraction: Fraction of each edge to remove, e.g. 0.10 removes 10 %
                       from every side.  Must be in (0, 0.49).
        restore_size:  If True, resize the cropped image back to the original
                       dimensions.  If False, leave it at the reduced size.
    """

    def __init__(self, crop_fraction: float = 0.10, restore_size: bool = True) -> None:
        if not (0.0 < crop_fraction < 0.49):
            raise ValueError("crop_fraction must be in (0, 0.49)")
        self.crop_fraction = crop_fraction
        self.restore_size = restore_size

    def apply(self, image: Image.Image) -> Image.Image:
        img = image.convert("RGB")
        w, h = img.size

        left = int(w * self.crop_fraction)
        top = int(h * self.crop_fraction)
        right = w - int(w * self.crop_fraction)
        bottom = h - int(h * self.crop_fraction)

        cropped = img.crop((left, top, right, bottom))

        if self.restore_size:
            return cropped.resize((w, h), Image.LANCZOS)
        return cropped

    def __repr__(self) -> str:
        return (
            f"CropAttack(crop_fraction={self.crop_fraction}, "
            f"restore_size={self.restore_size})"
        )


class PaddingAttack(BaseAttack):
    """Add a solid-colour border (padding) around the image.

    This simulates a scenario where the image is placed on a canvas or
    framed before redistribution.

    Args:
        pad_fraction: Fraction of the *shorter* edge to add as padding on each
                      side.
        fill_colour:  RGB tuple for the padding area.
    """

    def __init__(
        self,
        pad_fraction: float = 0.05,
        fill_colour: tuple = (0, 0, 0),
    ) -> None:
        self.pad_fraction = pad_fraction
        self.fill_colour = fill_colour

    def apply(self, image: Image.Image) -> Image.Image:
        img = image.convert("RGB")
        w, h = img.size
        pad = int(min(w, h) * self.pad_fraction)
        return ImageOps.expand(img, border=pad, fill=self.fill_colour)

    def __repr__(self) -> str:
        return f"PaddingAttack(pad_fraction={self.pad_fraction})"
