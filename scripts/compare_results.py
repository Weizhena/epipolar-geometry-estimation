import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import json

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    results_dir = os.path.join(base_dir, 'results', 'comparison')
    os.makedirs(results_dir, exist_ok=True)

    print("="*60)
    print("任务对比分析")
    print("="*60)

    task1_f_file = os.path.join(base_dir, 'results', 'task1', 'fundamental_matrix.txt')
    task2_f_file = os.path.join(base_dir, 'results', 'task2', 'fundamental_matrix.txt')

    task1_metrics_file = os.path.join(base_dir, 'results', 'task1', 'metrics.json')
    task2_metrics_file = os.path.join(base_dir, 'results', 'task2', 'ransac_statistics.json')

    with open(task1_metrics_file, 'r') as f:
        task1_metrics = json.load(f)

    with open(task2_metrics_file, 'r') as f:
        task2_metrics = json.load(f)

    task1_epipole_file = os.path.join(base_dir, 'results', 'task1', 'epipoles.txt')
    task2_epipole_file = os.path.join(base_dir, 'results', 'task2', 'epipoles.txt')

    with open(task1_epipole_file, 'r') as f:
        lines = f.readlines()
        task1_e_left = eval(lines[0].split(': ')[1].strip())
        task1_e_right = eval(lines[1].split(': ')[1].strip())

    with open(task2_epipole_file, 'r') as f:
        lines = f.readlines()
        task2_e_left = eval(lines[0].split(': ')[1].strip())
        task2_e_right = eval(lines[1].split(': ')[1].strip())

    e_left_diff = np.sqrt((task1_e_left[0] - task2_e_left[0])**2 +
                          (task1_e_left[1] - task2_e_left[1])**2)
    e_right_diff = np.sqrt((task1_e_right[0] - task2_e_right[0])**2 +
                           (task1_e_right[1] - task2_e_right[1])**2)

    print("\n极点对比:")
    print(f"任务1 左极点: ({task1_e_left[0]:.2f}, {task1_e_left[1]:.2f})")
    print(f"任务2 左极点: ({task2_e_left[0]:.2f}, {task2_e_left[1]:.2f})")
    print(f"差异: {e_left_diff:.2f} px")

    print(f"\n任务1 右极点: ({task1_e_right[0]:.2f}, {task1_e_right[1]:.2f})")
    print(f"任务2 右极点: ({task2_e_right[0]:.2f}, {task2_e_right[1]:.2f})")
    print(f"差异: {e_right_diff:.2f} px")

    print("\n误差对比:")
    print(f"任务1 对称极线距离: mean={task1_metrics['symmetric_distance_mean']:.2f}px, "
          f"median={task1_metrics['symmetric_distance_median']:.2f}px, "
          f"max={task1_metrics['symmetric_distance_max']:.2f}px")
    print(f"任务2 对称极线距离 (内点): mean={task2_metrics['symmetric_distance_mean']:.2f}px, "
          f"median={task2_metrics['symmetric_distance_median']:.2f}px, "
          f"max={task2_metrics['symmetric_distance_max']:.2f}px")

    print("\n数据统计:")
    print(f"任务1 匹配点数: {task1_metrics['num_matches']}")
    print(f"任务2 SIFT特征: 左{task2_metrics['num_features_left']} 右{task2_metrics['num_features_right']}")
    print(f"任务2 初始匹配: {task2_metrics['num_initial_matches']}")
    print(f"任务2 RANSAC内点: {task2_metrics['ransac_inlier_count']} ({100*task2_metrics['ransac_inlier_ratio']:.1f}%)")

    comparison_data = {
        'epipole_left_diff_px': float(e_left_diff),
        'epipole_right_diff_px': float(e_right_diff),
        'task1_mean_error': task1_metrics['symmetric_distance_mean'],
        'task2_mean_error': task2_metrics['symmetric_distance_mean'],
        'task1_num_matches': task1_metrics['num_matches'],
        'task2_num_inliers': task2_metrics['ransac_inlier_count'],
        'task2_inlier_ratio': task2_metrics['ransac_inlier_ratio']
    }

    with open(os.path.join(results_dir, 'comparison.json'), 'w') as f:
        json.dump(comparison_data, f, indent=2)

    with open(os.path.join(results_dir, 'comparison.txt'), 'w') as f:
        f.write("="*60 + "\n")
        f.write("任务对比分析\n")
        f.write("="*60 + "\n\n")
        f.write("极点对比:\n")
        f.write(f"任务1 左极点: ({task1_e_left[0]:.2f}, {task1_e_left[1]:.2f})\n")
        f.write(f"任务2 左极点: ({task2_e_left[0]:.2f}, {task2_e_left[1]:.2f})\n")
        f.write(f"差异: {e_left_diff:.2f} px\n\n")
        f.write(f"任务1 右极点: ({task1_e_right[0]:.2f}, {task1_e_right[1]:.2f})\n")
        f.write(f"任务2 右极点: ({task2_e_right[0]:.2f}, {task2_e_right[1]:.2f})\n")
        f.write(f"差异: {e_right_diff:.2f} px\n\n")
        f.write("误差对比:\n")
        f.write(f"任务1: mean={task1_metrics['symmetric_distance_mean']:.2f}px\n")
        f.write(f"任务2: mean={task2_metrics['symmetric_distance_mean']:.2f}px\n")

    print(f"\n对比结果已保存至 {results_dir}/")
    print("="*60)

if __name__ == '__main__':
    main()
