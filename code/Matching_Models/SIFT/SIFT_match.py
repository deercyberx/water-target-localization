import cv2
import numpy as np


def SIFT_Init():
    """Initialize SIFT detector and matcher"""
    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    return {'detector': sift, 'matcher': bf}


def SIFT_match(image0, image1, model, save_path, ransac_name, need_ransac=False, show_matches=False):
    """
    SIFT feature matching between two images.

    Args:
        image0: query image (numpy array, BGR)
        image1: reference image (numpy array, BGR)
        model: dict with 'detector' and 'matcher'
        save_path: path for saving visualization
        ransac_name: filename for ransac visualization
        need_ransac: whether to apply RANSAC filtering
        show_matches: whether to save match visualization

    Returns:
        inlier_keys_left: list of [x, y] points from image0
        inlier_keys_right: list of [x, y] points from image1
    """
    sift = model['detector']
    bf = model['matcher']

    # Convert to grayscale
    gray0 = cv2.cvtColor(image0, cv2.COLOR_BGR2GRAY) if len(image0.shape) == 3 else image0
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) if len(image1.shape) == 3 else image1

    # Detect keypoints and descriptors
    kp0, des0 = sift.detectAndCompute(gray0, None)
    kp1, des1 = sift.detectAndCompute(gray1, None)

    if des0 is None or des1 is None or len(kp0) < 5 or len(kp1) < 5:
        return [], []

    # Match using KNN
    matches = bf.knnMatch(des0, des1, k=2)

    # Apply Lowe's ratio test
    good_matches = []
    for m_n in matches:
        if len(m_n) == 2:
            m, n = m_n
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

    if len(good_matches) < 5:
        return [], []

    # Extract matched keypoints
    mkpts0 = np.array([kp0[m.queryIdx].pt for m in good_matches])
    mkpts1 = np.array([kp1[m.trainIdx].pt for m in good_matches])

    # Apply RANSAC if needed
    if need_ransac and len(mkpts0) > 5:
        from skimage.measure import ransac
        from skimage.transform import FundamentalMatrixTransform
        try:
            _, inliers = ransac(
                (mkpts0, mkpts1),
                FundamentalMatrixTransform, min_samples=8,
                residual_threshold=4, max_trials=10000
            )
            if inliers is not None:
                inlier_keys_left = [[point[0], point[1]] for point in mkpts0[inliers]]
                inlier_keys_right = [[point[0], point[1]] for point in mkpts1[inliers]]
            else:
                inlier_keys_left = [[point[0], point[1]] for point in mkpts0]
                inlier_keys_right = [[point[0], point[1]] for point in mkpts1]
        except:
            inlier_keys_left = [[point[0], point[1]] for point in mkpts0]
            inlier_keys_right = [[point[0], point[1]] for point in mkpts1]
    else:
        inlier_keys_left = [[point[0], point[1]] for point in mkpts0]
        inlier_keys_right = [[point[0], point[1]] for point in mkpts1]

    # Save visualization if needed
    if show_matches and len(inlier_keys_left) > 5:
        result_save_path = save_path + ransac_name
        kpts_left = [cv2.KeyPoint(x, y, 1) for x, y in inlier_keys_left]
        kpts_right = [cv2.KeyPoint(x, y, 1) for x, y in inlier_keys_right]
        matches_draw = [cv2.DMatch(i, i, 0) for i in range(len(kpts_left))]
        img_match = cv2.drawMatches(image0, kpts_left, image1, kpts_right, matches_draw, None)
        cv2.imwrite(result_save_path, img_match)

    return inlier_keys_left, inlier_keys_right
