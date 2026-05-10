# diffusion-image-watermark

**生成式图像水印嵌入与验证框架** — Watermark embedding and verification framework for diffusion-generated images.

---

## 功能概述 (Overview)

本项目面向生成式图像内容保护，提供以下功能：

| 功能 | 说明 |
|------|------|
| 🖼️ **水印嵌入** | 支持空间域、频域、神经网络三类水印算法 |
| ⚡ **扰动增强** | 高斯噪声、高斯模糊等鲁棒性测试 |
| 🗜️ **压缩攻击** | JPEG 多质量因子重编码攻击 |
| ✂️ **裁剪攻击** | 边缘裁剪 + 可选原始尺寸恢复 |
| ✅ **水印验证** | 自动提取并计算 BER / 比特精度 |
| 📊 **可视化报告** | 多算法对比柱状图 + HTML 检测报告 |
| 📋 **批量评测** | 多图像 × 多算法 × 多攻击全面对比，CSV 导出 |

---

## 项目结构 (Structure)

```
diffusion-image-watermark/
├── requirements.txt
├── main.py                  # CLI 入口
├── pipeline.py              # 端到端 embed→attack→extract 流程
├── evaluate.py              # 批量评测 + CSV 导出
├── visualize.py             # matplotlib 可视化 + HTML 报告
├── watermarks/
│   ├── spatial.py           # 空间域：LSB 水印
│   ├── frequency.py         # 频域：DCT 扩频水印
│   └── neural.py            # 神经网络：优化扰动水印（需 PyTorch）
├── attacks/
│   ├── perturbation.py      # 高斯噪声 / 模糊 / 亮度扰动
│   ├── compression.py       # JPEG 压缩攻击
│   └── crop.py              # 裁剪 / 填充攻击
├── metrics/
│   └── quality.py           # PSNR, SSIM, BER, 比特精度
└── examples/
    └── sample_pipeline.py   # 完整演示脚本
```

---

## 安装 (Installation)

```bash
pip install -r requirements.txt

# 如需神经水印，额外安装 PyTorch（可选）：
pip install torch torchvision
```

---

## 快速使用 (Quick Start)

### 运行完整演示

```bash
python examples/sample_pipeline.py
# 在 examples/demo_report/ 目录下生成报告
```

### CLI 嵌入水印

```bash
# 空间域 LSB 水印
python main.py embed input.png --method spatial --message "Hello AIGC" --output watermarked.png

# 频域 DCT 水印
python main.py embed input.png --method frequency --message "版权保护" --output watermarked_freq.png

# 神经网络水印（需要 PyTorch）
python main.py embed input.png --method neural --message-length 48 --n-steps 200 --output watermarked_nn.png
```

### CLI 提取水印

```bash
python main.py extract watermarked.png --method spatial --message-length 80 --decode-text
python main.py extract watermarked_freq.png --method frequency --message-length 48
```

### CLI 批量评测

```bash
# 对单张图像评测 spatial & frequency 算法
python main.py evaluate input.png --methods spatial frequency --csv --output-dir report/

# 对图像文件夹批量评测（含神经水印）
python main.py evaluate images/ --methods spatial frequency neural \
    --attacks perturbation jpeg75 jpeg50 crop10 crop20 \
    --message-length 48 --csv --output-dir report/
```

---

## Python API 示例

```python
from PIL import Image
from watermarks import SpatialWatermark, FrequencyWatermark
from attacks import CompressionAttack, CropAttack, PerturbationAttack
from pipeline import WatermarkPipeline
from evaluate import BatchEvaluator
from visualize import generate_report

# 1. 加载图像
image = Image.open("my_image.png")
message = [1, 0, 1, 1, 0, 0, 1, 0] * 6  # 48 bits

# 2. 单次水印流程
pipeline = WatermarkPipeline(FrequencyWatermark(key=42, strength=0.15))
result = pipeline.run(
    image, message,
    attacks=[CompressionAttack(75), CropAttack(0.10)],
)
print(f"PSNR: {result.embed_psnr:.2f} dB")

# 3. 批量评测
evaluator = BatchEvaluator(
    watermarks=[SpatialWatermark(), FrequencyWatermark()],
    attacks=[CompressionAttack(75), CropAttack(0.10)],
    message_length=48,
)
rows = evaluator.run([image], ["my_image"])
BatchEvaluator.save_csv(rows, "results.csv")

# 4. 生成报告
generate_report(rows, output_dir="report/", original=image)
```

---

## 水印算法对比 (Algorithm Comparison)

| 算法 | 类 | 嵌入域 | 特点 |
|------|-----|--------|------|
| 空间域 LSB | `SpatialWatermark` | 像素 LSB | 容量大、速度快、JPEG 压缩脆弱 |
| 频域 DCT | `FrequencyWatermark` | DCT 中频系数 | 对 JPEG 鲁棒、感知质量好 |
| 神经网络 | `NeuralWatermark` | 优化扰动 | 密钥安全、可差分、需 PyTorch |

### 支持的攻击类型

| 攻击 | CLI 名称 | 说明 |
|------|---------|------|
| 高斯噪声+模糊 | `perturbation` | 综合扰动 |
| JPEG 90% | `jpeg90` | 轻度压缩 |
| JPEG 75% | `jpeg75` | 中度压缩 |
| JPEG 50% | `jpeg50` | 重度压缩 |
| 裁剪 10% | `crop10` | 四周各裁 10% |
| 裁剪 20% | `crop20` | 四周各裁 20% |

---

## 评测指标 (Metrics)

| 指标 | 函数 | 说明 |
|------|------|------|
| PSNR | `metrics.psnr()` | 峰值信噪比 (dB)，越高越好 |
| SSIM | `metrics.ssim()` | 结构相似度 [0,1]，越高越好 |
| BER | `metrics.ber()` | 误码率 [0,1]，越低越好 |
| 比特精度 | `metrics.bit_accuracy()` | 1 − BER，越高越好 |

---

## 适用场景 (Use Cases)

- 🔍 **AIGC 内容溯源** — 验证图像来源与版权归属
- 🛡️ **生成式媒体版权保护** — 为扩散模型输出添加不可见水印
- 🎓 **人工智能安全课程** — 演示水印鲁棒性对比的教学实验
- 🔬 **后续研究基础** — 可追踪生成内容机制的研究起点

