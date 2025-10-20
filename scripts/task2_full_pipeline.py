import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import cv2
import json
from src.utils.io_utils import load_images
from src.features.detector import FeatureDetector
from src.features.matcher import FeatureMatcher
from src.core.ransac import FundamentalMatrixRANSAC
from src.core.epipolar_geometry import compute_epipoles, compute_symmetric_epipolar_distance
from src.visualization.epipolar_vis import draw_epipolar_lines, draw_matches_with_inliers

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    data_dir = base_dir
    results_dir = os.path.join(base_dir, 'results', 'task2')
    os.makedirs(results_dir, exist_ok=True)

    print("="*60)
    print("任务2：完整特征检测+RANSAC流程")
    print("="*60)

    left_img_path = os.path.join(data_dir, 'left_upscaled.jpg')
    right_img_path = os.path.join(data_dir, 'right_upscaled.jpg')

    img_left, img_right = load_images(left_img_path, right_img_path)

    print("\n特征检测:")
    detector = FeatureDetector(method='sift', nfeatures=0, contrastThreshold=0.03)

    kp_left, desc_left = detector.detect_and_compute(img_left)
    kp_right, desc_right = detector.detect_and_compute(img_right)

    print(f"- 左图检测到 {len(kp_left)} 个SIFT特征点")
    print(f"- 右图检测到 {len(kp_right)} 个SIFT特征点")

    img_kp_left = detector.visualize_keypoints(img_left, kp_left)
    img_kp_right = detector.visualize_keypoints(img_right, kp_right)

    h_left, w_left = img_left.shape[:2]
    h_right, w_right = img_right.shape[:2]
    max_h = max(h_left, h_right)
    img_kp_combined = np.zeros((max_h, w_left + w_right, 3), dtype=np.uint8)
    img_kp_combined[:h_left, :w_left] = img_kp_left
    img_kp_combined[:h_right, w_left:w_left+w_right] = img_kp_right
    cv2.imwrite(os.path.join(results_dir, 'detected_features.png'), img_kp_combined)

    print("\n特征匹配:")
    matcher = FeatureMatcher(method='flann', ratio_threshold=0.75)
    matches = matcher.match(desc_left, desc_right)
    print(f"- Ratio test后: {len(matches)} 对")

    pts_left, pts_right = matcher.extract_matched_points(kp_left, kp_right, matches)

    print("\nRANSAC估计:")
    ransac = FundamentalMatrixRANSAC(max_iters=2000, threshold=1.5, confidence=0.99)
    F, inlier_mask = ransac.fit(pts_left, pts_right)

    stats = ransac.get_statistics()
    print(f"- 收敛于迭代 {stats['actual_iterations']}, 最终内点: {stats['inlier_count']}/{stats['total_count']} ({100*stats['inlier_ratio']:.1f}%)")

    img_matches_inliers = draw_matches_with_inliers(img_left, kp_left, img_right, kp_right,
                                                     matches, inlier_mask)
    cv2.imwrite(os.path.join(results_dir, 'ransac_inliers.png'), img_matches_inliers)

    print("\n极点计算:")
    e_left, e_right = compute_epipoles(F)
    print(f"- 左极点: (x={e_left[0]:.2f}, y={e_left[1]:.2f})")
    print(f"- 右极点: (x={e_right[0]:.2f}, y={e_right[1]:.2f})")

    inlier_pts_left = pts_left[inlier_mask]
    inlier_pts_right = pts_right[inlier_mask]
    mean_dist, median_dist, std_dist, max_dist = compute_symmetric_epipolar_distance(
        F, inlier_pts_left, inlier_pts_right)

    print(f"\n评估指标:")
    print(f"- 内点平均误差: {mean_dist:.2f}px")

    img_left_with_lines = draw_epipolar_lines(img_left, F, inlier_pts_right[:20], e_left,
                                               direction='right_to_left', num_lines=20)
    img_right_with_lines = draw_epipolar_lines(img_right, F, inlier_pts_left[:20], e_right,
                                                direction='left_to_right', num_lines=20)

    cv2.imwrite(os.path.join(results_dir, 'left_epipolar_lines.png'), img_left_with_lines)
    cv2.imwrite(os.path.join(results_dir, 'right_epipolar_lines.png'), img_right_with_lines)

    with open(os.path.join(results_dir, 'fundamental_matrix.txt'), 'w') as f:
        f.write("Fundamental Matrix F:\n")
        f.write(str(F) + "\n")

    with open(os.path.join(results_dir, 'epipoles.txt'), 'w') as f:
        f.write(f"Left Epipole: ({e_left[0]:.6f}, {e_left[1]:.6f})\n")
        f.write(f"Right Epipole: ({e_right[0]:.6f}, {e_right[1]:.6f})\n")

    metrics = {
        'num_features_left': len(kp_left),
        'num_features_right': len(kp_right),
        'num_initial_matches': len(matches),
        'ransac_inlier_count': stats['inlier_count'],
        'ransac_inlier_ratio': stats['inlier_ratio'],
        'ransac_iterations': stats['actual_iterations'],
        'symmetric_distance_mean': float(mean_dist),
        'symmetric_distance_median': float(median_dist),
        'symmetric_distance_max': float(max_dist)
    }

    with open(os.path.join(results_dir, 'ransac_statistics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\n结果已保存至 {results_dir}/")
    print("="*60)

if __name__ == '__main__':
    main()
