"""
Batch evaluation: compare multiple watermark algorithms against multiple
attacks on one or more images.

Usage
-----
>>> from PIL import Image
>>> from evaluate import BatchEvaluator
>>> from watermarks import SpatialWatermark, FrequencyWatermark
>>> from attacks import CompressionAttack, CropAttack

>>> evaluator = BatchEvaluator(
...     watermarks=[SpatialWatermark(), FrequencyWatermark()],
...     attacks=[CompressionAttack(75), CropAttack(0.1)],
...     message_length=48,
... )
>>> results = evaluator.run([Image.open("img.png")])
>>> evaluator.save_csv(results, "report.csv")
"""

from __future__ import annotations

import csv
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Union

from PIL import Image
from tqdm import tqdm

from attacks.base import BaseAttack
from pipeline import PipelineResult, WatermarkPipeline
from watermarks.base import BaseWatermark


class BatchEvaluator:
    """Run a grid of (watermark × attack × image) experiments.

    Args:
        watermarks:     List of watermark algorithm instances.
        attacks:        List of attack instances; each is applied independently
                        to the watermarked image.
        message_length: Number of bits in the random test message.
        seed:           Random seed for reproducible message generation.
        verbose:        Forward verbose flag to each pipeline.
    """

    def __init__(
        self,
        watermarks: List[BaseWatermark],
        attacks: List[BaseAttack],
        message_length: int = 48,
        seed: int = 0,
        verbose: bool = False,
    ) -> None:
        self.watermarks = watermarks
        self.attacks = attacks
        self.message_length = message_length
        self.seed = seed
        self.verbose = verbose

    # ------------------------------------------------------------------
    def _random_message(self) -> List[int]:
        rng = random.Random(self.seed)
        return [rng.randint(0, 1) for _ in range(self.message_length)]

    # ------------------------------------------------------------------
    def run(
        self,
        images: List[Image.Image],
        image_names: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Run all experiments and return a flat list of result dicts.

        Args:
            images:      Input PIL images to watermark.
            image_names: Optional names for the images (used in the report).

        Returns:
            List of dicts, one per (image × watermark × attack) combination.
            Each dict has keys: image, watermark, attack, embed_psnr,
            embed_ssim, attack_psnr, attack_ssim, ber, bit_accuracy.
        """
        if image_names is None:
            image_names = [f"image_{i}" for i in range(len(images))]

        message = self._random_message()
        all_rows: List[Dict] = []

        total = len(images) * len(self.watermarks)
        with tqdm(total=total, desc="Evaluating") as pbar:
            for img, img_name in zip(images, image_names):
                for wm in self.watermarks:
                    pipeline = WatermarkPipeline(wm, verbose=self.verbose)
                    try:
                        result: PipelineResult = pipeline.run(
                            img, message, self.attacks
                        )
                    except Exception as exc:
                        print(
                            f"[BatchEvaluator] Error for {type(wm).__name__} "
                            f"on {img_name}: {exc}"
                        )
                        pbar.update(1)
                        continue

                    for row in result.summary():
                        row["image"] = img_name
                        all_rows.append(row)

                    pbar.update(1)

        return all_rows

    # ------------------------------------------------------------------
    @staticmethod
    def save_csv(rows: List[Dict], path: Union[str, Path]) -> None:
        """Save evaluation rows to a CSV file.

        Args:
            rows: Output of :meth:`run`.
            path: Destination file path (created or overwritten).
        """
        if not rows:
            print("[BatchEvaluator] No rows to save.")
            return
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"[BatchEvaluator] Saved {len(rows)} rows to {path}")

    # ------------------------------------------------------------------
    @staticmethod
    def load_images_from_dir(
        directory: Union[str, Path],
        extensions: tuple = (".png", ".jpg", ".jpeg", ".bmp", ".webp"),
        max_images: Optional[int] = None,
    ) -> tuple:
        """Load images from a directory.

        Args:
            directory:  Path to the folder containing images.
            extensions: Accepted file extensions.
            max_images: Maximum number of images to load.

        Returns:
            Tuple of (images, names).
        """
        directory = Path(directory)
        paths = sorted(
            p for p in directory.iterdir()
            if p.suffix.lower() in extensions
        )
        if max_images is not None:
            paths = paths[:max_images]

        images, names = [], []
        for p in paths:
            try:
                images.append(Image.open(p).convert("RGB"))
                names.append(p.stem)
            except Exception as exc:
                print(f"[BatchEvaluator] Could not load {p}: {exc}")

        return images, names
