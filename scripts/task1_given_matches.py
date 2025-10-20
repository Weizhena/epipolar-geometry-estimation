import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import cv2
import json
from src.utils.io_utils import load_matches, load_images
from src.core.fundamental_matrix import estimate_fundamental_8point
from src.core.epipolar_geometry import compute_epipoles, compute_symmetric_epipolar_distance
from src.visualization.epipolar_vis import draw_epipolar_lines

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    data_dir = base_dir
    results_dir = os.path.join(base_dir, 'results', 'task1')
    os.makedirs(results_dir, exist_ok=True)

    print("="*60)
    print("任务1：已知匹配点估计F")
    print("="*60)

    matches_file = os.path.join(data_dir, 'h_matches（对极几何实践作业数据文件）.txt')
    left_img_path = os.path.join(data_dir, 'left_upscaled.jpg')
    right_img_path = os.path.join(data_dir, 'right_upscaled.jpg')

    pts_left, pts_right = load_matches(matches_file)
    img_left, img_right = load_images(left_img_path, right_img_path)

    print(f"\n匹配点数: {len(pts_left)}")

    F = estimate_fundamental_8point(pts_left, pts_right)

    print(f"\nF矩阵:")
    print(F)

    U, S, Vt = np.linalg.svd(F)
    print(f"\nF矩阵秩检验: 奇异值 = [{S[0]:.6f}, {S[1]:.6f}, {S[2]:.6e}]", end="")
    if S[2] < 1e-6:
        print(" ✓")
    else:
        print(" (警告: 秩可能不为2)")

    e_left, e_right = compute_epipoles(F)
    print(f"\n左极点: (x={e_left[0]:.2f}, y={e_left[1]:.2f})", end="")
    if 0 <= e_left[0] < img_left.shape[1] and 0 <= e_left[1] < img_left.shape[0]:
        print("  [图像内]")
    else:
        print("  [图像外]")

    print(f"右极点: (x={e_right[0]:.2f}, y={e_right[1]:.2f})", end="")
    if 0 <= e_right[0] < img_right.shape[1] and 0 <= e_right[1] < img_right.shape[0]:
        print("  [图像内]")
    else:
        print("  [图像外]")

    mean_dist, median_dist, std_dist, max_dist = compute_symmetric_epipolar_distance(F, pts_left, pts_right)

    print(f"\n评估指标:")
    print(f"- 对称极线距离: mean={mean_dist:.2f}px, median={median_dist:.2f}px, max={max_dist:.2f}px")

    img_left_with_lines = draw_epipolar_lines(img_left, F, pts_right, e_left,
                                               direction='right_to_left', num_lines=20)
    img_right_with_lines = draw_epipolar_lines(img_right, F, pts_left, e_right,
                                                direction='left_to_right', num_lines=20)

    left_output = os.path.join(results_dir, 'left_epipolar_lines.png')
    right_output = os.path.join(results_dir, 'right_epipolar_lines.png')
    cv2.imwrite(left_output, img_left_with_lines)
    cv2.imwrite(right_output, img_right_with_lines)

    with open(os.path.join(results_dir, 'fundamental_matrix.txt'), 'w') as f:
        f.write("Fundamental Matrix F:\n")
        f.write(str(F) + "\n")

    with open(os.path.join(results_dir, 'epipoles.txt'), 'w') as f:
        f.write(f"Left Epipole: ({e_left[0]:.6f}, {e_left[1]:.6f})\n")
        f.write(f"Right Epipole: ({e_right[0]:.6f}, {e_right[1]:.6f})\n")

    metrics = {
        'num_matches': int(len(pts_left)),
        'symmetric_distance_mean': float(mean_dist),
        'symmetric_distance_median': float(median_dist),
        'symmetric_distance_std': float(std_dist),
        'symmetric_distance_max': float(max_dist),
        'singular_values': [float(s) for s in S]
    }

    with open(os.path.join(results_dir, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\n结果已保存至 {results_dir}/")
    print("="*60)

if __name__ == '__main__':
    main()
