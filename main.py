"""
Command-line interface for diffusion-image-watermark.

Sub-commands
------------
embed       Embed a watermark into an image.
extract     Extract a watermark from an image.
evaluate    Run a batch evaluation of all watermark × attack combinations.

Examples
--------
Embed a watermark (spatial method, default):
    python main.py embed input.png --output watermarked.png --message "HelloAI"

Extract a watermark:
    python main.py extract watermarked.png --method spatial --length 64

Run batch evaluation on a folder:
    python main.py evaluate images/ --output-dir report/

Run evaluation with neural watermark:
    python main.py evaluate images/ --methods spatial frequency neural \\
        --output-dir report/ --message-length 48
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_image(path: str):
    from PIL import Image
    return Image.open(path).convert("RGB")


def _make_watermark(method: str, key: int, strength: float, n_steps: int, msg_len: int):
    if method == "spatial":
        from watermarks import SpatialWatermark
        return SpatialWatermark()
    elif method == "frequency":
        from watermarks import FrequencyWatermark
        return FrequencyWatermark(key=key, strength=strength)
    elif method == "neural":
        from watermarks import NeuralWatermark
        return NeuralWatermark(key=key, message_length=msg_len, n_steps=n_steps)
    else:
        raise ValueError(f"Unknown watermark method: {method!r}")


def _make_attacks(names: list):
    from attacks import CompressionAttack, CropAttack, PerturbationAttack
    mapping = {
        "noise": PerturbationAttack(noise_std=15.0, blur_radius=0.0),
        "blur": PerturbationAttack(noise_std=0.0, blur_radius=2.0),
        "perturbation": PerturbationAttack(noise_std=10.0, blur_radius=1.0),
        "jpeg75": CompressionAttack(quality=75),
        "jpeg50": CompressionAttack(quality=50),
        "jpeg90": CompressionAttack(quality=90),
        "crop10": CropAttack(crop_fraction=0.10),
        "crop20": CropAttack(crop_fraction=0.20),
    }
    attacks = []
    for name in names:
        if name not in mapping:
            print(
                f"[main] Unknown attack {name!r}. "
                f"Available: {list(mapping)}"
            )
            sys.exit(1)
        attacks.append(mapping[name])
    return attacks


# ---------------------------------------------------------------------------
# Sub-command: embed
# ---------------------------------------------------------------------------

def cmd_embed(args: argparse.Namespace) -> None:
    from watermarks.base import BaseWatermark

    wm = _make_watermark(
        args.method, args.key, args.strength, args.n_steps, args.message_length
    )
    image = _load_image(args.input)

    # Build message bits
    if args.message:
        bits = BaseWatermark._to_bits(args.message)
    elif args.bits:
        bits = [int(b) for b in args.bits]
    else:
        import random
        rng = random.Random(args.key)
        bits = [rng.randint(0, 1) for _ in range(args.message_length)]
        print(f"[embed] Using random {args.message_length}-bit message (seed={args.key})")

    # Truncate or pad to message_length for neural
    if args.method == "neural":
        if len(bits) > args.message_length:
            bits = bits[: args.message_length]
        elif len(bits) < args.message_length:
            bits = bits + [0] * (args.message_length - len(bits))

    print(f"[embed] Message bits ({len(bits)}): {bits[:16]}{'…' if len(bits) > 16 else ''}")

    watermarked = wm.embed(image, bits)
    output = args.output or (Path(args.input).stem + "_watermarked.png")
    watermarked.save(output)
    print(f"[embed] Watermarked image saved to {output}")


# ---------------------------------------------------------------------------
# Sub-command: extract
# ---------------------------------------------------------------------------

def cmd_extract(args: argparse.Namespace) -> None:
    wm = _make_watermark(
        args.method, args.key, args.strength, args.n_steps, args.message_length
    )
    image = _load_image(args.input)
    bits = wm.extract(image, args.message_length)
    print(f"[extract] Extracted bits ({len(bits)}): {bits}")

    if args.decode_text:
        try:
            from watermarks.base import BaseWatermark
            text = BaseWatermark._from_bits(bits)
            print(f"[extract] Decoded text: {text!r}")
        except Exception as exc:
            print(f"[extract] Could not decode text: {exc}")


# ---------------------------------------------------------------------------
# Sub-command: evaluate
# ---------------------------------------------------------------------------

def cmd_evaluate(args: argparse.Namespace) -> None:
    from evaluate import BatchEvaluator
    from visualize import generate_report

    # Build watermarks
    wms = [
        _make_watermark(m, args.key, args.strength, args.n_steps, args.message_length)
        for m in args.methods
    ]

    # Build attacks
    atk_names = args.attacks or [
        "perturbation", "jpeg75", "jpeg50", "crop10"
    ]
    attacks = _make_attacks(atk_names)

    # Load images
    input_path = Path(args.input)
    if input_path.is_dir():
        images, names = BatchEvaluator.load_images_from_dir(
            input_path, max_images=args.max_images
        )
    else:
        images = [_load_image(args.input)]
        names = [input_path.stem]

    if not images:
        print(f"[evaluate] No images found in {args.input}")
        sys.exit(1)

    print(f"[evaluate] Found {len(images)} image(s)")

    evaluator = BatchEvaluator(
        watermarks=wms,
        attacks=attacks,
        message_length=args.message_length,
        seed=args.key,
        verbose=args.verbose,
    )
    rows = evaluator.run(images, names)

    out_dir = Path(args.output_dir)
    if args.csv:
        csv_path = out_dir / "results.csv"
        BatchEvaluator.save_csv(rows, csv_path)

    html = generate_report(rows, output_dir=out_dir, original=images[0])
    print(f"[evaluate] Report: {html}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="watermark",
        description="Diffusion image watermark – embed, extract, and evaluate.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--method", default="spatial",
                        choices=["spatial", "frequency", "neural"],
                        help="Watermark algorithm (default: spatial)")
    common.add_argument("--key", type=int, default=42,
                        help="Secret key / random seed (default: 42)")
    common.add_argument("--strength", type=float, default=0.15,
                        help="Embedding strength for frequency/neural (default: 0.15)")
    common.add_argument("--n-steps", dest="n_steps", type=int, default=200,
                        help="Optimisation steps for neural watermark (default: 200)")
    common.add_argument("--message-length", dest="message_length", type=int,
                        default=48, help="Watermark bit length (default: 48)")

    # ---- embed ----
    p_embed = sub.add_parser("embed", parents=[common],
                              help="Embed a watermark into an image.")
    p_embed.add_argument("input", help="Path to the input image.")
    p_embed.add_argument("--output", "-o", help="Output path (default: <input>_watermarked.png)")
    g = p_embed.add_mutually_exclusive_group()
    g.add_argument("--message", "-m", help="Text message to embed (UTF-8).")
    g.add_argument("--bits", nargs="+", help="Binary bits to embed (e.g. 1 0 1 1).")
    p_embed.set_defaults(func=cmd_embed)

    # ---- extract ----
    p_ext = sub.add_parser("extract", parents=[common],
                            help="Extract a watermark from an image.")
    p_ext.add_argument("input", help="Path to the (watermarked) image.")
    p_ext.add_argument("--decode-text", action="store_true",
                       help="Attempt to decode bits as UTF-8 text.")
    p_ext.set_defaults(func=cmd_extract)

    # ---- evaluate ----
    p_eval = sub.add_parser("evaluate",
                             help="Batch-evaluate watermark robustness.")
    p_eval.add_argument("input",
                        help="Image file or directory of images.")
    p_eval.add_argument("--methods", nargs="+",
                        default=["spatial", "frequency"],
                        choices=["spatial", "frequency", "neural"],
                        help="Watermark methods to compare (default: spatial frequency).")
    p_eval.add_argument("--attacks", nargs="+",
                        help="Attacks to apply (default: perturbation jpeg75 jpeg50 crop10).")
    p_eval.add_argument("--key", type=int, default=42)
    p_eval.add_argument("--strength", type=float, default=0.15)
    p_eval.add_argument("--n-steps", dest="n_steps", type=int, default=200)
    p_eval.add_argument("--message-length", dest="message_length", type=int, default=48)
    p_eval.add_argument("--max-images", dest="max_images", type=int, default=None)
    p_eval.add_argument("--output-dir", dest="output_dir", default="report",
                        help="Directory for report output (default: report/).")
    p_eval.add_argument("--csv", action="store_true",
                        help="Save results to results.csv in output-dir.")
    p_eval.add_argument("--verbose", "-v", action="store_true")
    p_eval.set_defaults(func=cmd_evaluate)

    return parser


# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
