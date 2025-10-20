import numpy as np

def normalize_points(points):
    centroid = np.mean(points, axis=0)
    shifted = points - centroid
    avg_dist = np.mean(np.sqrt(np.sum(shifted**2, axis=1)))
    scale = np.sqrt(2) / avg_dist
    T = np.array([
        [scale, 0, -scale * centroid[0]],
        [0, scale, -scale * centroid[1]],
        [0, 0, 1]
    ])
    normalized = scale * shifted
    return T, normalized

def estimate_fundamental_8point(pts_left, pts_right):
    T_left, pts_left_norm = normalize_points(pts_left)
    T_right, pts_right_norm = normalize_points(pts_right)

    n = pts_left.shape[0]
    A = np.zeros((n, 9))
    for i in range(n):
        x, y = pts_left_norm[i]
        xp, yp = pts_right_norm[i]
        A[i] = [xp*x, xp*y, xp, yp*x, yp*y, yp, x, y, 1]

    U, S, Vt = np.linalg.svd(A)
    F_norm = Vt[-1].reshape(3, 3)

    U_f, S_f, Vt_f = np.linalg.svd(F_norm)
    S_f[2] = 0
    F_norm = U_f @ np.diag(S_f) @ Vt_f

    F = T_right.T @ F_norm @ T_left

    F = F / F[2, 2]

    return F
