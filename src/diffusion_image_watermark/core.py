"""Project-specific public API."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from . import toolkit

PROJECT_NAME = "生成式图像水印嵌入与验证框架"
PROJECT_SLUG = "diffusion-image-watermark"
PROJECT_KIND = "value"
DEFAULT_KEY = "diffusion-image-watermark-key"


def embed_message(message: str, key: str = DEFAULT_KEY) -> toolkit.ExperimentResult:
    if PROJECT_KIND == "text":
        marked = toolkit.text_watermark_embed("网络空间安全信息隐藏实验文本载体。", message)
        recovered = toolkit.text_watermark_extract(marked)
        return toolkit.ExperimentResult(PROJECT_NAME, recovered, {"payload_ok": recovered == message, "marked_length": len(marked)})
    if PROJECT_KIND == "network":
        bits = toolkit.text_to_bits(message)
        packets = toolkit.synthesize_packets(max(128, len(bits)), key)
        marked = toolkit.embed_bits_in_timing(packets, bits)
        recovered = toolkit.bits_to_text(toolkit.extract_bits_from_timing(marked, len(bits)))
        metrics = toolkit.packet_features(marked)
        metrics["payload_ok"] = recovered == message
        return toolkit.ExperimentResult(PROJECT_NAME, recovered, metrics)
    if PROJECT_KIND == "federated":
        result = toolkit.run_federated_pipeline(PROJECT_NAME)
        result.notes.append("embed_message maps to the model watermark verification demo for this project.")
        return result
    values = toolkit.generate_carrier(8192, key)
    marked = toolkit.embed_text_in_values(values, message, key)
    recovered = toolkit.extract_text_from_values(marked, key)
    metrics: Dict[str, object] = toolkit.CarrierBundle(values, key).quality(toolkit.CarrierBundle(marked, key))
    metrics["payload_ok"] = recovered == message
    metrics["carrier_values"] = len(values)
    return toolkit.ExperimentResult(PROJECT_NAME, recovered, metrics)


def run_demo(message: str = "暨南大学网络空间安全学院信息隐藏开源项目") -> toolkit.ExperimentResult:
    if message:
        return embed_message(message)
    return toolkit.run_pipeline(PROJECT_NAME, PROJECT_KIND)


def write_report(output: Path, message: str = "demo payload") -> Path:
    result = run_demo(message)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.to_markdown(), encoding="utf-8")
    return output
