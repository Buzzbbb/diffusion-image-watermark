"""Abstract base class for all attack modules."""

from abc import ABC, abstractmethod
from PIL import Image


class BaseAttack(ABC):
    """Common interface for image attacks used in robustness evaluation."""

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        """Apply the attack to *image* and return the attacked image.

        Args:
            image: Input PIL image (RGB).

        Returns:
            Attacked PIL image.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
