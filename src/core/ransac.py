import numpy as np
from .fundamental_matrix import estimate_fundamental_8point
from .epipolar_geometry import point_to_line_distance

class FundamentalMatrixRANSAC:
    def __init__(self, max_iters=2000, threshold=1.5, confidence=0.99):
        self.max_iters = max_iters
        self.threshold = threshold
        self.confidence = confidence
        self.best_F = None
        self.best_inliers = None
        self.best_inlier_count = 0
        self.actual_iters = 0

    def compute_epipolar_distance(self, F, pts_left, pts_right):
        distances = []
        for i in range(len(pts_left)):
            x = np.array([pts_left[i, 0], pts_left[i, 1], 1])
            xp = np.array([pts_right[i, 0], pts_right[i, 1], 1])

            line_right = F @ x
            d1 = point_to_line_distance(pts_right[i], line_right)

            line_left = F.T @ xp
            d2 = point_to_line_distance(pts_left[i], line_left)

            distances.append((d1 + d2) / 2)

        return np.array(distances)

    def fit(self, pts_left, pts_right):
        n_points = len(pts_left)
        best_inlier_mask = np.zeros(n_points, dtype=bool)

        adaptive_max_iters = self.max_iters

        for iteration in range(self.max_iters):
            indices = np.random.choice(n_points, 8, replace=False)
            sample_left = pts_left[indices]
            sample_right = pts_right[indices]

            try:
                F_candidate = estimate_fundamental_8point(sample_left, sample_right)

                distances = self.compute_epipolar_distance(F_candidate, pts_left, pts_right)
                inlier_mask = distances < self.threshold
                inlier_count = np.sum(inlier_mask)

                if inlier_count > self.best_inlier_count:
                    self.best_inlier_count = inlier_count
                    self.best_inliers = inlier_mask
                    self.best_F = F_candidate

                    inlier_ratio = inlier_count / n_points
                    if inlier_ratio > 0:
                        num = np.log(1 - self.confidence)
                        denom = np.log(1 - inlier_ratio**8)
                        if denom < 0:
                            adaptive_max_iters = int(num / denom)
                            adaptive_max_iters = min(adaptive_max_iters, self.max_iters)

                if iteration + 1 >= adaptive_max_iters:
                    self.actual_iters = iteration + 1
                    break

            except:
                continue

        self.actual_iters = iteration + 1

        if self.best_inlier_count >= 8:
            inlier_left = pts_left[self.best_inliers]
            inlier_right = pts_right[self.best_inliers]
            self.best_F = estimate_fundamental_8point(inlier_left, inlier_right)

        return self.best_F, self.best_inliers

    def get_statistics(self):
        if self.best_inliers is None:
            return {}

        inlier_count = np.sum(self.best_inliers)
        total_count = len(self.best_inliers)
        inlier_ratio = inlier_count / total_count

        return {
            'inlier_count': int(inlier_count),
            'total_count': int(total_count),
            'inlier_ratio': float(inlier_ratio),
            'actual_iterations': int(self.actual_iters)
        }
