import cv2

class FeatureDetector:
    def __init__(self, method='sift', nfeatures=0, contrastThreshold=0.03):
        self.method = method.lower()
        if self.method == 'sift':
            self.detector = cv2.SIFT_create(nfeatures=nfeatures,
                                           contrastThreshold=contrastThreshold)
        elif self.method == 'orb':
            self.detector = cv2.ORB_create(nfeatures=nfeatures if nfeatures > 0 else 1000)
        else:
            raise ValueError(f"Unsupported method: {method}")

    def detect_and_compute(self, img):
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        keypoints, descriptors = self.detector.detectAndCompute(gray, None)
        return keypoints, descriptors

    def visualize_keypoints(self, img, keypoints):
        img_kp = cv2.drawKeypoints(img, keypoints, None,
                                   flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return img_kp
