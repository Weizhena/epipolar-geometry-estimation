import numpy as np

def compute_epipoles(F):
    U, S, Vt = np.linalg.svd(F)
    e_right = Vt[-1]
    e_right = e_right[:2] / e_right[2]

    U_t, S_t, Vt_t = np.linalg.svd(F.T)
    e_left = Vt_t[-1]
    e_left = e_left[:2] / e_left[2]

    return e_left, e_right

def compute_epipolar_line(F, point, direction='left_to_right'):
    x = np.array([point[0], point[1], 1])
    if direction == 'left_to_right':
        l = F @ x
    else:
        l = F.T @ x
    return l

def point_to_line_distance(point, line):
    a, b, c = line
    x, y = point
    return np.abs(a*x + b*y + c) / np.sqrt(a**2 + b**2)

def compute_symmetric_epipolar_distance(F, pts_left, pts_right):
    distances = []
    for i in range(len(pts_left)):
        x = np.array([pts_left[i, 0], pts_left[i, 1], 1])
        xp = np.array([pts_right[i, 0], pts_right[i, 1], 1])

        line_right = F @ x
        d1 = point_to_line_distance(pts_right[i], line_right)

        line_left = F.T @ xp
        d2 = point_to_line_distance(pts_left[i], line_left)

        distances.append((d1**2 + d2**2) / 2)

    distances = np.array(distances)
    return np.mean(distances), np.median(distances), np.std(distances), np.max(distances)
