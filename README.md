# 生成式图像水印嵌入与验证框架

`diffusion-image-watermark` 是一个信息隐藏与网络空间安全方向的可运行开源项目，包含核心算法代码、命令行入口、实验配置、示例脚本和 smoke tests。

## Overview

本项目面向生成式图像内容保护，提供扩散模型生成图像的水印嵌入、扰动增强、压缩攻击、裁剪攻击和水印验证流程。框架可对接本地生成图像样本，比较空间域水印、频域水印和神经水印的鲁棒性差异，并输出可视化检测报告。项目适用于 AIGC 内容溯源、生成式媒体版权保护和人工智能安全课程实践，可作为后续研究生成式内容可追踪机制的基础代码，并支持批量评测、样例导出和参数记录。

## Features

- 统一的数据加载、实验配置和结果保存流程
- 面向信息隐藏/数字水印/隐写分析任务的模块化设计
- 支持实验指标输出、样例结果归档和后续算法扩展
- 适合课程实验、毕业设计、论文复现实验和课题组日常开发

## Quick Start

```bash
python examples/demo.py
python -m unittest discover -s tests
python -m diffusion_image_watermark.cli --message "demo payload" --report docs/cli_report.md
```

## Keywords

AIGC · diffusion · image watermark · provenance

## Authors

- 负责人：林裕斌
- 参与人：曾科、田承金
- 指导教师：吕善翔
- 单位：暨南大学网络空间安全学院

## License

本项目采用 MIT License 开源。Copyright (c) 2026 Lin Yubin, Zeng Ke, Tian Chengjin, Shanxiang Lv, Jinan University.
