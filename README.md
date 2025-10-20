# 对极几何与基础矩阵估计
# Epipolar Geometry and Fundamental Matrix Estimation

中文版 | [English](README_en.md)

> **关键词 / Keywords**: 计算机视觉 Computer Vision | 对极几何 Epipolar Geometry | 基础矩阵 Fundamental Matrix | 8点算法 8-Point Algorithm | RANSAC | SIFT | 立体视觉 Stereo Vision | 运动恢复结构 Structure from Motion

计算机视觉实验4：实现对极几何算法，包括8点算法和RANSAC框架进行基础矩阵估计。

Computer Vision Experiment 4: Implementation of epipolar geometry algorithms including the 8-point algorithm and RANSAC framework for fundamental matrix estimation.

## 项目概述

本项目实现了两种估计立体图像对之间基础矩阵的方法：

1. **任务1**：使用168对人工标注的匹配点进行基础矩阵估计
2. **任务2**：完整流程，包括SIFT特征检测、匹配和基于RANSAC的鲁棒估计

## 主要功能

- 带Hartley归一化的8点算法
- 用于鲁棒估计的RANSAC框架
- 极点和极线计算
- SIFT特征检测与匹配
- 全面的结果可视化
- 详细的实验报告生成（DOCX格式）

## 项目结构

```
experiment4/
├── src/
│   ├── core/
│   │   ├── fundamental_matrix.py    # 8点算法、Hartley归一化
│   │   ├── epipolar_geometry.py     # 极点与极线计算
│   │   └── ransac.py                # RANSAC框架
│   ├── features/
│   │   ├── detector.py              # SIFT特征检测
│   │   └── matcher.py               # 特征匹配
│   ├── visualization/
│   │   └── epipolar_vis.py          # 可视化工具
│   └── utils/
│       └── io_utils.py              # 数据加载工具
├── scripts/
│   ├── task1_given_matches.py       # 任务1执行脚本
│   ├── task2_full_pipeline.py       # 任务2执行脚本
│   └── compare_results.py           # 结果对比脚本
├── results/                         # 实验结果
│   ├── task1/                       # 任务1结果
│   ├── task2/                       # 任务2结果
│   └── comparison/                  # 对比分析
├── generate_report.py               # 报告生成脚本
└── README.md
```

## 环境依赖

```bash
numpy
opencv-python
matplotlib
python-docx
```

## 安装

```bash
pip install numpy opencv-python matplotlib python-docx
```

## 使用方法

### 任务1：给定匹配点

使用168对人工标注的匹配点估计基础矩阵：

```bash
python scripts/task1_given_matches.py
```

结果：
- 平均误差：0.069 像素
- 中位数误差：0.032 像素
- 匹配点数：168对

### 任务2：SIFT + RANSAC 完整流程

包含自动特征检测和鲁棒估计的完整流程：

```bash
python scripts/task2_full_pipeline.py
```

结果：
- 检测到的SIFT特征：498个（左图）、465个（右图）
- 初始匹配数：133对
- RANSAC内点：101个（内点率75.9%）
- 平均对称距离：0.316 像素

### 对比结果

对比两种方法的结果：

```bash
python scripts/compare_results.py
```

### 生成报告

生成包含嵌入图片的完整实验报告（DOCX格式）：

```bash
python generate_report.py
```

## 结果汇总

| 指标 | 任务1 | 任务2 |
|------|-------|-------|
| 点数/内点数 | 168 | 101 |
| 平均误差 (px) | 0.069 | 0.316 |
| 中位数误差 (px) | 0.032 | 0.154 |
| 最大误差 (px) | 0.556 | 2.373 |
| 内点率 | - | 75.9% |

## 核心算法

### Hartley归一化
- 将点坐标平移至原点（零均值）
- 缩放使平均距离为√2
- 提高数值稳定性

### 8点算法
1. 归一化点坐标
2. 从点对应关系构建约束矩阵
3. 使用SVD求解
4. 强制秩为2约束
5. 反归一化得到最终基础矩阵F

### RANSAC框架
1. 随机采样8对点
2. 使用8点算法估计F
3. 计算对称极线距离
4. 统计阈值内的内点数
5. 自适应迭代并选择最佳模型

### 极点计算
- 左极点：F的零空间（通过SVD求解）
- 右极点：F^T的零空间

## 可视化

项目生成多种可视化结果：
- 匹配点可视化
- 叠加在图像上的极线
- RANSAC内点/离群点分类
- 极点对比

## 许可证

MIT License

## 作者

**weizhena**

计算机视觉课程 - 实验4

## 致谢

基于经典的对极几何和运动恢复结构算法。
