import cv2
import numpy as np

rng = np.random.default_rng(0)
K = np.array([[800.0, 0, 320], [0, 800.0, 240], [0, 0, 1]])  # intrinsics shared by both cameras

# 100 scene points seen by two cameras; the second sits 0.5 m to the right, turned 5 degrees
points = rng.uniform([-2, -1, 4], [2, 1, 8], (100, 3))
rvec = np.array([0.0, np.radians(5), 0.0])
tvec = -cv2.Rodrigues(rvec)[0] @ np.array([0.5, 0.0, 0.0])
x1 = cv2.projectPoints(points, np.zeros(3), np.zeros(3), K, None)[0].reshape(-1, 2) + rng.normal(0, 0.5, (100, 2))
x2 = cv2.projectPoints(points, rvec, tvec, K, None)[0].reshape(-1, 2) + rng.normal(0, 0.5, (100, 2))
x2[:20] = rng.uniform([0, 0], [640, 480], (20, 2))  # replace 20 matches with wrong ones

# Robust estimation keeps the matches that agree with a single fundamental matrix
F, inliers = cv2.findFundamentalMat(x1, x2, cv2.USAC_MAGSAC, 1.0)
kept = inliers.ravel() == 1
print(f"Kept {kept[20:].sum()} of 80 true matches and {kept[:20].sum()} of 20 wrong ones")

# Each point in image 1 defines a line a*x + b*y + c = 0 in image 2 that its match must lie on
lines = cv2.computeCorrespondEpilines(x1, 1, F).reshape(-1, 3)
dist = np.abs((lines[:, :2] * x2).sum(axis=1) + lines[:, 2])
print(f"Median distance to epipolar line: {np.median(dist[20:]):.2f} px (true), {np.median(dist[:20]):.0f} px (wrong)")
print(f"Wrong match that survived: {dist[:20][kept[:20]].round(2)} px from its line")