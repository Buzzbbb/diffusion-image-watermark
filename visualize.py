"""
Visualisation and HTML/PDF detection report generation.

The main entry-point is :func:`generate_report`, which accepts a list of
pipeline results (or batch-evaluation rows) and produces:

  * A multi-panel matplotlib figure comparing all watermark × attack pairs.
  * An optional HTML summary saved alongside the figure.

Individual helpers are also available for ad-hoc inspection.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional, Union

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for script / CI use
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# Low-level image-comparison panels
# ---------------------------------------------------------------------------

def show_image_comparison(
    original: Image.Image,
    watermarked: Image.Image,
    attacked: Optional[Image.Image] = None,
    titles: Optional[List[str]] = None,
    save_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Plot original, watermarked (and optionally attacked) side-by-side.

    Also displays the amplified difference image.

    Args:
        original:    Reference image.
        watermarked: Watermarked image.
        attacked:    Attacked image (optional).
        titles:      Custom sub-plot titles.
        save_path:   If provided, save the figure to this path.

    Returns:
        The matplotlib Figure.
    """
    images = [original, watermarked]
    default_titles = ["Original", "Watermarked"]

    if attacked is not None:
        images.append(attacked)
        default_titles.append("Attacked")

    if titles is None:
        titles = default_titles

    # Add difference panel
    orig_arr = np.array(original.convert("RGB"), dtype=np.float32)
    wm_arr = np.array(watermarked.convert("RGB").resize(original.size), dtype=np.float32)
    diff = np.clip(np.abs(orig_arr - wm_arr) * 10, 0, 255).astype(np.uint8)
    diff_img = Image.fromarray(diff)
    images.append(diff_img)
    titles.append("Difference ×10")

    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, img, title in zip(axes, images, titles):
        ax.imshow(np.array(img.convert("RGB")))
        ax.set_title(title, fontsize=10)
        ax.axis("off")

    fig.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


# ---------------------------------------------------------------------------
# Bar-chart comparison of multiple watermarks × attacks
# ---------------------------------------------------------------------------

def plot_robustness_comparison(
    rows: List[Dict],
    metric: str = "bit_accuracy",
    save_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Bar chart comparing watermark robustness across attacks.

    Args:
        rows:      Flat list of dicts as returned by
                   :meth:`~evaluate.BatchEvaluator.run`.
        metric:    Column to plot: ``'bit_accuracy'``, ``'ber'``,
                   ``'embed_psnr'``, or ``'attack_psnr'``.
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure.
    """
    if not rows:
        raise ValueError("rows is empty")

    # Collect watermark names and attack names (preserving insertion order)
    wm_names = list(dict.fromkeys(r["watermark"] for r in rows))
    atk_names = list(dict.fromkeys(r["attack"] for r in rows))

    # Build a data matrix: shape (n_wm, n_attacks)
    data: Dict[str, Dict[str, List[float]]] = {
        wm: {atk: [] for atk in atk_names} for wm in wm_names
    }
    for row in rows:
        data[row["watermark"]][row["attack"]].append(row[metric])

    means: np.ndarray = np.zeros((len(wm_names), len(atk_names)))
    for i, wm in enumerate(wm_names):
        for j, atk in enumerate(atk_names):
            vals = data[wm][atk]
            means[i, j] = np.mean(vals) if vals else 0.0

    x = np.arange(len(atk_names))
    width = 0.8 / max(len(wm_names), 1)

    fig, ax = plt.subplots(figsize=(max(8, 2 * len(atk_names)), 5))
    colours = plt.cm.tab10(np.linspace(0, 0.9, len(wm_names)))  # type: ignore[attr-defined]

    for i, (wm, colour) in enumerate(zip(wm_names, colours)):
        offset = (i - len(wm_names) / 2 + 0.5) * width
        bars = ax.bar(x + offset, means[i], width=width * 0.9,
                      label=wm, color=colour, alpha=0.85)
        # Add value labels
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.01,
                f"{h:.3f}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(atk_names, rotation=25, ha="right", fontsize=8)
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.set_title(f"Watermark Robustness Comparison — {metric}")
    ax.legend(loc="lower right", fontsize=8)

    if metric in ("bit_accuracy",):
        ax.set_ylim(0, 1.1)
    elif metric == "ber":
        ax.set_ylim(0, 1.05)

    ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8, label="random (50 %)")
    fig.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


# ---------------------------------------------------------------------------
# Full detection report
# ---------------------------------------------------------------------------

def generate_report(
    rows: List[Dict],
    output_dir: Union[str, Path] = "report",
    original: Optional[Image.Image] = None,
    watermarked: Optional[Image.Image] = None,
) -> Path:
    """Generate a detection report with charts and an HTML index.

    Args:
        rows:        Output of :meth:`~evaluate.BatchEvaluator.run`.
        output_dir:  Directory where report files are saved.
        original:    Optional original image for visual comparison panel.
        watermarked: Optional watermarked image for visual comparison panel.

    Returns:
        Path to the generated ``index.html`` file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_figures: List[str] = []

    # --- Bit accuracy chart ---
    for metric in ("bit_accuracy", "ber", "embed_psnr", "attack_psnr"):
        try:
            fig = plot_robustness_comparison(rows, metric=metric)
            fname = f"{metric}_comparison.png"
            fig.savefig(output_dir / fname, dpi=150, bbox_inches="tight")
            plt.close(fig)
            saved_figures.append(fname)
        except Exception as exc:
            print(f"[visualize] Could not plot {metric}: {exc}")

    # --- Image comparison panel (if images provided) ---
    if original is not None and watermarked is not None:
        fname = "image_comparison.png"
        fig = show_image_comparison(original, watermarked, save_path=output_dir / fname)
        plt.close(fig)
        saved_figures.append(fname)

    # --- HTML index ---
    html_path = output_dir / "index.html"
    _write_html(html_path, saved_figures, rows)
    print(f"[visualize] Report saved to {html_path}")
    return html_path


def _write_html(
    path: Path, figures: List[str], rows: List[Dict]
) -> None:
    """Write a minimal HTML report."""
    fig_tags = "\n".join(
        f'<div class="fig"><img src="{f}" alt="{f}"><p>{f}</p></div>'
        for f in figures
    )

    # Build a summary table
    if rows:
        headers = list(rows[0].keys())
        header_row = "".join(f"<th>{h}</th>" for h in headers)
        data_rows = ""
        for row in rows:
            cells = "".join(f"<td>{row[k]}</td>" for k in headers)
            data_rows += f"<tr>{cells}</tr>\n"
        table = (
            f"<table><thead><tr>{header_row}</tr></thead>"
            f"<tbody>{data_rows}</tbody></table>"
        )
    else:
        table = "<p>No data.</p>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>扩散模型图像水印检测报告</title>
<style>
  body {{ font-family: sans-serif; max-width: 1200px; margin: auto; padding: 1em; }}
  h1, h2 {{ color: #333; }}
  .fig {{ display: inline-block; margin: 1em; text-align: center; }}
  .fig img {{ max-width: 100%; border: 1px solid #ccc; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.85em; }}
  th, td {{ border: 1px solid #ccc; padding: 4px 8px; text-align: left; }}
  th {{ background: #f0f0f0; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
</style>
</head>
<body>
<h1>扩散模型图像水印检测报告</h1>
<h2>可视化比较</h2>
<div>{fig_tags}</div>
<h2>评测数据汇总</h2>
{table}
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
