import numpy as np
import cv2

def load_matches(filepath):
    data = np.loadtxt(filepath)
    pts_left = data[:, :2]
    pts_right = data[:, 2:]
    return pts_left, pts_right

def load_images(left_path, right_path):
    img_left = cv2.imread(left_path)
    img_right = cv2.imread(right_path)
    return img_left, img_right

def to_homogeneous(points):
    return np.hstack([points, np.ones((points.shape[0], 1))])

def from_homogeneous(points):
    return points[:, :-1] / points[:, -1:]
