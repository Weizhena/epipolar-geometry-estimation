import cv2
import numpy as np

def get_line_endpoints(line, img_shape):
    a, b, c = line
    h, w = img_shape[:2]
    points = []

    if abs(b) > 1e-6:
        y = 0
        x = -(b*y + c) / a
        if 0 <= x < w:
            points.append((int(x), int(y)))

        y = h - 1
        x = -(b*y + c) / a
        if 0 <= x < w:
            points.append((int(x), int(y)))

    if abs(a) > 1e-6:
        x = 0
        y = -(a*x + c) / b
        if 0 <= y < h:
            points.append((int(x), int(y)))

        x = w - 1
        y = -(a*x + c) / b
        if 0 <= y < h:
            points.append((int(x), int(y)))

    if len(points) >= 2:
        return points[0], points[1]
    return None

def draw_epipolar_lines(img, F, points_other_view, epipole, direction='left_to_right', num_lines=20):
    img_draw = img.copy()
    if len(img_draw.shape) == 2:
        img_draw = cv2.cvtColor(img_draw, cv2.COLOR_GRAY2BGR)

    points_to_draw = points_other_view[:num_lines]

    for pt in points_to_draw:
        if direction == 'left_to_right':
            line = F @ np.array([pt[0], pt[1], 1])
        else:
            line = F.T @ np.array([pt[0], pt[1], 1])

        endpoints = get_line_endpoints(line, img_draw.shape)
        if endpoints:
            cv2.line(img_draw, endpoints[0], endpoints[1], (255, 0, 0), 1)

    if 0 <= epipole[0] < img.shape[1] and 0 <= epipole[1] < img.shape[0]:
        cv2.circle(img_draw, (int(epipole[0]), int(epipole[1])), 5, (0, 0, 255), -1)
    else:
        pass

    return img_draw

def draw_matches_with_inliers(img1, kp1, img2, kp2, matches, inlier_mask):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    out_img = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)

    if len(img1.shape) == 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    if len(img2.shape) == 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    out_img[:h1, :w1] = img1
    out_img[:h2, w1:w1+w2] = img2

    for i, match in enumerate(matches):
        pt1 = tuple(map(int, kp1[match.queryIdx].pt))
        pt2 = tuple(map(int, (kp2[match.trainIdx].pt[0] + w1, kp2[match.trainIdx].pt[1])))

        color = (0, 255, 0) if inlier_mask[i] else (0, 0, 255)
        cv2.line(out_img, pt1, pt2, color, 1)
        cv2.circle(out_img, pt1, 3, color, -1)
        cv2.circle(out_img, pt2, 3, color, -1)

    inlier_count = np.sum(inlier_mask)
    total_count = len(matches)
    text = f"Inliers: {inlier_count}/{total_count} ({100*inlier_count/total_count:.1f}%)"
    cv2.putText(out_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return out_img
