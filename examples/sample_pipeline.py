"""
End-to-end demo: generate a synthetic test image, embed watermarks with three
algorithms, apply various attacks, evaluate robustness, and save a report.

Run:
    python examples/sample_pipeline.py

The report is saved to ``examples/demo_report/``.
"""

import sys
import os

# Allow running from the examples/ sub-folder or from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
from pathlib import Path

import numpy as np
from PIL import Image

from watermarks import SpatialWatermark, FrequencyWatermark
from attacks import PerturbationAttack, CompressionAttack, CropAttack
from pipeline import WatermarkPipeline
from evaluate import BatchEvaluator
from visualize import generate_report, show_image_comparison

# ---------------------------------------------------------------------------
# 1. Create a synthetic test image (256×256 gradient + noise)
# ---------------------------------------------------------------------------
print("=== Step 1: Generating synthetic test image ===")
rng = np.random.default_rng(0)
h, w = 256, 256
x = np.linspace(0, 255, w, dtype=np.float32)
y = np.linspace(0, 255, h, dtype=np.float32)
xx, yy = np.meshgrid(x, y)
r = np.clip(xx + rng.normal(0, 5, (h, w)), 0, 255).astype(np.uint8)
g = np.clip(yy + rng.normal(0, 5, (h, w)), 0, 255).astype(np.uint8)
b = np.clip(128 + rng.normal(0, 10, (h, w)), 0, 255).astype(np.uint8)
demo_image = Image.fromarray(np.stack([r, g, b], axis=2), "RGB")

output_dir = Path(__file__).parent / "demo_report"
output_dir.mkdir(parents=True, exist_ok=True)
demo_image.save(output_dir / "original.png")
print(f"  Saved demo image to {output_dir / 'original.png'}")

# ---------------------------------------------------------------------------
# 2. Define message and watermark algorithms
# ---------------------------------------------------------------------------
message_length = 48
random.seed(42)
message = [random.randint(0, 1) for _ in range(message_length)]
print(f"\n=== Step 2: Message ({message_length} bits) ===")
print(f"  {message}")

watermarks = [
    SpatialWatermark(),
    FrequencyWatermark(key=42, strength=0.15),
]

# Try to load the neural watermark (requires torch)
try:
    from watermarks import NeuralWatermark
    wm_neural = NeuralWatermark(key=42, message_length=message_length, n_steps=150)
    watermarks.append(wm_neural)
    print("\n[sample] NeuralWatermark loaded (torch available).")
except ImportError:
    print("\n[sample] Skipping NeuralWatermark (torch not installed).")

# ---------------------------------------------------------------------------
# 3. Quick single-image demo with SpatialWatermark
# ---------------------------------------------------------------------------
print("\n=== Step 3: Single-image pipeline demo (SpatialWatermark) ===")
pipeline = WatermarkPipeline(watermarks[0], verbose=True)
attacks = [
    PerturbationAttack(noise_std=10.0, blur_radius=1.0),
    CompressionAttack(quality=75),
    CropAttack(crop_fraction=0.10),
]
result = pipeline.run(demo_image, message, attacks)

# Save comparison figure
fig = show_image_comparison(
    result.original_image,
    result.watermarked_image,
    attacked=result.steps[0].attacked_image if result.steps else None,
    save_path=output_dir / "spatial_comparison.png",
)
print(f"\n  Saved comparison figure to {output_dir / 'spatial_comparison.png'}")

# ---------------------------------------------------------------------------
# 4. Batch evaluation: all watermarks × all attacks
# ---------------------------------------------------------------------------
print("\n=== Step 4: Batch evaluation ===")
all_attacks = [
    PerturbationAttack(noise_std=10.0, blur_radius=1.0),
    CompressionAttack(quality=90),
    CompressionAttack(quality=75),
    CompressionAttack(quality=50),
    CropAttack(crop_fraction=0.10),
    CropAttack(crop_fraction=0.20),
]

evaluator = BatchEvaluator(
    watermarks=watermarks,
    attacks=all_attacks,
    message_length=message_length,
    seed=42,
    verbose=False,
)
rows = evaluator.run([demo_image], image_names=["demo"])
print(f"\n  Evaluation complete: {len(rows)} result rows")

# Save CSV
csv_path = output_dir / "results.csv"
BatchEvaluator.save_csv(rows, csv_path)

# ---------------------------------------------------------------------------
# 5. Generate visualisation report
# ---------------------------------------------------------------------------
print("\n=== Step 5: Generating report ===")
html = generate_report(
    rows,
    output_dir=output_dir,
    original=demo_image,
    watermarked=result.watermarked_image,
)
print(f"\n  Report: {html}")
print("\nDone!  Open the report in a browser:")
print(f"  {html}")
