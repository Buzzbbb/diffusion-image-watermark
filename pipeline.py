"""
End-to-end watermark pipeline.

Usage
-----
>>> from PIL import Image
>>> from pipeline import WatermarkPipeline
>>> from watermarks import SpatialWatermark
>>> from attacks import CompressionAttack

>>> pipeline = WatermarkPipeline(watermark=SpatialWatermark())
>>> result = pipeline.run(
...     image=Image.open("my_image.png"),
...     message=[1, 0, 1, 1, 0, 0, 1, 0],
...     attacks=[CompressionAttack(quality=75)],
... )
>>> print(result)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from PIL import Image

from attacks.base import BaseAttack
from metrics.quality import bit_accuracy, ber, psnr, ssim
from watermarks.base import BaseWatermark


@dataclass
class StepResult:
    """Metrics for a single attack step."""

    attack_name: str
    psnr_db: float
    ssim_score: float
    ber_score: float
    bit_accuracy_score: float
    extracted_bits: List[int]
    attacked_image: Image.Image = field(repr=False)


@dataclass
class PipelineResult:
    """Full result of one pipeline run."""

    watermark_name: str
    message: List[int]
    original_image: Image.Image = field(repr=False)
    watermarked_image: Image.Image = field(repr=False)
    # Quality of the watermarked image vs original (before attacks)
    embed_psnr: float = 0.0
    embed_ssim: float = 0.0
    # Per-attack results
    steps: List[StepResult] = field(default_factory=list)

    def summary(self) -> Dict:
        """Return a flat dict suitable for CSV export."""
        rows = []
        for step in self.steps:
            rows.append(
                {
                    "watermark": self.watermark_name,
                    "attack": step.attack_name,
                    "embed_psnr": round(self.embed_psnr, 4),
                    "embed_ssim": round(self.embed_ssim, 4),
                    "attack_psnr": round(step.psnr_db, 4),
                    "attack_ssim": round(step.ssim_score, 4),
                    "ber": round(step.ber_score, 4),
                    "bit_accuracy": round(step.bit_accuracy_score, 4),
                }
            )
        return rows


class WatermarkPipeline:
    """Orchestrate the embed → attack → extract → evaluate workflow.

    Args:
        watermark: A watermark algorithm instance (SpatialWatermark,
                   FrequencyWatermark, or NeuralWatermark).
        verbose:   Print progress messages when True.
    """

    def __init__(self, watermark: BaseWatermark, verbose: bool = True) -> None:
        self.watermark = watermark
        self.verbose = verbose

    # ------------------------------------------------------------------
    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[Pipeline] {msg}")

    # ------------------------------------------------------------------
    def run(
        self,
        image: Image.Image,
        message: List[int],
        attacks: Optional[List[BaseAttack]] = None,
    ) -> PipelineResult:
        """Run the full pipeline.

        Args:
            image:   Input PIL image (RGB).
            message: Binary watermark message as a list of 0/1 ints.
            attacks: List of attack objects to apply sequentially.
                     Each attack is applied independently to the watermarked
                     image (not chained).

        Returns:
            A PipelineResult containing all metrics and intermediate images.
        """
        attacks = attacks or []
        wm_name = type(self.watermark).__name__

        self._log(f"Embedding with {wm_name} ({len(message)} bits) …")
        watermarked = self.watermark.embed(image.convert("RGB"), message)

        embed_p = psnr(image, watermarked)
        embed_s = ssim(image, watermarked)
        self._log(f"  Embed PSNR={embed_p:.2f} dB  SSIM={embed_s:.4f}")

        result = PipelineResult(
            watermark_name=wm_name,
            message=message,
            original_image=image,
            watermarked_image=watermarked,
            embed_psnr=embed_p,
            embed_ssim=embed_s,
        )

        for attack in attacks:
            a_name = repr(attack)
            self._log(f"  Applying attack: {a_name}")
            attacked = attack.apply(watermarked)

            extracted = self.watermark.extract(attacked, len(message))
            b = ber(message, extracted)
            ba = bit_accuracy(message, extracted)
            ap = psnr(watermarked, attacked)
            as_ = ssim(watermarked, attacked)

            self._log(
                f"    BER={b:.4f}  BitAcc={ba:.4f}  "
                f"PSNR={ap:.2f} dB  SSIM={as_:.4f}"
            )

            result.steps.append(
                StepResult(
                    attack_name=a_name,
                    psnr_db=ap,
                    ssim_score=as_,
                    ber_score=b,
                    bit_accuracy_score=ba,
                    extracted_bits=extracted,
                    attacked_image=attacked,
                )
            )

        return result
