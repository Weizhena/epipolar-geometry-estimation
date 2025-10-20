# Epipolar Geometry and Fundamental Matrix Estimation
# 对极几何与基础矩阵估计

[中文版](README_zh.md) | English

> **Keywords / 关键词**: Computer Vision 计算机视觉 | Epipolar Geometry 对极几何 | Fundamental Matrix 基础矩阵 | 8-Point Algorithm 8点算法 | RANSAC | SIFT | Stereo Vision 立体视觉 | Structure from Motion 运动恢复结构

Computer Vision Experiment 4: Implementation of epipolar geometry algorithms including the 8-point algorithm and RANSAC framework for fundamental matrix estimation.

计算机视觉实验4：实现对极几何算法，包括8点算法和RANSAC框架进行基础矩阵估计。

## Overview

This project implements two approaches for estimating the fundamental matrix between stereo image pairs:

1. **Task 1**: Fundamental matrix estimation using 168 manually annotated matching points
2. **Task 2**: Complete pipeline with SIFT feature detection, matching, and RANSAC-based robust estimation

## Features

- 8-point algorithm with Hartley normalization
- RANSAC framework for robust estimation
- Epipole and epipolar line computation
- SIFT feature detection and matching
- Comprehensive visualization of results
- Detailed experimental report generation (DOCX format)

## Project Structure

```
experiment4/
├── src/
│   ├── core/
│   │   ├── fundamental_matrix.py    # 8-point algorithm, Hartley normalization
│   │   ├── epipolar_geometry.py     # Epipole & epipolar line computation
│   │   └── ransac.py                # RANSAC framework
│   ├── features/
│   │   ├── detector.py              # SIFT feature detection
│   │   └── matcher.py               # Feature matching
│   ├── visualization/
│   │   └── epipolar_vis.py          # Visualization utilities
│   └── utils/
│       └── io_utils.py              # Data loading utilities
├── scripts/
│   ├── task1_given_matches.py       # Task 1 execution script
│   ├── task2_full_pipeline.py       # Task 2 execution script
│   └── compare_results.py           # Results comparison script
├── results/                         # Experimental results
│   ├── task1/                       # Task 1 results
│   ├── task2/                       # Task 2 results
│   └── comparison/                  # Comparison analysis
├── generate_report.py               # Report generation script
└── README.md
```

## Requirements

```bash
numpy
opencv-python
matplotlib
python-docx
```

## Installation

```bash
pip install numpy opencv-python matplotlib python-docx
```

## Usage

### Task 1: Given Matching Points

Estimate fundamental matrix using 168 manually annotated matching points:

```bash
python scripts/task1_given_matches.py
```

Results:
- Mean error: 0.069 px
- Median error: 0.032 px
- 168 matched points

### Task 2: SIFT + RANSAC Pipeline

Complete pipeline with automatic feature detection and robust estimation:

```bash
python scripts/task2_full_pipeline.py
```

Results:
- SIFT features detected: 498 (left), 465 (right)
- Initial matches: 133
- RANSAC inliers: 101 (75.9% inlier ratio)
- Mean symmetric distance: 0.316 px

### Compare Results

Compare the two approaches:

```bash
python scripts/compare_results.py
```

### Generate Report

Generate comprehensive experimental report (DOCX with embedded images):

```bash
python generate_report.py
```

## Results Summary

| Metric | Task 1 | Task 2 |
|--------|--------|--------|
| Points/Inliers | 168 | 101 |
| Mean Error (px) | 0.069 | 0.316 |
| Median Error (px) | 0.032 | 0.154 |
| Max Error (px) | 0.556 | 2.373 |
| Inlier Ratio | - | 75.9% |

## Key Algorithms

### Hartley Normalization
- Center points at origin (zero mean)
- Scale to average distance √2
- Improves numerical stability

### 8-Point Algorithm
1. Normalize point coordinates
2. Construct constraint matrix from point correspondences
3. Solve using SVD
4. Enforce rank-2 constraint
5. Denormalize to obtain final F

### RANSAC Framework
1. Randomly sample 8 point pairs
2. Estimate F using 8-point algorithm
3. Compute symmetric epipolar distances
4. Count inliers below threshold
5. Adaptive iteration with best model selection

### Epipole Computation
- Left epipole: null space of F (SVD)
- Right epipole: null space of F^T

## Visualization

The project generates multiple visualizations:
- Matching points visualization
- Epipolar lines overlaid on images
- RANSAC inlier/outlier classification
- Epipole comparison

## License

MIT License

## Author

**weizhena**

Computer Vision Course - Experiment 4

## Acknowledgments

Based on classical computer vision algorithms for epipolar geometry and structure from motion.
