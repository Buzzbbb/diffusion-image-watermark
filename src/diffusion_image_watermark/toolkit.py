"""Reusable utilities for information hiding experiments.

The module intentionally uses only the Python standard library so that the
repository can run in teaching, review, and CI environments without downloading
heavy third-party dependencies.  It provides compact but real implementations
for payload encoding, least-significant-bit embedding, report generation,
traffic simulation, toy federated averaging, and metric calculation.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import math
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


BitList = List[int]
NumberList = List[float]


def text_to_bits(text: str) -> BitList:
    data = text.encode("utf-8")
    length = len(data).to_bytes(4, "big")
    return bytes_to_bits(length + data)


def bits_to_text(bits: Sequence[int]) -> str:
    data = bits_to_bytes(bits)
    if len(data) < 4:
        return ""
    size = int.from_bytes(data[:4], "big")
    return data[4 : 4 + size].decode("utf-8", errors="replace")


def bytes_to_bits(data: bytes) -> BitList:
    result: BitList = []
    for value in data:
        for shift in range(7, -1, -1):
            result.append((value >> shift) & 1)
    return result


def bits_to_bytes(bits: Sequence[int]) -> bytes:
    clean = [1 if bit else 0 for bit in bits]
    if len(clean) % 8:
        clean.extend([0] * (8 - len(clean) % 8))
    out = bytearray()
    for index in range(0, len(clean), 8):
        value = 0
        for bit in clean[index : index + 8]:
            value = (value << 1) | bit
        out.append(value)
    return bytes(out)


def keyed_seed(key: str) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def keyed_positions(length: int, count: int, key: str) -> List[int]:
    if count > length:
        raise ValueError(f"payload requires {count} positions but carrier has {length}")
    positions = list(range(length))
    rng = random.Random(keyed_seed(key))
    rng.shuffle(positions)
    return positions[:count]


def lsb_embed_values(values: Sequence[int], bits: Sequence[int], key: str = "default") -> List[int]:
    output = [int(v) & 0xFF for v in values]
    positions = keyed_positions(len(output), len(bits), key)
    for pos, bit in zip(positions, bits):
        output[pos] = (output[pos] & 0xFE) | (1 if bit else 0)
    return output


def lsb_extract_values(values: Sequence[int], bit_count: int, key: str = "default") -> BitList:
    positions = keyed_positions(len(values), bit_count, key)
    return [int(values[pos]) & 1 for pos in positions]


def embed_text_in_values(values: Sequence[int], message: str, key: str = "default") -> List[int]:
    return lsb_embed_values(values, text_to_bits(message), key)


def extract_text_from_values(values: Sequence[int], key: str = "default", max_bytes: int = 4096) -> str:
    header = lsb_extract_values(values, 32, key)
    size = int.from_bytes(bits_to_bytes(header), "big")
    size = max(0, min(size, max_bytes))
    body = lsb_extract_values(values, 32 + size * 8, key)
    return bits_to_text(body)


def generate_carrier(length: int, key: str = "carrier") -> List[int]:
    rng = random.Random(keyed_seed(key))
    return [rng.randrange(0, 256) for _ in range(length)]


def mse(before: Sequence[int], after: Sequence[int]) -> float:
    if len(before) != len(after):
        raise ValueError("mse expects sequences of equal length")
    if not before:
        return 0.0
    return sum((int(a) - int(b)) ** 2 for a, b in zip(before, after)) / len(before)


def psnr(before: Sequence[int], after: Sequence[int], peak: float = 255.0) -> float:
    value = mse(before, after)
    if value == 0:
        return float("inf")
    return 20.0 * math.log10(peak / math.sqrt(value))


def bit_error_rate(expected: Sequence[int], observed: Sequence[int]) -> float:
    size = min(len(expected), len(observed))
    if size == 0:
        return 0.0
    errors = sum(1 for left, right in zip(expected[:size], observed[:size]) if int(left) != int(right))
    return errors / size


def normalized_correlation(left: Sequence[int], right: Sequence[int]) -> float:
    size = min(len(left), len(right))
    if size == 0:
        return 0.0
    xs = [float(v) for v in left[:size]]
    ys = [float(v) for v in right[:size]]
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def histogram(values: Sequence[int], bins: int = 16) -> List[int]:
    bins = max(1, bins)
    result = [0 for _ in range(bins)]
    for value in values:
        index = min(bins - 1, int(value) * bins // 256)
        result[index] += 1
    return result


def chi_square_uniform(values: Sequence[int], bins: int = 16) -> float:
    hist = histogram(values, bins)
    if not hist:
        return 0.0
    expected = sum(hist) / len(hist)
    if expected == 0:
        return 0.0
    return sum((item - expected) ** 2 / expected for item in hist)


def moving_average(values: Sequence[float], window: int = 5) -> List[float]:
    window = max(1, window)
    result: List[float] = []
    for index in range(len(values)):
        left = max(0, index - window + 1)
        result.append(sum(values[left : index + 1]) / (index - left + 1))
    return result


def add_noise(values: Sequence[int], amplitude: int = 1, key: str = "noise") -> List[int]:
    rng = random.Random(keyed_seed(key))
    return [max(0, min(255, int(v) + rng.randint(-amplitude, amplitude))) for v in values]


def quantize_values(values: Sequence[int], step: int = 4) -> List[int]:
    step = max(1, step)
    return [max(0, min(255, round(int(v) / step) * step)) for v in values]


def crop_values(values: Sequence[int], ratio: float = 0.9) -> List[int]:
    keep = max(1, int(len(values) * max(0.05, min(1.0, ratio))))
    return list(values[:keep])


def encode_base64_text(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def decode_base64_text(text: str) -> str:
    return base64.urlsafe_b64decode(text.encode("ascii")).decode("utf-8", errors="replace")


TEXT_ZERO = "，"
TEXT_ONE = "。"


def text_watermark_embed(carrier: str, watermark: str) -> str:
    bits = text_to_bits(watermark)
    chars = list(carrier)
    if not chars:
        chars = ["水印"]
    output: List[str] = []
    for index, bit in enumerate(bits):
        output.append(chars[index % len(chars)])
        output.append(TEXT_ONE if bit else TEXT_ZERO)
    output.extend(chars[len(bits) % len(chars) :])
    return "".join(output)


def text_watermark_extract(marked: str) -> str:
    bits = [1 if char == TEXT_ONE else 0 for char in marked if char in (TEXT_ZERO, TEXT_ONE)]
    return bits_to_text(bits)


def frame_sequence(frame_count: int = 6, frame_size: int = 256, key: str = "frames") -> List[List[int]]:
    return [generate_carrier(frame_size, f"{key}-{index}") for index in range(frame_count)]


def flatten_frames(frames: Sequence[Sequence[int]]) -> List[int]:
    result: List[int] = []
    for frame in frames:
        result.extend(int(v) for v in frame)
    return result


def split_frames(values: Sequence[int], frame_size: int) -> List[List[int]]:
    return [list(values[index : index + frame_size]) for index in range(0, len(values), frame_size)]


def synthesize_packets(count: int = 96, key: str = "packets") -> List[Dict[str, float]]:
    rng = random.Random(keyed_seed(key))
    packets: List[Dict[str, float]] = []
    current = 0.0
    for index in range(count):
        current += 0.03 + rng.random() * 0.01
        packets.append({"index": index, "time": current, "length": rng.randint(80, 1500), "label": 0})
    return packets


def embed_bits_in_timing(packets: Sequence[Dict[str, float]], bits: Sequence[int], delta: float = 0.015) -> List[Dict[str, float]]:
    output = [dict(packet) for packet in packets]
    for index, bit in enumerate(bits[: len(output)]):
        output[index]["time"] += delta if bit else -delta
        output[index]["label"] = 1
    output.sort(key=lambda packet: packet["time"])
    return output


def extract_bits_from_timing(packets: Sequence[Dict[str, float]], count: int, threshold: float = 0.04) -> BitList:
    if not packets:
        return []
    ordered = sorted(packets, key=lambda packet: packet["index"])
    gaps = [ordered[0]["time"]]
    for left, right in zip(ordered, ordered[1:]):
        gaps.append(right["time"] - left["time"])
    return [1 if gap >= threshold else 0 for gap in gaps[:count]]


def packet_features(packets: Sequence[Dict[str, float]]) -> Dict[str, float]:
    lengths = [float(packet["length"]) for packet in packets]
    times = [float(packet["time"]) for packet in packets]
    gaps = [b - a for a, b in zip(times, times[1:])] or [0.0]
    return {
        "count": float(len(packets)),
        "length_mean": statistics.mean(lengths) if lengths else 0.0,
        "length_stdev": statistics.pstdev(lengths) if lengths else 0.0,
        "gap_mean": statistics.mean(gaps),
        "gap_stdev": statistics.pstdev(gaps),
    }


def anomaly_score(values: Sequence[int]) -> float:
    hist = histogram(values, 32)
    even = sum(hist[::2])
    odd = sum(hist[1::2])
    total = max(1, even + odd)
    balance = abs(even - odd) / total
    return min(1.0, balance + chi_square_uniform(values, 32) / 500.0)


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-60.0, min(60.0, value))))


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def train_linear_classifier(samples: Sequence[Sequence[float]], labels: Sequence[int], epochs: int = 40, lr: float = 0.1) -> List[float]:
    if not samples:
        return []
    weights = [0.0 for _ in samples[0]]
    for _ in range(epochs):
        for sample, label in zip(samples, labels):
            prediction = sigmoid(dot(weights, sample))
            error = float(label) - prediction
            for index, value in enumerate(sample):
                weights[index] += lr * error * value
    return weights


def predict_linear(weights: Sequence[float], sample: Sequence[float]) -> int:
    return 1 if sigmoid(dot(weights, sample)) >= 0.5 else 0


def fedavg(models: Sequence[Sequence[float]]) -> List[float]:
    if not models:
        return []
    width = len(models[0])
    result = []
    for index in range(width):
        result.append(sum(model[index] for model in models) / len(models))
    return result


def trigger_samples(count: int = 8, width: int = 6, key: str = "trigger") -> List[List[float]]:
    rng = random.Random(keyed_seed(key))
    samples = []
    for _ in range(count):
        samples.append([1.0 if rng.random() > 0.35 else 0.0 for _ in range(width)])
    return samples


def watermark_success_rate(weights: Sequence[float], triggers: Sequence[Sequence[float]]) -> float:
    if not triggers:
        return 0.0
    positives = sum(predict_linear(weights, sample) for sample in triggers)
    return positives / len(triggers)


def write_json(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def markdown_report(title: str, metrics: Dict[str, object], notes: Sequence[str]) -> str:
    lines = [f"# {title}", ""]
    lines.append("## Metrics")
    lines.append("")
    for key, value in metrics.items():
        lines.append(f"- **{key}**: {value}")
    if notes:
        lines.append("")
        lines.append("## Notes")
        lines.append("")
        for note in notes:
            lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


@dataclass
class ExperimentResult:
    project: str
    recovered: str
    metrics: Dict[str, object]
    notes: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        return markdown_report(self.project, self.metrics, self.notes)


@dataclass
class CarrierBundle:
    values: List[int]
    key: str
    metadata: Dict[str, object] = field(default_factory=dict)

    def embed(self, message: str) -> "CarrierBundle":
        return CarrierBundle(embed_text_in_values(self.values, message, self.key), self.key, dict(self.metadata))

    def extract(self) -> str:
        return extract_text_from_values(self.values, self.key)

    def quality(self, other: "CarrierBundle") -> Dict[str, float]:
        return {"mse": mse(self.values, other.values), "psnr": psnr(self.values, other.values)}


def demo_payload(project_name: str) -> str:
    return f"{project_name} demo watermark payload"


def run_value_pipeline(project_name: str, key: str = "demo") -> ExperimentResult:
    carrier = CarrierBundle(generate_carrier(8192, project_name), key, {"kind": "value"})
    payload = demo_payload(project_name)
    marked = carrier.embed(payload)
    recovered = marked.extract()
    quality = carrier.quality(marked)
    quality["payload_ok"] = recovered == payload
    quality["anomaly_score"] = round(anomaly_score(marked.values), 6)
    return ExperimentResult(project_name, recovered, quality, ["LSB embedding over deterministic teaching carrier."])


def run_text_pipeline(project_name: str) -> ExperimentResult:
    carrier = "网络空间安全课程实验材料用于演示中文文本水印与隐写。"
    payload = demo_payload(project_name)
    marked = text_watermark_embed(carrier, payload)
    recovered = text_watermark_extract(marked)
    metrics = {"payload_ok": recovered == payload, "marked_length": len(marked), "carrier_length": len(carrier)}
    return ExperimentResult(project_name, recovered, metrics, ["Punctuation-based Chinese text watermark demo."])


def run_packet_pipeline(project_name: str) -> ExperimentResult:
    payload = demo_payload(project_name)
    bits = text_to_bits(payload)
    packets = synthesize_packets(max(128, len(bits)), project_name)
    marked = embed_bits_in_timing(packets, bits)
    recovered_bits = extract_bits_from_timing(marked, len(bits))
    recovered = bits_to_text(recovered_bits)
    features = packet_features(marked)
    metrics = {"payload_ok": recovered == payload, "gap_mean": round(features["gap_mean"], 6), "gap_stdev": round(features["gap_stdev"], 6)}
    return ExperimentResult(project_name, recovered, metrics, ["Timing-channel simulation for defensive analysis."])


def run_federated_pipeline(project_name: str) -> ExperimentResult:
    rng = random.Random(keyed_seed(project_name))
    local_models: List[List[float]] = []
    for client in range(4):
        samples = [[rng.random(), rng.random(), 1.0] for _ in range(32)]
        labels = [1 if sample[0] + sample[1] + client * 0.03 > 0.85 else 0 for sample in samples]
        local_models.append(train_linear_classifier(samples, labels, epochs=30, lr=0.08))
    global_model = fedavg(local_models)
    triggers = trigger_samples(12, len(global_model), project_name)
    success = watermark_success_rate(global_model, triggers)
    metrics = {"clients": 4, "model_width": len(global_model), "watermark_success_rate": round(success, 4)}
    return ExperimentResult(project_name, f"success={success:.4f}", metrics, ["Toy FedAvg model ownership verification demo."])


def run_pipeline(project_name: str, project_kind: str) -> ExperimentResult:
    if project_kind == "text":
        return run_text_pipeline(project_name)
    if project_kind == "network":
        return run_packet_pipeline(project_name)
    if project_kind == "federated":
        return run_federated_pipeline(project_name)
    return run_value_pipeline(project_name)
